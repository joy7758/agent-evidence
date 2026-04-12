package org.agentevidence.edc.spike.model;

import org.agentevidence.edc.spike.fixtures.ControlPlaneEventFixtures;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;

class ObservedControlPlaneEventTest {
    @Test
    void shouldExtractAgreementAndParticipantsFromFinalizedNegotiationPayload() {
        var observed = ObservedControlPlaneEvent.from(
                ControlPlaneEventFixtures.contractNegotiationFinalizedEnvelope("env-neg-finalized", 1_712_780_800_000L)
        );

        assertEquals("contract.negotiation.finalized", observed.edcEventType());
        assertEquals(ControlPlaneEventFixtures.PARTICIPANT_CONTEXT_ID, observed.participantContextId());
        assertEquals(ControlPlaneEventFixtures.PROVIDER_ID, observed.providerParticipantId());
        assertEquals(ControlPlaneEventFixtures.CONSUMER_ID, observed.consumerParticipantId());
        assertEquals(ControlPlaneEventFixtures.ASSET_ID, observed.assetId());
        assertEquals(ControlPlaneEventFixtures.CONTRACT_NEGOTIATION_ID, observed.contractNegotiationId());
        assertEquals(ControlPlaneEventFixtures.CONTRACT_AGREEMENT_ID, observed.contractAgreementId());
        assertEquals(ControlPlaneEventFixtures.PROTOCOL, observed.protocol());
        assertEquals(ControlPlaneEventFixtures.CONSUMER_ID, observed.counterPartyId());
        assertNull(observed.transferProcessId());
    }

    @Test
    void shouldExtractTransferFieldsFromStartedTransferPayload() {
        var observed = ObservedControlPlaneEvent.from(
                ControlPlaneEventFixtures.transferProcessStartedEnvelope("env-transfer-started", 1_712_780_801_000L)
        );

        assertEquals("transfer.process.started", observed.edcEventType());
        assertEquals(ControlPlaneEventFixtures.PARTICIPANT_CONTEXT_ID, observed.participantContextId());
        assertEquals(ControlPlaneEventFixtures.ASSET_ID, observed.assetId());
        assertEquals(ControlPlaneEventFixtures.CONTRACT_AGREEMENT_ID, observed.contractAgreementId());
        assertEquals(ControlPlaneEventFixtures.TRANSFER_PROCESS_ID, observed.transferProcessId());
        assertEquals(ControlPlaneEventFixtures.PROTOCOL, observed.protocol());
        assertEquals(ControlPlaneEventFixtures.TRANSFER_TYPE, observed.transferType());
        assertEquals("participant-a::env-transfer-started", observed.envelopeDeduplicationKey());
    }
}
