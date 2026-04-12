# EDC Java Spike Entry

## 结论

这条 EDC Java spike 是 `agent-evidence` 在 dataspace / EDC control-plane 场景中的 augmentation-layer validation，不是新主线，不是 EDC 产品线，也不是要把主仓改造成 Java runtime 仓库。

## 它验证了什么

它验证的是一条尽量薄的 Java 接入路径是否成立：

- control-plane event mapping
- grouping / dedup
- exporter handoff
- runtime wiring
- startup smoke
- startup failure contract
- runtime-facing exporter integration

## 为什么现在先停在 freeze package

因为这条线已经足够证明 augmentation layer 可行。

当前更有价值的是把它变成可稳定引用的资产，而不是继续往 runtime 细节上扩。继续把 spike 做宽，只会让 scope 再次膨胀。

## 为什么不直接把整条 spike 并进主功能

当前更适合把它作为 freeze package 引用，而不是把整条 Java / Gradle spike 直接并入 `main`。

原因很简单：

1. 当前目标是可见性和可引用性，不是继续扩张。
2. 这条线已经足够证明 augmentation layer 可行。
3. 继续把 spike 大量并入 `main` 会再次放大 scope，并把主仓重心从当前 Python 主包拉偏。

## 从哪里开始看

稳定冻结 tag：`edc-java-spike-freeze-v0.1`

建议阅读顺序：

1. [SPIKE_FREEZE_SUMMARY.md](https://github.com/joy7758/agent-evidence/blob/edc-java-spike-freeze-v0.1/spikes/edc-java-extension/SPIKE_FREEZE_SUMMARY.md)
2. [VALIDATED_SURFACES.md](https://github.com/joy7758/agent-evidence/blob/edc-java-spike-freeze-v0.1/spikes/edc-java-extension/VALIDATED_SURFACES.md)
3. [UPSTREAM_HANDOFF_NOTE.md](https://github.com/joy7758/agent-evidence/blob/edc-java-spike-freeze-v0.1/spikes/edc-java-extension/UPSTREAM_HANDOFF_NOTE.md)
4. [TESTING_AND_RUNBOOK.md](https://github.com/joy7758/agent-evidence/blob/edc-java-spike-freeze-v0.1/spikes/edc-java-extension/TESTING_AND_RUNBOOK.md)
5. [RUNTIME_WIRING_SAMPLE.md](https://github.com/joy7758/agent-evidence/blob/edc-java-spike-freeze-v0.1/spikes/edc-java-extension/RUNTIME_WIRING_SAMPLE.md)
6. [FAILURE_TRIAGE_RECIPE.md](https://github.com/joy7758/agent-evidence/blob/edc-java-spike-freeze-v0.1/spikes/edc-java-extension/FAILURE_TRIAGE_RECIPE.md)

## 如何使用这个入口

- 主仓读者：先看 freeze summary，再看 validated surfaces。
- 需要对外说明的人：直接引用 upstream handoff note。
- 需要复现实验的人：直接用 testing and runbook。

这里的重点是“稳定引用”，不是“继续开发这条 Java 线”。
