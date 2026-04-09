# Pass/Fail Matrix

以下矩阵来自实际运行：

```text
| file | reference | reference labels | independent | independent labels |
| --- | --- | --- | --- | --- |
| `examples/minimal-valid-evidence.json` | PASS | - | PASS | - |
| `examples/valid-retention-review-evidence.json` | PASS | - | PASS | - |
| `examples/invalid-missing-required.json` | FAIL | schema_violation | FAIL | missing_validation_declaration |
| `examples/invalid-unclosed-reference.json` | FAIL | unresolved_output_ref | FAIL | broken_evidence_continuity |
| `examples/invalid-policy-link-broken.json` | FAIL | unresolved_evidence_policy_ref | FAIL | broken_policy_linkage |
| `examples/invalid-provenance-output-mismatch.json` | FAIL | provenance_output_refs_mismatch | FAIL | broken_evidence_continuity |
| `examples/invalid-validation-provenance-link-broken.json` | FAIL | unresolved_validation_provenance_ref | FAIL | broken_evidence_continuity |
| `paper/flagship/assets/specimens/scenario_03_access_decision_valid.json` | PASS | - | PASS | - |
| `paper/flagship/assets/specimens/scenario_03_access_decision_invalid_missing_policy_linkage.json` | FAIL | unresolved_policy_ref | FAIL | broken_policy_linkage |
| `paper/flagship/assets/specimens/scenario_04_object_derivation_handoff_valid.json` | PASS | - | PASS | - |
| `paper/flagship/assets/specimens/scenario_04_object_derivation_handoff_invalid_broken_evidence_continuity.json` | FAIL | unresolved_output_ref | FAIL | broken_evidence_continuity |
| `paper/flagship/assets/specimens/scenario_05_failed_or_denied_operation_valid.json` | PASS | - | PASS | - |
| `paper/flagship/assets/specimens/scenario_05_failed_or_denied_operation_invalid_missing_outcome.json` | FAIL | schema_violation | FAIL | missing_outcome_presence |
| `paper/flagship/assets/specimens/scenario_06_missing_identity_binding_invalid.json` | FAIL | unresolved_actor_ref | FAIL | broken_identity_binding |
| `paper/flagship/assets/specimens/scenario_07_temporal_inconsistency_invalid.json` | PASS | - | FAIL | temporal_inconsistency |
| `paper/flagship/assets/specimens/scenario_08_implementation_coupled_evidence_invalid.json` | PASS | - | FAIL | implementation_coupling_marker |
| `paper/flagship/assets/specimens/scenario_09_missing_target_binding_invalid.json` | FAIL | unresolved_subject_ref | FAIL | broken_target_binding |
| `paper/flagship/assets/specimens/scenario_10_ambiguous_operation_semantics_invalid.json` | PASS | - | FAIL | ambiguous_operation_semantics |
| `paper/flagship/assets/specimens/scenario_11_outcome_unverifiability_invalid.json` | PASS | - | FAIL | outcome_unverifiable |
```

## Immediate Reading

- 当前 matrix 覆盖 19-file corpus
- 其中 15 个文件保持 pass/fail 对齐
- 4 个文件出现真实 pass/fail divergence：
  - `scenario_07_temporal_inconsistency_invalid.json`
  - `scenario_08_implementation_coupled_evidence_invalid.json`
  - `scenario_10_ambiguous_operation_semantics_invalid.json`
  - `scenario_11_outcome_unverifiability_invalid.json`

对应的 machine-readable freeze 见：

- `paper/flagship/assets/run_archive/json/reference_validator_results.json`
- `paper/flagship/assets/run_archive/json/independent_checker_results.json`
- `paper/flagship/assets/run_archive/json/comparison_matrix.json`

## Why This Matters

这个矩阵现在已经不只是“第二个 checker 也能跑”。它已经能诚实展示：

- 哪些 failure surfaces 已被 current reference validator 覆盖
- 哪些 failure surfaces 当前只被 independent checker 显式命名并拒绝
- 哪些差异只是 label abstraction level 不同
