# Java Spike Boundary

## 结论先行

这个 Java spike 只验证 EDC control-plane augmentation skeleton。

它不负责重做 `agent-evidence`，也不负责重做 EDC。

当前它已经推进到 compile-capable subscriber / mapper / grouping spike，但这个事实不改变边界，只说明最小接入链在 Java 侧可以先站住。

## Java extension 侧负责什么

- 接进 EDC runtime 的 `ServiceExtension`
- 注册 control-plane event family subscriber
- 接收 `EventEnvelope` 与 payload
- 抽取 envelope metadata
- 抽取 agreement / transfer / asset 等领域 id
- 做两级去重入口
- 生成 semantic evidence fragment
- 选择最小 exporter 实现
- 输出可交给 `agent-evidence` 的中间导出物

这些职责都属于：

- observation
- normalization
- export

## Python `agent-evidence` 侧负责什么

- evidence profile 定义
- schema
- validator
- manifest / digest 规则
- signing
- anchor / trust binding
- 独立验证结果输出
- examples / invalid corpus / CLI / demo

这些职责都属于：

- verification
- artifact packaging
- external validation

## 为什么这轮不把 signing / verification / anchor 下沉到 Java

因为那会直接把 spike 从“接入骨架验证”拉成“复制一套主线能力”。

这轮 Java 侧只需要证明：

- 能接收到 control-plane event
- 能把 event 变成 semantic evidence fragment
- 能把 fragment 带出 runtime
- 能把 exporter 选择和 handoff 边界稳定交给外部 evidence 层

一旦 fragment 已经成功带出 runtime，签名、anchor、独立验证就应该继续复用
Python `agent-evidence` 侧，而不是在 Java 里重写一套。

## 为什么这轮不改 EDC persistence

因为一旦开始改 persistence，就会立刻把 spike 绑到：

- 表结构
- 事务细节
- state machine 内部实现
- 具体版本差异

这会把 augmentation layer 变成 runtime 内部改造。

第一轮更稳的做法，是先站在官方扩展面上：

- `ServiceExtension`
- `EventRouter`
- `EventEnvelope`

## 为什么这轮也不碰 data plane

EDC 官方文档已经明确：

- control plane 治理 transfer
- data plane 实际发送数据

这轮 `agent-evidence` 想补的是 execution evidence layer，而不是新的传输实现。

所以这轮不做：

- provisioner
- data plane signaling 深入集成
- connector 产品化封装

## 为什么这轮只做最小 exporter 集合

因为这轮要压实的是“Java augmentation layer 如何把 fragments 带出 runtime”，不是“Java 侧最终怎么验证它们”。

所以当前 exporter 只保留最小集合：

- `filesystem`
- `noop` / `disabled`

这足够验证：

- exporter 选择
- 配置注入
- output-dir handoff
- no-output 边界

但不会把 spike 扩张成：

- queue / broker 集成
- remote API exporter
- signing / verification / anchor runtime

## 当前边界判断标准

如果一个改动开始要求下面这些事情之一，它就已经超出这轮范围：

- 需要自定义 connector 运行时组装
- 需要真实部署 provider / consumer runtime
- 需要依赖内部数据库记录才能理解 evidence
- 需要在 Java 侧完成完整 validation / signing / anchor

达到这些点，就说明该停在 spike 边界外。
