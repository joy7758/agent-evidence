package org.agentevidence.edc.spike.writer;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class AgentEvidenceExporterConfigurationTest {
    @Test
    void shouldNormalizeExporterTypeByTrimmingAndLowercasing() {
        var configuration = new AgentEvidenceExporterConfiguration("  NoOp  ", " build/custom-output ");

        assertEquals("noop", configuration.normalizedExporterType());
        assertEquals("build/custom-output", configuration.normalizedOutputDirectory());
    }

    @Test
    void shouldFallbackToDefaultsWhenConfigurationValuesAreBlank() {
        var configuration = new AgentEvidenceExporterConfiguration("   ", "   ");

        assertEquals(AgentEvidenceExporterConfiguration.DEFAULT_EXPORTER_TYPE, configuration.normalizedExporterType());
        assertEquals(AgentEvidenceExporterConfiguration.DEFAULT_OUTPUT_DIR, configuration.normalizedOutputDirectory());
    }
}
