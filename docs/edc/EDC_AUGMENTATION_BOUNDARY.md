# EDC Augmentation Boundary

## 结论先行

EDC 在这里不是新研究主线，不是替代品，也不是竞争关系。

在 `agent-evidence` 的语境里，EDC 更合适的定位是一个
execution-evidence augmentation layer 所依附的高价值场景：EDC 负责
dataspace 中的数据交换、合同协商和传输治理，`agent-evidence` 负责把
执行过程整理成可独立验证的 evidence。

这轮只收敛三件事：

- 最小接入 demo 的边界
- 最小 EDC 场景 evidence profile 草案
- 最小独立验证说明

## 1. 做什么

这轮要做的是把 `agent-evidence` 明确挂到 EDC 的控制面附近，而不是重做
EDC 本体。

最小工作范围是：

- 把 EDC 明确写成 `agent-evidence` 的 execution-evidence augmentation layer
- 只围绕 dataspace / policy-governed data exchange 场景收敛最小接入面
- 优先使用 control-plane event extension 捕获与导出 evidence
- 为一个最小 transfer 链路定义最少字段、最少产物、最少验证动作
- 保持 evidence 可以被第三方独立验证，而不是只能回看 EDC 内部日志

换句话说，这里不是“做一个 EDC”，而是“在 EDC 已经负责 catalog /
contract / transfer governance 的前提下，给执行过程补一个可验证证据层”。

## 2. 不做什么

这轮明确不做下面这些事：

- 不把 EDC 变成新的研究主线
- 不做 EDC 替代实现
- 不做完整 EDC 平台
- 不做 connector 产品
- 不做 dataspace 全栈
- 不做通用 usage control 系统
- 不先改 persistence 层
- 不先碰 data plane 传输实现
- 不追求一次解决所有 dataspace flavor 的证据映射

如果一项工作会把范围推向“平台化”或“产品化”，这一轮就先不做。

## 3. 最小可交付是什么

本轮最小可交付只有三块：

1. 一份边界文档
   明确 EDC 和 `agent-evidence` 各自负责什么，以及为什么首个切口是
   control-plane event extension。

2. 一份最小 profile 草案
   只保留独立验证一个最小 transfer 过程所需字段，不带 secrets、
   privateProperties 或内部实现细节。

3. 一条最小 demo 路径说明
   从 asset 到 policy / contract definition，再到 contract agreement、
   transfer process、evidence bundle、independent verify，画出闭环。

这三块加起来的意义，是先把“怎么接、接哪里、交付什么”讲清楚，而不是
先跳进 Java 代码。

## 为什么 EDC 是高价值场景，而不是新方向

EDC 值得接，不是因为我们要换方向，而是因为它天然具备三件事：

- 它已经有真实的 policy-governed data exchange 语境，不是抽象 demo
- 它已经把 catalog、contract、transfer governance 这些关键控制面对象定义清楚
- 它已经给了扩展口，允许在不重做控制面的前提下接入额外能力

这对 `agent-evidence` 很重要。`agent-evidence` 想证明的不是“自己也能做一个
dataspace 控制面”，而是“当现有 dataspace 控制面已经处理交换与治理时，
我们可以把执行过程补成可验证证据”。

所以，EDC 在这里是高价值落地场景，不是新的产品线，也不是新的研究中心。

## 为什么首个接入面是 control-plane event extension

推荐先做 control-plane event extension，而不是先改 persistence 或 data
plane，原因很直接：

- 官方已经把 `ServiceExtension` 作为运行时扩展入口
- 官方已经把 `EventRouter` 作为 in-process 事件订阅入口
- 官方已经提供 callbacks 作为外部接收状态变化的标准方式
- 控制面事件天然覆盖 contract negotiation 和 transfer process 的关键状态变化
- 这些状态变化正好是 evidence 最需要的“谁、何时、对哪条交换链路做了什么”

反过来看，为什么不先动别的面：

- 先改 persistence，会把方案绑到具体表结构、事务实现和版本细节
- 先碰 data plane，会过早卷入真实数据传输协议和连接器能力差异
- 两者都会把“增强层”拉成“平台内部改造”

最小接入 demo 更稳的做法是：

- 在 control plane 订阅关键事件
- 把这些事件归一成最小 evidence bundle
- 让 bundle 脱离运行时后仍可独立验证

如果后面需要更强一致性，再考虑把 exporter 从 async 订阅升级到更可靠的
transactional dispatch 或持久化出口，而不是一开始就侵入底层存储。

## 角色边界

### EDC 负责什么

- 发布和检索 catalog
- 管理 policy definition 和 contract definition
- 生成和协商 contract agreement
- 启动和治理 transfer process
- 协调 control plane 与 data plane 的交互

### `agent-evidence` 负责什么

- 把一次执行过程相关的关键状态变化整理成 evidence bundle
- 记录最小但闭合的 participant / asset / contract / transfer 关联
- 生成可对外传递的 digest、signature、anchor 等验证材料
- 提供独立验证入口，不要求验证者接入 EDC 内部数据库或日志系统

## 当前推荐的最小接入形态

第一轮建议把接入形态收敛成：

- 一个 control-plane event subscriber / exporter 草图
- 一个最小 evidence profile
- 一个独立验证说明

不先承诺：

- 完整 Java 扩展实现
- 完整 management API 自动化
- 全状态机覆盖
- 跨 connector 产品化部署

## 官方依据

以下链接为 2026-04-12 检索时使用的官方入口：

- EDC Control Plane
  [https://eclipse-edc.github.io/documentation/for-adopters/control-plane/](https://eclipse-edc.github.io/documentation/for-adopters/control-plane/)
  说明控制面负责 catalog、contract agreement、transfer governance，并明确
  transfer 只控制数据流，不直接发送数据。

- EDC Extensions / `ServiceExtension`
  [https://eclipse-edc.github.io/documentation/for-adopters/extensions/](https://eclipse-edc.github.io/documentation/for-adopters/extensions/)
  说明运行时扩展的官方入口是 `ServiceExtension`。

- EDC Events and Callbacks / `EventRouter`
  [https://eclipse-edc.github.io/documentation/for-contributors/runtime/service-layers/](https://eclipse-edc.github.io/documentation/for-contributors/runtime/service-layers/)
  说明控制面状态变化通过事件传播，支持 in-process 订阅和 webhook callbacks。

- EDC Control-plane entities and transfer callbacks
  [https://eclipse-edc.github.io/documentation/for-contributors/control-plane/entities/](https://eclipse-edc.github.io/documentation/for-contributors/control-plane/entities/)
  说明 transfer process 的回调事件类型，以及 callbackAddresses 的使用方式。

- Eclipse Dataspace Protocol scope
  [https://eclipse-dataspace-protocol-base.github.io/DataspaceProtocol/HEAD/](https://eclipse-dataspace-protocol-base.github.io/DataspaceProtocol/HEAD/)
  说明 DSP 的范围是 publish data、negotiate agreements、access data。

## 下一步路线图

1. 先画清楚 control-plane event -> evidence field mapping，只覆盖最小成功链路。
2. 再把 mapping 收敛成 EDC minimal evidence schema / JSON 草案。
3. 最后补一个最小 exporter demo 和独立 verify 说明，不提前产品化。
