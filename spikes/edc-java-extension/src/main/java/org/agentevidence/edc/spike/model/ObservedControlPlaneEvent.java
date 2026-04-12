package org.agentevidence.edc.spike.model;

import org.eclipse.edc.connector.controlplane.asset.spi.event.AssetEvent;
import org.eclipse.edc.connector.controlplane.contract.spi.event.contractdefinition.ContractDefinitionEvent;
import org.eclipse.edc.connector.controlplane.contract.spi.event.contractnegotiation.ContractNegotiationEvent;
import org.eclipse.edc.connector.controlplane.contract.spi.event.contractnegotiation.ContractNegotiationFinalized;
import org.eclipse.edc.connector.controlplane.policy.spi.event.PolicyDefinitionEvent;
import org.eclipse.edc.connector.controlplane.transfer.spi.event.TransferProcessEvent;
import org.eclipse.edc.spi.event.Event;
import org.eclipse.edc.spi.event.EventEnvelope;

import java.time.Instant;

public record ObservedControlPlaneEvent(
        String envelopeId,
        Instant observedAt,
        String edcEventType,
        String payloadClassName,
        String participantContextId,
        String providerParticipantId,
        String consumerParticipantId,
        String assetId,
        String policyDefinitionId,
        String contractDefinitionId,
        String contractNegotiationId,
        String contractAgreementId,
        String transferProcessId,
        String protocol,
        String counterPartyId,
        String transferType
) {
    public static ObservedControlPlaneEvent from(EventEnvelope<? extends Event> envelope) {
        var payload = envelope.getPayload();
        return new ObservedControlPlaneEvent(
                envelope.getId(),
                Instant.ofEpochMilli(envelope.getAt()),
                payload.name(),
                payload.getClass().getName(),
                participantContextId(payload),
                providerParticipantId(payload),
                consumerParticipantId(payload),
                assetId(payload),
                policyDefinitionId(payload),
                contractDefinitionId(payload),
                contractNegotiationId(payload),
                contractAgreementId(payload),
                transferProcessId(payload),
                protocol(payload),
                counterPartyId(payload),
                transferType(payload)
        );
    }

    public String envelopeDeduplicationKey() {
        return join(participantContextId, envelopeId);
    }

    private static String participantContextId(Event payload) {
        if (payload instanceof AssetEvent event) {
            return event.getParticipantContextId();
        }
        if (payload instanceof PolicyDefinitionEvent event) {
            return event.getParticipantContextId();
        }
        if (payload instanceof ContractDefinitionEvent event) {
            return event.getParticipantContextId();
        }
        if (payload instanceof ContractNegotiationEvent event) {
            return event.getParticipantContextId();
        }
        if (payload instanceof TransferProcessEvent event) {
            return event.getParticipantContextId();
        }
        return null;
    }

    private static String providerParticipantId(Event payload) {
        if (payload instanceof ContractNegotiationFinalized event) {
            return event.getContractAgreement().getProviderId();
        }
        return null;
    }

    private static String consumerParticipantId(Event payload) {
        if (payload instanceof ContractNegotiationFinalized event) {
            return event.getContractAgreement().getConsumerId();
        }
        return null;
    }

    private static String assetId(Event payload) {
        if (payload instanceof AssetEvent event) {
            return event.getAssetId();
        }
        if (payload instanceof TransferProcessEvent event) {
            return event.getAssetId();
        }
        if (payload instanceof ContractNegotiationFinalized event) {
            return event.getContractAgreement().getAssetId();
        }
        return null;
    }

    private static String policyDefinitionId(Event payload) {
        if (payload instanceof PolicyDefinitionEvent event) {
            return event.getPolicyDefinitionId();
        }
        return null;
    }

    private static String contractDefinitionId(Event payload) {
        if (payload instanceof ContractDefinitionEvent event) {
            return event.getContractDefinitionId();
        }
        return null;
    }

    private static String contractNegotiationId(Event payload) {
        if (payload instanceof ContractNegotiationEvent event) {
            return event.getContractNegotiationId();
        }
        return null;
    }

    private static String contractAgreementId(Event payload) {
        if (payload instanceof ContractNegotiationFinalized event) {
            var agreement = event.getContractAgreement();
            return firstNonBlank(agreement.getAgreementId(), agreement.getId());
        }
        if (payload instanceof TransferProcessEvent event) {
            return event.getContractId();
        }
        return null;
    }

    private static String transferProcessId(Event payload) {
        if (payload instanceof TransferProcessEvent event) {
            return event.getTransferProcessId();
        }
        return null;
    }

    private static String protocol(Event payload) {
        if (payload instanceof ContractNegotiationEvent event) {
            return event.getProtocol();
        }
        if (payload instanceof TransferProcessEvent event) {
            return event.getProtocol();
        }
        return null;
    }

    private static String counterPartyId(Event payload) {
        if (payload instanceof ContractNegotiationEvent event) {
            return event.getCounterPartyId();
        }
        return null;
    }

    private static String transferType(Event payload) {
        if (payload instanceof TransferProcessEvent event) {
            return event.getType();
        }
        return null;
    }

    private static String firstNonBlank(String first, String fallback) {
        if (first != null && !first.isBlank()) {
            return first;
        }
        return fallback;
    }

    private static String join(String left, String right) {
        return (left == null ? "unknown" : left) + "::" + (right == null ? "unknown" : right);
    }
}
