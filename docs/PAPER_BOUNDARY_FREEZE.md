# Paper Boundary Freeze

This document freezes the paper-facing boundary for the current minimal
operation-accountability path in `agent-evidence`.

## Frozen Object

The paper studies one `operation accountability statement`.

The paper-facing object is a single JSON statement that binds:

- `profile`
- `statement_id`
- `timestamp`
- `actor`
- `subject`
- `operation`
- `policy`
- `constraints`
- `provenance`
- `evidence`
- `validation`

The paper does not study a full workflow graph, multi-agent conversation, agent
registry, runtime platform, or governance platform.

## Frozen Profile

The paper introduces only:

`Execution Evidence and Operation Accountability Profile v0.1`

The profile is used as a small, reviewable boundary for independently
checkable execution evidence. It is not an official FDO standard and is not a
general provenance model.

## Frozen Validator Path

The paper evaluates one `profile-aware validator` path:

1. `schema conformance`
2. `reference closure`
3. `cross-field consistency`
4. `integrity digest recomputation`

This path is exposed through:

```bash
agent-evidence validate-profile <profile-json>
```

## Frozen Evidence Set

The paper-minimal path uses exactly:

- 1 valid example: `examples/minimal-valid-evidence.json`
- 3 controlled invalid examples:
  - `examples/invalid-missing-required.json`
  - `examples/invalid-unclosed-reference.json`
  - `examples/invalid-policy-link-broken.json`
- 1 metadata-enrichment demo: `demo/run_operation_accountability_demo.py`

The controlled invalid examples ground three representative failure codes:

- `schema_violation`
- `unresolved_output_ref`
- `unresolved_evidence_policy_ref`

## Non-Claims

The paper does not claim:

- registry design
- multi-agent orchestration
- full FDO interoperability
- legal non-repudiation
- production deployment
- broad governance platform
- compliance approval
- semantic correctness of AI output
- complete cryptographic trust fabric

## Out-of-Scope Lines

The following lines are preserved in the repository for research continuity but
are not part of this frozen paper-minimal path:

- AEP-Media
- AI Act
- Sovereign-pFDO
- new runtime integrations
- full-repository refactors
- broad platform narratives

## Review Rule

Any future change that broadens the paper-facing claim must first update this
boundary document and the minimal rerun path. Until then, the paper-facing core
stays bounded to one statement, one profile, one validator path, one valid
example, three invalid examples, one demo, and one review package.
