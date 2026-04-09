# Divergence Notes

## Real Pass/Fail Divergences

### Temporal Inconsistency

- file:
  - `scenario_07_temporal_inconsistency_invalid.json`
- reference validator:
  - `PASS`
- independent checker:
  - `FAIL` with `temporal_inconsistency`

含义：

- current reference validator 尚未覆盖 temporal consistency
- independent checker 已将其视为 minimal boundary sanity condition

### Implementation-Coupled Evidence

- file:
  - `scenario_08_implementation_coupled_evidence_invalid.json`
- reference validator:
  - `PASS`
- independent checker:
  - `FAIL` with `implementation_coupling_marker`

含义：

- current reference validator 尚未覆盖 implementation-coupling / portability 风险
- independent checker 已将其视为 boundary warning surface

### Ambiguous Operation Semantics

- file:
  - `scenario_10_ambiguous_operation_semantics_invalid.json`
- reference validator:
  - `PASS`
- independent checker:
  - `FAIL` with `ambiguous_operation_semantics`

含义：

- current reference validator 接受了结构上完整、但语义上过泛的 operation statement
- independent checker 把 “`operation.type` 过于 generic” 当成 boundary-level failure surface

### Outcome Unverifiability

- file:
  - `scenario_11_outcome_unverifiability_invalid.json`
- reference validator:
  - `PASS`
- independent checker:
  - `FAIL` with `outcome_unverifiable`

含义：

- current reference validator 可以接受 “成功声明 + output ref 存在” 这个结构
- independent checker 进一步要求 outcome 至少能指向一个可区分的 output object

## Still-Aligned but Differently Named

### Missing Identity Binding

- file:
  - `scenario_06_missing_identity_binding_invalid.json`
- reference validator:
  - `FAIL` with `unresolved_actor_ref`
- independent checker:
  - `FAIL` with `broken_identity_binding`

### Missing Target Binding

- file:
  - `scenario_09_missing_target_binding_invalid.json`
- reference validator:
  - `FAIL` with `unresolved_subject_ref`
- independent checker:
  - `FAIL` with `broken_target_binding`

含义：

- 这两类目前没有 pass/fail divergence
- 但仍存在 label-layer divergence：
  - reference validator 更偏 staged reference-closure reading
  - independent checker 更偏 boundary-taxonomy reading

## Reviewer-Facing Interpretation

本轮最重要的 reviewer-facing 结论不是“两个 checker 全面对齐”，而是：

- 当前已经出现 4 类真实的 coverage divergence
- 这些 divergence 都不是随机噪音，而是同一个问题的不同边界读法：
  - temporal consistency
  - implementation-coupling
  - operation semantics
  - outcome verifiability

## Current Bottom Line

这个 appendix run archive 现在已经能够诚实展示：

- 哪些 failure classes 已由 reference validator 覆盖
- 哪些 failure classes 当前只被 independent checker 直接捕获
- 哪些差异只是 naming / abstraction-layer difference

补充说明：

- 当前 `json/` 目录已与 frozen markdown matrix 对齐
- 本轮未发现 markdown summary 与 machine-readable freeze 之间的结果不一致

它还不能证明：

- independent checker 一定更正确
- 当前 taxonomy 已经最终冻结
- external community implementation 已经收敛
