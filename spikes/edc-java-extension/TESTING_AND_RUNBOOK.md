# Testing And Runbook

## 最常用命令

默认工作目录：

```bash
cd /Users/zhangbin/GitHub/agent-evidence-edc-java-spike/spikes/edc-java-extension
```

最小编译验证：

```bash
./gradlew compileJava
```

最小测试验证：

```bash
./gradlew test
```

仅跑 runtime module sample 测试：

```bash
./gradlew :runtime-module-sample:test
```

带超时保护的真实 startup smoke：

```bash
runtime-module-sample/run-startup-smoke.sh
```

如需验证 `noop` properties：

```bash
RUNTIME_PROPERTIES_PATH=runtime-module-sample/src/main/resources/agent-evidence-runtime-noop.properties \
runtime-module-sample/run-startup-smoke.sh
```

如需验证 `JAVA_OPTS` override：

```bash
JAVA_OPTS="-Dedc.agent-evidence.exporter.type=noop -Dedc.agent-evidence.output-dir=./runtime-module-sample/override-output" \
runtime-module-sample/run-startup-smoke.sh
```

## `JAVA_HOME` 要求

这条 spike 默认按 Java 17 运行。

在当前环境里，最稳定的方式是显式设置：

```bash
export JAVA_HOME=/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home
export PATH="$JAVA_HOME/bin:/opt/homebrew/bin:$PATH"
```

如果 `java` 或 `gradle` 不在当前 shell 里可见，先检查这一层，而不是先怀疑 spike 代码路径。

## `BaseRuntime` smoke 的最小成功信号

`runtime-module-sample/run-startup-smoke.sh` 最小成功信号只有这些：

- exporter type 已打印
- output directory 已打印
- control-plane subscribers 已注册
- `Runtime ... ready` 已出现

只要这四个信号都出现，当前 startup smoke 就认为 runtime-facing augmentation path 已经站住。

## 已知执行注意事项

之前出现过一次 `runtime-module-sample/build/test-results` 的并行写入冲突。

这属于 Gradle 测试执行方式问题，不是功能问题。串行重跑 `:runtime-module-sample:test` 和 `./gradlew test` 后结果通过。

如果再次遇到类似问题，先避免并行跑两个会同时写相同 test-results 目录的命令。

## 出错先看哪里

- 先看 [STARTUP_FAILURE_CONTRACT.md](STARTUP_FAILURE_CONTRACT.md)：这里定义了已知失败面的日志和退出契约。
- 再看 [FAILURE_TRIAGE_RECIPE.md](FAILURE_TRIAGE_RECIPE.md)：这里给出最短排障顺序。
- 再看 [RUNTIME_STARTUP_LOG_CONTRACT.md](RUNTIME_STARTUP_LOG_CONTRACT.md)：这里定义了 startup 成功时最小必须出现的日志。
