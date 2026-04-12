package org.agentevidence.edc.spike;

import org.agentevidence.edc.spike.grouping.AgentEvidenceGroupingStrategy;
import org.agentevidence.edc.spike.mapper.AgentEvidenceEventMapper;
import org.agentevidence.edc.spike.subscriber.ControlPlaneEvidenceSubscriber;
import org.agentevidence.edc.spike.writer.FileSystemEvidenceEnvelopeWriter;
import org.eclipse.edc.connector.controlplane.asset.spi.event.AssetEvent;
import org.eclipse.edc.connector.controlplane.contract.spi.event.contractdefinition.ContractDefinitionEvent;
import org.eclipse.edc.connector.controlplane.contract.spi.event.contractnegotiation.ContractNegotiationEvent;
import org.eclipse.edc.connector.controlplane.policy.spi.event.PolicyDefinitionEvent;
import org.eclipse.edc.connector.controlplane.transfer.spi.event.TransferProcessEvent;
import org.eclipse.edc.runtime.metamodel.annotation.Extension;
import org.eclipse.edc.runtime.metamodel.annotation.Inject;
import org.eclipse.edc.spi.event.EventRouter;
import org.eclipse.edc.spi.monitor.Monitor;
import org.eclipse.edc.spi.system.ServiceExtension;
import org.eclipse.edc.spi.system.ServiceExtensionContext;
import org.eclipse.edc.transaction.spi.TransactionContext;

import java.nio.file.Path;

@Extension(value = AgentEvidenceEdcExtension.NAME)
public class AgentEvidenceEdcExtension implements ServiceExtension {
    public static final String NAME = "Agent Evidence EDC control-plane extension spike";
    public static final String OUTPUT_DIR = "edc.agent-evidence.output-dir";
    public static final String DEFAULT_OUTPUT_DIR = "build/agent-evidence-spike";

    @Inject
    private EventRouter eventRouter;

    @Inject
    private Monitor monitor;

    @Override
    public String name() {
        return NAME;
    }

    @Override
    public void initialize(ServiceExtensionContext context) {
        var extensionMonitor = monitor.withPrefix("AgentEvidenceEdcExtension");
        var mapper = new AgentEvidenceEventMapper();
        var groupingStrategy = new AgentEvidenceGroupingStrategy();
        var writer = new FileSystemEvidenceEnvelopeWriter(
                Path.of(context.getSetting(OUTPUT_DIR, DEFAULT_OUTPUT_DIR)),
                extensionMonitor
        );

        var transactionContext = optionalTransactionContext(context);
        var subscriber = new ControlPlaneEvidenceSubscriber(
                mapper,
                groupingStrategy,
                writer,
                transactionContext,
                extensionMonitor
        );

        // Async registration keeps the first spike focused on low-friction export.
        // TODO: evaluate registerSync(...) once the writer moves to an outbox or staged local store.
        eventRouter.register(AssetEvent.class, subscriber);
        eventRouter.register(PolicyDefinitionEvent.class, subscriber);
        eventRouter.register(ContractDefinitionEvent.class, subscriber);
        eventRouter.register(ContractNegotiationEvent.class, subscriber);
        eventRouter.register(TransferProcessEvent.class, subscriber);

        extensionMonitor.info("Registered control-plane event subscribers for agent-evidence spike");
    }

    private TransactionContext optionalTransactionContext(ServiceExtensionContext context) {
        if (context.hasService(TransactionContext.class)) {
            return context.getService(TransactionContext.class);
        }
        return null;
    }
}
