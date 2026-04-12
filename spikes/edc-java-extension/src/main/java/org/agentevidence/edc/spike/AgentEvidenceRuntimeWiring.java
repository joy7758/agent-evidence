package org.agentevidence.edc.spike;

import org.agentevidence.edc.spike.grouping.AgentEvidenceGroupingStrategy;
import org.agentevidence.edc.spike.mapper.AgentEvidenceEventMapper;
import org.agentevidence.edc.spike.subscriber.ControlPlaneEvidenceSubscriber;
import org.agentevidence.edc.spike.writer.AgentEvidenceEnvelopeWriter;
import org.agentevidence.edc.spike.writer.AgentEvidenceExporterConfiguration;
import org.agentevidence.edc.spike.writer.ConfigurableEvidenceEnvelopeWriterFactory;
import org.eclipse.edc.spi.monitor.Monitor;
import org.eclipse.edc.spi.system.ServiceExtensionContext;
import org.eclipse.edc.transaction.spi.TransactionContext;

record AgentEvidenceRuntimeWiring(
        AgentEvidenceExporterConfiguration exporterConfiguration,
        AgentEvidenceEventMapper mapper,
        AgentEvidenceGroupingStrategy groupingStrategy,
        AgentEvidenceEnvelopeWriter writer,
        TransactionContext transactionContext,
        ControlPlaneEvidenceSubscriber subscriber
) {
    static AgentEvidenceRuntimeWiring from(
            ServiceExtensionContext context,
            Monitor monitor,
            ConfigurableEvidenceEnvelopeWriterFactory exporterFactory
    ) {
        var mapper = new AgentEvidenceEventMapper();
        var groupingStrategy = new AgentEvidenceGroupingStrategy();
        var exporterConfiguration = AgentEvidenceExporterConfiguration.from(context);
        var writer = exporterFactory.create(exporterConfiguration, monitor);
        var transactionContext = optionalTransactionContext(context);
        var subscriber = new ControlPlaneEvidenceSubscriber(
                mapper,
                groupingStrategy,
                writer,
                transactionContext,
                monitor
        );

        return new AgentEvidenceRuntimeWiring(
                exporterConfiguration,
                mapper,
                groupingStrategy,
                writer,
                transactionContext,
                subscriber
        );
    }

    private static TransactionContext optionalTransactionContext(ServiceExtensionContext context) {
        if (context.hasService(TransactionContext.class)) {
            return context.getService(TransactionContext.class);
        }
        return null;
    }
}
