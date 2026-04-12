package org.agentevidence.edc.spike.mapper;

import org.agentevidence.edc.spike.fixtures.ControlPlaneEventFixtures;
import org.agentevidence.edc.spike.model.EvidenceFragment;
import org.agentevidence.edc.spike.model.ObservedControlPlaneEvent;
import org.eclipse.edc.spi.event.Event;
import org.eclipse.edc.spi.event.EventEnvelope;
import org.junit.jupiter.api.Test;

import java.util.function.Consumer;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AgentEvidenceEventMapperTest {
    private final AgentEvidenceEventMapper mapper = new AgentEvidenceEventMapper();

    @Test
    void shouldMapGovernanceRegistrationEventsInMinimalScope() {
        assertMapped(
                ControlPlaneEventFixtures.assetCreatedEnvelope("env-asset-created", 1_712_780_800_000L),
                "dataspace.asset.registered",
                fragment -> assertEquals(ControlPlaneEventFixtures.ASSET_ID, fragment.assetId())
        );
        assertMapped(
                ControlPlaneEventFixtures.policyDefinitionCreatedEnvelope("env-policy-created", 1_712_780_801_000L),
                "dataspace.policy.definition.registered",
                fragment -> assertEquals(ControlPlaneEventFixtures.POLICY_DEFINITION_ID, fragment.policyDefinitionId())
        );
        assertMapped(
                ControlPlaneEventFixtures.contractDefinitionCreatedEnvelope("env-contract-definition-created", 1_712_780_802_000L),
                "dataspace.contract.definition.bound",
                fragment -> assertEquals(ControlPlaneEventFixtures.CONTRACT_DEFINITION_ID, fragment.contractDefinitionId())
        );
    }

    @Test
    void shouldMapContractNegotiationEventsInMinimalScope() {
        assertMapped(
                ControlPlaneEventFixtures.contractNegotiationRequestedEnvelope("env-neg-requested", 1_712_780_803_000L),
                "dataspace.contract.negotiation.requested",
                fragment -> {
                    assertEquals(ControlPlaneEventFixtures.CONTRACT_NEGOTIATION_ID, fragment.contractNegotiationId());
                    assertEquals(ControlPlaneEventFixtures.CONSUMER_ID, fragment.counterPartyId());
                }
        );
        assertMapped(
                ControlPlaneEventFixtures.contractNegotiationFinalizedEnvelope("env-neg-finalized", 1_712_780_804_000L),
                "dataspace.contract.agreement.established",
                fragment -> {
                    assertEquals(ControlPlaneEventFixtures.PROVIDER_ID, fragment.providerParticipantId());
                    assertEquals(ControlPlaneEventFixtures.CONSUMER_ID, fragment.consumerParticipantId());
                    assertEquals(ControlPlaneEventFixtures.CONTRACT_AGREEMENT_ID, fragment.contractAgreementId());
                }
        );
        assertMapped(
                ControlPlaneEventFixtures.contractNegotiationTerminatedEnvelope("env-neg-terminated", 1_712_780_805_000L),
                "dataspace.contract.negotiation.terminated",
                fragment -> assertEquals(ControlPlaneEventFixtures.CONTRACT_NEGOTIATION_ID, fragment.contractNegotiationId())
        );
    }

    @Test
    void shouldMapTransferProcessEventsInMinimalScope() {
        assertMapped(
                ControlPlaneEventFixtures.transferProcessRequestedEnvelope("env-transfer-requested", 1_712_780_806_000L),
                "dataspace.transfer.requested",
                fragment -> {
                    assertEquals(ControlPlaneEventFixtures.TRANSFER_PROCESS_ID, fragment.transferProcessId());
                    assertEquals(ControlPlaneEventFixtures.CONTRACT_AGREEMENT_ID, fragment.contractAgreementId());
                }
        );
        assertMapped(
                ControlPlaneEventFixtures.transferProcessStartedEnvelope("env-transfer-started", 1_712_780_807_000L),
                "dataspace.transfer.started",
                fragment -> {
                    assertEquals(ControlPlaneEventFixtures.TRANSFER_PROCESS_ID, fragment.transferProcessId());
                    assertEquals(ControlPlaneEventFixtures.TRANSFER_TYPE, fragment.transferType());
                }
        );
        assertMapped(
                ControlPlaneEventFixtures.transferProcessCompletedEnvelope("env-transfer-completed", 1_712_780_808_000L),
                "dataspace.transfer.completed",
                fragment -> assertEquals(ControlPlaneEventFixtures.TRANSFER_PROCESS_ID, fragment.transferProcessId())
        );
        assertMapped(
                ControlPlaneEventFixtures.transferProcessTerminatedEnvelope("env-transfer-terminated", 1_712_780_809_000L),
                "dataspace.transfer.terminated",
                fragment -> assertEquals(ControlPlaneEventFixtures.TRANSFER_PROCESS_ID, fragment.transferProcessId())
        );
    }

    @Test
    void shouldIgnoreOutOfScopeTransferProcessSuspendedPayload() {
        var observed = ObservedControlPlaneEvent.from(
                ControlPlaneEventFixtures.transferProcessSuspendedEnvelope("env-transfer-suspended", 1_712_780_802_000L)
        );

        assertFalse(mapper.isInMinimalScope(observed.edcEventType()));
        assertTrue(mapper.map(observed).isEmpty());
    }

    private void assertMapped(
            EventEnvelope<? extends Event> envelope,
            String expectedSemanticEventType,
            Consumer<EvidenceFragment> assertions
    ) {
        var observed = ObservedControlPlaneEvent.from(envelope);
        var mapped = mapper.map(observed);

        assertTrue(mapped.isPresent());
        assertEquals(expectedSemanticEventType, mapped.get().semanticEventType());
        assertEquals(observed.edcEventType(), mapped.get().edcEventType());
        assertions.accept(mapped.get());
    }
}
