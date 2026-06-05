# EEOAP Clauses

This file defines the initial stable clause set for the Execution Evidence and
Operation Accountability Profile.

Agents should cite these clause IDs in implementation notes, task summaries,
and pull-request summaries when a change affects the profile boundary.

## EEOAP-001

Clause ID: `EEOAP-001`

Requirement: Completed operation must produce an operation accountability
statement.

Rationale: A completed operation needs a compact statement that can be reviewed
outside the original runtime.

Related files:

- `spec/execution-evidence-operation-accountability-profile-v0.1.md`
- `schema/execution-evidence-operation-accountability-profile-v0.1.schema.json`
- `examples/minimal-valid-evidence.json`

Validator surface: schema and profile validation.

Out-of-scope note: This clause does not prove that every underlying event is
externally true.

## EEOAP-002

Clause ID: `EEOAP-002`

Requirement: Statement must bind actor, subject, operation, and timestamp.

Rationale: Reviewers and agents need stable identity, target, action, and time
fields before they can evaluate the operation statement.

Related files:

- `schema/execution-evidence-operation-accountability-profile-v0.1.schema.json`
- `examples/minimal-valid-evidence.json`

Validator surface: schema validation.

Out-of-scope note: This clause does not provide external identity attestation or
trusted timestamping.

## EEOAP-003

Clause ID: `EEOAP-003`

Requirement: Statement must bind policy, evidence, and provenance references.

Rationale: Reviewable evidence needs explicit links between the operation,
governing policy, supporting evidence, and provenance records.

Related files:

- `schema/execution-evidence-operation-accountability-profile-v0.1.schema.json`
- `examples/minimal-valid-evidence.json`
- `examples/invalid-unclosed-reference.json`
- `examples/invalid-policy-link-broken.json`

Validator surface: reference and consistency validation.

Out-of-scope note: This clause does not make the linked policy authoritative or
the evidence externally certified.

## EEOAP-004

Clause ID: `EEOAP-004`

Requirement: Statement must produce or reference a validator-readable
validation report.

Rationale: A downstream agent or reviewer should be able to inspect a
machine-readable validation result instead of relying only on narrative logs.

Related files:

- `docs/REPRODUCE_PAPER_MINIMAL.md`
- `demo/run_operation_accountability_demo.py`
- `scripts/reproduce_paper_minimal.sh`

Validator surface: validation-report output.

Out-of-scope note: Passing validation does not prove deployment robustness,
legal compliance, or publication status.

## EEOAP-005

Clause ID: `EEOAP-005`

Requirement: Implementation changes must cite affected EEOAP clauses in task or
pull-request summaries.

Rationale: Stable clause citations let coding agents, reviewers, and future
retrieval agents connect code changes to protocol requirements.

Related files:

- `.github/pull_request_template.md`
- `scripts/check_protocol_citations.py`
- `protocol/clause-index.json`

Validator surface: local clause-citation check.

Out-of-scope note: Clause citation is a repository workflow rule, not evidence
of external review or acceptance.
