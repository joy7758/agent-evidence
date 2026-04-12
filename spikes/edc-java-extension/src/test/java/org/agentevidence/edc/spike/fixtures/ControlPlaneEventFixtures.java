package org.agentevidence.edc.spike.fixtures;

import org.eclipse.edc.connector.controlplane.asset.spi.event.AssetCreated;
import org.eclipse.edc.connector.controlplane.contract.spi.event.contractdefinition.ContractDefinitionCreated;
import org.eclipse.edc.connector.controlplane.contract.spi.event.contractnegotiation.ContractNegotiationFinalized;
import org.eclipse.edc.connector.controlplane.contract.spi.event.contractnegotiation.ContractNegotiationRequested;
import org.eclipse.edc.connector.controlplane.contract.spi.event.contractnegotiation.ContractNegotiationTerminated;
import org.eclipse.edc.connector.controlplane.contract.spi.types.agreement.ContractAgreement;
import org.eclipse.edc.connector.controlplane.contract.spi.types.offer.ContractOffer;
import org.eclipse.edc.connector.controlplane.policy.spi.event.PolicyDefinitionCreated;
import org.eclipse.edc.connector.controlplane.transfer.spi.event.TransferProcessCompleted;
import org.eclipse.edc.connector.controlplane.transfer.spi.event.TransferProcessRequested;
import org.eclipse.edc.connector.controlplane.transfer.spi.event.TransferProcessStarted;
import org.eclipse.edc.connector.controlplane.transfer.spi.event.TransferProcessSuspended;
import org.eclipse.edc.connector.controlplane.transfer.spi.event.TransferProcessTerminated;
import org.eclipse.edc.policy.model.Policy;
import org.eclipse.edc.policy.model.PolicyType;
import org.eclipse.edc.spi.event.Event;
import org.eclipse.edc.spi.event.EventEnvelope;
import org.eclipse.edc.spi.types.domain.DataAddress;
import org.eclipse.edc.spi.types.domain.callback.CallbackAddress;

import java.util.List;
import java.util.Set;

public final class ControlPlaneEventFixtures {
    public static final String PARTICIPANT_CONTEXT_ID = "participant-a";
    public static final String PROVIDER_ID = "provider-a";
    public static final String CONSUMER_ID = "consumer-b";
    public static final String ASSET_ID = "asset-1";
    public static final String POLICY_DEFINITION_ID = "policy-1";
    public static final String CONTRACT_DEFINITION_ID = "contract-def-1";
    public static final String CONTRACT_NEGOTIATION_ID = "neg-1";
    public static final String CONTRACT_AGREEMENT_ID = "agreement-1";
    public static final String CONTRACT_AGREEMENT_INTERNAL_ID = "agreement-internal-1";
    public static final String TRANSFER_PROCESS_ID = "tp-1";
    public static final String PROTOCOL = "dataspace-protocol-http";
    public static final String COUNTERPARTY_ADDRESS = "https://consumer.example/protocol";
    public static final String CALLBACK_URI = "https://consumer.example/callback";
    public static final String TRANSFER_TYPE = "HttpData-PULL";

    private ControlPlaneEventFixtures() {
    }

    public static EventEnvelope<AssetCreated> assetCreatedEnvelope(String envelopeId, long at) {
        var payload = AssetCreated.Builder.newInstance()
                .assetId(ASSET_ID)
                .participantContextId(PARTICIPANT_CONTEXT_ID)
                .build();
        return envelope(envelopeId, at, payload);
    }

    public static EventEnvelope<PolicyDefinitionCreated> policyDefinitionCreatedEnvelope(String envelopeId, long at) {
        var payload = PolicyDefinitionCreated.Builder.newInstance()
                .policyDefinitionId(POLICY_DEFINITION_ID)
                .participantContextId(PARTICIPANT_CONTEXT_ID)
                .build();
        return envelope(envelopeId, at, payload);
    }

    public static EventEnvelope<ContractDefinitionCreated> contractDefinitionCreatedEnvelope(String envelopeId, long at) {
        var payload = ContractDefinitionCreated.Builder.newInstance()
                .contractDefinitionId(CONTRACT_DEFINITION_ID)
                .participantContextId(PARTICIPANT_CONTEXT_ID)
                .build();
        return envelope(envelopeId, at, payload);
    }

    public static EventEnvelope<ContractNegotiationRequested> contractNegotiationRequestedEnvelope(String envelopeId, long at) {
        var payload = ContractNegotiationRequested.Builder.newInstance()
                .contractNegotiationId(CONTRACT_NEGOTIATION_ID)
                .counterPartyAddress(COUNTERPARTY_ADDRESS)
                .counterPartyId(CONSUMER_ID)
                .contractOffers(List.of(contractOffer()))
                .callbackAddresses(List.of(callbackAddress("contract.negotiation.requested")))
                .participantContextId(PARTICIPANT_CONTEXT_ID)
                .protocol(PROTOCOL)
                .build();
        return envelope(envelopeId, at, payload);
    }

    public static EventEnvelope<ContractNegotiationFinalized> contractNegotiationFinalizedEnvelope(String envelopeId, long at) {
        var payload = ContractNegotiationFinalized.Builder.newInstance()
                .contractNegotiationId(CONTRACT_NEGOTIATION_ID)
                .counterPartyAddress(COUNTERPARTY_ADDRESS)
                .counterPartyId(CONSUMER_ID)
                .contractOffers(List.of(contractOffer()))
                .callbackAddresses(List.of(callbackAddress("contract.negotiation.finalized")))
                .participantContextId(PARTICIPANT_CONTEXT_ID)
                .protocol(PROTOCOL)
                .contractAgreement(contractAgreement())
                .build();
        return envelope(envelopeId, at, payload);
    }

