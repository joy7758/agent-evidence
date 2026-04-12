package org.agentevidence.edc.spike.grouping;

import org.agentevidence.edc.spike.fixtures.ControlPlaneEventFixtures;
import org.agentevidence.edc.spike.mapper.AgentEvidenceEventMapper;
import org.agentevidence.edc.spike.model.ObservedControlPlaneEvent;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;

class AgentEvidenceGroupingStrategyTest {
    private final AgentEvidenceEventMapper mapper = new AgentEvidenceEventMapper();
    private final AgentEvidenceGroupingStrategy strategy = new AgentEvidenceGroupingStrategy();

    @Test
    void shouldPreferTransferProcessIdForFinalBundleKeyOnRealTransferPayload() {
        var observed = ObservedControlPlaneEvent.from(
                ControlPlaneEventFixtures.transferProcessStartedEnvelope("env-transfer-started", 1_712_780_800_000L)
        );
        var fragment = mapper.map(observed).orElseThrow();

        var correlation = strategy.correlate(fragment);

        assertEquals("contract_agreement_id", strategy.stagingCorrelationField());
        assertEquals("transfer_process_id", strategy.recommendedGroupingKey());
        assertEquals(ControlPlaneEventFixtures.CONTRACT_AGREEMENT_ID, correlation.stagingCorrelationKey());
        assertEquals(ControlPlaneEventFixtures.TRANSFER_PROCESS_ID, correlation.finalBundleKey());
        assertEquals(ControlPlaneEventFixtures.TRANSFER_PROCESS_ID, correlation.effectiveOutputKey());
        assertEquals(
                "participant-a::tp-1::dataspace.transfer.started",
                correlation.semanticDeduplicationKey()
        );
    }

    @Test
    void shouldFallBackToAgreementIdBeforeTransferExists() {
        var observed = ObservedControlPlaneEvent.from(
                ControlPlaneEventFixtures.contractNegotiationFinalizedEnvelope("env-neg-finalized", 1_712_780_801_000L)
        );
        var fragment = mapper.map(observed).orElseThrow();

        var correlation = strategy.correlate(fragment);

        assertEquals(ControlPlaneEventFixtures.CONTRACT_AGREEMENT_ID, correlation.stagingCorrelationKey());
        assertNull(correlation.finalBundleKey());
        assertEquals(ControlPlaneEventFixtures.CONTRACT_AGREEMENT_ID, correlation.effectiveOutputKey());
        assertNotNull(correlation.semanticDeduplicationKey());
    }
}
