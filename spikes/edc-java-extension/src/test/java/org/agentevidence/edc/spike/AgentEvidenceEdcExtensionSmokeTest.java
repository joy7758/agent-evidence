package org.agentevidence.edc.spike;

import org.agentevidence.edc.spike.fixtures.ControlPlaneEventFixtures;
import org.eclipse.edc.connector.controlplane.asset.spi.event.AssetEvent;
import org.eclipse.edc.connector.controlplane.contract.spi.event.contractdefinition.ContractDefinitionEvent;
import org.eclipse.edc.connector.controlplane.contract.spi.event.contractnegotiation.ContractNegotiationEvent;
import org.eclipse.edc.connector.controlplane.policy.spi.event.PolicyDefinitionEvent;
import org.eclipse.edc.connector.controlplane.transfer.spi.event.TransferProcessEvent;
import org.eclipse.edc.spi.event.Event;
import org.eclipse.edc.spi.event.EventEnvelope;
import org.eclipse.edc.spi.event.EventRouter;
import org.eclipse.edc.spi.event.EventSubscriber;
import org.eclipse.edc.spi.monitor.Monitor;
import org.eclipse.edc.spi.system.ServiceExtensionContext;
import org.eclipse.edc.spi.system.configuration.Config;
import org.eclipse.edc.transaction.spi.TransactionContext;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AgentEvidenceEdcExtensionSmokeTest {
    @TempDir
    Path tempDir;

    @Test
    void shouldRegisterMinimalControlPlaneFamiliesAsAsyncSubscribers() {
        var eventRouter = new RecordingEventRouter();
        var monitor = new RecordingMonitor();
        var extension = new AgentEvidenceEdcExtension(eventRouter, monitor);
        var context = new FakeServiceExtensionContext(Map.of(), Map.of(), monitor);

        extension.initialize(context);

        assertEquals(
                Set.of(
                        AssetEvent.class,
                        PolicyDefinitionEvent.class,
                        ContractDefinitionEvent.class,
                        ContractNegotiationEvent.class,
                        TransferProcessEvent.class
                ),
                eventRouter.asyncRegistrations()
        );
        assertTrue(eventRouter.syncRegistrations().isEmpty());
    }

    @Test
    void shouldRoutePublishedEventsIntoConfiguredOutputDirectoryUsingTransactionHandoff() throws Exception {
        var eventRouter = new RecordingEventRouter();
        var monitor = new RecordingMonitor();
        var transactionContext = new RecordingTransactionContext();
        var outputDir = tempDir.resolve("custom-export-root");
        var extension = new AgentEvidenceEdcExtension(eventRouter, monitor);
        var context = new FakeServiceExtensionContext(
                Map.of(AgentEvidenceEdcExtension.OUTPUT_DIR, outputDir.toString()),
                Map.of(TransactionContext.class, transactionContext),
                monitor
        );

        extension.initialize(context);

        eventRouter.publish(ControlPlaneEventFixtures.contractNegotiationFinalizedEnvelope("env-neg-finalized", 1_712_780_800_000L));
        eventRouter.publish(ControlPlaneEventFixtures.transferProcessStartedEnvelope("env-transfer-started", 1_712_780_801_000L));

        var agreementFile = outputDir.resolve("agreement-1").resolve("evidence-fragments.jsonl");
        var transferFile = outputDir.resolve("tp-1").resolve("evidence-fragments.jsonl");

        assertEquals(2, transactionContext.executeCount());
        assertTrue(Files.exists(agreementFile));
        assertTrue(Files.exists(transferFile));
        assertTrue(Files.readString(agreementFile).contains("\"effectiveOutputKey\":\"agreement-1\""));
        assertTrue(Files.readString(transferFile).contains("\"effectiveOutputKey\":\"tp-1\""));
        assertTrue(monitor.infoMessages().stream().anyMatch(it -> it.contains("Using agent-evidence exporter type 'filesystem'")));
        assertTrue(monitor.infoMessages().stream().anyMatch(it -> it.contains("Registered control-plane event subscribers")));
    }

    @Test
    void shouldRunSubscriberChainWithoutWritingFilesWhenNoopExporterIsConfigured() throws Exception {
        var eventRouter = new RecordingEventRouter();
        var monitor = new RecordingMonitor();
        var transactionContext = new RecordingTransactionContext();
        var outputDir = tempDir.resolve("noop-export-root");
        var extension = new AgentEvidenceEdcExtension(eventRouter, monitor);
        var context = new FakeServiceExtensionContext(
                Map.of(
                        AgentEvidenceEdcExtension.EXPORTER_TYPE, "noop",
                        AgentEvidenceEdcExtension.OUTPUT_DIR, outputDir.toString()
                ),
                Map.of(TransactionContext.class, transactionContext),
                monitor
        );

        extension.initialize(context);
        eventRouter.publish(ControlPlaneEventFixtures.transferProcessStartedEnvelope("env-transfer-started", 1_712_780_802_000L));

        assertEquals(1, transactionContext.executeCount());
        assertTrue(Files.notExists(outputDir));
        assertTrue(monitor.infoMessages().stream().anyMatch(it -> it.contains("Using agent-evidence exporter type 'noop'")));
    }

    @Test
    void shouldFailFastWhenExporterTypeIsUnsupported() {
        var eventRouter = new RecordingEventRouter();
        var monitor = new RecordingMonitor();
        var extension = new AgentEvidenceEdcExtension(eventRouter, monitor);
        var context = new FakeServiceExtensionContext(
                Map.of(AgentEvidenceEdcExtension.EXPORTER_TYPE, "s3"),
                Map.of(),
                monitor
        );

        var error = assertThrows(IllegalArgumentException.class, () -> extension.initialize(context));

        assertTrue(error.getMessage().contains("Unsupported agent-evidence exporter type 's3'"));
        assertTrue(eventRouter.asyncRegistrations().isEmpty());
    }

    private static final class RecordingEventRouter implements EventRouter {
        private final Map<Class<? extends Event>, List<EventSubscriber>> asyncSubscribers = new LinkedHashMap<>();
        private final Map<Class<? extends Event>, List<EventSubscriber>> syncSubscribers = new LinkedHashMap<>();

        @Override
        public <E extends Event> void registerSync(Class<E> eventType, EventSubscriber subscriber) {
            syncSubscribers.computeIfAbsent(eventType, ignored -> new ArrayList<>()).add(subscriber);
        }

        @Override
        public <E extends Event> void register(Class<E> eventType, EventSubscriber subscriber) {
            asyncSubscribers.computeIfAbsent(eventType, ignored -> new ArrayList<>()).add(subscriber);
        }

        @Override
        public <E extends Event> void publish(E event) {
            publish(EventEnvelope.Builder.<E>newInstance().id("generated-envelope").at(0L).payload(event).build());
        }

        @Override
        public <E extends Event> void publish(EventEnvelope<E> envelope) {
            dispatch(syncSubscribers, envelope);
            dispatch(asyncSubscribers, envelope);
        }

        Set<Class<? extends Event>> asyncRegistrations() {
            return asyncSubscribers.keySet();
        }

        Set<Class<? extends Event>> syncRegistrations() {
            return syncSubscribers.keySet();
        }

        @SuppressWarnings("unchecked")
        private <E extends Event> void dispatch(Map<Class<? extends Event>, List<EventSubscriber>> registry, EventEnvelope<E> envelope) {
            registry.forEach((eventType, subscribers) -> {
                if (eventType.isAssignableFrom(envelope.getPayload().getClass())) {
                    subscribers.forEach(subscriber -> subscriber.on((EventEnvelope) envelope));
                }
            });
        }
    }

    private static final class RecordingMonitor implements Monitor {
        private final List<String> infoMessages = new ArrayList<>();

        @Override
        public void info(String message, Throwable... errors) {
            infoMessages.add(message);
        }

        @Override
        public Monitor withPrefix(String prefix) {
            return this;
        }

        List<String> infoMessages() {
            return infoMessages;
        }
    }

    private static final class RecordingTransactionContext implements TransactionContext {
        private int executeCount;

        @Override
        public void execute(TransactionBlock block) {
            executeCount++;
            block.execute();
        }

        @Override
        public <T> T execute(ResultTransactionBlock<T> block) {
            executeCount++;
            return block.execute();
        }

        @Override
        public void registerSynchronization(TransactionSynchronization synchronization) {
        }

        int executeCount() {
            return executeCount;
        }
    }

    private static final class FakeServiceExtensionContext implements ServiceExtensionContext {
        private final Map<String, String> settings;
        private final Map<Class<?>, Object> services;
        private final Monitor monitor;
        private final Config config;

        private FakeServiceExtensionContext(Map<String, String> settings, Map<Class<?>, Object> services, Monitor monitor) {
            this.settings = settings;
            this.services = services;
            this.monitor = monitor;
            this.config = new MapBackedConfig(settings);
        }

        @Override
        public String getRuntimeId() {
            return "runtime-spike";
        }

        @Override
        public String getComponentId() {
            return "component-spike";
        }

        @Override
        public Monitor getMonitor() {
            return monitor;
        }

        @Override
        public <T> boolean hasService(Class<T> serviceType) {
            return services.containsKey(serviceType);
        }

        @Override
        public <T> T getService(Class<T> serviceType) {
            return serviceType.cast(services.get(serviceType));
        }

        @Override
        public void initialize() {
        }

        @Override
        public Config getConfig(String path) {
            return config;
        }

        @Override
        public String getSetting(String key, String defaultValue) {
            return settings.getOrDefault(key, defaultValue);
        }
    }

    private static final class MapBackedConfig implements Config {
        private final Map<String, String> entries;

        private MapBackedConfig(Map<String, String> entries) {
            this.entries = entries;
        }

        @Override
        public String getString(String key) {
            return entries.get(key);
        }

        @Override
        public String getString(String key, String defaultValue) {
            return entries.getOrDefault(key, defaultValue);
        }

        @Override
        public Integer getInteger(String key) {
            return entries.containsKey(key) ? Integer.valueOf(entries.get(key)) : null;
        }

        @Override
        public Integer getInteger(String key, Integer defaultValue) {
            return entries.containsKey(key) ? Integer.valueOf(entries.get(key)) : defaultValue;
        }

        @Override
        public Long getLong(String key) {
            return entries.containsKey(key) ? Long.valueOf(entries.get(key)) : null;
        }

        @Override
        public Long getLong(String key, Long defaultValue) {
            return entries.containsKey(key) ? Long.valueOf(entries.get(key)) : defaultValue;
        }

        @Override
        public Boolean getBoolean(String key) {
            return entries.containsKey(key) ? Boolean.valueOf(entries.get(key)) : null;
        }

        @Override
        public Boolean getBoolean(String key, Boolean defaultValue) {
            return entries.containsKey(key) ? Boolean.valueOf(entries.get(key)) : defaultValue;
        }

        @Override
        public Config getConfig(String path) {
            return this;
        }

        @Override
        public Config merge(Config other) {
            return this;
        }

        @Override
        public Stream<Config> partition() {
            return Stream.empty();
        }

        @Override
        public Map<String, String> getEntries() {
            return entries;
        }

        @Override
        public Map<String, String> getRelativeEntries() {
            return entries;
        }

        @Override
        public Map<String, String> getRelativeEntries(String prefix) {
            return entries;
        }

        @Override
        public String currentNode() {
            return "";
        }

        @Override
        public boolean isLeaf() {
            return false;
        }

        @Override
        public boolean hasKey(String key) {
            return entries.containsKey(key);
        }

        @Override
        public boolean hasPath(String path) {
            return entries.containsKey(path);
        }
    }
}
