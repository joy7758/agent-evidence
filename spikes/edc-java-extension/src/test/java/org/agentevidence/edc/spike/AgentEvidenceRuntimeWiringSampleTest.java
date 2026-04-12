package org.agentevidence.edc.spike;

import org.agentevidence.edc.spike.fixtures.ControlPlaneEventFixtures;
import org.agentevidence.edc.spike.support.RuntimeWiringTestSupport.FakeServiceExtensionContext;
import org.agentevidence.edc.spike.support.RuntimeWiringTestSupport.RecordingEventRouter;
import org.agentevidence.edc.spike.support.RuntimeWiringTestSupport.RecordingMonitor;
import org.agentevidence.edc.spike.support.RuntimeWiringTestSupport.RecordingTransactionContext;
import org.agentevidence.edc.spike.writer.ConfigurableEvidenceEnvelopeWriterFactory;
import org.eclipse.edc.transaction.spi.TransactionContext;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AgentEvidenceRuntimeWiringSampleTest {
    @TempDir
    Path tempDir;

    @Test
    void shouldMatchFilesystemRuntimeWiringSample() throws Exception {
        var eventRouter = new RecordingEventRouter();
        var monitor = new RecordingMonitor();
        var transactionContext = new RecordingTransactionContext();
        var outputDir = tempDir.resolve("filesystem-sample");
        var context = new FakeServiceExtensionContext(
                Map.of(AgentEvidenceEdcExtension.OUTPUT_DIR, outputDir.toString()),
                Map.of(TransactionContext.class, transactionContext),
                monitor
        );

        var wiring = AgentEvidenceRuntimeWiring.from(
                context,
                monitor,
                new ConfigurableEvidenceEnvelopeWriterFactory()
        );
        AgentEvidenceEdcExtension.registerMinimalControlPlaneSubscribers(eventRouter, wiring.subscriber());

        eventRouter.publish(ControlPlaneEventFixtures.contractNegotiationFinalizedEnvelope("sample-neg-finalized", 1_712_780_900_000L));
        eventRouter.publish(ControlPlaneEventFixtures.transferProcessStartedEnvelope("sample-transfer-started", 1_712_780_901_000L));

        var agreementFile = outputDir.resolve("agreement-1").resolve("evidence-fragments.jsonl");
        var transferFile = outputDir.resolve("tp-1").resolve("evidence-fragments.jsonl");

        assertEquals("filesystem", wiring.exporterConfiguration().normalizedExporterType());
        assertEquals(outputDir.toString(), wiring.exporterConfiguration().normalizedOutputDirectory());
        assertEquals(2, transactionContext.executeCount());
        assertTrue(Files.exists(agreementFile));
        assertTrue(Files.exists(transferFile));
        assertTrue(Files.readString(agreementFile).contains("\"semanticEventType\":\"dataspace.contract.agreement.established\""));
        assertTrue(Files.readString(agreementFile).contains("\"effectiveOutputKey\":\"agreement-1\""));
        assertTrue(Files.readString(transferFile).contains("\"semanticEventType\":\"dataspace.transfer.started\""));
        assertTrue(Files.readString(transferFile).contains("\"effectiveOutputKey\":\"tp-1\""));
    }

    @Test
    void shouldMatchNoopRuntimeWiringSample() throws Exception {
        var eventRouter = new RecordingEventRouter();
        var monitor = new RecordingMonitor();
        var transactionContext = new RecordingTransactionContext();
        var outputDir = tempDir.resolve("noop-sample");
        var context = new FakeServiceExtensionContext(
                Map.of(
                        AgentEvidenceEdcExtension.EXPORTER_TYPE, "noop",
                        AgentEvidenceEdcExtension.OUTPUT_DIR, outputDir.toString()
                ),
                Map.of(TransactionContext.class, transactionContext),
                monitor
        );

        var wiring = AgentEvidenceRuntimeWiring.from(
                context,
                monitor,
                new ConfigurableEvidenceEnvelopeWriterFactory()
        );
        AgentEvidenceEdcExtension.registerMinimalControlPlaneSubscribers(eventRouter, wiring.subscriber());

        eventRouter.publish(ControlPlaneEventFixtures.transferProcessStartedEnvelope("sample-transfer-started", 1_712_780_902_000L));

        assertEquals("noop", wiring.exporterConfiguration().normalizedExporterType());
        assertEquals(outputDir.toString(), wiring.exporterConfiguration().normalizedOutputDirectory());
        assertEquals(1, transactionContext.executeCount());
        assertTrue(Files.notExists(outputDir));
    }
}
