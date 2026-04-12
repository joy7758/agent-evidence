package org.agentevidence.edc.spike.writer;

import org.eclipse.edc.spi.monitor.Monitor;

import java.nio.file.Path;

public class ConfigurableEvidenceEnvelopeWriterFactory {
    public AgentEvidenceEnvelopeWriter create(AgentEvidenceExporterConfiguration configuration, Monitor monitor) {
        var exporterType = configuration.normalizedExporterType();
        return switch (exporterType) {
            case "filesystem" -> new FileSystemEvidenceEnvelopeWriter(
                    Path.of(configuration.outputDirectory()),
                    monitor
            );
            case "noop", "disabled" -> new NoOpEvidenceEnvelopeWriter(monitor);
            default -> throw new IllegalArgumentException(
                    "Unsupported agent-evidence exporter type '" + configuration.exporterType()
                            + "'. Supported values: filesystem, noop, disabled."
            );
        };
    }
}
