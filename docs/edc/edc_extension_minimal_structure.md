# EDC Extension Minimal Structure

## 结论先行

第一轮需要的是 extension 结构草图，不是正式实现。

最小 Java extension 只要把下面五件事拆清楚，就够支持下一轮 skeleton spike：

- `ServiceExtension` 负责装配
- `EventRouter` 负责订阅 control-plane events
- subscriber 负责收包、去重入口和字段抽取
- mapper / exporter 负责把事件变成 evidence fragment
- bundle / verify 继续留在 `agent-evidence` 仓库侧，不在 Java 里重写

## 这份草图的边界

这不是正式实现，也不要求可编译。

它只回答：

- 一个最小 Java extension 应该有哪些部分
- 哪些职责应该留在 EDC runtime 内
- 哪些职责应该继续留在 Python `agent-evidence` 侧

它不回答：

- 持久化表怎么设计
- bundle 文件格式最终定稿长什么样
- runtime 间怎样汇总
- data plane / provisioner 怎么接

## 一个最小 Java extension 的组成

### 1. `ServiceExtension`

职责：

- 在 `initialize` 中注册 subscriber
- 注入 monitor、router、可选 transaction 组件
- 装配 mapper、grouping、writer

### 2. `EventRouter` subscriber registration

职责：

- 订阅 `AssetEvent`
- 订阅 `PolicyDefinitionEvent`
- 订阅 `ContractDefinitionEvent`
- 订阅 `ContractNegotiationEvent`
- 订阅 `TransferProcessEvent`

第一轮建议按 family 注册，而不是每个 concrete event 单独注册。

### 3. `Monitor`

职责：

- 记录扩展初始化、订阅成功、过滤丢弃、导出失败等运行时诊断信息

这不是 evidence 本身，但对 extension 可运维性是必要的。

### 4. optional `TransactionContext`

职责：

- 如果未来要做 sync subscriber 下的本地 staging / outbox，可作为事务边界工具

第一轮只是草图，所以它是 optional。

是否真的要接它，应该由“你要不要保证至少一次导出”决定，而不是先入为主地把
扩展做重。

### 5. exporter / mapper / bundle writer interface

职责最好拆成三层：

- `EventToEvidenceMapper`
  - 输入 `EventEnvelope<E>`
  - 输出 semantic evidence fragment

- `EvidenceGroupingService`
  - 决定 fragment 归到哪个 staging bucket / bundle

- `EvidenceBundleWriter`
  - 负责把分组后的内容导出成 JSON、JSONL、bundle 目录或其他中间物

这样后面无论你要写本地文件、HTTP exporter 还是 outbox，都不用重写 mapping。

## 极简伪代码级结构

```java
@Extension("Agent Evidence Control Plane Extension")
public class AgentEvidenceControlPlaneExtension implements ServiceExtension {

    @Inject private EventRouter eventRouter;
    @Inject private Monitor monitor;
    @Inject(required = false) private TransactionContext transactionContext;

    @Override
    public void initialize(ServiceExtensionContext context) {
        var deduplicator = new EnvelopeDeduplicator();
        var mapper = new EventToEvidenceMapper(monitor);
        var grouper = new EvidenceGroupingService(monitor);
        var writer = new EvidenceBundleWriter(monitor);

        var subscriber = new ControlPlaneEvidenceSubscriber(
                deduplicator, mapper, grouper, writer, transactionContext, monitor
        );

        eventRouter.register(AssetEvent.class, subscriber);
        eventRouter.register(PolicyDefinitionEvent.class, subscriber);
        eventRouter.register(ContractDefinitionEvent.class, subscriber);
        eventRouter.register(ContractNegotiationEvent.class, subscriber);
        eventRouter.register(TransferProcessEvent.class, subscriber);
    }
}

public class ControlPlaneEvidenceSubscriber implements EventSubscriber {
    @Override
    public <E extends Event> void on(EventEnvelope<E> envelope) {
        if (deduplicator.seen(envelope)) {
            return;
        }

        var fragment = mapper.map(envelope);
        if (fragment == null) {
            return;
        }

        var groupKey = grouper.resolve(fragment);
        writer.append(groupKey, fragment);
    }
}
```

## EDC runtime 内负责什么

建议只把下面这些责任留在 Java / EDC runtime 内：

- 订阅 control-plane events
- 抽取 envelope metadata 和最小领域 id
- 做第一层去重
- 做最小 semantic mapping
- 产出可带出 runtime 的 evidence fragment / bundle draft

这些事情都属于“观察和导出”。

## `agent-evidence` 仓库侧负责什么

