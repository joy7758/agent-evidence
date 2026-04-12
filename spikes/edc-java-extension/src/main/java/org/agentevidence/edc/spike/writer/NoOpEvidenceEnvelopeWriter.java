package org.agentevidence.edc.spike.writer;

import org.agentevidence.edc.spike.model.BundleCorrelationContext;
import org.agentevidence.edc.spike.model.EvidenceFragment;
import org.eclipse.edc.spi.monitor.Monitor;

public class NoOpEvidenceEnvelopeWriter implements AgentEvidenceEnvelopeWriter {
    private final Monitor monitor;

    public NoOpEvidenceEnvelopeWriter(Monitor monitor) {
        this.monitor = monitor;
    }

    @Override
    public void write(BundleCorrelationContext correlationContext, EvidenceFragment fragment) {
        monitor.debug("No-op exporter discarded fragment " + fragment.semanticEventType()
                + " for output key " + correlationContext.effectiveOutputKey());
    }
}
