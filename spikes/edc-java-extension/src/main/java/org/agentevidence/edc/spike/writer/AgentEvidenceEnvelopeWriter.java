package org.agentevidence.edc.spike.writer;

import org.agentevidence.edc.spike.model.BundleCorrelationContext;
import org.agentevidence.edc.spike.model.EvidenceFragment;

import java.io.IOException;

public interface AgentEvidenceEnvelopeWriter {
    void write(BundleCorrelationContext correlationContext, EvidenceFragment fragment) throws IOException;
}
