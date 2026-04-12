package org.agentevidence.edc.spike.mapper;

import org.agentevidence.edc.spike.model.EvidenceFragment;
import org.agentevidence.edc.spike.model.ObservedControlPlaneEvent;

import java.util.Optional;
import java.util.Set;

public class AgentEvidenceEventMapper {
    private static final Set<String> MINIMAL_EVENT_SCOPE = Set.of(
            "asset.created",
            "policy.definition.created",
            "contract.definition.created",
            "contract.negotiation.requested",
            "contract.negotiation.finalized",
            "contract.negotiation.terminated",
            "transfer.process.requested",
            "transfer.process.started",
            "transfer.process.completed",
            "transfer.process.terminated"
    );

    public Optional<EvidenceFragment> map(ObservedControlPlaneEvent event) {
        var semanticEventType = semanticEventType(event.edcEventType());
        if (semanticEventType == null) {
            return Optional.empty();
        }

        return Optional.of(new EvidenceFragment(
                semanticEventType,
                event.edcEventType(),
                event.envelopeId(),
                event.observedAt(),
                event.participantContextId(),
                event.providerParticipantId(),
                event.consumerParticipantId(),
                event.assetId(),
                event.policyDefinitionId(),
                event.contractDefinitionId(),
                event.contractNegotiationId(),
                event.contractAgreementId(),
                event.transferProcessId(),
                event.protocol(),
                event.counterPartyId(),
                event.transferType()
        ));
    }

    public boolean isInMinimalScope(String edcEventType) {
        return MINIMAL_EVENT_SCOPE.contains(edcEventType);
    }

    private String semanticEventType(String edcEventType) {
        return switch (edcEventType) {
            case "asset.created" -> "dataspace.asset.registered";
            case "policy.definition.created" -> "dataspace.policy.definition.registered";
            case "contract.definition.created" -> "dataspace.contract.definition.bound";
            case "contract.negotiation.requested" -> "dataspace.contract.negotiation.requested";
            case "contract.negotiation.finalized" -> "dataspace.contract.agreement.established";
            case "contract.negotiation.terminated" -> "dataspace.contract.negotiation.terminated";
            case "transfer.process.requested" -> "dataspace.transfer.requested";
            case "transfer.process.started" -> "dataspace.transfer.started";
            case "transfer.process.completed" -> "dataspace.transfer.completed";
            case "transfer.process.terminated" -> "dataspace.transfer.terminated";
            default -> null;
        };
    }
}
