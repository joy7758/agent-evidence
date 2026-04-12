# Startup Failure Contract

## 结论先行

这份契约不是在给 runtime 增加新的容错层。

它只收敛一件事：当 `agent-evidence` augmentation layer 在 startup 阶段失败时，
日志和退出行为必须可预期，不能只剩一个模糊的非零退出码。

当前只覆盖三类已经足够关键的失败面：

- 端口占用
- 缺失 control-plane event SPI
- 非法 `edc.agent-evidence.exporter.type`

## Failure Cases

### 1. Port Already in Use

如果 runtime 绑定的 `web.http.port` 已被占用，startup smoke 必须把底层启动失败
归一成一个清楚的错误摘要。

最小要求：

- stderr 出现 `Error: Port <port> is already in use.`
- 进程以非零退出码退出
- 原始 runtime 日志仍然保留并输出，便于看底层堆栈

这类错误主要由 `run-startup-smoke.sh` 归一，而不是让 extension 自己判断。

### 2. Missing Event SPI

如果 runtime classpath 缺少 extension 需要的 control-plane event family，
extension 初始化必须 fail-fast。

最小要求：

- 日志里出现：
  - `Runtime initialization failed: Missing Event SPI for '<event-family>'...`
- smoke 脚本归一成：
  - `Error: Missing Event SPI for <event-family>.`
- 进程以非零退出码退出

当前最小 family 仍然只包括：

- `AssetEvent`
- `PolicyDefinitionEvent`
- `ContractDefinitionEvent`
- `ContractNegotiationEvent`
- `TransferProcessEvent`

### 3. Invalid Exporter Type

如果 `edc.agent-evidence.exporter.type` 配成不支持的值，不能 silent fallback。

最小要求：

- extension 初始化直接 fail-fast
- 日志里出现：
  - `Runtime initialization failed: Invalid exporter type '<value>' specified for edc.agent-evidence.exporter.type...`
- smoke 脚本归一成：
  - `Error: Invalid exporter type <value> specified.`
- 进程以非零退出码退出

当前唯一支持的 exporter 仍然只有：

- `filesystem`
- `noop`
- `disabled`

## Expected Exit Behavior

这三类失败当前统一遵守同一条退出约定：

- startup 失败时必须返回非零退出码
- stdout / stderr 必须能看出失败摘要
- 原始 startup log 不能被吞掉

如果脚本无法识别成已知失败面，也必须至少输出：

- `Runtime initialization failed. See startup log for details.`

## Why This Boundary

这一步的价值不是“做健壮性平台”。

价值在于把 augmentation layer 和 runtime module 的交界收清楚：

- 配置错误要尽早暴露
- classpath 缺口要尽早暴露
- runtime 启动失败要有稳定可断言的信号

这样后面即使继续补 runtime sample，也不会把失败路径埋在随机日志里。

## Test Scenarios

当前最小验证场景包括：

- 显式占住 `web.http.port`，验证 `Error: Port <port> is already in use.`
- 用无效 `exporter.type` 启动 runtime，验证 invalid exporter fail-fast
- 用裁剪过的 launcher classpath 启动 runtime，验证 missing event SPI fail-fast

这些测试只验证 startup 边界，不扩展新的 exporter、事件范围或 connector 功能。

如果想看出错后的最小排障顺序，可以直接看
[FAILURE_TRIAGE_RECIPE.md](FAILURE_TRIAGE_RECIPE.md)。
