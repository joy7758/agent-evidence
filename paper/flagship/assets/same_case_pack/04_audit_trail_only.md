# Audit-Trail-Only Representation

## Sample Representation

```text
audit_entry_id: audit:retention-review-001
actor: retention-reviewer
subject: dataset-package-042
action: retention.review
ticket: retention-ticket-042
decision: retained-with-restrictions
policy_version: retention-review-v1
recorded_by: internal-review-service
recorded_at: 2026-03-31T00:00:04Z
```

## What It Supports

- 可以保留较完整的审计记录
- 可以看出 actor、subject、action、ticket、decision、policy_version
- 比普通 logs 更接近 accountability 叙述

## What It Cannot Conclude Alone

- 输入输出 refs 是否严格闭合
- evidence artifact 与 object digest 是否形成最小 continuity
- validation path 是否明确
- 离开原审计系统语义后能否做局部独立检查

## Why It Is Insufficient Alone

它更像内部审计保留面，而不是一个最小、portable、checker-facing statement。
