# Independent Checker Outputs

## Earlier Direct-Failure Batch Retained in the Archive

```text
FAIL paper/flagship/assets/specimens/scenario_06_missing_identity_binding_invalid.json (1 issue(s))
- [broken_identity_binding] provenance.actor_ref: provenance.actor_ref must match actor.id
FAIL paper/flagship/assets/specimens/scenario_07_temporal_inconsistency_invalid.json (1 issue(s))
- [temporal_inconsistency] timestamp: timestamp is implausibly far in the future
FAIL paper/flagship/assets/specimens/scenario_08_implementation_coupled_evidence_invalid.json (1 issue(s))
- [implementation_coupling_marker] evidence.artifacts[0].locator: value appears coupled to a local or implementation-specific environment
```

## Newly Run in the Current Freeze

```text
FAIL paper/flagship/assets/specimens/scenario_09_missing_target_binding_invalid.json (1 issue(s))
- [broken_target_binding] operation.subject_ref: operation.subject_ref must match subject.id
FAIL paper/flagship/assets/specimens/scenario_10_ambiguous_operation_semantics_invalid.json (1 issue(s))
- [ambiguous_operation_semantics] operation.type: operation.type is too generic for boundary-level review
FAIL paper/flagship/assets/specimens/scenario_11_outcome_unverifiability_invalid.json (1 issue(s))
- [outcome_unverifiable] operation.output_refs: succeeded operation does not identify any distinguishable output object
```

## Reading

- `scenario_09` 以 target-binding 视角失败
- `scenario_10` 以 operation-semantics 视角失败
- `scenario_11` 以 outcome-verifiability 视角失败

## What This Means

independent checker 当前已经把 direct failure coverage 推进到 6 个类：

- identity binding
- target binding
- temporal consistency
- implementation coupling
- operation semantics
- outcome unverifiability

其中后四类当前都还没有被 reference validator 显式接住。
