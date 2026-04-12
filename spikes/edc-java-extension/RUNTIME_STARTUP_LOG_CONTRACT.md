# Runtime Startup Log Contract

## 结论先行

这份契约不是在定义一个新的日志系统。

它只收敛 `runtime-module-sample` 启动阶段必须出现的最小日志信号，让我们能回答一个具体问题：

`AgentEvidenceEdcExtension` 是否真的被 runtime 加载，并完成了最小 control-plane subscriber 注册。

当前只覆盖 startup 阶段，不覆盖后续 transfer 运行期的全量日志。

## Expected Logs During Startup

启动日志至少应包含下面四类信息。

### 1. Configuration Logs

必须能看出当前 startup 使用的关键 handoff 配置。

最小要求：

- `edc.agent-evidence.exporter.type`
- `edc.agent-evidence.output-dir`

当前最小契约里，`AgentEvidenceEdcExtension` 至少会明确输出 exporter type。
`output-dir` 不要求在 startup 第一屏就打印，但必须能从配置文件或后续 writer 日志中追到。

### 2. Event Subscription Logs

必须能看出 extension 已完成最小 family 注册。

最小要求：

- 日志中出现 `Registered control-plane event subscribers for agent-evidence spike`

这条日志的意义不是“所有业务都可用”，而是说明 augmentation layer 已经接入：

- `AssetEvent`
- `PolicyDefinitionEvent`
- `ContractDefinitionEvent`
- `ContractNegotiationEvent`
- `TransferProcessEvent`

### 3. Export Path / Exporter Logs

必须能看出当前 exporter 选择结果。

最小要求：

- 日志中出现 `Using agent-evidence exporter type 'filesystem'`
  或
- 日志中出现 `Using agent-evidence exporter type 'noop'`

如果是 `filesystem`，后续 writer 运行时还应能把写入目标路径打到 debug 日志中。
startup smoke 不强制等待这条 writer debug 日志，但它属于后续运行期应保留的可观测信号。

### 4. Startup Completion

必须能看出 runtime 已经完成 boot。

最小要求：

- 日志中出现 `Runtime ... ready`

如果启动失败，则应直接保留异常堆栈，而不是吞掉错误。
当前 smoke 也把这点当作契约的一部分：失败必须可见，不能只给一个模糊退出码。

## Required Log Order

当前最小启动顺序约定如下：

1. `Booting EDC runtime`
2. runtime 自身的基础配置 / warning 日志
3. `Using agent-evidence exporter type '...'`
4. `Registered control-plane event subscribers for agent-evidence spike`
5. `Runtime ... ready`

不要求完全逐行相邻，但这几个阶段性信号必须保持这个逻辑顺序。

## Why These Logs

这几条日志合起来解决的是最小接入验证，而不是生产观测全景：

- 配置是否真的流到了 extension
- extension 是否真的被 runtime 加载
- subscriber 是否真的完成注册
- runtime 是否真的完成 boot

如果少了其中任意一类，我们就很难区分：

- classpath 问题
- provider file 未生效
- extension 初始化失败
- runtime 已启动但 augmentation layer 没接上

## Startup Smoke Pass Condition

当前 `runtime-module-sample/run-startup-smoke.sh` 的成功条件就是：

- 看到 `Using agent-evidence exporter type 'filesystem'`
- 看到 `Registered control-plane event subscribers for agent-evidence spike`
- 看到 `Runtime ... ready`

满足后脚本会主动结束 runtime 进程，并返回成功。

## Out of Scope

这份契约当前不要求：

- 打印全部 EDC 配置项
- 打印所有 event payload
- 打印每次 writer 写盘的完整路径列表
- 打印 signing / verification / anchor 信息
- 覆盖 persistence 或 data plane 生命周期日志

原因很简单：这些都已经超出当前 augmentation startup 的最小验证边界。