建议继续把下面这些责任留在 Python `agent-evidence` 仓库侧：

- bundle 结构定义的主线演进
- manifest 生成与 digest 规则
- 独立 validator
- human-readable failure summary
- machine-readable JSON validation report
- CLI / demo / examples

这些事情都属于“脱离 EDC runtime 之后如何验证和复用”。

## 为什么不要在 Java 侧重写全部验证

因为那会很快把“扩展接入”变成“复制一套 agent-evidence 核心逻辑”。

第一轮更合理的边界是：

- Java 侧负责采集和导出
- Python 侧负责验证和演示

这样仓库主线不会被 EDC 绑死。

## 哪些部分建议保留在 Python `agent-evidence` 仓库侧

- semantic evidence profile 的正式定义
- schema / validator 逻辑
- manifest canonicalization 与 digest 规则
- bundle 验证 CLI
- examples 和 invalid corpus
- 对外 demo 和 release artifact

## 哪些部分未来如果真做 EDC extension，需要落在 Java 侧

- `ServiceExtension` 本体
- `EventRouter` family-level subscriber 注册
- envelope 级去重入口
- raw event -> semantic evidence fragment mapper
- runtime 内的轻量 staging / outbox
- 最小 exporter

## sync 还是 async，第一轮怎么选

第一轮如果只是做 skeleton spike，我建议：

- 默认先画 async subscriber 路线
- 在文档里预留 sync + `TransactionContext` 的升级口

原因很简单：

- async 更贴近“先证明能观察并导出”
- sync 会立刻把你带进事务性和失败处理设计

但要明确一点：

- 如果后续目标变成“至少一次写入本地 staging”，那就该认真评估 sync subscriber
  和事务边界了

## 推荐的接口切分

为了避免后面改一处牵一片，建议最少切出这四个接口：

- `EnvelopeDeduplicator`
- `EventToEvidenceMapper`
- `EvidenceGroupingService`
- `EvidenceBundleWriter`

这样下一轮做 Java skeleton spike 时，就能先把骨架立起来，而不必先决定：

- 写文件
- 发 HTTP
- 走消息队列
- 还是落本地 outbox

## 官方参考

以下链接为 2026-04-12 检索时使用的官方入口：

- Extensions
  [https://eclipse-edc.github.io/documentation/for-adopters/extensions/](https://eclipse-edc.github.io/documentation/for-adopters/extensions/)

- Service Layers / events and callbacks
  [https://eclipse-edc.github.io/documentation/for-contributors/runtime/service-layers/](https://eclipse-edc.github.io/documentation/for-contributors/runtime/service-layers/)

- Official `ServiceExtension` source
  [https://github.com/eclipse-edc/Connector/blob/main/spi/common/boot-spi/src/main/java/org/eclipse/edc/spi/system/ServiceExtension.java](https://github.com/eclipse-edc/Connector/blob/main/spi/common/boot-spi/src/main/java/org/eclipse/edc/spi/system/ServiceExtension.java)

- Official `EventRouter` / `EventSubscriber` sources
  [https://github.com/eclipse-edc/Connector/blob/main/spi/common/core-spi/src/main/java/org/eclipse/edc/spi/event/EventRouter.java](https://github.com/eclipse-edc/Connector/blob/main/spi/common/core-spi/src/main/java/org/eclipse/edc/spi/event/EventRouter.java)
  [https://github.com/eclipse-edc/Connector/blob/main/spi/common/core-spi/src/main/java/org/eclipse/edc/spi/event/EventSubscriber.java](https://github.com/eclipse-edc/Connector/blob/main/spi/common/core-spi/src/main/java/org/eclipse/edc/spi/event/EventSubscriber.java)

- Official callback dispatcher extension example
  [https://github.com/eclipse-edc/Connector/blob/main/extensions/control-plane/callback/callback-event-dispatcher/src/main/java/org/eclipse/edc/connector/controlplane/callback/dispatcher/CallbackEventDispatcherExtension.java](https://github.com/eclipse-edc/Connector/blob/main/extensions/control-plane/callback/callback-event-dispatcher/src/main/java/org/eclipse/edc/connector/controlplane/callback/dispatcher/CallbackEventDispatcherExtension.java)

- Official CloudEvents extension example
  [https://github.com/eclipse-edc/Connector/blob/main/extensions/common/events/events-cloud-http/src/main/java/org/eclipse/edc/event/cloud/http/CloudEventsHttpExtension.java](https://github.com/eclipse-edc/Connector/blob/main/extensions/common/events/events-cloud-http/src/main/java/org/eclipse/edc/event/cloud/http/CloudEventsHttpExtension.java)
