package org.agentevidence.edc.spike.writer;

import org.eclipse.edc.spi.monitor.Monitor;

import java.nio.file.Path;

public class ConfigurableEvidenceEnvelopeWriterFactory {
    private static final String SUPPORTED_EXPORTERS = "filesystem, noop, disabled";

    public AgentEvidenceEnvelopeWriter create(AgentEvidenceExporterConfiguration configuration, Monitor monitor) {
        var exporterType = configuration.normalizedExporterType();
        return switch (exporterType) {
            case "filesystem" -> new FileSystemEvidenceEnvelopeWriter(
                    Path.of(configuration.outputDirectory()),
                    monitor
            );
            case "noop", "disabled" -> new NoOpEvidenceEnvelopeWriter(monitor);
            default -> throw new IllegalArgumentException(
                    "Invalid exporter type '" + configuration.exporterType()
                            + "' specified for " + AgentEvidenceExporterConfiguration.EXPORTER_TYPE
                            + ". Supported values: " + SUPPORTED_EXPORTERS + "."
            );
        };
    }
}
