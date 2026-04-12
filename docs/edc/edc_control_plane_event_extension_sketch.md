# EDC Control-Plane Event Extension Sketch

## 结论先行

第一轮真正值得做的接入面，就是 EDC control-plane event extension。

原因不是它“最炫”，而是它最稳：

- 当前只讨论 control plane
- 当前不碰 persistence store 改造
- 当前不碰 data plane / provisioner / connector 产品化
- 官方已经把 `ServiceExtension` 和 `EventRouter` 定义成运行时扩展与事件订阅入口
- control plane 已经覆盖 catalog、contract agreement、transfer governance 这些最关键的治理对象
- `EventEnvelope` 已经把 event id、timestamp 这类去重和审计最需要的元数据独立出来

所以，这一轮最合理的目标不是“写一个 Java 扩展跑起来”，而是先把：

- 订阅哪些事件
- 哪些事件该进 evidence
- 这些事件怎样归一成 `agent-evidence` 语义事件
- 最小 extension 结构应该怎么拆
- 第三方独立验证怎么接上

这些问题先钉住。

## 这次草图的边界

这份文档只覆盖：

- EDC control plane 里的事件接入
- control-plane event -> semantic evidence 的最小映射
- 一个最小 extension 的职责切分
- 独立验证如何挂在导出物之后

这份文档明确不覆盖：

- persistence store 改造
- SQL / JPA / JDBC 表设计
- data plane / provisioner 行为
- connector 产品化
- 多 runtime 聚合平台

## EDC control plane 负责什么

按官方 adopter 文档，control plane 负责三件大事：

- 处理 catalog / dataset / offer 暴露
- 管理 contract negotiation 和 contract agreement
- 启动并治理 transfer process

官方文档还明确写了另一件很关键的事：

- data transfer “controls the flow of data, but it does not send it”

也就是说，control plane 负责治理链路，不负责真实数据发送。真实发送由独立的
data planes 完成。

这正好解释了为什么 `agent-evidence` 在这里应该补“执行证据层”，而不是去做
新的传输面。

## 为什么 `ServiceExtension` + `EventRouter` 是最稳切口

### `ServiceExtension`

官方把 `ServiceExtension` 定义为 runtime service 的扩展入口，并且提供了
`initialize`、`prepare`、`start`、`shutdown`、`cleanup` 这些标准生命周期。

对于这轮目标来说，最小接入只需要做两件事：

- 在 `initialize` 阶段注册 subscriber
- 把收到的 control-plane events 送进 mapper / exporter

这比改 store、改 state machine、改 data plane 都更稳，因为它不要求侵入 EDC
核心实体持久化逻辑。

### `EventRouter`

官方 contributor 文档和官方源码都把 `EventRouter` 定义成事件分发中心。

它允许：

- `registerSync(Class<E>, EventSubscriber)` 注册同步 subscriber
- `register(Class<E>, EventSubscriber)` 注册异步 subscriber

这两个模式的意义很直接：

- sync 适合“至少要有一次”的本地持久化、事务内导出或 outbox 风格动作
- async 适合通知、外发、send-and-forget

对于 `agent-evidence` 来说，这意味着可以先画清楚两种部署姿态：

- 最小草图：async exporter，低侵入，先跑通语义映射
- 稍强一致性版本：sync subscriber + 本地 staging / outbox，再异步写 bundle

## `Event` 和 `EventEnvelope` 的区别为什么重要

这点对 evidence 尤其重要。

官方 contributor 文档明确说明：

- `Event` payload 应该带领域信息，比如 asset id、transfer process id
- event metadata 不应该塞在 payload 里
- event id、timestamp 这类元数据应该放在 `EventEnvelope`

这对 evidence 设计有三个直接好处：

1. 语义和运输元数据分离
   evidence mapper 可以把 payload 当成“发生了什么”，把 envelope 当成
   “这条记录何时、以什么事件 id 被看到”。

2. 去重更自然
   `EventEnvelope.id` 很适合做一次投递级别去重键。

3. 时间锚更清楚
   `EventEnvelope.at` 可以直接作为事件观测时间，而不用再从 payload 猜。

如果把这两层混在一起，后面的 idempotency、重放、重组 bundle 都会变脆。

## 这个 extension 应该订阅哪些事件

第一轮建议订阅五个 control-plane 事件族，而不是只盯着 transfer：

- `AssetEvent`
- `PolicyDefinitionEvent`
- `ContractDefinitionEvent`
- `ContractNegotiationEvent`
- `TransferProcessEvent`

原因是最小 demo 虽然最后落在 transfer 上，但一个可解释的 evidence bundle
不能只知道“传输了”，还要知道：

- 交换对象是谁
- 它受哪条 policy / contract definition 约束
- agreement 是怎么来的
- transfer 是哪条 agreement 驱动的

这五个事件族正好覆盖这条最小闭环。

## 这些事件如何整理成 `agent-evidence` 语义事件

第一轮不要照搬所有 EDC 原始事件名到最终 bundle。

更稳的做法是分两层：

1. raw control-plane event layer
   保留 `payload.name()`、`EventEnvelope.id`、`EventEnvelope.at` 和最小领域 id。

2. semantic evidence layer
   只把对独立验证有意义的状态，归一成较稳定的语义事件。

建议的最小语义事件类型可以是：

- `dataspace.asset.registered`
- `dataspace.policy.definition.registered`
- `dataspace.contract.definition.bound`
- `dataspace.contract.agreement.established`
- `dataspace.contract.negotiation.terminated`
- `dataspace.transfer.started`
- `dataspace.transfer.completed`
- `dataspace.transfer.terminated`

这里有两个刻意的收敛：

