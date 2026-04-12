# Minimal Runtime Wiring Sample

## 结论先行

这不是一个新的 connector sample，也不是一个完整 runtime 工程。

它只是把当前 spike 已经验证过的最小装配链，用一条人能直接读懂的路径写清楚：

`config -> runtime wiring -> EventRouter subscriber -> semantic fragment -> exporter output`

当前只覆盖两种 exporter：

- `filesystem`
- `noop`

这一步的价值不是扩功能，而是把 Java augmentation layer 如何把 evidence fragment 交给外部 evidence 层的边界再钉死一层。

## 样例 1：默认 `filesystem`

最小配置只有一个必要项：

```text
edc.agent-evidence.output-dir=/tmp/agent-evidence-spike
```

如果没有显式配置 `edc.agent-evidence.exporter.type`，当前默认就是 `filesystem`。

最小装配链可以理解成：

```java
var wiring = AgentEvidenceRuntimeWiring.from(context, monitor, new ConfigurableEvidenceEnvelopeWriterFactory());
AgentEvidenceEdcExtension.registerMinimalControlPlaneSubscribers(eventRouter, wiring.subscriber());

eventRouter.publish(contractNegotiationFinalizedEnvelope(...));
eventRouter.publish(transferProcessStartedEnvelope(...));
```

当前推荐观察的最小输出是：

- `agreement-1/evidence-fragments.jsonl`
- `tp-1/evidence-fragments.jsonl`

这能直接体现两件事：

- transfer 之前，`contract_agreement_id` 仍然可以作为 staging correlation key
- transfer 出现后，最终 bundle grouping key 仍然收在 `transfer_process_id`

## 样例 2：`noop`

最小配置：

```text
edc.agent-evidence.exporter.type=noop
edc.agent-evidence.output-dir=/tmp/ignored-by-noop
```

装配链不变，差别只在 writer 选择：

```java
var wiring = AgentEvidenceRuntimeWiring.from(context, monitor, new ConfigurableEvidenceEnvelopeWriterFactory());
AgentEvidenceEdcExtension.registerMinimalControlPlaneSubscribers(eventRouter, wiring.subscriber());

eventRouter.publish(transferProcessStartedEnvelope(...));
```

预期结果：

- subscriber / mapper / grouping 仍然执行
- 不生成输出文件

这个模式的用途是：

- 验证 runtime handoff 边界
- 验证 exporter 配置选择
- 不把 verify / sign / anchor 逻辑提前塞回 Java

## 非法配置

如果 `edc.agent-evidence.exporter.type` 不是：

- `filesystem`
- `noop`
- `disabled`

当前行为是 fail-fast，而不是 silent fallback。

原因很简单：exporter 是 Java augmentation layer 和外部 evidence 层之间的运行时边界。配置写错时静默回退，会让导出语义变得不明确。

## 对应验证

当前样例直接对应这些测试：

- [AgentEvidenceRuntimeWiringSampleTest](src/test/java/org/agentevidence/edc/spike/AgentEvidenceRuntimeWiringSampleTest.java)
- [AgentEvidenceEdcExtensionSmokeTest](src/test/java/org/agentevidence/edc/spike/AgentEvidenceEdcExtensionSmokeTest.java)

运行方式：

```bash
cd /Users/zhangbin/GitHub/agent-evidence-edc-java-spike/spikes/edc-java-extension
./gradlew test --tests org.agentevidence.edc.spike.AgentEvidenceRuntimeWiringSampleTest
./gradlew test --tests org.agentevidence.edc.spike.AgentEvidenceEdcExtensionSmokeTest
```

## 边界提醒

这份样例仍然不做这些事：

- 不做 connector 产品化
- 不做 persistence store 改造
- 不做 data plane
- 不做 signing / verification / anchor 下沉
- 不做 schema JSON 正式化
