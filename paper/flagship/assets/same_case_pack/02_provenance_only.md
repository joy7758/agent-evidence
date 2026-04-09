# Provenance-Only Representation

## Sample Representation

```text
entity(obj:dataset-package-042)
entity(obj:retention-ticket-042)
entity(obj:retention-decision-042)
agent(actor:retention-reviewer)
activity(op:retention-review-001)
used(op:retention-review-001, obj:dataset-package-042)
used(op:retention-review-001, obj:retention-ticket-042)
wasAssociatedWith(op:retention-review-001, actor:retention-reviewer)
wasGeneratedBy(obj:retention-decision-042, op:retention-review-001)
```

## What It Supports

- 可以说明对象之间的 derivation relation
- 可以说明 actor 与 operation 的关联
- 可以说明 decision output 来源于当前 operation

## What It Cannot Conclude Alone

- governing policy 是哪一个
- 哪些 constraint 实际适用
- evidence artifact 是否足够支撑 decision
- validation method 与 validation status 是什么

## Why It Is Insufficient Alone

它擅长表达 lineage，但没有把 policy、evidence、validation 绑定进同一个可检查 statement。