- 不把所有中间态都提升成 first-class evidence
- 不把语义事件名字绑死在 EDC 某个内部类名上

这样后续即使换 connector flavor，语义层也更容易保持稳定。

## 推荐的最小 extension 结构

第一轮建议只画下面这条线：

1. `ServiceExtension`
   在 runtime 启动时注册 subscriber 和 mapper 组件。

2. `EventRouter` subscriber registration
   按事件族注册，不先细分到每个具体事件类。

3. `ControlPlaneEventSubscriber`
   收到 `EventEnvelope<E>` 后先做 envelope 级去重和最小字段抽取。

4. `EventToEvidenceMapper`
   把 EDC raw event 归一成 `agent-evidence` semantic evidence fragment。

5. `EvidenceGroupingService`
   根据 grouping key 把碎片归组到同一条最小 demo 链路。

6. `BundleWriter` / `Exporter`
   把分组后的 evidence 写成外部 bundle 或中间导出物。

7. 独立 validator
   这一步不放在 EDC runtime 内，而是交给 `agent-evidence` 仓库侧的 bundle /
   verify 路径。

## 第三方独立验证怎么接上

这里的核心原则是：

EDC runtime 负责“观察并导出”，`agent-evidence` 负责“脱离 runtime 后还能验证”。

最小接法是：

- extension 产出一个独立 evidence bundle
- bundle 至少带上 participant、asset、policy、contract、transfer、manifest 信息
- Python 侧 validator 读取 bundle，做字段闭合、状态一致性、digest 校验

第三方不需要：

- 连进 EDC 内部数据库
- 读取 connector 本地日志
- 理解 EDC 内部线程或表结构

第三方只需要：

- bundle 本身
- 最小 manifest / digest / signature 材料
- 可选外部 anchor 信息

这也是为什么第一轮先做 event sketch，而不是先做 Java 可运行代码：真正需要先固定的，
不是“怎么写类”，而是“导出后独立验证到底看什么”。

## 为什么这一层是 augmentation layer，而不是替代 EDC

因为它不替代 EDC 已有职责。

EDC 仍然负责：

- catalog
- contract negotiation
- contract agreement
- transfer governance

这层 extension 只负责：

- 监听控制面事件
- 把关键状态变化整理成 semantic evidence
- 把这些证据导出成外部可验证 bundle

换句话说，它不改变 EDC 的治理逻辑，只给 EDC 场景增加一个 execution
evidence layer。

## 推荐的第一轮实现姿态

如果下一轮真要开始动代码，建议顺序是：

1. 先做 family-level subscriber，不先做复杂 per-event wiring
2. 先做 raw event journal + semantic fragment mapper，不先做完整 schema
3. 先做 transfer-centered grouping，不先做跨 runtime 合并
4. 先把 bundle 导出去给 Python validator，不在 Java 里重写验证器

## 官方参考

以下链接为 2026-04-12 检索时使用的官方入口：

- Control Plane
  [https://eclipse-edc.github.io/documentation/for-adopters/control-plane/](https://eclipse-edc.github.io/documentation/for-adopters/control-plane/)

- Extensions
  [https://eclipse-edc.github.io/documentation/for-adopters/extensions/](https://eclipse-edc.github.io/documentation/for-adopters/extensions/)

- Service Layers / events and callbacks
  [https://eclipse-edc.github.io/documentation/for-contributors/runtime/service-layers/](https://eclipse-edc.github.io/documentation/for-contributors/runtime/service-layers/)

- Control-plane entities
  [https://eclipse-edc.github.io/documentation/for-contributors/control-plane/entities/](https://eclipse-edc.github.io/documentation/for-contributors/control-plane/entities/)

- DSP scope
  [https://eclipse-dataspace-protocol-base.github.io/DataspaceProtocol/HEAD/](https://eclipse-dataspace-protocol-base.github.io/DataspaceProtocol/HEAD/)

- Official `ServiceExtension` source
  [https://github.com/eclipse-edc/Connector/blob/main/spi/common/boot-spi/src/main/java/org/eclipse/edc/spi/system/ServiceExtension.java](https://github.com/eclipse-edc/Connector/blob/main/spi/common/boot-spi/src/main/java/org/eclipse/edc/spi/system/ServiceExtension.java)

- Official `EventRouter`, `EventSubscriber`, `EventEnvelope` sources
  [https://github.com/eclipse-edc/Connector/blob/main/spi/common/core-spi/src/main/java/org/eclipse/edc/spi/event/EventRouter.java](https://github.com/eclipse-edc/Connector/blob/main/spi/common/core-spi/src/main/java/org/eclipse/edc/spi/event/EventRouter.java)
  [https://github.com/eclipse-edc/Connector/blob/main/spi/common/core-spi/src/main/java/org/eclipse/edc/spi/event/EventSubscriber.java](https://github.com/eclipse-edc/Connector/blob/main/spi/common/core-spi/src/main/java/org/eclipse/edc/spi/event/EventSubscriber.java)
  [https://github.com/eclipse-edc/Connector/blob/main/spi/common/core-spi/src/main/java/org/eclipse/edc/spi/event/EventEnvelope.java](https://github.com/eclipse-edc/Connector/blob/main/spi/common/core-spi/src/main/java/org/eclipse/edc/spi/event/EventEnvelope.java)

- Official `EventRouterImpl` source
  [https://github.com/eclipse-edc/Connector/blob/main/core/common/runtime-core/src/main/java/org/eclipse/edc/runtime/core/event/EventRouterImpl.java](https://github.com/eclipse-edc/Connector/blob/main/core/common/runtime-core/src/main/java/org/eclipse/edc/runtime/core/event/EventRouterImpl.java)
