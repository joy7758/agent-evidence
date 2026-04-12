# EDC Demo Minimal Path

## 结论先行

这个 demo 路径不是 EDC 替代实现。

它只是说明：当 EDC 已经负责 catalog、contract、transfer governance 时，
`agent-evidence` 如何作为增强层，补出一条最小可验证的 execution-evidence
闭环。

## 最小路径

| 输入 | 系统动作 | 生成的 evidence | 第三方如何验证 |
| --- | --- | --- | --- |
| `asset` | 提供方在 EDC control plane 中登记可交换资产，并让它出现在 catalog / dataset / distribution 语境里 | 记录 `asset_id`、provider participant、最小对象引用 | 验证 `asset_id` 存在且后续 contract / transfer 都引用同一资产 |
| `policy / contract definition` | 提供方配置 policy definition 与 contract definition，把治理规则绑定到资产选择条件 | 记录 `policy_definition_id`、`contract_definition_id` 以及它们与 `asset_id` 的关联 | 验证 policy / contract 定义与资产选择逻辑闭合，不要求读取内部库表 |
| `contract agreement` | 消费方发起 negotiation，控制面生成 contract agreement | 记录 `contract_agreement_id`、consumer participant、provider participant | 验证 agreement 与前面的 participant、asset、policy / contract 定义能串起来 |
| `transfer process` | 消费方基于 agreement 发起 transfer，控制面推进状态机；事件订阅器捕获关键状态变化 | 记录 `transfer_process_id`、`flow_type`、`state_transitions`、`started_at`、`completed_at` 或 `terminated_at` | 验证状态序列和时间戳合理，且 transfer 绑定到同一 agreement |
| `evidence bundle` | augmentation exporter 把最小字段打包成 evidence bundle，计算 manifest digest，并附带签名或外部锚定摘要 | 记录 `manifest_digest`、`signature_count`、可选 `anchor_type` / `anchor_id` | 重算或比对 manifest digest，继续检查签名数量和可选锚定信息 |
| `independent verify` | 独立验证器读取 bundle，不需要接入 EDC 内部日志或数据库 | 输出机器可读结果和人可读结论 | 检查字段完整性、引用闭合、状态一致性、digest 一致性、可选锚定可追溯性 |

## 这个 demo 为什么是增强层

因为 EDC 仍然负责：

- catalog 暴露
- policy / contract 定义
- contract negotiation
- transfer governance

而 `agent-evidence` 只负责：

- 订阅关键控制面事件
- 导出最小 evidence bundle
- 让 bundle 在 EDC 外部也能被验证

也就是说，这个 demo 的目标不是“换掉 EDC”，而是“让 EDC 场景里的执行过程
有一份可单独带走、可单独核验的证据”。

## 推荐的最小实现顺序

建议把实现顺序收敛成下面这一条线：

1. 先用 control-plane event subscriber 捕获最小事件集
   先覆盖 agreement finalized、transfer started、transfer completed /
   terminated。

2. 再把事件归一成最小 evidence bundle
   先只保留 participant、asset、policy、contract、transfer、manifest 相关字段。

3. 最后接独立 verify
   先验证字段闭合、状态一致性和 manifest digest，不急着做复杂外部信任基础设施。

## 非目标

这个最小 demo 当前不包括：

- 自定义 data plane
- 新的 connector 产品封装
- 对 EDC persistence 的侵入式改造
- 完整 usage control 执行系统
- 全状态机、全协议、全后端一次打通

## 非常小的后续实现建议

下一步最值得先做的是：

`control-plane event subscriber / exporter`

原因是它最贴近官方扩展面，最不容易把范围拉向 persistence 或 data plane，
也最适合先把 `event -> evidence mapping` 画清楚。

## 官方参考

以下链接为 2026-04-12 检索时使用的官方入口：

- Control Plane
  [https://eclipse-edc.github.io/documentation/for-adopters/control-plane/](https://eclipse-edc.github.io/documentation/for-adopters/control-plane/)

- Extensions / `ServiceExtension`
  [https://eclipse-edc.github.io/documentation/for-adopters/extensions/](https://eclipse-edc.github.io/documentation/for-adopters/extensions/)

- Events / `EventRouter` / callbacks
  [https://eclipse-edc.github.io/documentation/for-contributors/runtime/service-layers/](https://eclipse-edc.github.io/documentation/for-contributors/runtime/service-layers/)

- Transfer callbacks and event names
  [https://eclipse-edc.github.io/documentation/for-contributors/control-plane/entities/](https://eclipse-edc.github.io/documentation/for-contributors/control-plane/entities/)

- DSP scope
  [https://eclipse-dataspace-protocol-base.github.io/DataspaceProtocol/HEAD/](https://eclipse-dataspace-protocol-base.github.io/DataspaceProtocol/HEAD/)
