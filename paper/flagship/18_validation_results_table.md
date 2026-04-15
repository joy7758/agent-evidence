# Validation Results Table

这张表是 reviewer-facing 的简明结果截面。它只汇总旗舰包新增的 specimen slice；完整 19-file corpus 仍以 `paper/flagship/assets/run_archive/04_pass_fail_matrix.md` 为准，对应的 machine-readable mirror 见 `paper/flagship/assets/run_archive/json/comparison_matrix.json`。其中 `agreement` 指 pass/fail 一致，`boundary-level divergence` 指差异直接落在 verification boundary 的覆盖面上，而不是随机实现噪音。

下面的主表仍然是 canonical flagship validation slice。其后的 supplementary note 和 rows 只用于接入 paper-facing supporting evidence，not counted in canonical B1 minimal-frozen rows.

| specimen/scenario | intended class | reference validator | independent checker | agreement/divergence note |
| --- | --- | --- | --- | --- |
| `scenario_03_access_decision_valid.json` | valid scenario anchor | PASS | PASS | agreement |
| `scenario_03_access_decision_invalid_missing_policy_linkage.json` | broken policy linkage | FAIL (`unresolved_policy_ref`) | FAIL (`broken_policy_linkage`) | agreement, label-layer difference |
| `scenario_04_object_derivation_handoff_valid.json` | valid scenario anchor | PASS | PASS | agreement |
| `scenario_04_object_derivation_handoff_invalid_broken_evidence_continuity.json` | broken evidence continuity | FAIL (`unresolved_output_ref`) | FAIL (`broken_evidence_continuity`) | agreement, label-layer difference |
| `scenario_05_failed_or_denied_operation_valid.json` | valid scenario anchor | PASS | PASS | agreement |
| `scenario_05_failed_or_denied_operation_invalid_missing_outcome.json` | missing outcome | FAIL (`schema_violation`) | FAIL (`missing_outcome_presence`) | agreement, label-layer difference |
| `scenario_06_missing_identity_binding_invalid.json` | missing/broken identity binding | FAIL (`unresolved_actor_ref`) | FAIL (`broken_identity_binding`) | agreement, label-layer difference |
| `scenario_07_temporal_inconsistency_invalid.json` | temporal inconsistency | PASS | FAIL (`temporal_inconsistency`) | boundary-level divergence |
| `scenario_08_implementation_coupled_evidence_invalid.json` | implementation-coupled evidence | PASS | FAIL (`implementation_coupling_marker`) | boundary-level divergence |
| `scenario_09_missing_target_binding_invalid.json` | missing/broken target binding | FAIL (`unresolved_subject_ref`) | FAIL (`broken_target_binding`) | agreement, label-layer difference |
| `scenario_10_ambiguous_operation_semantics_invalid.json` | ambiguous operation semantics | PASS | FAIL (`ambiguous_operation_semantics`) | boundary-level divergence |
| `scenario_11_outcome_unverifiability_invalid.json` | outcome unverifiability | PASS | FAIL (`outcome_unverifiable`) | boundary-level divergence |

## Supplementary B1 Supporting Rows

These rows are supplementary, paper-facing, and not counted in canonical B1 minimal-frozen counts.

| supplementary item | checker path | result | note |
| --- | --- | --- | --- |
| `external_context/data_space_metadata_update.valid.json` | current validator path | PASS (`ok=true`) | supplementary external-context evidence beyond the original minimal example family |
| `examples/minimal-valid-evidence.json` | repo-local second checker | PASS (`ok=true`) | supplementary checker surface, canonical valid anchor |
| `examples/invalid-unclosed-reference.json` | repo-local second checker | FAIL (`ok=false`) | supplementary checker surface, canonical invalid anchor |
| `external_context/data_space_metadata_update.valid.json` | repo-local second checker | PASS (`ok=true`) | supplementary checker surface applied to the external-context specimen |
