package org.agentevidence.edc.spike.grouping;

import org.agentevidence.edc.spike.model.BundleCorrelationContext;
import org.agentevidence.edc.spike.model.EvidenceFragment;

public class AgentEvidenceGroupingStrategy {
    public BundleCorrelationContext correlate(EvidenceFragment fragment) {
        return new BundleCorrelationContext(
                fragment.contractAgreementId(),
                fragment.transferProcessId(),
                envelopeDeduplicationKey(fragment),
                semanticDeduplicationKey(fragment)
        );
    }

    public String recommendedGroupingKey() {
        return "transfer_process_id";
    }

    public String stagingCorrelationField() {
        return "contract_agreement_id";
    }

    private String envelopeDeduplicationKey(EvidenceFragment fragment) {
        return join(fragment.participantContextId(), fragment.envelopeId());
    }

    private String semanticDeduplicationKey(EvidenceFragment fragment) {
        var domainId = firstNonBlank(
                fragment.transferProcessId(),
                fragment.contractAgreementId(),
                fragment.contractNegotiationId(),
                fragment.assetId()
        );
        return join(join(fragment.participantContextId(), domainId), fragment.semanticEventType());
    }

    private String firstNonBlank(String... values) {
        for (var value : values) {
            if (value != null && !value.isBlank()) {
                return value;
            }
        }
        return "unassigned";
    }

    private String join(String left, String right) {
        return (left == null ? "unknown" : left) + "::" + (right == null ? "unknown" : right);
    }
}
