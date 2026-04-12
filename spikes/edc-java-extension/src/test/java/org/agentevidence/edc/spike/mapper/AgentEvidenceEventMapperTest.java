package org.agentevidence.edc.spike.mapper;

import org.agentevidence.edc.spike.fixtures.ControlPlaneEventFixtures;
import org.agentevidence.edc.spike.model.ObservedControlPlaneEvent;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AgentEvidenceEventMapperTest {
    private final AgentEvidenceEventMapper mapper = new AgentEvidenceEventMapper();

    @Test
    void shouldMapTransferProcessStartedPayloadToSemanticEvent() {
        var observed = ObservedControlPlaneEvent.from(
                ControlPlaneEventFixtures.transferProcessStartedEnvelope("env-transfer-started", 1_712_780_800_000L)
        );

        var mapped = mapper.map(observed);

        assertTrue(mapped.isPresent());
        assertEquals("transfer.process.started", observed.edcEventType());
        assertEquals("dataspace.transfer.started", mapped.get().semanticEventType());
        assertEquals(ControlPlaneEventFixtures.TRANSFER_PROCESS_ID, mapped.get().transferProcessId());
        assertEquals(ControlPlaneEventFixtures.CONTRACT_AGREEMENT_ID, mapped.get().contractAgreementId());
    }

    @Test
    void shouldMapContractNegotiationFinalizedPayloadToAgreementEstablishedEvent() {
        var observed = ObservedControlPlaneEvent.from(
                ControlPlaneEventFixtures.contractNegotiationFinalizedEnvelope("env-neg-finalized", 1_712_780_801_000L)
        );

        var mapped = mapper.map(observed);

        assertTrue(mapped.isPresent());
        assertEquals("contract.negotiation.finalized", observed.edcEventType());
        assertEquals("dataspace.contract.agreement.established", mapped.get().semanticEventType());
        assertEquals(ControlPlaneEventFixtures.PROVIDER_ID, mapped.get().providerParticipantId());
        assertEquals(ControlPlaneEventFixtures.CONSUMER_ID, mapped.get().consumerParticipantId());
        assertEquals(ControlPlaneEventFixtures.CONTRACT_AGREEMENT_ID, mapped.get().contractAgreementId());
    }

    @Test
    void shouldIgnoreOutOfScopeTransferProcessSuspendedPayload() {
        var observed = ObservedControlPlaneEvent.from(
                ControlPlaneEventFixtures.transferProcessSuspendedEnvelope("env-transfer-suspended", 1_712_780_802_000L)
        );

        assertFalse(mapper.isInMinimalScope(observed.edcEventType()));
        assertTrue(mapper.map(observed).isEmpty());
    }
}
