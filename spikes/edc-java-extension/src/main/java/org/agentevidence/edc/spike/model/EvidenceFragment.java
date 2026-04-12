package org.agentevidence.edc.spike.model;

import java.time.Instant;

public record EvidenceFragment(
        String semanticEventType,
        String edcEventType,
        String envelopeId,
        Instant observedAt,
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
}
