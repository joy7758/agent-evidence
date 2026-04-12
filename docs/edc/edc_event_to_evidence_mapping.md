# EDC Event To Evidence Mapping

## 结论先行

第一轮不要把所有 control-plane events 原样倒进 evidence。

更稳的做法是：

- 先订阅五个控制面事件族
- 先保留 raw event + envelope metadata
- 再只把独立验证真正需要的状态，提升成 semantic evidence

这意味着：

- Asset / PolicyDefinition / ContractDefinition 事件主要负责补治理背景
- ContractNegotiation / TransferProcess 事件才是 execution evidence 主干
- `EventEnvelope.id` 和 `EventEnvelope.at` 应该直接进入去重和时间锚逻辑

## 总体映射表

| EDC event family | Typical trigger / state | Why it matters for evidence | Proposed agent-evidence semantic event type | Required fields to capture | Nice-to-have fields | Whether it should be part of the minimal demo |
| --- | --- | --- | --- | --- | --- | --- |
| `AssetEvent` | `asset.created` | 证明 demo 中被交换对象何时进入 control plane | `dataspace.asset.registered` | `envelope.id`, `envelope.at`, `payload.name()`, `assetId`, `participantContextId` | asset public properties digest、asset descriptor snapshot digest | Yes, if the demo creates the asset in the same run |
| `AssetEvent` | `asset.updated` | 可解释资产治理背景变化，但不是最小闭环必需 | `dataspace.asset.updated` | `envelope.id`, `envelope.at`, `assetId`, `participantContextId` | changed property names、before/after snapshot digest | No |
| `AssetEvent` | `asset.deleted` | 适合做生命周期审计，不是首个 transfer demo 的主干 | `dataspace.asset.deleted` | `envelope.id`, `envelope.at`, `assetId`, `participantContextId` | deletion reason、operator context | No |
| `PolicyDefinitionEvent` | `policy.definition.created` | 证明治理规则对象已存在，可被 contract / transfer 引用 | `dataspace.policy.definition.registered` | `envelope.id`, `envelope.at`, `policyDefinitionId`, `participantContextId` | policy digest、policy scope summary | Yes, if the demo creates the policy in the same run |
| `PolicyDefinitionEvent` | `policy.definition.updated` | 有助于审计规则演变，但不是首个最小链路必需 | `dataspace.policy.definition.updated` | `envelope.id`, `envelope.at`, `policyDefinitionId`, `participantContextId` | old/new policy digest | No |
| `PolicyDefinitionEvent` | `policy.definition.deleted` | 适合治理审计，不是 transfer evidence 主干 | `dataspace.policy.definition.deleted` | `envelope.id`, `envelope.at`, `policyDefinitionId`, `participantContextId` | deletion reason | No |
| `ContractDefinitionEvent` | `contract.definition.created` | 证明某条 policy 与 asset selector 已被绑定成可协商合同入口 | `dataspace.contract.definition.bound` | `envelope.id`, `envelope.at`, `contractDefinitionId`, `participantContextId` | referenced policy ids、selector digest | Yes, if the demo creates the contract definition in the same run |
| `ContractDefinitionEvent` | `contract.definition.updated` | 有助于理解规则变更，但不是首个最小闭环必需 | `dataspace.contract.definition.updated` | `envelope.id`, `envelope.at`, `contractDefinitionId`, `participantContextId` | old/new selector digest | No |
| `ContractDefinitionEvent` | `contract.definition.deleted` | 生命周期补充，不是最小 transfer demo 主干 | `dataspace.contract.definition.deleted` | `envelope.id`, `envelope.at`, `contractDefinitionId`, `participantContextId` | deletion reason | No |
| `ContractNegotiationEvent` | `contract.negotiation.requested` | 证明交换请求正式进入 negotiation state machine | `dataspace.contract.negotiation.requested` | `envelope.id`, `envelope.at`, `contractNegotiationId`, `counterPartyId`, `counterPartyAddress`, `protocol`, `participantContextId` | last contract offer digest、callback presence | Yes |
| `ContractNegotiationEvent` | `contract.negotiation.offered` / `accepted` / `agreed` / `verified` | 提供协商中间态，可帮助诊断，但对最小独立验证不是必须 | `dataspace.contract.negotiation.progressed` | `envelope.id`, `envelope.at`, `payload.name()`, `contractNegotiationId`, `counterPartyId`, `protocol` | offer digest、transition reason | No |
| `ContractNegotiationEvent` | `contract.negotiation.finalized` | 这是 governance 闭环的关键点，带出 contract agreement | `dataspace.contract.agreement.established` | `envelope.id`, `envelope.at`, `contractNegotiationId`, `contractAgreement.id`, `contractAgreement.assetId`, `contractAgreement.providerId`, `contractAgreement.consumerId`, `contractAgreement.contractSigningDate`, `participantContextId`, `protocol` | contract policy digest、claims digest | Yes |
| `ContractNegotiationEvent` | `contract.negotiation.terminated` | 证明协商失败或中止，是 fail path 的终点 | `dataspace.contract.negotiation.terminated` | `envelope.id`, `envelope.at`, `contractNegotiationId`, `counterPartyId`, `participantContextId`, `protocol` | termination reason、last offer digest | Yes, for failure demo |
| `TransferProcessEvent` | `transfer.process.requested` | 证明 agreement 已被用于发起具体 transfer | `dataspace.transfer.requested` | `envelope.id`, `envelope.at`, `transferProcessId`, `assetId`, `contractId`, `type`, `participantContextId`, `protocol` | callback presence | Yes |
| `TransferProcessEvent` | `transfer.process.initiated` | 证明 transfer state machine 已启动 | `dataspace.transfer.initiated` | `envelope.id`, `envelope.at`, `transferProcessId`, `assetId`, `contractId`, `type`, `participantContextId`, `protocol` | participant role hint | Optional |
| `TransferProcessEvent` | `transfer.process.started` | execution evidence 真正开始变强的节点，表示 transfer 已进入 started state | `dataspace.transfer.started` | `envelope.id`, `envelope.at`, `transferProcessId`, `assetId`, `contractId`, `type`, `participantContextId`, `protocol` | `dataAddress` digest only、flow endpoint class | Yes |
| `TransferProcessEvent` | `transfer.process.completed` | success path 的终点，支撑 `completed_at` | `dataspace.transfer.completed` | `envelope.id`, `envelope.at`, `transferProcessId`, `assetId`, `contractId`, `participantContextId` | completion summary | Yes |
| `TransferProcessEvent` | `transfer.process.terminated` | fail path / stop path 的终点，支撑 `terminated_at` | `dataspace.transfer.terminated` | `envelope.id`, `envelope.at`, `transferProcessId`, `assetId`, `contractId`, `participantContextId` | termination reason | Yes |
| `TransferProcessEvent` | `transfer.process.suspended` | 对长生命周期 transfer 很有用，但会让首个 demo 的状态链变复杂 | `dataspace.transfer.suspended` | `envelope.id`, `envelope.at`, `transferProcessId`, `assetId`, `contractId`, `participantContextId` | suspension reason | No |
| `TransferProcessEvent` | `transfer.process.preparationRequested` / `prepared` | 与 preparation phase 相关，适合扩展版链路，不是最小成功闭环必需 | `dataspace.transfer.preparation.progressed` | `envelope.id`, `envelope.at`, `transferProcessId`, `assetId`, `contractId`, `participantContextId` | preparation handler name | No |
| `TransferProcessEvent` | `transfer.process.provisioned` / `deprovisioningRequested` / `deprovisioned` | 这些事件在官方源码里已标记 deprecated，不适合作为首个最小 demo 基石 | `dataspace.transfer.legacy.lifecycle` | `envelope.id`, `envelope.at`, `transferProcessId` | none | No |

