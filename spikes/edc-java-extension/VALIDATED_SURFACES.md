# Validated Surfaces

## 已验证能力清单

| 能力面 | 已有文件 / 测试 | 验证方式 | 当前状态 |
| --- | --- | --- | --- |
| event family registration | `src/main/java/org/agentevidence/edc/spike/AgentEvidenceEdcExtension.java`, `src/test/java/org/agentevidence/edc/spike/AgentEvidenceEdcExtensionSmokeTest.java` | smoke test 验证五类 control-plane family 注册到 `EventRouter` | 已验证 |
| semantic mapping | `src/main/java/org/agentevidence/edc/spike/mapper/AgentEvidenceEventMapper.java`, `src/test/java/org/agentevidence/edc/spike/mapper/AgentEvidenceEventMapperTest.java` | real-payload tests 验证 event family 到 semantic event 的映射 | 已验证 |
| grouping key | `src/main/java/org/agentevidence/edc/spike/grouping/AgentEvidenceGroupingStrategy.java`, `src/test/java/org/agentevidence/edc/spike/grouping/AgentEvidenceGroupingStrategyTest.java` | 单元测试验证 `transfer_process_id` 最终归组与 agreement staging 回落 | 已验证 |
| dedup | `src/main/java/org/agentevidence/edc/spike/subscriber/ControlPlaneEvidenceSubscriber.java`, `src/test/java/org/agentevidence/edc/spike/subscriber/ControlPlaneEvidenceSubscriberTest.java` | 单元测试验证 envelope-level 与 semantic-level 两级去重 | 已验证 |
| filesystem exporter | `src/main/java/org/agentevidence/edc/spike/writer/FileSystemEvidenceEnvelopeWriter.java`, `src/test/java/org/agentevidence/edc/spike/writer/FileSystemEvidenceEnvelopeWriterTest.java` | writer test 和 export contract test 验证文件输出与追加写入 | 已验证 |
| noop exporter | `src/main/java/org/agentevidence/edc/spike/writer/NoOpEvidenceEnvelopeWriter.java`, `src/test/java/org/agentevidence/edc/spike/writer/ConfigurableEvidenceEnvelopeWriterFactoryTest.java` | factory test 与 runtime integration test 验证 no-output 行为 | 已验证 |
| config handoff | `src/main/java/org/agentevidence/edc/spike/writer/AgentEvidenceExporterConfiguration.java`, `src/main/java/org/agentevidence/edc/spike/AgentEvidenceRuntimeWiring.java`, `src/test/java/org/agentevidence/edc/spike/writer/AgentEvidenceExporterConfigurationTest.java` | 单元测试和 wiring sample test 验证 exporter.type / output-dir 归一化与流转 | 已验证 |
| runtime module integration | `runtime-module-sample/build.gradle.kts`, `runtime-module-sample/src/test/java/org/agentevidence/edc/spike/runtime/AgentEvidenceRuntimeModuleIntegrationTest.java` | `BaseRuntime` sample + integration tests | 已验证 |
| startup smoke | `runtime-module-sample/run-startup-smoke.sh`, `runtime-module-sample/src/test/java/org/agentevidence/edc/spike/runtime/AgentEvidenceRuntimeModuleIntegrationTest.java` | 脚本和测试共同验证 startup 成功信号 | 已验证 |
| startup failure contract | `STARTUP_FAILURE_CONTRACT.md`, `FAILURE_TRIAGE_RECIPE.md`, `runtime-module-sample/run-startup-smoke.sh`, `runtime-module-sample/src/test/java/org/agentevidence/edc/spike/runtime/AgentEvidenceRuntimeModuleIntegrationTest.java` | runtime tests + smoke 脚本验证三类失败摘要 | 已验证 |

## 哪些结论已经足够稳，可以对外说

- 这条 spike 已经验证了 `ServiceExtension -> EventRouter subscriber -> semantic mapping -> grouping -> exporter handoff` 这条最小 Java 接入链。
- `agent-evidence` 可以坐在 EDC control plane 之上，作为 execution-evidence augmentation layer，而不需要变成 EDC 本体。
- Java 侧可以只负责观察、归一化、分组和 fragment 导出，把 signing、anchor、independent verification 留在 Python `agent-evidence` 主包侧。
- `filesystem` 和 `noop` 已经足够覆盖当前 spike 需要回答的 exporter 边界问题。

## 哪些仍然只能说是 spike-level evidence，不能过度表述

- 不能说“已经完成 EDC 集成”。
- 不能说“已经形成生产可用的 runtime module”。
- 不能说“已经覆盖 dataspace 全流程”。
- 不能说“已经解决 persistence、data plane、signing 或 external verification”。
- 不能把当前 sample 和 smoke tests 表述成 connector 产品化能力。
