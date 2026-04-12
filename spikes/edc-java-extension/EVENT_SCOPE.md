# Event Scope

## 结论先行

这轮 Java spike 只覆盖最小 demo 事件范围，不扩到更完整状态机。

当前最小事件范围是：

- `asset.created`
- `policy.definition.created`
- `contract.definition.created`
- `contract.negotiation.requested`
- `contract.negotiation.finalized`
- `contract.negotiation.terminated`
- `transfer.process.requested`
- `transfer.process.started`
- `transfer.process.completed`
- `transfer.process.terminated`

## 第一阶段必须先接的事件

### 治理背景事件

- `asset.created`
- `policy.definition.created`
- `contract.definition.created`

这些事件的作用不是证明 transfer 已经执行，而是把后面的 transfer 绑定回：

- 哪个 asset
- 哪条 policy definition
- 哪个 contract definition

### 执行主干事件

- `contract.negotiation.requested`
- `contract.negotiation.finalized`
- `contract.negotiation.terminated`
- `transfer.process.requested`
- `transfer.process.started`
- `transfer.process.completed`
- `transfer.process.terminated`

这些事件构成最小 success / fail 链。

## 第二阶段再接的事件

建议第二阶段之后再考虑：

- `asset.updated`
- `policy.definition.updated`
- `contract.definition.updated`
- `contract.negotiation.offered`
- `contract.negotiation.accepted`
- `contract.negotiation.agreed`
- `contract.negotiation.verified`
- `transfer.process.initiated`
- `transfer.process.suspended`
- `transfer.process.preparationRequested`
- `transfer.process.prepared`

原因很简单：

- 它们会让第一轮 spike 迅速膨胀成更完整状态机实现
- 但对最小 demo 的独立验证闭环不是门槛

## 当前首选 grouping key

当前首选最终 grouping key 是：

`transfer_process_id`

原因：

- 一个 evidence bundle 最终对应一条具体执行链
- 一个 contract agreement 后面可能出现多条 transfer
- `transfer_process_id` 更适合承载 `started_at`、`completed_at`、`terminated_at`

## `contract_agreement_id` 的当前角色

`contract_agreement_id` 仍然很重要，但它当前更适合作为：

- transfer 出现前的 staging correlation key

而不是最终 bundle key。

也就是说：

- staging correlation: `contract_agreement_id`
- final grouping key: `transfer_process_id`

## 两级去重策略

### 一级：envelope 级去重

用途：

- 去掉完全重复的事件投递

推荐键：

- `(participant_context_id, envelope_id)`

这里的 `envelope_id` 来自 `EventEnvelope.id`。

## 二级：语义状态级去重

用途：

- 去掉“不同 envelope、同一领域对象、同一状态”造成的重复记证

推荐键：

- `(participant_context_id, domain_id, semantic_event_type)`

这里的 `domain_id` 优先级建议是：

1. `transfer_process_id`
2. `contract_agreement_id`
3. `contract_negotiation_id`
4. `asset_id`

## envelope metadata 和 domain IDs 如何配合

建议分工如下：

- `EventEnvelope.id`
  - 判断这条投递是否已经见过
- `EventEnvelope.at`
  - 作为观测时间锚
- domain IDs
  - 决定这条 evidence fragment 属于哪条治理链路

如果只用 envelope metadata，不够做链路归组。
如果只用 domain IDs，不够做重复投递去重。

所以两者必须一起保留。

## 当前最小验证覆盖

这轮轻量测试已经覆盖三件事：

- mapper 对最小事件范围的语义映射
- grouping strategy 对 `transfer_process_id` 的最终归组判断
- subscriber 对 envelope 级与语义级的两级去重

这些测试现在直接使用 EDC 官方 control-plane event builders 生成 payload，而不是自定义 stub event。

这说明当前事件范围不只是文档约定，也已经进入更贴近真实 payload 的最小可执行验证。

## 当前最小覆盖深度

当前 10 个最小事件都已经进入 real-payload 测试：

- `asset.created`
- `policy.definition.created`
- `contract.definition.created`
- `contract.negotiation.requested`
- `contract.negotiation.finalized`
- `contract.negotiation.terminated`
- `transfer.process.requested`
- `transfer.process.started`
- `transfer.process.completed`
- `transfer.process.terminated`

同时，文件导出契约也已经被显式验证：

- pre-transfer 事件会先落到 `contract_agreement_id` 对应的 staging 输出目录
- transfer 事件会落到 `transfer_process_id` 对应的最终输出目录
- 同一 transfer 链路内的多个 semantic fragments 会追加到同一个 `evidence-fragments.jsonl`

当前 exporter 选择不会改变事件范围本身。

- `filesystem` 影响的是 fragments 写到哪里
- `noop` / `disabled` 影响的是 fragments 是否真正落盘

但两者都不改变：

- 订阅哪些 control-plane event
- semantic mapping 规则
- grouping key
- dedup 规则
