# Startup Failure Triage Recipe

## 结论先行

这不是新的运行机制。

它只是一个最小排障配方，回答一个很具体的问题：

当 `runtime-module-sample/run-startup-smoke.sh` 失败时，应该先看哪一层，
再做哪一步，而不是从一大段日志里盲猜。

当前只覆盖已经固定下来的三类 startup failure：

- 端口占用
- 缺失 control-plane event SPI
- 非法 `edc.agent-evidence.exporter.type`

## 最短排障顺序

1. 先看脚本 stderr 里的归一化错误摘要。
2. 再看 `LOG_PATH` 对应的原始 runtime 日志。
3. 确认问题属于哪一层：
   - runtime 端口绑定
   - runtime classpath / event SPI
   - exporter 配置
4. 只修这一层，不要同时改事件范围、writer 逻辑或 sample 结构。

## Quick Lookup

| 看到的错误摘要 | 先判断哪一层 | 先看哪里 | 最小修复动作 |
| --- | --- | --- | --- |
| `Error: Port <port> is already in use.` | runtime 端口绑定 | `JAVA_OPTS`、properties 里的 `web.http.port`、原始 startup log 里的 `BindException` | 换一个空闲端口，或让脚本自动分配 |
| `Error: Missing Event SPI for <event-family>.` | runtime classpath / launcher 依赖 | launcher `lib/`、`runtime-module-sample/build.gradle.kts`、原始 startup log | 补回缺失的 SPI 依赖，重新 `installDist` |
| `Error: Invalid exporter type <value> specified.` | extension 配置 | `agent-evidence-runtime.properties`、`JAVA_OPTS` 覆盖项 | 改成 `filesystem`、`noop` 或 `disabled` |

## Case 1: Port Already in Use

### 这说明什么

这不是 `agent-evidence` mapper / grouping / writer 逻辑的问题。

这说明 `BaseRuntime` 还没完成 HTTP 端口绑定，就已经在 Jetty 启动阶段失败了。

### 先看什么

- stderr 是否有 `Error: Port <port> is already in use.`
- startup log 是否有 `BindException` 或 `Address already in use`
- 当前是否显式传了：
  - `JAVA_OPTS=-Dweb.http.port=<port>`

### 最小修复动作

如果只是想跑通 smoke，最简单的是不要手动固定端口：

```bash
cd /Users/zhangbin/GitHub/agent-evidence-edc-java-spike/spikes/edc-java-extension
runtime-module-sample/run-startup-smoke.sh
```

脚本会自动挑一个空闲端口。

如果你必须指定端口，就换一个空闲值：

```bash
cd /Users/zhangbin/GitHub/agent-evidence-edc-java-spike/spikes/edc-java-extension
JAVA_OPTS="-Dweb.http.port=19291" runtime-module-sample/run-startup-smoke.sh
```

## Case 2: Missing Event SPI

### 这说明什么

这不是 exporter 配置错误。

这说明 runtime launcher classpath 上缺了 extension 注册最小 control-plane family 所需的 SPI jar。

### 先看什么

- stderr 是否有 `Error: Missing Event SPI for <event-family>.`
- startup log 里缺的是哪一个 family
- `runtime-module-sample/build.gradle.kts` 的 `runtimeOnly(...)` 是否还包含：
  - `asset-spi`
  - `policy-spi`
  - `contract-spi`
  - `transfer-spi`
  - `transaction-spi`

### 最小修复动作

1. 先确认 launcher 依赖还在。
2. 重新生成 runtime distribution：

```bash
cd /Users/zhangbin/GitHub/agent-evidence-edc-java-spike/spikes/edc-java-extension
./gradlew :runtime-module-sample:installDist
```

3. 再重新跑 smoke：

```bash
cd /Users/zhangbin/GitHub/agent-evidence-edc-java-spike/spikes/edc-java-extension
runtime-module-sample/run-startup-smoke.sh
```

### 不要做什么

- 不要为了解决 classpath 缺口去放宽 event 范围
- 不要把 missing SPI 变成 silent fallback
- 不要把问题误判成 mapper / evidence fragment 输出问题

## Case 3: Invalid Exporter Type

### 这说明什么

这不是 runtime 端口问题，也不是 event SPI 缺失。

这说明 extension 已经被加载，但 exporter 选择阶段拿到了不支持的配置值。

### 先看什么

- stderr 是否有 `Error: Invalid exporter type <value> specified.`
- properties 文件里是否写了不支持的值
- `JAVA_OPTS` 是否覆盖了：
  - `-Dedc.agent-evidence.exporter.type=<value>`

### 当前唯一支持的值

- `filesystem`
- `noop`
- `disabled`

### 最小修复动作

直接把值改回最小支持集合之一：

```bash
cd /Users/zhangbin/GitHub/agent-evidence-edc-java-spike/spikes/edc-java-extension
JAVA_OPTS="-Dedc.agent-evidence.exporter.type=noop" runtime-module-sample/run-startup-smoke.sh
```

或者恢复默认 `filesystem`：

```bash
cd /Users/zhangbin/GitHub/agent-evidence-edc-java-spike/spikes/edc-java-extension
runtime-module-sample/run-startup-smoke.sh
```

## 如果没有匹配到三类已知失败

先不要扩代码。

先保留当前 startup log，并检查：

- stderr 是否已经出现 `Runtime initialization failed. See startup log for details.`
- startup log 里是 runtime boot 失败，还是 extension 初始化失败
- 失败发生在：
  - `Using agent-evidence exporter type ...` 之前
  - 还是 `Registered control-plane event subscribers ...` 之后

如果失败发生在这三类之外，再单独补新契约；不要把未知失败硬塞进现有三类。

## 这份配方的边界

它只服务于当前最小 runtime startup smoke。

它不覆盖：

- management API / DSP 场景
- transfer 运行期错误
- evidence fragment 写盘后的内容校验
- Python `agent-evidence` validator / signing / anchor
