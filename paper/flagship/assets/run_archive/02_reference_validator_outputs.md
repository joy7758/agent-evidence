# Reference Validator Outputs

## Earlier Direct-Failure Batch Retained in the Archive

```text
paper/flagship/assets/specimens/scenario_06_missing_identity_binding_invalid.json FAIL unresolved_actor_ref
paper/flagship/assets/specimens/scenario_07_temporal_inconsistency_invalid.json PASS -
paper/flagship/assets/specimens/scenario_08_implementation_coupled_evidence_invalid.json PASS -
```

## Newly Run in the Current Freeze

```text
paper/flagship/assets/specimens/scenario_09_missing_target_binding_invalid.json FAIL unresolved_subject_ref
paper/flagship/assets/specimens/scenario_10_ambiguous_operation_semantics_invalid.json PASS -
paper/flagship/assets/specimens/scenario_11_outcome_unverifiability_invalid.json PASS -
```

## Reading

- `scenario_09` 被 reference validator 拒绝，主 code 为 `unresolved_subject_ref`
- `scenario_10` 被 reference validator 接受，当前未触发 operation-semantics rule
- `scenario_11` 被 reference validator 接受，当前未触发 outcome-verifiability rule

## What This Means

reference validator 当前仍然主要覆盖：

- schema
- reference closure
- cross-field consistency
- integrity recomputation

在当前 direct failure set 中，它仍然没有把以下 boundary classes 纳入当前 rule surface：

- temporal inconsistency
- implementation-coupled evidence
- ambiguous operation semantics
- stronger outcome unverifiability
