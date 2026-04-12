# Upstream Handoff Note

## What This Spike Validates

这条 spike 只验证一件事：`agent-evidence` 是否可以作为 EDC control plane 上的一层 execution-evidence augmentation layer 接入，而不把自己做成 EDC 本体。

验证范围集中在：

- control-plane event observation
- semantic mapping
- grouping / dedup
- exporter handoff
- minimal runtime wiring
- startup smoke and failure behavior

This spike validates that agent-evidence can sit as an execution-evidence augmentation layer on the EDC control plane without becoming an EDC product line.

## What This Spike Is Not

这条 spike 不是：

- 一个新的 EDC connector 产品
- 一个 dataspace platform
- 一个 data plane implementation
- 一个 persistence rework
- 一个 Java-side signing / verification / anchor stack

它也不主张修改 EDC 的主线职责边界。这里验证的是一种尽量薄的 augmentation path。

## Relationship To The Python `agent-evidence` Package

Java spike 和 Python 主包是刻意分层的：

- Java 侧负责从 EDC control-plane events 中提取最小 evidence fragments，并把它们稳定导出。
- Python `agent-evidence` 主包继续负责 profile、validator、manifest、signing、anchor 和 independent verification 相关能力。

这意味着 Java 侧不是主产品，而是面向 EDC 场景的接入层。

## Why It Should Stop Here For Now

到当前为止，这条 spike 已经回答了最值得回答的问题：augmentation layer 能不能站住。

再继续往下扩，最容易发生的不是“把结论变得更强”，而是把 scope 推向 runtime 细节、connector 装配和产品化维护面。对当前目标来说，这个方向收益不高。

## Best Continuation Path

当前最合适的继续方式不是继续加 Java 功能，而是：

- 先把这条 spike 整理成主仓可见入口，便于仓库读者、协作者和后续 issue / PR 直接引用。
- 如果需要对外同步，再基于当前 freeze package 整理一份克制的 note，而不是把 spike 说成“已完成集成”。
