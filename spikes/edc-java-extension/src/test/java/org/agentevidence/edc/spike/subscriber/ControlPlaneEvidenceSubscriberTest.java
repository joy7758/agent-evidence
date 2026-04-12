package org.agentevidence.edc.spike.subscriber;

import org.agentevidence.edc.spike.fixtures.ControlPlaneEventFixtures;
import org.agentevidence.edc.spike.grouping.AgentEvidenceGroupingStrategy;
import org.agentevidence.edc.spike.mapper.AgentEvidenceEventMapper;
import org.agentevidence.edc.spike.model.BundleCorrelationContext;
import org.agentevidence.edc.spike.model.EvidenceFragment;
import org.agentevidence.edc.spike.support.RuntimeWiringTestSupport.RecordingMonitor;
import org.agentevidence.edc.spike.writer.AgentEvidenceEnvelopeWriter;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ControlPlaneEvidenceSubscriberTest {
    @Test
    void shouldDeduplicateEnvelopeIdAndSemanticEventForRealAssetCreatedPayload() {
        var writer = new RecordingWriter();
        var subscriber = new ControlPlaneEvidenceSubscriber(
                new AgentEvidenceEventMapper(),
                new AgentEvidenceGroupingStrategy(),
                writer,
                null,
                new RecordingMonitor()
        );

        subscriber.on(ControlPlaneEventFixtures.assetCreatedEnvelope("env-asset-1", 1_712_780_800_000L));
        subscriber.on(ControlPlaneEventFixtures.assetCreatedEnvelope("env-asset-1", 1_712_780_800_000L));
        subscriber.on(ControlPlaneEventFixtures.assetCreatedEnvelope("env-asset-2", 1_712_780_801_000L));

        assertEquals(1, writer.writes.size());
        assertEquals(
                "participant-a::asset-1::dataspace.asset.registered",
                writer.writes.get(0).correlationContext.semanticDeduplicationKey()
        );
    }

    @Test
    void shouldGroupTransferPayloadByTransferProcessId() {
        var writer = new RecordingWriter();
        var subscriber = new ControlPlaneEvidenceSubscriber(
                new AgentEvidenceEventMapper(),
                new AgentEvidenceGroupingStrategy(),
                writer,
                null,
                new RecordingMonitor()
        );

        subscriber.on(ControlPlaneEventFixtures.transferProcessStartedEnvelope("env-transfer-started", 1_712_780_802_000L));

        assertEquals(1, writer.writes.size());
        assertEquals("tp-1", writer.writes.get(0).correlationContext.finalBundleKey());
        assertEquals("agreement-1", writer.writes.get(0).correlationContext.stagingCorrelationKey());
        assertEquals("dataspace.transfer.started", writer.writes.get(0).fragment.semanticEventType());
    }

    @Test
    void shouldIgnoreOutOfScopePayloadAndEmitDebugSignal() {
        var writer = new RecordingWriter();
        var monitor = new RecordingMonitor();
        var subscriber = new ControlPlaneEvidenceSubscriber(
                new AgentEvidenceEventMapper(),
                new AgentEvidenceGroupingStrategy(),
                writer,
                null,
                monitor
        );

        subscriber.on(ControlPlaneEventFixtures.transferProcessSuspendedEnvelope("env-transfer-suspended", 1_712_780_803_000L));

        assertTrue(writer.writes.isEmpty());
        assertTrue(monitor.debugMessages().stream().anyMatch(it -> it.contains("Ignoring out-of-scope control-plane event transfer.process.suspended")));
    }

    @Test
    void shouldSwallowWriterFailureAndEmitWarning() {
        var monitor = new RecordingMonitor();
        var subscriber = new ControlPlaneEvidenceSubscriber(
                new AgentEvidenceEventMapper(),
                new AgentEvidenceGroupingStrategy(),
                new FailingWriter(),
                null,
                monitor
        );

        subscriber.on(ControlPlaneEventFixtures.transferProcessStartedEnvelope("env-transfer-started", 1_712_780_804_000L));

        assertTrue(monitor.warningMessages().stream().anyMatch(it -> it.contains("Failed to export evidence fragment for event transfer.process.started")));
    }

    private record RecordedWrite(BundleCorrelationContext correlationContext, EvidenceFragment fragment) {
    }

    private static class RecordingWriter implements AgentEvidenceEnvelopeWriter {
        private final List<RecordedWrite> writes = new ArrayList<>();

        @Override
        public void write(BundleCorrelationContext correlationContext, EvidenceFragment fragment) throws IOException {
            writes.add(new RecordedWrite(correlationContext, fragment));
        }
    }

    private static class FailingWriter implements AgentEvidenceEnvelopeWriter {
        @Override
        public void write(BundleCorrelationContext correlationContext, EvidenceFragment fragment) throws IOException {
            throw new IOException("disk-full");
        }
    }
}
