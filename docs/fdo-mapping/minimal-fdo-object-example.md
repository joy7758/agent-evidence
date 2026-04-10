# Minimal FDO-style Object Example

Historical note: this example preserves older FDO-style wrapper wording from
the `Execution Evidence Object` line. It is supporting lineage material, not
the current primary repository entry.

**English**  Minimal FDO-style Object Example
**中文**  最小 FDO 风格对象示例。

## Key Message / 核心说明

**English**  The FDO-style example keeps the verified evidence payload inside a wrapper with identity, integrity, and provenance.
**中文**  这个 FDO 风格示例把已验证的证据载荷放进一个带身份、完整性和来源信息的外壳里。

## What Comes from the Evidence Object / 哪些部分来自证据对象
- **EN**: The embedded payload contributes steps, context, framework, hashes, and timestamp.
- **中文**：内嵌载荷提供步骤、上下文、框架、哈希和时间戳。

## What Represents FDO-style Identity / 哪些部分代表 FDO 风格身份
- **EN**: `object_id`, `object_type`, `pid_placeholder`, and `metadata` are the outer identity layer.
- **中文**：`object_id`、`object_type`、`pid_placeholder` 和 `metadata` 是外层身份层。

## What Represents Integrity and Provenance / 哪些部分代表完整性和来源
- **EN**: `integrity.*` carries hash material, and `provenance.*` carries runtime origin.
- **中文**：`integrity.*` 承载哈希材料，`provenance.*` 承载运行来源。
