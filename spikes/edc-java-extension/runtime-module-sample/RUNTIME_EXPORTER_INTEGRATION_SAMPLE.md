# Runtime Exporter Integration Sample

## 结论先行

这份样例只回答一个问题：

在最小 `BaseRuntime` launcher 里，`exporter` 配置和 control-plane 事件处理是怎么装配到
`AgentEvidenceEdcExtension` 里的。

它不是新的 runtime 工程，也不是新的 exporter 设计。

## 最小流转

当前最小运行时装配链只有这一条：

1. `edc.fs.config`
2. `agent-evidence-runtime.properties` 或 `agent-evidence-runtime-noop.properties`
3. `AgentEvidenceEdcExtension.initialize(...)`
4. `AgentEvidenceRuntimeWiring.from(...)`
5. `ConfigurableEvidenceEnvelopeWriterFactory`
6. `ControlPlaneEvidenceSubscriber`
7. `filesystem` 写出 fragment，或 `noop` 不写出

## 两个最小样例

### 1. Filesystem handoff

配置文件：

- [agent-evidence-runtime.properties](src/main/resources/agent-evidence-runtime.properties)

关键配置：

- `edc.agent-evidence.exporter.type=filesystem`
- `edc.agent-evidence.output-dir=./runtime-module-sample/output`

事件流转结果：

- extension 读取配置
- 选择 `FileSystemEvidenceEnvelopeWriter`
- 注册 control-plane subscriber
- 收到事件后输出 evidence fragments

### 2. Noop handoff

配置文件：

- [agent-evidence-runtime-noop.properties](src/main/resources/agent-evidence-runtime-noop.properties)

关键配置：

- `edc.agent-evidence.exporter.type=noop`
- `edc.agent-evidence.output-dir=./runtime-module-sample/noop-output`

事件流转结果：

- extension 读取配置
- 选择 `NoOpEvidenceEnvelopeWriter`
- subscriber / mapper / grouping 链继续执行
- 不写文件

## Startup Smoke 也会跟着配置走

`run-startup-smoke.sh` 现在不再把 `filesystem` 写死在成功条件里。

它会先看：

1. `RUNTIME_PROPERTIES_PATH` 指向的 properties
2. `JAVA_OPTS` 里的 `-Dedc.agent-evidence.exporter.type=...`
3. `JAVA_OPTS` 里的 `-Dedc.agent-evidence.output-dir=...`

然后再决定 startup 时应该看到哪一种 exporter 和哪一个 output-dir。

这意味着同一个 smoke 脚本现在可以直接验证：

- 默认 `filesystem`
- sample `noop` properties
- `JAVA_OPTS` 覆盖 exporter / output-dir

## 最小运行方式

Filesystem:

```bash
cd /Users/zhangbin/GitHub/agent-evidence-edc-java-spike/spikes/edc-java-extension
JAVA_OPTS="-Dedc.fs.config=runtime-module-sample/src/main/resources/agent-evidence-runtime.properties" \
runtime-module-sample/build/install/runtime-module-sample/bin/runtime-module-sample
```

Noop:

```bash
cd /Users/zhangbin/GitHub/agent-evidence-edc-java-spike/spikes/edc-java-extension
JAVA_OPTS="-Dedc.fs.config=runtime-module-sample/src/main/resources/agent-evidence-runtime-noop.properties" \
runtime-module-sample/build/install/runtime-module-sample/bin/runtime-module-sample
```

Noop startup smoke:

```bash
cd /Users/zhangbin/GitHub/agent-evidence-edc-java-spike/spikes/edc-java-extension
RUNTIME_PROPERTIES_PATH=runtime-module-sample/src/main/resources/agent-evidence-runtime-noop.properties \
runtime-module-sample/run-startup-smoke.sh
```

Override exporter from `JAVA_OPTS`:

```bash
cd /Users/zhangbin/GitHub/agent-evidence-edc-java-spike/spikes/edc-java-extension
JAVA_OPTS="-Dedc.agent-evidence.exporter.type=noop -Dedc.agent-evidence.output-dir=./runtime-module-sample/override-output" \
runtime-module-sample/run-startup-smoke.sh
```

## 对应验证

当前 runtime module tests 会直接验证：

- sample properties 能否被读取
- exporter type 是否正确流到 extension
- publish 真实 control-plane payload 后：
  - `filesystem` 会写出 fragments
  - `noop` 不写文件

这一步只验证 runtime-facing exporter handoff，不扩新的 exporter、事件面或 connector 行为。
