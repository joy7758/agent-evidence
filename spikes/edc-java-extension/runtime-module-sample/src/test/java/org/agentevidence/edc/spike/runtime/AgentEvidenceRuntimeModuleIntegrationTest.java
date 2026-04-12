package org.agentevidence.edc.spike.runtime;

import org.eclipse.edc.connector.controlplane.contract.spi.event.contractnegotiation.ContractNegotiationFinalized;
import org.eclipse.edc.connector.controlplane.contract.spi.types.agreement.ContractAgreement;
import org.eclipse.edc.connector.controlplane.contract.spi.types.offer.ContractOffer;
import org.eclipse.edc.connector.controlplane.transfer.spi.event.TransferProcessStarted;
import org.eclipse.edc.policy.model.Policy;
import org.eclipse.edc.policy.model.PolicyType;
import org.eclipse.edc.spi.event.Event;
import org.eclipse.edc.spi.event.EventEnvelope;
import org.eclipse.edc.spi.event.EventRouter;
import org.eclipse.edc.spi.event.EventSubscriber;
import org.eclipse.edc.spi.monitor.Monitor;
import org.eclipse.edc.spi.system.ServiceExtension;
import org.eclipse.edc.spi.system.ServiceExtensionContext;
import org.eclipse.edc.spi.system.configuration.Config;
import org.eclipse.edc.spi.types.domain.DataAddress;
import org.eclipse.edc.spi.types.domain.callback.CallbackAddress;
import org.eclipse.edc.transaction.spi.TransactionContext;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.io.IOException;
import java.io.InputStream;
import java.lang.reflect.Field;
import java.nio.file.Files;
import java.nio.file.Path;
import java.net.ServerSocket;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.ServiceLoader;
import java.util.Set;
import java.util.concurrent.TimeUnit;
import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

@SuppressWarnings({"rawtypes", "unchecked"})
class AgentEvidenceRuntimeModuleIntegrationTest {
    private static final String EXTENSION_CLASS_NAME = "org.agentevidence.edc.spike.AgentEvidenceEdcExtension";
    private static final String OUTPUT_DIR_KEY = "edc.agent-evidence.output-dir";
    private static final String EXPORTER_TYPE_KEY = "edc.agent-evidence.exporter.type";

    private static final String PARTICIPANT_CONTEXT_ID = "participant-a";
    private static final String PROVIDER_ID = "provider-a";
    private static final String CONSUMER_ID = "consumer-b";
    private static final String ASSET_ID = "asset-1";
    private static final String CONTRACT_NEGOTIATION_ID = "neg-1";
    private static final String CONTRACT_AGREEMENT_ID = "agreement-1";
    private static final String CONTRACT_AGREEMENT_INTERNAL_ID = "agreement-internal-1";
    private static final String TRANSFER_PROCESS_ID = "tp-1";
    private static final String PROTOCOL = "dataspace-protocol-http";
    private static final String COUNTERPARTY_ADDRESS = "https://consumer.example/protocol";
    private static final String CALLBACK_URI = "https://consumer.example/callback";
    private static final String TRANSFER_TYPE = "HttpData-PULL";

    @TempDir
    Path tempDir;

    @Test
    void shouldDiscoverAgentEvidenceExtensionViaServiceLoader() {
        var extensionNames = ServiceLoader.load(ServiceExtension.class).stream()
                .map(provider -> provider.type().getName())
                .toList();

        assertTrue(extensionNames.contains(EXTENSION_CLASS_NAME));
    }

    @Test
    void shouldShipFilesystemDefaultRuntimePropertiesTemplate() throws Exception {
        var properties = loadRuntimeProperties();

        assertEquals("19191", properties.getProperty("web.http.port"));
        assertEquals("/api", properties.getProperty("web.http.path"));
        assertEquals("filesystem", properties.getProperty(EXPORTER_TYPE_KEY));
        assertEquals("./runtime-module-sample/output", properties.getProperty(OUTPUT_DIR_KEY));
    }

