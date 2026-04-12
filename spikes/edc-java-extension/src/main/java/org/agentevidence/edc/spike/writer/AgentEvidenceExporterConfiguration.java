package org.agentevidence.edc.spike.writer;

import org.eclipse.edc.spi.system.ServiceExtensionContext;

import java.util.Locale;

public record AgentEvidenceExporterConfiguration(
        String exporterType,
        String outputDirectory
) {
    public static final String EXPORTER_TYPE = "edc.agent-evidence.exporter.type";
    public static final String OUTPUT_DIR = "edc.agent-evidence.output-dir";
    public static final String DEFAULT_EXPORTER_TYPE = "filesystem";
    public static final String DEFAULT_OUTPUT_DIR = "build/agent-evidence-spike";

    public static AgentEvidenceExporterConfiguration from(ServiceExtensionContext context) {
        return new AgentEvidenceExporterConfiguration(
                context.getSetting(EXPORTER_TYPE, DEFAULT_EXPORTER_TYPE),
                context.getSetting(OUTPUT_DIR, DEFAULT_OUTPUT_DIR)
        );
    }

    public String normalizedExporterType() {
        if (exporterType == null || exporterType.isBlank()) {
            return DEFAULT_EXPORTER_TYPE;
        }
        return exporterType.trim().toLowerCase(Locale.ROOT);
    }

    public String normalizedOutputDirectory() {
        if (outputDirectory == null || outputDirectory.isBlank()) {
            return DEFAULT_OUTPUT_DIR;
        }
        return outputDirectory.trim();
    }
}