    public static EventEnvelope<ContractNegotiationTerminated> contractNegotiationTerminatedEnvelope(String envelopeId, long at) {
        var payload = ContractNegotiationTerminated.Builder.newInstance()
                .contractNegotiationId(CONTRACT_NEGOTIATION_ID)
                .counterPartyAddress(COUNTERPARTY_ADDRESS)
                .counterPartyId(CONSUMER_ID)
                .contractOffers(List.of(contractOffer()))
                .callbackAddresses(List.of(callbackAddress("contract.negotiation.terminated")))
                .participantContextId(PARTICIPANT_CONTEXT_ID)
                .protocol(PROTOCOL)
                .reason("consumer rejected the offer")
                .build();
        return envelope(envelopeId, at, payload);
    }

    public static EventEnvelope<TransferProcessRequested> transferProcessRequestedEnvelope(String envelopeId, long at) {
        var payload = TransferProcessRequested.Builder.newInstance()
                .transferProcessId(TRANSFER_PROCESS_ID)
                .assetId(ASSET_ID)
                .callbackAddresses(List.of(callbackAddress("transfer.process.requested")))
                .type(TRANSFER_TYPE)
                .contractId(CONTRACT_AGREEMENT_ID)
                .participantContextId(PARTICIPANT_CONTEXT_ID)
                .protocol(PROTOCOL)
                .build();
        return envelope(envelopeId, at, payload);
    }

    public static EventEnvelope<TransferProcessStarted> transferProcessStartedEnvelope(String envelopeId, long at) {
        var payload = TransferProcessStarted.Builder.newInstance()
                .transferProcessId(TRANSFER_PROCESS_ID)
                .assetId(ASSET_ID)
                .callbackAddresses(List.of(callbackAddress("transfer.process.started")))
                .type(TRANSFER_TYPE)
                .contractId(CONTRACT_AGREEMENT_ID)
                .participantContextId(PARTICIPANT_CONTEXT_ID)
                .protocol(PROTOCOL)
                .dataAddress(dataAddress())
                .build();
        return envelope(envelopeId, at, payload);
    }

    public static EventEnvelope<TransferProcessCompleted> transferProcessCompletedEnvelope(String envelopeId, long at) {
        var payload = TransferProcessCompleted.Builder.newInstance()
                .transferProcessId(TRANSFER_PROCESS_ID)
                .assetId(ASSET_ID)
                .callbackAddresses(List.of(callbackAddress("transfer.process.completed")))
                .type(TRANSFER_TYPE)
                .contractId(CONTRACT_AGREEMENT_ID)
                .participantContextId(PARTICIPANT_CONTEXT_ID)
                .protocol(PROTOCOL)
                .build();
        return envelope(envelopeId, at, payload);
    }

    public static EventEnvelope<TransferProcessTerminated> transferProcessTerminatedEnvelope(String envelopeId, long at) {
        var payload = TransferProcessTerminated.Builder.newInstance()
                .transferProcessId(TRANSFER_PROCESS_ID)
                .assetId(ASSET_ID)
                .callbackAddresses(List.of(callbackAddress("transfer.process.terminated")))
                .type(TRANSFER_TYPE)
                .contractId(CONTRACT_AGREEMENT_ID)
                .participantContextId(PARTICIPANT_CONTEXT_ID)
                .protocol(PROTOCOL)
                .reason("provider aborted the transfer")
                .build();
        return envelope(envelopeId, at, payload);
    }

    public static EventEnvelope<TransferProcessSuspended> transferProcessSuspendedEnvelope(String envelopeId, long at) {
        var payload = TransferProcessSuspended.Builder.newInstance()
                .transferProcessId(TRANSFER_PROCESS_ID)
                .assetId(ASSET_ID)
                .callbackAddresses(List.of(callbackAddress("transfer.process.suspended")))
                .type(TRANSFER_TYPE)
                .contractId(CONTRACT_AGREEMENT_ID)
                .participantContextId(PARTICIPANT_CONTEXT_ID)
                .protocol(PROTOCOL)
                .build();
        return envelope(envelopeId, at, payload);
    }

    private static ContractOffer contractOffer() {
        return ContractOffer.Builder.newInstance()
                .id("offer-1")
                .assetId(ASSET_ID)
                .policy(contractPolicy())
                .build();
    }

    private static ContractAgreement contractAgreement() {
        return ContractAgreement.Builder.newInstance()
                .id(CONTRACT_AGREEMENT_INTERNAL_ID)
                .agreementId(CONTRACT_AGREEMENT_ID)
                .providerId(PROVIDER_ID)
                .consumerId(CONSUMER_ID)
                .contractSigningDate(1_712_780_800_000L)
                .assetId(ASSET_ID)
                .participantContextId(PARTICIPANT_CONTEXT_ID)
                .policy(contractPolicy())
                .build();
    }

    private static Policy contractPolicy() {
        return Policy.Builder.newInstance()
                .type(PolicyType.CONTRACT)
                .assignee(CONSUMER_ID)
                .assigner(PROVIDER_ID)
                .target(ASSET_ID)
                .build();
    }

    private static CallbackAddress callbackAddress(String eventName) {
        return CallbackAddress.Builder.newInstance()
                .uri(CALLBACK_URI)
                .events(Set.of(eventName))
                .transactional(false)
                .build();
    }

    private static DataAddress dataAddress() {
        return DataAddress.Builder.newInstance()
                .type("HttpProxy")
                .property("endpoint", "https://provider.example/data")
                .build();
    }

    private static <E extends Event> EventEnvelope<E> envelope(String envelopeId, long at, E payload) {
        return EventEnvelope.Builder.<E>newInstance()
                .id(envelopeId)
                .at(at)
                .payload(payload)
                .build();
    }
}