    @Test
    void shouldInitializeDiscoveredExtensionAndWriteFragmentsInFilesystemMode() throws Exception {
        var extension = loadExtensionInstance();
        var eventRouter = new RecordingEventRouter();
        var monitor = new RecordingMonitor();
        var transactionContext = new RecordingTransactionContext();
        var outputDir = tempDir.resolve("runtime-module-filesystem-output");
        var context = new FakeServiceExtensionContext(
                Map.of(OUTPUT_DIR_KEY, outputDir.toString()),
                Map.of(TransactionContext.class, transactionContext),
                monitor
        );

        inject(extension, "eventRouter", eventRouter);
        inject(extension, "monitor", monitor);

        extension.initialize(context);

        eventRouter.publish(contractNegotiationFinalizedEnvelope("module-neg-finalized", 1_712_781_000_000L));
        eventRouter.publish(transferProcessStartedEnvelope("module-transfer-started", 1_712_781_001_000L));

        var agreementFile = outputDir.resolve("agreement-1").resolve("evidence-fragments.jsonl");
        var transferFile = outputDir.resolve("tp-1").resolve("evidence-fragments.jsonl");

        assertEquals(2, transactionContext.executeCount());
        assertTrue(Files.exists(agreementFile));
        assertTrue(Files.exists(transferFile));
        assertTrue(Files.readString(agreementFile).contains("\"semanticEventType\":\"dataspace.contract.agreement.established\""));
        assertTrue(Files.readString(transferFile).contains("\"semanticEventType\":\"dataspace.transfer.started\""));
        assertTrue(monitor.infoMessages().stream().anyMatch(message -> message.contains("Using agent-evidence exporter type 'filesystem'")));
        assertTrue(monitor.infoMessages().stream().anyMatch(message -> message.contains("Using agent-evidence output directory '" + outputDir)));
    }

    @Test
    void shouldInitializeDiscoveredExtensionAndSuppressOutputInNoopMode() throws Exception {
        var extension = loadExtensionInstance();
        var eventRouter = new RecordingEventRouter();
        var monitor = new RecordingMonitor();
        var transactionContext = new RecordingTransactionContext();
        var outputDir = tempDir.resolve("runtime-module-noop-output");
        var context = new FakeServiceExtensionContext(
                Map.of(
                        EXPORTER_TYPE_KEY, "noop",
                        OUTPUT_DIR_KEY, outputDir.toString()
                ),
                Map.of(TransactionContext.class, transactionContext),
                monitor
        );

        inject(extension, "eventRouter", eventRouter);
        inject(extension, "monitor", monitor);

        extension.initialize(context);

        eventRouter.publish(transferProcessStartedEnvelope("module-transfer-noop", 1_712_781_002_000L));

        assertEquals(1, transactionContext.executeCount());
        assertTrue(Files.notExists(outputDir));
        assertTrue(monitor.infoMessages().stream().anyMatch(message -> message.contains("Using agent-evidence exporter type 'noop'")));
        assertTrue(monitor.infoMessages().stream().anyMatch(message -> message.contains("Using agent-evidence output directory '" + outputDir)));
    }

    @Test
    void shouldStartInstalledRuntimeAndLogAgentEvidenceRegistration() throws Exception {
        var moduleDir = resolveRuntimeModuleDirectory();
        var smokeScript = moduleDir.resolve("run-startup-smoke.sh");
        var logPath = tempDir.resolve("runtime-startup-smoke.log");
        var httpPort = findFreePort();

        var processBuilder = new ProcessBuilder("bash", smokeScript.toString());
        processBuilder.directory(moduleDir.getParent().toFile());
        processBuilder.environment().put("TIMEOUT_SECONDS", "60");
        processBuilder.environment().put("LOG_PATH", logPath.toString());
        processBuilder.environment().put("JAVA_HOME", System.getenv().getOrDefault("JAVA_HOME", "/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"));
        processBuilder.environment().put("JAVA_OPTS", "-Dweb.http.port=" + httpPort);

        var existingPath = processBuilder.environment().getOrDefault("PATH", "");
        var javaBin = processBuilder.environment().get("JAVA_HOME") + "/bin";
        processBuilder.environment().put("PATH", javaBin + ":/opt/homebrew/bin:" + existingPath);

        var process = processBuilder.start();
        if (!process.waitFor(90, TimeUnit.SECONDS)) {
            process.destroyForcibly();
            fail("Runtime startup smoke did not exit within 90 seconds");
        }
        assertEquals(0, process.exitValue());

        var log = Files.readString(logPath);
        assertTrue(log.contains("Using agent-evidence exporter type 'filesystem'"));
        assertTrue(log.contains("Using agent-evidence output directory './runtime-module-sample/output'"));
        assertTrue(log.contains("Registered control-plane event subscribers for agent-evidence spike"));
        assertTrue(log.matches("(?s).*Runtime .* ready.*"));
    }

