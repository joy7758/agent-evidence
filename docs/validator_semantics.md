# Validator Semantics For Representative SE Workflow Cases

This document describes the Phase 30 prototype semantics. It is not a publication claim and does not make TSE v3 ready.

## Stage Boundary

The prototype keeps three layers separate:

- core profile validator: existing `agent-evidence validate-profile`;
- case adapter/checker: case-specific semantics for representative SE workflow fixtures;
- baseline runners: schema-only, log-only, and policy-only comparisons.

## Core Stages

| Stage | Prototype meaning |
|---|---|
| Schema/profile identity | The statement satisfies the current operation-accountability JSON Schema and profile identity. |
| Local reference closure | Operation, evidence, provenance, policy, and validation refs resolve inside the local statement. |
| Policy/evidence linkage | Evidence and validation point to the declared policy object. |
| Provenance/output consistency | Provenance input/output refs match the operation refs. |
| Validation/provenance closure | The validation object closes over the provenance object. |
| Integrity/digest consistency | The statement, reference, and artifact digests match canonical recomputation. |
| Report generation | The runner writes deterministic report JSON and markdown summaries. |

## Case-Level Semantic Checks

| Code | Case | Meaning |
|---|---|---|
| `invalid_label_transition` | issue / PR metadata | The output label is not allowed by the triage policy. |
| `stale_source_digest` | doc/data transform | The generated output names a source digest that does not match the source artifact. |
| `test_summary_count_mismatch` | test-result summary | The summary counts do not match the raw test result. |
| `policy_threshold_violation` | test-result summary | The summary violates the local failed-test threshold. |

## Primary Error Tie-Breaking

The runner uses this order:

1. core profile validator primary error, if present;
2. first case-semantic issue, if the core profile report passes;
3. `null` for a valid case.

## Soundness Boundary

A passing result establishes only that the local fixture package satisfies the represented profile and case-adapter checks. It does not establish deployment robustness, legal sufficiency, industrial validation, or broad empirical generalization.

## Completeness Boundary

The prototype checks selected representative fixtures and controlled invalid variants only. It is not exhaustive.
