package org.agentevidence.edc.spike.model;

public record BundleCorrelationContext(
        String stagingCorrelationKey,
        String finalBundleKey,
        String envelopeDeduplicationKey,
        String semanticDeduplicationKey
) {
    public String effectiveOutputKey() {
        if (finalBundleKey != null && !finalBundleKey.isBlank()) {
            return finalBundleKey;
        }
        if (stagingCorrelationKey != null && !stagingCorrelationKey.isBlank()) {
            return stagingCorrelationKey;
        }
        return "unassigned";
    }
}