    private int findFreePort() throws IOException {
        try (var socket = new ServerSocket(0)) {
            return socket.getLocalPort();
        }
    }

    private Path resolveRuntimeModuleDirectory() {
        var userDir = Path.of(System.getProperty("user.dir"));
        if (Files.exists(userDir.resolve("run-startup-smoke.sh"))) {
            return userDir;
        }
        var nestedModuleDir = userDir.resolve("runtime-module-sample");
        if (Files.exists(nestedModuleDir.resolve("run-startup-smoke.sh"))) {
            return nestedModuleDir;
        }
        throw new IllegalStateException("Unable to locate runtime-module-sample directory from " + userDir);
    }

    private ServiceExtension loadExtensionInstance() {
        return ServiceLoader.load(ServiceExtension.class).stream()
                .map(ServiceLoader.Provider::get)
                .filter(extension -> extension.getClass().getName().equals(EXTENSION_CLASS_NAME))
                .findFirst()
                .orElseThrow(() -> new IllegalStateException("AgentEvidenceEdcExtension not found on runtime classpath"));
    }

    private Properties loadRuntimeProperties() throws IOException {
        var properties = new Properties();
        try (InputStream stream = getClass().getClassLoader().getResourceAsStream("agent-evidence-runtime.properties")) {
            assertNotNull(stream);
            properties.load(stream);
        }
        return properties;
    }

    private void inject(ServiceExtension extension, String fieldName, Object value) throws ReflectiveOperationException {
        Field field = extension.getClass().getDeclaredField(fieldName);
        field.setAccessible(true);
        field.set(extension, value);
    }

    private EventEnvelope<ContractNegotiationFinalized> contractNegotiationFinalizedEnvelope(String envelopeId, long at) {
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

    private EventEnvelope<TransferProcessStarted> transferProcessStartedEnvelope(String envelopeId, long at) {
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

    private ContractOffer contractOffer() {
        return ContractOffer.Builder.newInstance()
                .id("offer-1")
                .assetId(ASSET_ID)
                .policy(contractPolicy())
                .build();
    }

    private ContractAgreement contractAgreement() {
        return ContractAgreement.Builder.newInstance()
                .id(CONTRACT_AGREEMENT_INTERNAL_ID)
                .agreementId(CONTRACT_AGREEMENT_ID)
                .providerId(PROVIDER_ID)
                .consumerId(CONSUMER_ID)
                .contractSigningDate(1_712_781_000_000L)
                .assetId(ASSET_ID)
                .participantContextId(PARTICIPANT_CONTEXT_ID)
                .policy(contractPolicy())
                .build();
    }

    private Policy contractPolicy() {
        return Policy.Builder.newInstance()
                .type(PolicyType.CONTRACT)
                .assignee(CONSUMER_ID)
                .assigner(PROVIDER_ID)
                .target(ASSET_ID)
                .build();
    }

    private CallbackAddress callbackAddress(String eventName) {
        return CallbackAddress.Builder.newInstance()
                .uri(CALLBACK_URI)
                .events(Set.of(eventName))
                .transactional(false)
                .build();
    }

    private DataAddress dataAddress() {
        return DataAddress.Builder.newInstance()
                .type("HttpProxy")
                .property("endpoint", "https://provider.example/data")
                .build();
    }

    private <E extends Event> EventEnvelope<E> envelope(String envelopeId, long at, E payload) {
        return EventEnvelope.Builder.<E>newInstance()
                .id(envelopeId)
                .at(at)
                .payload(payload)
                .build();
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

        private List<String> infoMessages() {
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

        private int executeCount() {
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
            return "runtime-module-sample";
        }

        @Override
        public String getComponentId() {
            return "runtime-module-sample";
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
