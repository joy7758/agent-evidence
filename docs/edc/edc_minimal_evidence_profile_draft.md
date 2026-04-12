# EDC Minimal Evidence Profile Draft

## 结论先行

这不是一个大而全的 EDC profile。

这只是一个最小字段草案，用来支持一个最小 dataspace 交换链路的独立验证：
谁和谁交换、基于哪条 policy / contract、走了哪条 transfer process、
最后导出了什么 evidence。

## 适用边界

这个草案默认挂在 EDC control-plane event extension / exporter 上。

它不试图表达：

- EDC 的全部实体模型
- data plane 的所有传输细节
- connector 的全部内部状态
- vault、database、secret 管理细节

## 最小字段表

| 字段名 | 含义 | 来源 | 是否必填 | 为什么需要 |
| --- | --- | --- | --- | --- |
| `provider_participant_id` | 提供方参与者标识 | 控制面 participant 配置、catalog / contract 相关对象 | 是 | 让第三方知道证据指向哪一方提供数据 |
| `consumer_participant_id` | 消费方参与者标识 | contract negotiation / agreement / transfer 相关对象 | 是 | 让第三方知道合同和传输绑定到哪一方消费者 |
| `asset_id` | 被交换资产标识 | asset / dataset / catalog offer 关联对象 | 是 | 把 evidence 绑定到具体被治理对象 |
| `policy_definition_id` | 生效的 policy definition 标识 | policy definition | 是 | 让验证者知道治理约束来自哪条 policy |
| `contract_definition_id` | 触发该交换的 contract definition 标识 | contract definition | 是 | 衔接 asset 选择和合同生成入口 |
| `contract_agreement_id` | 已达成合同标识 | contract agreement | 是 | 这是 transfer process 的核心治理绑定点 |
| `transfer_process_id` | 传输过程标识 | transfer process | 是 | 把 evidence 绑定到单条控制面交换链路 |
| `flow_type` | 传输流型，如 `consumer-pull` / `provider-push` | transfer request、distribution、transfer metadata | 是 | 让验证者知道链路语义，不必反推 data plane 内部实现 |
| `state_transitions` | 控制面观测到的关键状态序列 | control-plane events / callbacks | 是 | 这是最小执行证据主体，证明链路如何推进 |
| `started_at` | 链路开始进入运行态的时间 | `transfer.process.started` 或等价事件时间戳 | 是 | 为第三方提供最小时间锚点 |
| `completed_at` | 成功完成时间 | `transfer.process.completed` 事件时间戳 | 否 | 只在成功完成路径需要 |
| `terminated_at` | 终止时间 | `transfer.process.terminated` 事件时间戳 | 否 | 只在失败或被终止路径需要 |
| `manifest_digest` | evidence bundle manifest 的摘要 | `agent-evidence` exporter 生成的 manifest | 是 | 让第三方验证 bundle 没被篡改 |
| `signature_count` | bundle 上可见签名数量 | manifest / signature material | 是 | 让验证者知道当前证据带不带签名以及有几个 |
| `anchor_type` | 外部锚定机制类型，如 transparency log / registry | augmentation exporter 生成的可选 binding | 否 | 用来声明是否有外部可核验锚点 |
| `anchor_id` | 外部锚定标识 | 外部 anchor / receipt / transparency entry | 否 | 让第三方能追到外部验证对象 |

## 字段解释上的几个收敛原则

- `state_transitions` 应只保留对外可解释的最小状态，不照搬内部所有中间态
- `flow_type` 只保留验证所需的链路语义，不展开 data plane 实现细节
- `manifest_digest` 是证据包完整性的最小抓手，不等于 EDC 内部对象哈希总表
- `signature_count` 可以为 `0`，但字段本身保留，避免验证者猜测有没有签名层

## 哪些字段故意不带

下面这些内容这版故意不带：

- secrets
- `privateProperties`
- vault key / secret alias
- callback `authKey` / `authCodeId`
- EDR token、临时访问令牌、连接凭证
- `DataAddress` 的内部实现细节
- JDBC 表主键、行版本号、重试计数器、调度器元数据
- connector 内部线程、队列、事务日志
- 任意会把验证者绑定到某个具体部署实现的内部字段

原因很简单：

- 这些字段不是独立验证最小闭环所必需
- 它们容易泄露安全信息
- 它们会把 profile 从“可移植证据”拉成“实现内省导出”

## 如何支持第三方 independent verification，而不依赖 EDC 内部日志

目标不是让第三方接进 EDC 数据库或日志系统，而是给第三方一个足够小、但能
闭环验证的 evidence bundle。

最小做法是：

- 由 control-plane event extension / exporter 导出一个 bundle
- bundle 内至少包含上表中的最小字段
- `state_transitions` 使用事件时间戳和状态名表达链路推进
- `manifest_digest` 保护导出物本身
- 如有签名或外部锚定，再通过 `signature_count`、`anchor_type`、`anchor_id`
  暴露出来

第三方验证时至少做四件事：

1. 检查字段完整性和必填项
   看 participant、asset、policy、contract、transfer 是否闭合。

2. 检查关联闭合
   看 `asset_id`、`policy_definition_id`、`contract_definition_id`、
   `contract_agreement_id`、`transfer_process_id` 是否属于同一条交换链路。

3. 检查时间与状态一致性
   看 `state_transitions` 是否合理，`started_at`、`completed_at`、
   `terminated_at` 是否与状态路径相符。

4. 检查证据完整性
   重算或核对 `manifest_digest`，并在存在签名或锚定时继续核对外部材料。

这意味着验证者拿到 bundle 后，不需要访问 EDC 内部日志，只需要：

- 证据包本身
- 公开或可共享的 agreement / transfer 标识
- 可选的外部签名或锚定材料

## 当前建议的最小成功链路

最先支持的不是所有状态，而是一条最小成功链路：

- contract agreement 已生成
- transfer process 已启动
- transfer process 已完成
- evidence bundle 已导出
- 第三方可独立核对 manifest 和关联字段

终止态、暂停态、恢复态可以作为下一轮扩展，而不是这轮的门槛。

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
