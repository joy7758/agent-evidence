# EEOAP v0.1 Public-Facing Research Specification

Affected clauses: EEOAP-001, EEOAP-002, EEOAP-003, EEOAP-004, EEOAP-005.

Status: research specification artifact for local review. This document does
not claim standards-body adoption, external certification, legal compliance,
production deployment proof, or publication status.

## Definition

Execution Evidence and Operation Accountability Profile (EEOAP) v0.1 is a
bounded research abstraction for representing a completed software or agent
operation as a reviewable evidence statement. It binds an operation identifier,
actor, subject, timestamp, policy reference, provenance links, evidence
artifacts, integrity digests, and a validator-readable result so that a
reviewer or coding agent can inspect the operation outside the original
runtime.

## Operational Semantics

An EEOAP statement is emitted after an operation or trace-derived conversion
has completed. The statement does four things:

1. Names the operation and the object being reviewed.
2. Binds the operation to local policy, provenance, and evidence references.
3. Records integrity digests for referenced inputs, outputs, and artifacts.
4. Provides a validation surface through `agent-evidence validate-profile`.

An EEOAP statement does not prove that the underlying external event is true,
that a policy is legally authoritative, that a timestamp is trusted, or that a
system is production-ready. It is a local reviewability layer, not a legal or
standards certification layer.

## Trace Binding Rule

For an OpenTelemetry OTLP JSON trace, the adapter applies this mapping:

| OTLP field or artifact | EEOAP target | Rule |
| --- | --- | --- |
| Raw OTLP JSON file | `subject.digest` and input evidence digest | Canonical JSON digest binds the trace input. |
| `traceId` | `subject.id`, `statement_id`, and operation suffix | The trace identifier anchors the converted operation statement. |
| `spanId` / `parentSpanId` | `spans[]` and derived evidence metadata | Span identifiers are preserved for reviewer inspection. |
| `startTimeUnixNano` | `timestamp` | Earliest selected span start becomes the statement timestamp. |
| Conversion output | output evidence reference | The generated EEOAP statement is recorded as the conversion output. |
| Local validator result | `validation` | The statement is checked by schema, reference, consistency, and integrity stages. |

This mapping is implemented by `scripts/convert_otel_trace_to_eeoap.py`.

## Invariants

The following invariants must always hold for a valid local EEOAP statement:

- `operation.subject_ref` resolves to `subject.id`.
- `operation.policy_ref` resolves to `policy.id`.
- `policy.constraint_refs[]` resolves to declared `constraints[].id` values.
- `operation.input_refs[]` and `operation.output_refs[]` resolve to
  `evidence.references[].ref_id` values.
- `provenance.actor_ref`, `provenance.operation_ref`, and
  `provenance.subject_ref` resolve to the same actor, operation, and subject
  used by the statement.
- `evidence.subject_ref`, `evidence.operation_ref`, and `evidence.policy_ref`
  remain consistent with subject, operation, and policy sections.
- `validation.evidence_ref`, `validation.provenance_ref`, and
  `validation.policy_ref` resolve to local statement components.
- `evidence.integrity.references_digest`, `artifacts_digest`, and
  `statement_digest` match canonical recomputation.
- For an OTLP conversion, the raw trace digest is retained as an input evidence
  digest and at least one span identifier is visible in the trace-grounding
  record.

## Non-Goals

EEOAP v0.1 is not:

- a new telemetry standard;
- an official FDO or standards-body specification;
- a legal non-repudiation system;
- a compliance certification mechanism;
- a trusted timestamping layer;
- a production forensic authenticity system;
- a deployment robustness proof;
- a hosted API, remote MCP service, or decision system.

## Versioning Policy

`v0.1` is the first repository-local research specification version. Compatible
changes may add examples, diagrams, explanatory text, or experiment receipts
without changing the version. Any change that removes required fields, changes
field semantics, weakens validation invariants, or changes the trace-binding
rule requires a new versioned schema path and a new version note.

The current related files are:

- `schema/execution-evidence-operation-accountability-profile-v0.1.schema.json`
- `specs/eeoap/v0.1/eeoap.schema.json`
- `docs/specs/EEOAP_v0_1.md`
- `protocol/clause-index.json`

## Example With Real Trace

Input trace:

```text
data/otel/raw_demo_trace.json
```

Trace provenance:

```text
data/otel/trace_provenance_record.json
```

Selected span:

```json
{
  "traceId": "5B8EFFF798038103D269B633813FC60C",
  "spanId": "EEE19B7EC3C1B174",
  "parentSpanId": "EEE19B7EC3C1B173",
  "name": "I'm a server span",
  "startTimeUnixNano": "1544712660000000000",
  "endTimeUnixNano": "1544712661000000000",
  "kind": 2
}
```

Generated statement:

```text
data/eeoap/real_trace_evidence.json
```

Validation command:

```bash
.venv/bin/agent-evidence validate-profile data/eeoap/real_trace_evidence.json
```

Expected local result:

```text
ok=true
issue_count=0
```

This example is a public trace-format grounding fixture. It is not production
telemetry and does not establish external validation of the EEOAP abstraction.
