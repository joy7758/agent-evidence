# EDC Runtime Module Integration Sample

## 结论先行

这不是一个新的 connector 产品，也不是一个完整 dataspace runtime。

它只是一个最小 launcher 子模块，用来验证两件事：

- `AgentEvidenceEdcExtension` 能不能按 EDC 官方 extension model 被放进 runtime classpath
- `edc.agent-evidence.exporter.type` 和 `edc.agent-evidence.output-dir` 能不能在 runtime module 侧稳定流转到 exporter handoff

这个子模块故意只覆盖 control-plane augmentation layer。

它不做：

- persistence 改造
- data plane
- signing / verification / anchor 下沉
- 新 exporter 类型

## 为什么是这个结构

EDC 官方 adopter 文档把 extension 装配说得很清楚：

- extension 必须在 runtime classpath 上
- extension 通过 `META-INF/services/org.eclipse.edc.spi.system.ServiceExtension` 被加载
- runnable connector 可以用 `BaseRuntime` 加少量 runtime 依赖拼出来

官方参考：

- [Extensions](https://eclipse-edc.github.io/documentation/for-adopters/extensions/)
- [Basic connector sample](https://github.com/eclipse-edc/Samples/tree/main/basic/basic-01-basic-connector)

因此，这个子模块刻意采用和官方 basic sample 接近的形状：

- `BaseRuntime` 作为 main class
- `boot` / `runtime-core` / `connector-core` / `http`
- `configuration-filesystem` 用于 properties 文件
- `runtimeOnly(project(":"))` 把当前 spike extension 放进 runtime module

这里故意不再加 fat-jar 打包插件，而是用 Gradle 自带的 `application` / `installDist`。
原因很简单：这轮要验证的是 runtime module 装配边界，不是额外的打包链。

## 目录

- `build.gradle.kts`
- `src/main/resources/agent-evidence-runtime.properties`
- `src/main/resources/agent-evidence-runtime-noop.properties`
- `RUNTIME_EXPORTER_INTEGRATION_SAMPLE.md`
- `src/test/java/.../AgentEvidenceRuntimeModuleIntegrationTest.java`

## 最小配置

默认 properties 文件：

- [agent-evidence-runtime.properties](src/main/resources/agent-evidence-runtime.properties)
- [agent-evidence-runtime-noop.properties](src/main/resources/agent-evidence-runtime-noop.properties)

当前只固定两个 augmentation 相关配置：

- `edc.agent-evidence.exporter.type`
- `edc.agent-evidence.output-dir`

其中：

- 不写 `exporter.type` 时，仍默认 `filesystem`
- 也可以直接使用单独的 noop properties 样例

同时，launcher 侧会显式把 control-plane event SPI 放进 runtime classpath。
这是这轮 smoke 暴露出来的实际接入要求：extension jar 本身不是孤立运行的，它依赖这些 event family 类型在 runtime 启动期可见。

## 构建

```bash
cd /Users/zhangbin/GitHub/agent-evidence-edc-java-spike/spikes/edc-java-extension
./gradlew :runtime-module-sample:installDist
```

生成物：

- `runtime-module-sample/build/install/runtime-module-sample/`

## 运行提示

```bash
cd /Users/zhangbin/GitHub/agent-evidence-edc-java-spike/spikes/edc-java-extension
JAVA_OPTS="-Dedc.fs.config=runtime-module-sample/src/main/resources/agent-evidence-runtime.properties" \
runtime-module-sample/build/install/runtime-module-sample/bin/runtime-module-sample
```

如果只想验证 no-output handoff，可以追加：

```bash
JAVA_OPTS="-Dedc.fs.config=runtime-module-sample/src/main/resources/agent-evidence-runtime.properties -Dedc.agent-evidence.exporter.type=noop"
```

也可以直接用 noop properties：

```bash
cd /Users/zhangbin/GitHub/agent-evidence-edc-java-spike/spikes/edc-java-extension
JAVA_OPTS="-Dedc.fs.config=runtime-module-sample/src/main/resources/agent-evidence-runtime-noop.properties" \
runtime-module-sample/build/install/runtime-module-sample/bin/runtime-module-sample
```

如果想看最小的配置 -> exporter -> subscriber -> writer 装配说明，可以直接看
[RUNTIME_EXPORTER_INTEGRATION_SAMPLE.md](RUNTIME_EXPORTER_INTEGRATION_SAMPLE.md)。

## Runtime Startup Smoke

这轮额外补了一个带超时保护的真实启动 smoke：

- [run-startup-smoke.sh](run-startup-smoke.sh)

运行方式：

```bash
cd /Users/zhangbin/GitHub/agent-evidence-edc-java-spike/spikes/edc-java-extension
env JAVA_HOME=/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home \
  PATH=/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home/bin:/opt/homebrew/bin:$PATH \
  runtime-module-sample/run-startup-smoke.sh
```

默认超时是 120 秒，也可以覆盖：

```bash
TIMEOUT_SECONDS=60 runtime-module-sample/run-startup-smoke.sh
```

脚本默认会先刷新一次 `:runtime-module-sample:installDist`，避免拿旧的 launcher 产物做 smoke。
如果你明确知道当前 `installDist` 已经是新的，可以传：

```bash
REFRESH_INSTALL_DIST=0 runtime-module-sample/run-startup-smoke.sh
```

脚本默认还会自动挑一个空闲 `web.http.port`，避免本机已有进程占住 `19191`。
只有在你显式传入 `JAVA_OPTS=-Dweb.http.port=...` 时，它才会使用你指定的端口。

这条 smoke 的成功条件不是“进程永远跑着”，而是日志里出现：

- `Using agent-evidence exporter type '<expected-exporter>'`
- `Using agent-evidence output directory '<expected-output-dir>'`
- `Registered control-plane event subscribers for agent-evidence spike`
- `Runtime ... ready`

满足这四个条件后，脚本会主动结束 runtime 进程并返回成功。

这里的 `<expected-exporter>` 和 `<expected-output-dir>` 会按下面顺序推导：

1. `JAVA_OPTS` 覆盖值
2. `RUNTIME_PROPERTIES_PATH` 指向的 properties
3. 默认值

如果 startup 失败，脚本会尽量把已知失败面归一成稳定摘要：

- `Error: Port <port> is already in use.`
- `Error: Missing Event SPI for <event-family>.`
- `Error: Invalid exporter type <value> specified.`

具体契约见
[../STARTUP_FAILURE_CONTRACT.md](../STARTUP_FAILURE_CONTRACT.md)。

如果想看最短排障步骤，可以直接看
[../FAILURE_TRIAGE_RECIPE.md](../FAILURE_TRIAGE_RECIPE.md)。

如果想看 exporter 配置和 startup smoke 如何一起流转，可以直接看
[RUNTIME_EXPORTER_INTEGRATION_SAMPLE.md](RUNTIME_EXPORTER_INTEGRATION_SAMPLE.md)。

## 这轮实际验证了什么

- runtime module build 能生成最小 launcher distribution
- 运行时 classpath 上能通过 `ServiceLoader` 发现 `AgentEvidenceEdcExtension`
- 最小 config 能流转到 extension 初始化链
- publish control-plane event 后，`filesystem` 会写出 fragment，`noop` 不写文件
- 真实 runtime startup smoke 能在超时窗口内看到 extension 注册日志并安全退出
- runtime integration tests 现在直接用 sample properties 验证 exporter 选择和事件流转

另外，这轮也把 subscriber family 注册收成了按类名解析。
目的不是“躲开类型系统”，而是减少 runtime startup 时对 event family 的过早静态链接，让 launcher classpath 负责最终提供这些类型。

## 仍然没做什么

- 没有把 connector 跑成完整对外 API 场景
- 没有补 management API / DSP / transfer scenario
- 没有把 schema JSON 正式化
- 没有把 Python 侧 validator 或 signing 搬回 Java