## ContractNegotiation 推荐的最小状态链

### 最小成功链

| Stage | Recommended EDC event | Why keep it |
| --- | --- | --- |
| negotiation entered | `contract.negotiation.requested` | 证明协商正式开始 |
| agreement established | `contract.negotiation.finalized` | 这是最关键的治理闭环节点，能带出 contract agreement |

### 最小失败链

| Stage | Recommended EDC event | Why keep it |
| --- | --- | --- |
| negotiation entered | `contract.negotiation.requested` | 证明请求确实发生过 |
| negotiation failed / stopped | `contract.negotiation.terminated` | 给出失败或终止终点 |

### 为什么不把所有中间态都放进最小 demo

`offered`、`accepted`、`agreed`、`verified` 当然有价值，但它们更像协商轨迹细节。

第一轮最小 demo 先需要回答的是：

- agreement 有没有建立
- agreement 建立后 transfer 有没有开始和结束

所以第一轮推荐只把：

- `requested`
- `finalized`
- `terminated`

视作 negotiation 的最小核心事件。

## TransferProcess 推荐的最小状态链

### 最小成功链

| Stage | Recommended EDC event | Why keep it |
| --- | --- | --- |
| transfer requested | `transfer.process.requested` | 证明 agreement 已被用来发起具体 transfer |
| transfer started | `transfer.process.started` | execution evidence 的核心起点 |
| transfer completed | `transfer.process.completed` | success path 终点 |

### 最小失败链

| Stage | Recommended EDC event | Why keep it |
| --- | --- | --- |
| transfer requested | `transfer.process.requested` | 证明 transfer 被发起 |
| transfer started | `transfer.process.started` | 证明执行已经进入运行态 |
| transfer terminated | `transfer.process.terminated` | fail / stop path 终点 |

### 为什么不把 preparation / suspend 先放进最小 demo

因为那会立刻把第一轮扩成更完整的长生命周期状态机说明。

第一轮先证明下面这件事就够了：

- agreement 建立
- transfer 发起
- transfer 开始
- transfer 成功完成或失败终止

`suspended`、`preparationRequested`、`prepared` 更适合作为第三轮之后的扩展。

## 哪些事件暂时不进最小 demo

第一轮建议先不进最小 demo 的主要是四类：

1. update / delete 类管理事件
   这些事件对治理审计有用，但不是最小 transfer 闭环的骨架。

