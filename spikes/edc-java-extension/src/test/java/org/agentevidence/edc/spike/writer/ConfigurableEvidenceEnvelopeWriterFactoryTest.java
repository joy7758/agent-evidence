package org.agentevidence.edc.spike.writer;

import org.eclipse.edc.spi.monitor.Monitor;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertThrows;

class ConfigurableEvidenceEnvelopeWriterFactoryTest {
    private final ConfigurableEvidenceEnvelopeWriterFactory factory = new ConfigurableEvidenceEnvelopeWriterFactory();
    private final Monitor monitor = new SilentMonitor();

    @Test
    void shouldDefaultToFilesystemWhenExporterTypeIsMissing() {
        var configuration = new AgentEvidenceExporterConfiguration(null, "build/test-export");

        var writer = factory.create(configuration, monitor);

        assertInstanceOf(FileSystemEvidenceEnvelopeWriter.class, writer);
    }

    @Test
    void shouldSelectNoopExporterForNoopAndDisabledTypes() {
        assertInstanceOf(
                NoOpEvidenceEnvelopeWriter.class,
                factory.create(new AgentEvidenceExporterConfiguration("noop", "build/test-export"), monitor)
        );
        assertInstanceOf(
                NoOpEvidenceEnvelopeWriter.class,
                factory.create(new AgentEvidenceExporterConfiguration("disabled", "build/test-export"), monitor)
        );
        assertInstanceOf(
                NoOpEvidenceEnvelopeWriter.class,
                factory.create(new AgentEvidenceExporterConfiguration("  NoOp  ", "build/test-export"), monitor)
        );
    }

    @Test
    void shouldFailFastOnUnsupportedExporterType() {
        var error = assertThrows(
                IllegalArgumentException.class,
                () -> factory.create(new AgentEvidenceExporterConfiguration("s3", "build/test-export"), monitor)
        );

        org.junit.jupiter.api.Assertions.assertTrue(
                error.getMessage().contains("Invalid exporter type 's3' specified for edc.agent-evidence.exporter.type")
        );
    }

    private static class SilentMonitor implements Monitor {
    }
}
