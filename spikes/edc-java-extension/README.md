# EDC Java Extension Skeleton Spike

## 结论先行

这是一份 `agent-evidence` 的 EDC control-plane augmentation skeleton。

它不是 connector 产品，不是 EDC 替代品，也不是一个新的 dataspace 平台。

这轮的目标只有一个：验证 `ServiceExtension` + `EventRouter` 这条最小 Java
接入骨架是否顺手，是否足够承载后续的 control-plane event -> evidence
fragment 导出路径。

## 为什么先做 `ServiceExtension` + `EventRouter`

因为这是 EDC 官方当前最稳的扩展面：

- Extension Model 文档明确写了，注册一个 extension module 需要
  `ServiceExtension`、provider file 和 runtime `runtimeOnly(...)` 集成。
- Service Layers 文档明确写了，控制面事件通过 `EventRouter` 暴露，既支持
  sync listener，也支持 async listener。
- control plane 已经覆盖 catalog、contract agreement、transfer governance，
  而 data transfer 本身并不在 control plane 内完成。

这意味着第一轮最值得验证的，不是 persistence 或 data plane，而是：

- Java extension 能不能清楚接进 control-plane events
- event family 能不能清楚映射成 `agent-evidence` semantic evidence
- Java 侧能不能只导出中间 evidence fragment，而不把 Python validator 逻辑搬过来

## 这轮验证什么

- Java 17 下的最小 Gradle extension module 结构
- provider file 的放置方式
- Java 侧最小职责分解：
  - extension entry
  - subscriber
  - mapper
  - grouping strategy
  - file-system writer
- bundle grouping key 以 `transfer_process_id` 为主的接口表达
- `contract_agreement_id` 作为 transfer 出现前 staging correlation key 的表达

## 这轮不验证什么

- 不验证完整 connector 运行
- 不验证 persistence 改造
- 不验证 data plane / provisioner
- 不验证生产级文件格式
- 不验证签名、anchor、独立 verifier 下沉到 Java
- 不验证完整 EDC 版本锁定和依赖矩阵

## Java 侧与 Python `agent-evidence` 侧分工

### Java extension 侧

- 监听 control-plane events
- 保留 envelope metadata 与最小领域 id
- 做两级去重入口
- 把 EDC event family 映射成 semantic evidence fragment
- 把 fragment 导出成可交给外部处理的中间产物

### Python `agent-evidence` 侧

- evidence profile 主线定义
- schema / validator
- manifest / digest / signing / anchor 逻辑
- demo、examples、CLI 和独立验证结果输出

## 这轮参考的仓库内文档

- [EDC augmentation boundary](../../docs/edc/EDC_AUGMENTATION_BOUNDARY.md)
- [Control-plane event extension sketch](../../docs/edc/edc_control_plane_event_extension_sketch.md)
- [Event to evidence mapping](../../docs/edc/edc_event_to_evidence_mapping.md)
- [Extension minimal structure](../../docs/edc/edc_extension_minimal_structure.md)

## 目录说明

- `settings.gradle.kts`
- `build.gradle.kts`
- `gradle.properties`
- `BOUNDARY.md`
- `EVENT_SCOPE.md`
- `src/main/java/...`
- `src/main/resources/META-INF/services/org.eclipse.edc.spi.system.ServiceExtension`

## 环境与验证说明

这份 spike 默认按 Java 17 起手，和 EDC 官方 Samples 当前 README 的前提一致。

本地这次已经补齐 Java 17 与 Gradle，并完成了最小构建验证：

- `gradle wrapper`
- `./gradlew tasks --all`
- `./gradlew compileJava`
- `./gradlew test`

因此，这一轮的结论更新为：

- 目录结构、provider file、类职责、边界和事件范围已经固化
- build 文件已经收敛到 compile-capable spike，并带最小轻量测试
- 轻量测试已经不再依赖自定义假事件，而是直接使用 EDC control-plane event builders 组装真实 payload
- 最小事件范围的 10 个 control-plane event 已全部进入 real-payload 映射测试
- `FileSystemEvidenceEnvelopeWriter` 与 `subscriber -> writer` 的导出契约已经进入最小文件输出验证
- `AgentEvidenceEdcExtension` 的 `EventRouter` 注册与导出目录 handoff 已进入 smoke test 验证
- `ServiceExtension -> EventRouter subscriber -> mapper -> grouping -> writer` 这条 Java 接入链在编译期与最小测试层面已经站住
- 这仍然不是 connector 产品，也还没有验证真实 runtime 部署、persistence 或 data plane

## 官方参考

- EDC Extension Model
  [https://eclipse-edc.github.io/documentation/for-contributors/runtime/extension-model/](https://eclipse-edc.github.io/documentation/for-contributors/runtime/extension-model/)

- EDC Service Layers / events and callbacks
  [https://eclipse-edc.github.io/documentation/for-contributors/runtime/service-layers/](https://eclipse-edc.github.io/documentation/for-contributors/runtime/service-layers/)

- EDC Control Plane
  [https://eclipse-edc.github.io/documentation/for-adopters/control-plane/](https://eclipse-edc.github.io/documentation/for-adopters/control-plane/)

- EDC Samples
  [https://github.com/eclipse-edc/Samples](https://github.com/eclipse-edc/Samples)
