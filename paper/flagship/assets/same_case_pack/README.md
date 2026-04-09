# Same-Case Pack

## 用途

这组文件把一个固定 case 用五种不同表示方式展开：

- logs-only
- provenance-only
- policy-only
- audit-trail-only
- boundary-based accountability statement

目的不是证明替代物“没用”，而是让 reviewer 直接看到：它们能支持什么，不能单独推出什么，以及为什么 boundary-based statement 才能完整回答 single-operation accountability 问题。

## 固定 case

本 pack 统一使用 `retention review` 作为底层 case。

原因：

- 当前 repo 已有最稳的 decision-style anchor：
  - `examples/valid-retention-review-evidence.json`
- 它同时具备：
  - 双输入
  - 单 decision output
  - 明确 policy basis
  - 可复核 artifact

## 文件说明

- `00_case_description.md`：固定 case 说明
- `01_logs_only.md`：logs-only 表示
- `02_provenance_only.md`：provenance-only 表示
- `03_policy_only.md`：policy-only 表示
- `04_audit_trail_only.md`：audit-trail-only 表示
- `05_boundary_based_accountability.json`：OAP-style boundary 表示
- `06_unprovable_points_matrix.md`：弱表示下仍不可证明的点

## 注意

这组文件是 reviewer-facing comparison assets，不是 empirical superiority study，也不是 benchmark artifact。
