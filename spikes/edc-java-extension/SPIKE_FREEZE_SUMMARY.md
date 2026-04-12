# Spike Freeze Summary

## 结论

当前这条 EDC Java spike 已经足以证明：`agent-evidence` 可以作为 EDC control plane 上的一层 execution-evidence augmentation layer 存在，而且不需要演变成 EDC 本体、connector 产品线或 dataspace 平台。

这条线现在更适合先冻结、交接和引用，而不是继续往 runtime 细节上扩张。

## 已经验证通过的能力面

- control-plane event mapping
  - `Asset`、`PolicyDefinition`、`ContractDefinition`、`ContractNegotiation`、`TransferProcess` 五类事件都已进入最小范围。
- grouping / dedup
  - 最终 grouping key 固定为 `transfer_process_id`。
  - `contract_agreement_id` 只作为 transfer 出现前的 staging correlation key。
  - envelope-level 和 semantic-level 两级去重都已有测试覆盖。
- exporter handoff
  - Java 侧已固定最小 exporter 集合：`filesystem`、`noop`、`disabled`。
  - `edc.agent-evidence.exporter.type` 和 `edc.agent-evidence.output-dir` 已进入稳定 handoff 路径。
- runtime wiring
  - `config -> factory -> writer -> subscriber` 的最小装配链已经跑通。
- startup smoke
  - 最小 `BaseRuntime` 启动样例已能在超时保护下验证 extension 加载和 subscriber 注册。
- startup failure contract
  - 端口占用、缺失 event SPI、非法 exporter.type 三类失败面已收成稳定契约。
- runtime-facing exporter integration
  - runtime properties、`JAVA_OPTS` override、`filesystem` / `noop` 启动路径都已对齐并验证。

## 刻意未做的内容

- schema JSON 正式化
- persistence store 改造
- data plane / provisioner
- signing / verification / anchor 下沉到 Java
- connector 产品化
- 更宽的 dataspace / usage control 路线

这些不是漏做，而是当前刻意不做。它们一旦进入这条 spike，就会把 augmentation layer 拉向更宽的 EDC 产品线。

## 为什么现在应该先停止扩张，而不是继续加功能

原因很直接：

- 当前最关键的问题已经回答了：这条 augmentation layer 能不能站住。
- 再继续加 runtime 细节，收益开始递减，但会显著增加“看起来像在做 EDC 本体”的风险。
- 当前成果已经足够支撑主仓入口整理、对外说明、issue / PR / paper note 引用。
- 在没有新的明确问题之前，继续扩功能只会扩大维护面，而不会明显提高论证质量。

换句话说，这条 spike 现在最值钱的状态不是“再多做一点”，而是“先收成一个可交付、可解释、可引用的包”。

## 当前应如何表述这条 spike

- 它验证的是接入边界，不是完整集成。
- 它证明的是可行性，不是产品完成度。
- 它提供的是 spike-level evidence，而不是 production-ready runtime module。

## 最小下一步建议

- 把这条 spike 收进主仓的可见入口，让主仓读者能直接找到边界、验证面和运行方式。
- 基于现有 freeze package 整理一份对外 note 或 issue，而不是继续追加新的 Java 功能。