2. contract negotiation 中间态
   `offered`、`accepted`、`agreed`、`verified` 容易把读者拉进更细的协商协议过程。

3. transfer 的 suspension / preparation 类事件
   它们对长生命周期 transfer 很重要，但不是首个最小成功链路的门槛。

4. 官方已标记 deprecated 的 transfer lifecycle 事件
   例如 `provisioned`、`deprovisioningRequested`、`deprovisioned`。

## 如何做 idempotency / de-duplication

第一轮建议做两级去重，而不是只做一级。

### 一级：envelope 级去重

目标：去掉完全重复投递。

建议键：

- `(participantContextId, envelope.id)`

理由：

- `EventEnvelope.id` 是官方定义的事件唯一标识
- `participantContextId` 能避免多参与者上下文混写时的误判

### 二级：语义状态级折叠

目标：去掉“同一个领域对象、同一个状态”被重复记证。

建议键：

- Asset: `(participantContextId, assetId, payload.name())`
- PolicyDefinition: `(participantContextId, policyDefinitionId, payload.name())`
- ContractDefinition: `(participantContextId, contractDefinitionId, payload.name())`
- ContractNegotiation: `(participantContextId, contractNegotiationId, payload.name())`
- TransferProcess: `(participantContextId, transferProcessId, payload.name())`

理由：

- envelope 去重只能挡住“同一个 envelope 重放”
- 语义折叠才能挡住“不同 envelope、同一状态重复发布或重试”

### `EventEnvelope` metadata 和 domain IDs 应该怎么一起用

建议把两类 id 分工用：

- `EventEnvelope.id` 用于“这条消息我见过没有”
- domain IDs 用于“这条消息对应哪条治理链路”

最小链路里最关键的 domain IDs 是：

- `contractNegotiationId`
- `contractAgreement.id` 或 `contractId`
- `transferProcessId`

推荐做法：

1. 先按 `EventEnvelope.id` 去掉精确重复
2. 再按 domain ID + `payload.name()` 折叠同一状态
3. 最后再按 bundle grouping key 把 evidence fragment 归组

## 对 bundle grouping key 的含义提醒

第一轮 mapping 里，最关键的不是“所有事件都立刻有最终 bundle key”，而是：

- 事件先被可靠识别
- 事件能被关联到同一治理链路
- bundle 在 transfer 开始后有明确归宿

因此更稳的思路是：

- negotiation finalized 前：允许先用 `contractAgreement.id` 做临时关联
- transfer started 后：再把最终 bundle 归到 `transferProcessId`

这能避免把多个 transfer 混进同一个 agreement-level bundle。

## 官方参考

以下链接为 2026-04-12 检索时使用的官方入口：

- Control Plane
  [https://eclipse-edc.github.io/documentation/for-adopters/control-plane/](https://eclipse-edc.github.io/documentation/for-adopters/control-plane/)

- Service Layers / events and callbacks
  [https://eclipse-edc.github.io/documentation/for-contributors/runtime/service-layers/](https://eclipse-edc.github.io/documentation/for-contributors/runtime/service-layers/)

- Control-plane entities
  [https://eclipse-edc.github.io/documentation/for-contributors/control-plane/entities/](https://eclipse-edc.github.io/documentation/for-contributors/control-plane/entities/)

- Official event family sources
  [https://github.com/eclipse-edc/Connector/tree/main/spi/control-plane/asset-spi/src/main/java/org/eclipse/edc/connector/controlplane/asset/spi/event](https://github.com/eclipse-edc/Connector/tree/main/spi/control-plane/asset-spi/src/main/java/org/eclipse/edc/connector/controlplane/asset/spi/event)
  [https://github.com/eclipse-edc/Connector/tree/main/spi/control-plane/policy-spi/src/main/java/org/eclipse/edc/connector/controlplane/policy/spi/event](https://github.com/eclipse-edc/Connector/tree/main/spi/control-plane/policy-spi/src/main/java/org/eclipse/edc/connector/controlplane/policy/spi/event)
  [https://github.com/eclipse-edc/Connector/tree/main/spi/control-plane/contract-spi/src/main/java/org/eclipse/edc/connector/controlplane/contract/spi/event](https://github.com/eclipse-edc/Connector/tree/main/spi/control-plane/contract-spi/src/main/java/org/eclipse/edc/connector/controlplane/contract/spi/event)
  [https://github.com/eclipse-edc/Connector/tree/main/spi/control-plane/transfer-spi/src/main/java/org/eclipse/edc/connector/controlplane/transfer/spi/event](https://github.com/eclipse-edc/Connector/tree/main/spi/control-plane/transfer-spi/src/main/java/org/eclipse/edc/connector/controlplane/transfer/spi/event)

- Official `EventEnvelope` source
  [https://github.com/eclipse-edc/Connector/blob/main/spi/common/core-spi/src/main/java/org/eclipse/edc/spi/event/EventEnvelope.java](https://github.com/eclipse-edc/Connector/blob/main/spi/common/core-spi/src/main/java/org/eclipse/edc/spi/event/EventEnvelope.java)
