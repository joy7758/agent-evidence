package org.agentevidence.edc.spike.subscriber;

import org.agentevidence.edc.spike.fixtures.ControlPlaneEventFixtures;
import org.agentevidence.edc.spike.grouping.AgentEvidenceGroupingStrategy;
import org.agentevidence.edc.spike.mapper.AgentEvidenceEventMapper;
import org.agentevidence.edc.spike.writer.FileSystemEvidenceEnvelopeWriter;
import org.eclipse.edc.spi.monitor.Monitor;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ControlPlaneEvidenceSubscriberExportContractTest {
    @TempDir
    Path tempDir;

    @Test
    void shouldExportAgreementAndTransferFragmentsIntoExpectedOutputGroups() throws Exception {
        var subscriber = new ControlPlaneEvidenceSubscriber(
                new AgentEvidenceEventMapper(),
                new AgentEvidenceGroupingStrategy(),
                new FileSystemEvidenceEnvelopeWriter(tempDir, new SilentMonitor()),
                null,
                new SilentMonitor()
        );

        subscriber.on(ControlPlaneEventFixtures.contractNegotiationFinalizedEnvelope("env-neg-finalized", 1_712_780_800_000L));
        subscriber.on(ControlPlaneEventFixtures.transferProcessRequestedEnvelope("env-transfer-requested-1", 1_712_780_801_000L));
        subscriber.on(ControlPlaneEventFixtures.transferProcessRequestedEnvelope("env-transfer-requested-1", 1_712_780_801_000L));
        subscriber.on(ControlPlaneEventFixtures.transferProcessRequestedEnvelope("env-transfer-requested-2", 1_712_780_802_000L));
        subscriber.on(ControlPlaneEventFixtures.transferProcessStartedEnvelope("env-transfer-started", 1_712_780_803_000L));
        subscriber.on(ControlPlaneEventFixtures.transferProcessCompletedEnvelope("env-transfer-completed", 1_712_780_804_000L));

        var agreementFile = tempDir.resolve("agreement-1").resolve("evidence-fragments.jsonl");
        var transferFile = tempDir.resolve("tp-1").resolve("evidence-fragments.jsonl");

        List<String> agreementLines = Files.readAllLines(agreementFile);
        List<String> transferLines = Files.readAllLines(transferFile);

        assertEquals(1, agreementLines.size());
        assertTrue(agreementLines.get(0).contains("\"semanticEventType\":\"dataspace.contract.agreement.established\""));
        assertTrue(agreementLines.get(0).contains("\"effectiveOutputKey\":\"agreement-1\""));

        assertEquals(3, transferLines.size());
        assertTrue(transferLines.get(0).contains("\"semanticEventType\":\"dataspace.transfer.requested\""));
        assertTrue(transferLines.get(1).contains("\"semanticEventType\":\"dataspace.transfer.started\""));
        assertTrue(transferLines.get(2).contains("\"semanticEventType\":\"dataspace.transfer.completed\""));
        assertTrue(transferLines.get(0).contains("\"effectiveOutputKey\":\"tp-1\""));
    }

    private static class SilentMonitor implements Monitor {
    }
}
