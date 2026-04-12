package org.agentevidence.edc.spike;

import org.agentevidence.edc.spike.grouping.AgentEvidenceGroupingStrategy;
import org.agentevidence.edc.spike.mapper.AgentEvidenceEventMapper;
import org.agentevidence.edc.spike.subscriber.ControlPlaneEvidenceSubscriber;
import org.agentevidence.edc.spike.writer.AgentEvidenceExporterConfiguration;
import org.agentevidence.edc.spike.writer.ConfigurableEvidenceEnvelopeWriterFactory;
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

@Extension(value = AgentEvidenceEdcExtension.NAME)
public class AgentEvidenceEdcExtension implements ServiceExtension {
    public static final String NAME = "Agent Evidence EDC control-plane extension spike";
    public static final String EXPORTER_TYPE = AgentEvidenceExporterConfiguration.EXPORTER_TYPE;
    public static final String OUTPUT_DIR = AgentEvidenceExporterConfiguration.OUTPUT_DIR;
    public static final String DEFAULT_EXPORTER_TYPE = AgentEvidenceExporterConfiguration.DEFAULT_EXPORTER_TYPE;
    public static final String DEFAULT_OUTPUT_DIR = AgentEvidenceExporterConfiguration.DEFAULT_OUTPUT_DIR;

    @Inject
    private EventRouter eventRouter;

    @Inject
    private Monitor monitor;

    private final ConfigurableEvidenceEnvelopeWriterFactory exporterFactory;

    public AgentEvidenceEdcExtension() {
        this(new ConfigurableEvidenceEnvelopeWriterFactory());
    }

    AgentEvidenceEdcExtension(EventRouter eventRouter, Monitor monitor) {
        this(eventRouter, monitor, new ConfigurableEvidenceEnvelopeWriterFactory());
    }

    AgentEvidenceEdcExtension(
            EventRouter eventRouter,
            Monitor monitor,
            ConfigurableEvidenceEnvelopeWriterFactory exporterFactory
    ) {
        this(exporterFactory);
        this.eventRouter = eventRouter;
        this.monitor = monitor;
    }

    private AgentEvidenceEdcExtension(ConfigurableEvidenceEnvelopeWriterFactory exporterFactory) {
        this.exporterFactory = exporterFactory;
    }

    @Override
    public String name() {
        return NAME;
    }

    @Override
    public void initialize(ServiceExtensionContext context) {
        var extensionMonitor = resolveMonitor(context).withPrefix("AgentEvidenceEdcExtension");
        var wiring = buildRuntimeWiring(context, extensionMonitor);

        // Async registration keeps the first spike focused on low-friction export.
        // TODO: evaluate registerSync(...) once the writer moves to an outbox or staged local store.
        registerMinimalControlPlaneSubscribers(eventRouter, wiring.subscriber());

        extensionMonitor.info("Using agent-evidence exporter type '" + wiring.exporterConfiguration().normalizedExporterType() + "'");
        extensionMonitor.info("Registered control-plane event subscribers for agent-evidence spike");
    }

    private Monitor resolveMonitor(ServiceExtensionContext context) {
        return monitor != null ? monitor : context.getMonitor();
    }

    AgentEvidenceRuntimeWiring buildRuntimeWiring(
            ServiceExtensionContext context,
            Monitor extensionMonitor
    ) {
        return AgentEvidenceRuntimeWiring.from(context, extensionMonitor, exporterFactory);
    }

    static void registerMinimalControlPlaneSubscribers(
            EventRouter eventRouter,
            ControlPlaneEvidenceSubscriber subscriber
    ) {
        eventRouter.register(AssetEvent.class, subscriber);
        eventRouter.register(PolicyDefinitionEvent.class, subscriber);
        eventRouter.register(ContractDefinitionEvent.class, subscriber);
        eventRouter.register(ContractNegotiationEvent.class, subscriber);
        eventRouter.register(TransferProcessEvent.class, subscriber);
    }
}
