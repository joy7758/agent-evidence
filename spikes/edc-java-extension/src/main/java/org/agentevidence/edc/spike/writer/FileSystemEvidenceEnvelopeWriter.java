package org.agentevidence.edc.spike.writer;

import org.agentevidence.edc.spike.model.BundleCorrelationContext;
import org.agentevidence.edc.spike.model.EvidenceFragment;
import org.eclipse.edc.spi.monitor.Monitor;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

public class FileSystemEvidenceEnvelopeWriter implements AgentEvidenceEnvelopeWriter {
    private final Path rootDirectory;
    private final Monitor monitor;

    public FileSystemEvidenceEnvelopeWriter(Path rootDirectory, Monitor monitor) {
        this.rootDirectory = rootDirectory;
        this.monitor = monitor;
    }

    @Override
    public void write(BundleCorrelationContext correlationContext, EvidenceFragment fragment) throws IOException {
        var groupDirectory = rootDirectory.resolve(sanitize(correlationContext.effectiveOutputKey()));
        Files.createDirectories(groupDirectory);

        var targetFile = groupDirectory.resolve("evidence-fragments.jsonl");
        Files.writeString(
                targetFile,
                toJsonLine(correlationContext, fragment) + System.lineSeparator(),
                StandardOpenOption.CREATE,
                StandardOpenOption.APPEND
        );

        monitor.debug("Wrote evidence fragment to " + targetFile);
    }

    private String toJsonLine(BundleCorrelationContext correlationContext, EvidenceFragment fragment) {
        return "{"
                + field("semanticEventType", fragment.semanticEventType()) + ","
                + field("edcEventType", fragment.edcEventType()) + ","
                + field("envelopeId", fragment.envelopeId()) + ","
                + field("observedAt", fragment.observedAt().toString()) + ","
                + field("participantContextId", fragment.participantContextId()) + ","
                + field("providerParticipantId", fragment.providerParticipantId()) + ","
                + field("consumerParticipantId", fragment.consumerParticipantId()) + ","
                + field("assetId", fragment.assetId()) + ","
                + field("policyDefinitionId", fragment.policyDefinitionId()) + ","
                + field("contractDefinitionId", fragment.contractDefinitionId()) + ","
                + field("contractNegotiationId", fragment.contractNegotiationId()) + ","
                + field("contractAgreementId", fragment.contractAgreementId()) + ","
                + field("transferProcessId", fragment.transferProcessId()) + ","
                + field("protocol", fragment.protocol()) + ","
                + field("counterPartyId", fragment.counterPartyId()) + ","
                + field("transferType", fragment.transferType()) + ","
                + field("stagingCorrelationKey", correlationContext.stagingCorrelationKey()) + ","
                + field("finalBundleKey", correlationContext.finalBundleKey()) + ","
                + field("effectiveOutputKey", correlationContext.effectiveOutputKey()) + ","
                + field("envelopeDeduplicationKey", correlationContext.envelopeDeduplicationKey()) + ","
                + field("semanticDeduplicationKey", correlationContext.semanticDeduplicationKey())
                + "}";
    }

    private String field(String key, String value) {
        return "\"" + escape(key) + "\":" + quote(value);
    }

    private String quote(String value) {
        if (value == null) {
            return "null";
        }
        return "\"" + escape(value) + "\"";
    }

    private String escape(String value) {
        return value.replace("\\", "\\\\").replace("\"", "\\\"");
    }

    private String sanitize(String value) {
        return value.replaceAll("[^A-Za-z0-9._-]", "_");
    }
}
