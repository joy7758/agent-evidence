package org.agentevidence.edc.spike.writer;

import org.agentevidence.edc.spike.fixtures.ControlPlaneEventFixtures;
import org.agentevidence.edc.spike.grouping.AgentEvidenceGroupingStrategy;
import org.agentevidence.edc.spike.mapper.AgentEvidenceEventMapper;
import org.agentevidence.edc.spike.model.ObservedControlPlaneEvent;
import org.eclipse.edc.spi.monitor.Monitor;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class FileSystemEvidenceEnvelopeWriterTest {
    private final AgentEvidenceEventMapper mapper = new AgentEvidenceEventMapper();
    private final AgentEvidenceGroupingStrategy grouping = new AgentEvidenceGroupingStrategy();

    @TempDir
    Path tempDir;

    @Test
    void shouldWriteAgreementScopedFragmentBeforeTransferExists() throws Exception {
        var writer = new FileSystemEvidenceEnvelopeWriter(tempDir, new SilentMonitor());
        var fragment = mapper.map(ObservedControlPlaneEvent.from(
                ControlPlaneEventFixtures.contractNegotiationFinalizedEnvelope("env-neg-finalized", 1_712_780_800_000L)
        )).orElseThrow();
        var correlation = grouping.correlate(fragment);

        writer.write(correlation, fragment);

        var outputFile = tempDir.resolve("agreement-1").resolve("evidence-fragments.jsonl");
        var lines = Files.readAllLines(outputFile);

        assertEquals(1, lines.size());
        assertTrue(lines.get(0).contains("\"semanticEventType\":\"dataspace.contract.agreement.established\""));
        assertTrue(lines.get(0).contains("\"providerParticipantId\":\"provider-a\""));
        assertTrue(lines.get(0).contains("\"consumerParticipantId\":\"consumer-b\""));
        assertTrue(lines.get(0).contains("\"effectiveOutputKey\":\"agreement-1\""));
        assertTrue(lines.get(0).contains("\"finalBundleKey\":null"));
    }

    @Test
    void shouldAppendTransferFragmentsIntoSameTransferScopedOutput() throws Exception {
        var writer = new FileSystemEvidenceEnvelopeWriter(tempDir, new SilentMonitor());
        var started = mapper.map(ObservedControlPlaneEvent.from(
                ControlPlaneEventFixtures.transferProcessStartedEnvelope("env-transfer-started", 1_712_780_801_000L)
        )).orElseThrow();
        var completed = mapper.map(ObservedControlPlaneEvent.from(
                ControlPlaneEventFixtures.transferProcessCompletedEnvelope("env-transfer-completed", 1_712_780_802_000L)
        )).orElseThrow();

        writer.write(grouping.correlate(started), started);
        writer.write(grouping.correlate(completed), completed);

        var outputFile = tempDir.resolve("tp-1").resolve("evidence-fragments.jsonl");
        List<String> lines = Files.readAllLines(outputFile);

        assertEquals(2, lines.size());
        assertTrue(lines.get(0).contains("\"semanticEventType\":\"dataspace.transfer.started\""));
        assertTrue(lines.get(1).contains("\"semanticEventType\":\"dataspace.transfer.completed\""));
        assertTrue(lines.get(0).contains("\"effectiveOutputKey\":\"tp-1\""));
        assertTrue(lines.get(1).contains("\"transferType\":\"HttpData-PULL\""));
    }

    private static class SilentMonitor implements Monitor {
    }
}
