package org.agentevidence.edc.spike.subscriber;

import org.agentevidence.edc.spike.grouping.AgentEvidenceGroupingStrategy;
import org.agentevidence.edc.spike.mapper.AgentEvidenceEventMapper;
import org.agentevidence.edc.spike.model.BundleCorrelationContext;
import org.agentevidence.edc.spike.model.EvidenceFragment;
import org.agentevidence.edc.spike.model.ObservedControlPlaneEvent;
import org.agentevidence.edc.spike.writer.AgentEvidenceEnvelopeWriter;
import org.eclipse.edc.spi.event.Event;
import org.eclipse.edc.spi.event.EventEnvelope;
import org.eclipse.edc.spi.event.EventSubscriber;
import org.eclipse.edc.spi.monitor.Monitor;
import org.eclipse.edc.transaction.spi.TransactionContext;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

public class ControlPlaneEvidenceSubscriber implements EventSubscriber {
    private final AgentEvidenceEventMapper mapper;
    private final AgentEvidenceGroupingStrategy groupingStrategy;
    private final AgentEvidenceEnvelopeWriter writer;
    private final TransactionContext transactionContext;
    private final Monitor monitor;
    private final Set<String> seenEnvelopeKeys = ConcurrentHashMap.newKeySet();
    private final Set<String> seenSemanticKeys = ConcurrentHashMap.newKeySet();

    public ControlPlaneEvidenceSubscriber(
            AgentEvidenceEventMapper mapper,
            AgentEvidenceGroupingStrategy groupingStrategy,
            AgentEvidenceEnvelopeWriter writer,
            TransactionContext transactionContext,
            Monitor monitor
    ) {
        this.mapper = mapper;
        this.groupingStrategy = groupingStrategy;
        this.writer = writer;
        this.transactionContext = transactionContext;
        this.monitor = monitor;
    }

    @Override
    public <E extends Event> void on(EventEnvelope<E> envelope) {
        var observedEvent = ObservedControlPlaneEvent.from(envelope);
        if (isOutOfMinimalScope(observedEvent)) {
            return;
        }

        if (isDuplicateEnvelope(observedEvent)) {
            return;
        }

        mapper.map(observedEvent).ifPresent(fragment -> handleMappedFragment(observedEvent, fragment));
    }

    private boolean isOutOfMinimalScope(ObservedControlPlaneEvent observedEvent) {
        if (!mapper.isInMinimalScope(observedEvent.edcEventType())) {
            monitor.debug("Ignoring out-of-scope control-plane event " + observedEvent.edcEventType());
            return true;
        }
        return false;
    }

    private boolean isDuplicateEnvelope(ObservedControlPlaneEvent observedEvent) {
        if (!seenEnvelopeKeys.add(observedEvent.envelopeDeduplicationKey())) {
            monitor.debug("Ignoring duplicate envelope " + observedEvent.envelopeDeduplicationKey());
            return true;
        }
        return false;
    }

    private void handleMappedFragment(ObservedControlPlaneEvent observedEvent, EvidenceFragment fragment) {
        var correlationContext = groupingStrategy.correlate(fragment);
        if (isDuplicateSemanticFragment(correlationContext)) {
            return;
        }

        try {
            writeFragment(correlationContext, fragment);
        } catch (RuntimeException e) {
            monitor.warning("Failed to export evidence fragment for event " + observedEvent.edcEventType(), e);
        }
    }

    private boolean isDuplicateSemanticFragment(BundleCorrelationContext correlationContext) {
        if (!seenSemanticKeys.add(correlationContext.semanticDeduplicationKey())) {
            monitor.debug("Ignoring duplicate semantic fragment " + correlationContext.semanticDeduplicationKey());
            return true;
        }
        return false;
    }

    private void writeFragment(BundleCorrelationContext correlationContext, EvidenceFragment fragment) {
        Runnable writeAction = () -> {
            try {
                writer.write(correlationContext, fragment);
            } catch (IOException e) {
                throw new UncheckedIOException(e);
            }
        };

        if (transactionContext != null) {
            transactionContext.execute(writeAction::run);
        } else {
            writeAction.run();
        }
    }
}
