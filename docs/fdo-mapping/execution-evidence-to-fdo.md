# Execution Evidence to FDO

Historical note: this document preserves older FDO-mapping wording from the
`Execution Evidence Object` line. It is supporting lineage material, not the
current primary repository entry.

**English**  Execution Evidence to FDO
**中文**  执行证据到 FDO 的映射。

## Key Message / 核心说明

**English**  An execution evidence bundle can be interpreted as a digital object shell plus a bounded evidence payload.
**中文**  一个执行证据包可以被解释为“数字对象外壳 + 有边界的证据载荷”。

## Evidence Bundle Identity / 证据包身份
- **EN**: Identity comes from `object_type`, `run_id`, `agent_framework`, and integrity fields.
- **中文**：身份来自 `object_type`、`run_id`、`agent_framework` 和完整性字段。

## Persistent Identifier Placeholder / 持久标识占位
- **EN**: The current placeholder is `pid:pending/execution-evidence-object/<run_id>`.
- **中文**：当前占位符是 `pid:pending/execution-evidence-object/<run_id>`。

## Metadata Layer / 元数据层
- **EN**: Metadata comes from context, timestamp, framework, and step summary.
- **中文**：元数据来自上下文、时间戳、框架信息和步骤摘要。

## Integrity Layer / 完整性层
- **EN**: `action_hash`, `trace_hash`, and `proof_hash` form the integrity layer.
- **中文**：`action_hash`、`trace_hash` 和 `proof_hash` 构成完整性层。

## Provenance Reference / 来源引用
- **EN**: Runtime origin and agent identity form the provenance-oriented surface.
- **中文**：运行来源和 agent 身份构成来源导向表面。

## Diagram Description / 图示说明
- **EN**: Agent Run → Evidence Bundle → Digital Object → FDO Registry.
- **中文**：Agent Run → Evidence Bundle → Digital Object → FDO Registry。
