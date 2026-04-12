package org.agentevidence.edc.spike.subscriber;

import org.agentevidence.edc.spike.fixtures.ControlPlaneEventFixtures;
import org.agentevidence.edc.spike.grouping.AgentEvidenceGroupingStrategy;
import org.agentevidence.edc.spike.mapper.AgentEvidenceEventMapper;
import org.agentevidence.edc.spike.model.BundleCorrelationContext;
import org.agentevidence.edc.spike.model.EvidenceFragment;
import org.agentevidence.edc.spike.writer.AgentEvidenceEnvelopeWriter;
import org.eclipse.edc.spi.monitor.Monitor;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ControlPlaneEvidenceSubscriberTest {
    @Test
    void shouldDeduplicateEnvelopeIdAndSemanticEventForRealAssetCreatedPayload() {
        var writer = new RecordingWriter();
        var subscriber = new ControlPlaneEvidenceSubscriber(
                new AgentEvidenceEventMapper(),
                new AgentEvidenceGroupingStrategy(),
                writer,
                null,
                new SilentMonitor()
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
                new SilentMonitor()
        );

        subscriber.on(ControlPlaneEventFixtures.transferProcessStartedEnvelope("env-transfer-started", 1_712_780_802_000L));

        assertEquals(1, writer.writes.size());
        assertEquals("tp-1", writer.writes.get(0).correlationContext.finalBundleKey());
        assertEquals("agreement-1", writer.writes.get(0).correlationContext.stagingCorrelationKey());
        assertEquals("dataspace.transfer.started", writer.writes.get(0).fragment.semanticEventType());
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

    private static class SilentMonitor implements Monitor {
    }
}
