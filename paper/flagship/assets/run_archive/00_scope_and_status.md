# Scope and Status

## Scope

当前 run archive 的冻结目标有三件事：

1. 保留新增 direct failure specimens 的真实运行结果
2. 刷新 broader flagship corpus 的双 checker pass/fail matrix
3. 为主文 validation section 与 appendix text 提供可追溯的 reviewer-facing 依据，并冻结 machine-readable result files

## Actually Run in This Archive State

### Earlier direct-failure batch already preserved

- `scenario_06_missing_identity_binding_invalid.json`
- `scenario_07_temporal_inconsistency_invalid.json`
- `scenario_08_implementation_coupled_evidence_invalid.json`

### Newly run in the current freeze

- `scenario_09_missing_target_binding_invalid.json`
- `scenario_10_ambiguous_operation_semantics_invalid.json`
- `scenario_11_outcome_unverifiability_invalid.json`

### Refreshed broader comparison

- `paper/flagship/prototype/independent_checker/compare_checkers.py`
- broader corpus 当前覆盖 19 个文件

### Machine-readable freeze derived from the current archive state

- `paper/flagship/assets/run_archive/json/reference_validator_results.json`
- `paper/flagship/assets/run_archive/json/independent_checker_results.json`
- `paper/flagship/assets/run_archive/json/comparison_matrix.json`

## Not Yet Run in This Archive

- 第三方 checker
- repo 外场景或外部 corpus
- same-case pack 中 weaker representations 的 machine validation

说明：

- same-case pack 里只有 `05_boundary_based_accountability.json` 属于 OAP-style JSON，可被 checker 直接处理。
- `logs-only / provenance-only / policy-only / audit-trail-only` 本来就是 intentionally incomplete representations，不属于 checker input。

## Current Status

当前 run archive 已经是 reviewer-facing，但仍然是 partial reviewer-facing package。

理由很具体：

- 已有真实命令
- 已有真实输出
- 已有真实 pass/fail matrix
- 已有 4 类真实 pass/fail divergence

但仍缺：

- third-party checker
- 外部语境 corpus
- 更细粒度的 raw stage-level archival
