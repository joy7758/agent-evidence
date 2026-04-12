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
- `src/test/java/.../AgentEvidenceRuntimeModuleIntegrationTest.java`

## 最小配置

默认 properties 文件：

- [agent-evidence-runtime.properties](src/main/resources/agent-evidence-runtime.properties)

当前只固定两个 augmentation 相关配置：

- `edc.agent-evidence.exporter.type`
- `edc.agent-evidence.output-dir`

其中：

- 不写 `exporter.type` 时，仍默认 `filesystem`
- 可以用 JVM 参数覆盖成 `noop`

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

## 这轮实际验证了什么

- runtime module build 能生成最小 launcher distribution
- 运行时 classpath 上能通过 `ServiceLoader` 发现 `AgentEvidenceEdcExtension`
- 最小 config 能流转到 extension 初始化链
- publish control-plane event 后，`filesystem` 会写出 fragment，`noop` 不写文件

## 仍然没做什么

- 没有把 connector 跑成完整对外 API 场景
- 没有补 management API / DSP / transfer scenario
- 没有把 schema JSON 正式化
- 没有把 Python 侧 validator 或 signing 搬回 Java
