package org.agentevidence.edc.spike;

import org.agentevidence.edc.spike.fixtures.ControlPlaneEventFixtures;
import org.agentevidence.edc.spike.support.RuntimeWiringTestSupport.FakeServiceExtensionContext;
import org.agentevidence.edc.spike.support.RuntimeWiringTestSupport.RecordingEventRouter;
import org.agentevidence.edc.spike.support.RuntimeWiringTestSupport.RecordingMonitor;
import org.agentevidence.edc.spike.support.RuntimeWiringTestSupport.RecordingTransactionContext;
import org.agentevidence.edc.spike.writer.FileSystemEvidenceEnvelopeWriter;
import org.agentevidence.edc.spike.writer.NoOpEvidenceEnvelopeWriter;
import org.eclipse.edc.connector.controlplane.asset.spi.event.AssetEvent;
import org.eclipse.edc.connector.controlplane.contract.spi.event.contractdefinition.ContractDefinitionEvent;
import org.eclipse.edc.connector.controlplane.contract.spi.event.contractnegotiation.ContractNegotiationEvent;
import org.eclipse.edc.connector.controlplane.policy.spi.event.PolicyDefinitionEvent;
import org.eclipse.edc.connector.controlplane.transfer.spi.event.TransferProcessEvent;
import org.eclipse.edc.transaction.spi.TransactionContext;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AgentEvidenceEdcExtensionSmokeTest {
    @TempDir
    Path tempDir;

    @Test
    void shouldRegisterMinimalControlPlaneFamiliesAsAsyncSubscribers() {
        var eventRouter = new RecordingEventRouter();
        var monitor = new RecordingMonitor();
        var extension = new AgentEvidenceEdcExtension(eventRouter, monitor);
        var context = new FakeServiceExtensionContext(Map.of(), Map.of(), monitor);

        extension.initialize(context);

        assertEquals(
                Set.of(
                        AssetEvent.class,
                        PolicyDefinitionEvent.class,
                        ContractDefinitionEvent.class,
                        ContractNegotiationEvent.class,
                        TransferProcessEvent.class
                ),
                eventRouter.asyncRegistrations()
        );
        assertTrue(eventRouter.syncRegistrations().isEmpty());
    }

    @Test
    void shouldAssembleDefaultFilesystemRuntimeWiring() {
        var eventRouter = new RecordingEventRouter();
        var monitor = new RecordingMonitor();
        var extension = new AgentEvidenceEdcExtension(eventRouter, monitor);
        var context = new FakeServiceExtensionContext(Map.of(), Map.of(), monitor);

        var wiring = extension.buildRuntimeWiring(context, monitor);

        assertEquals(AgentEvidenceEdcExtension.DEFAULT_EXPORTER_TYPE, wiring.exporterConfiguration().normalizedExporterType());
        assertEquals(AgentEvidenceEdcExtension.DEFAULT_OUTPUT_DIR, wiring.exporterConfiguration().outputDirectory());
        assertInstanceOf(FileSystemEvidenceEnvelopeWriter.class, wiring.writer());
        assertNotNull(wiring.mapper());
        assertNotNull(wiring.groupingStrategy());
        assertNotNull(wiring.subscriber());
        assertNull(wiring.transactionContext());
    }

    @Test
    void shouldAssembleNoopRuntimeWiringWhenConfigured() {
        var eventRouter = new RecordingEventRouter();
        var monitor = new RecordingMonitor();
        var transactionContext = new RecordingTransactionContext();
        var extension = new AgentEvidenceEdcExtension(eventRouter, monitor);
        var context = new FakeServiceExtensionContext(
                Map.of(
                        AgentEvidenceEdcExtension.EXPORTER_TYPE, "noop",
                        AgentEvidenceEdcExtension.OUTPUT_DIR, tempDir.resolve("ignored-output").toString()
                ),
                Map.of(TransactionContext.class, transactionContext),
                monitor
        );

        var wiring = extension.buildRuntimeWiring(context, monitor);

        assertEquals("noop", wiring.exporterConfiguration().normalizedExporterType());
        assertInstanceOf(NoOpEvidenceEnvelopeWriter.class, wiring.writer());
        assertEquals(transactionContext, wiring.transactionContext());
    }

    @Test
    void shouldRoutePublishedEventsIntoConfiguredOutputDirectoryUsingTransactionHandoff() throws Exception {
        var eventRouter = new RecordingEventRouter();
        var monitor = new RecordingMonitor();
        var transactionContext = new RecordingTransactionContext();
        var outputDir = tempDir.resolve("custom-export-root");
        var extension = new AgentEvidenceEdcExtension(eventRouter, monitor);
        var context = new FakeServiceExtensionContext(
                Map.of(AgentEvidenceEdcExtension.OUTPUT_DIR, outputDir.toString()),
                Map.of(TransactionContext.class, transactionContext),
                monitor
        );

        extension.initialize(context);

        eventRouter.publish(ControlPlaneEventFixtures.contractNegotiationFinalizedEnvelope("env-neg-finalized", 1_712_780_800_000L));
        eventRouter.publish(ControlPlaneEventFixtures.transferProcessStartedEnvelope("env-transfer-started", 1_712_780_801_000L));

        var agreementFile = outputDir.resolve("agreement-1").resolve("evidence-fragments.jsonl");
        var transferFile = outputDir.resolve("tp-1").resolve("evidence-fragments.jsonl");

        assertEquals(2, transactionContext.executeCount());
        assertTrue(Files.exists(agreementFile));
        assertTrue(Files.exists(transferFile));
        assertTrue(Files.readString(agreementFile).contains("\"effectiveOutputKey\":\"agreement-1\""));
        assertTrue(Files.readString(transferFile).contains("\"effectiveOutputKey\":\"tp-1\""));
        assertTrue(monitor.infoMessages().stream().anyMatch(it -> it.contains("Using agent-evidence exporter type 'filesystem'")));
        assertTrue(monitor.infoMessages().stream().anyMatch(it -> it.contains("Using agent-evidence output directory '" + outputDir)));
        assertTrue(monitor.infoMessages().stream().anyMatch(it -> it.contains("Registered control-plane event subscribers")));
    }

    @Test
    void shouldRunSubscriberChainWithoutWritingFilesWhenNoopExporterIsConfigured() throws Exception {
        var eventRouter = new RecordingEventRouter();
        var monitor = new RecordingMonitor();
        var transactionContext = new RecordingTransactionContext();
        var outputDir = tempDir.resolve("noop-export-root");
        var extension = new AgentEvidenceEdcExtension(eventRouter, monitor);
        var context = new FakeServiceExtensionContext(
                Map.of(
                        AgentEvidenceEdcExtension.EXPORTER_TYPE, "noop",
                        AgentEvidenceEdcExtension.OUTPUT_DIR, outputDir.toString()
                ),
                Map.of(TransactionContext.class, transactionContext),
                monitor
        );

        extension.initialize(context);
        eventRouter.publish(ControlPlaneEventFixtures.transferProcessStartedEnvelope("env-transfer-started", 1_712_780_802_000L));

        assertEquals(1, transactionContext.executeCount());
        assertTrue(Files.notExists(outputDir));
        assertTrue(monitor.infoMessages().stream().anyMatch(it -> it.contains("Using agent-evidence exporter type 'noop'")));
        assertTrue(monitor.infoMessages().stream().anyMatch(it -> it.contains("Using agent-evidence output directory '" + outputDir)));
    }

    @Test
    void shouldFailFastWhenExporterTypeIsUnsupported() {
        var eventRouter = new RecordingEventRouter();
        var monitor = new RecordingMonitor();
        var extension = new AgentEvidenceEdcExtension(eventRouter, monitor);
        var context = new FakeServiceExtensionContext(
                Map.of(AgentEvidenceEdcExtension.EXPORTER_TYPE, "s3"),
                Map.of(),
                monitor
        );

        var error = assertThrows(IllegalArgumentException.class, () -> extension.initialize(context));

        assertTrue(error.getMessage().contains("Unsupported agent-evidence exporter type 's3'"));
        assertTrue(eventRouter.asyncRegistrations().isEmpty());
    }
}
