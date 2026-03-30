# Execution Evidence and Operation Accountability Profile v0.1

## 1. Scope

This profile defines one minimal operation accountability statement for a
single
operation executed within an FDO-based agent system.

It is intentionally narrow. It covers only:

- who executed
- which subject object was acted on
- which operation was invoked
- which policy and constraints governed the action
- how input and output objects were referenced
- what evidence and integrity material were emitted
- how a third party can verify the statement

It does not attempt to define a general registry, a full governance platform,
or a full cryptographic trust fabric.

## 2. Core Object Model

One operation accountability statement consists of the following top-level
sections:

- `profile`: fixed profile identity and version
- `statement_id`: stable identifier for the accountability statement
- `timestamp`: statement emission time
- `actor`: the executor
- `subject`: the primary object acted on
- `operation`: the action and its result
- `policy`: the governing policy
- `constraints`: the concrete rule set referenced by the policy
- `provenance`: the linkage between actor, subject, operation, and I/O refs
- `evidence`: the referenced materials and integrity digests
- `validation`: how an independent verifier checks the statement

## 3. Required Fields

The minimal required fields are:

- `profile.name`
- `profile.version`
- `statement_id`
- `timestamp`
- `actor.id`
- `actor.type`
- `actor.name`
- `actor.runtime`
- `subject.id`
- `subject.type`
- `subject.digest`
- `subject.locator`
- `operation.id`
- `operation.type`
- `operation.subject_ref`
- `operation.policy_ref`
- `operation.input_refs`
- `operation.output_refs`
- `operation.result.status`
- `operation.result.summary`
- `policy.id`
- `policy.name`
- `policy.constraint_refs`
- `constraints[].id`
- `constraints[].description`
- `provenance.id`
- `provenance.actor_ref`
- `provenance.operation_ref`
- `provenance.subject_ref`
- `provenance.input_refs`
- `provenance.output_refs`
- `evidence.id`
- `evidence.subject_ref`
- `evidence.operation_ref`
- `evidence.policy_ref`
- `evidence.references[]`
- `evidence.artifacts[]`
- `evidence.integrity.references_digest`
- `evidence.integrity.artifacts_digest`
- `evidence.integrity.statement_digest`
- `validation.id`
- `validation.evidence_ref`
- `validation.provenance_ref`
- `validation.policy_ref`
- `validation.validator`
- `validation.method`
- `validation.status`

## 4. Optional Fields

The profile keeps optional fields to a minimum:

- `operation.description`

The required locator fields remain flexible in value shape:

- `subject.locator` may be a URI, path, or persistent identifier placeholder
- `evidence.references[].locator` may be a URI, path, or persistent identifier placeholder
- `evidence.artifacts[].locator` may be a URI, path, or persistent identifier placeholder

No optional extension fields are required for conformance in v0.1.

## 5. Field Relationships

The minimum link rules are:

- `operation.subject_ref` must equal `subject.id`
- `operation.policy_ref` must equal `policy.id`
- every `policy.constraint_refs[]` value must resolve to one `constraints[].id`
- every `operation.input_refs[]` and `operation.output_refs[]` value must resolve to one `evidence.references[].ref_id`
- `provenance.actor_ref` must equal `actor.id`
- `provenance.operation_ref` must equal `operation.id`
- `provenance.subject_ref` must equal `subject.id`
- `provenance.input_refs` must match `operation.input_refs`
- `provenance.output_refs` must match `operation.output_refs`
- `evidence.subject_ref` must equal `subject.id`
- `evidence.operation_ref` must equal `operation.id`
- `evidence.policy_ref` must equal `policy.id`
- `validation.evidence_ref` must equal `evidence.id`
- `validation.provenance_ref` must equal `provenance.id`
- `validation.policy_ref` must equal `policy.id`

## 6. Compliance Conditions

An operation accountability statement is compliant only if all of the
following hold:

1. `profile.name` is `execution-evidence-operation-accountability-profile`.
2. `profile.version` is `0.1`.
3. The JSON instance satisfies the schema.
4. Every internal reference resolves to an existing local identifier.
5. Input refs point to evidence references with role `input`.
6. Output refs point to evidence references with role `output`.
7. Policy, provenance, and evidence carry a consistent linkage to the same
   operation statement.
8. `evidence.integrity.references_digest` equals the canonical digest of
   `evidence.references`.
9. `evidence.integrity.artifacts_digest` equals the canonical digest of
   `evidence.artifacts`.
10. `evidence.integrity.statement_digest` equals the canonical digest of the
    statement core: `actor`, `subject`, `operation`, `policy`, `constraints`,
    and `provenance`.

## 7. Failure Conditions

Validation fails when at least one of the following occurs:

- a required field is missing
- a field shape violates the schema
- a local reference is unclosed
- an input ref points to a non-input evidence reference
- an output ref points to a non-output evidence reference
- `policy`, `provenance`, and `evidence` do not agree on the linked entities
- any integrity digest fails recomputation

## 8. Minimal JSON Expression Suggestion

```json
{
  "profile": {
    "name": "execution-evidence-operation-accountability-profile",
    "version": "0.1"
  },
  "statement_id": "eeoap:demo-001",
  "timestamp": "2026-03-30T00:00:00Z",
  "actor": {
    "id": "actor:metadata-enricher",
    "type": "agent",
    "name": "metadata-enricher",
    "runtime": "openai-agents"
  },
  "subject": {
    "id": "obj:note-001",
    "type": "fdo-record",
    "digest": "sha256:<64 lowercase hex chars>",
    "locator": "urn:demo:note-001"
  },
  "operation": {
    "id": "op:metadata-enrich-001",
    "type": "metadata.enrich",
    "subject_ref": "obj:note-001",
    "policy_ref": "policy:approved-metadata-v1",
    "input_refs": ["ref:input-note"],
    "output_refs": ["ref:output-note"],
    "result": {
      "status": "succeeded",
      "summary": "one derived object emitted"
    }
  },
  "policy": {
    "id": "policy:approved-metadata-v1",
    "name": "approved-metadata-policy",
    "constraint_refs": ["constraint:approved-fields"]
  },
  "constraints": [
    {
      "id": "constraint:approved-fields",
      "description": "Only approved metadata fields may be added."
    }
  ],
  "provenance": {
    "id": "prov:demo-001",
    "actor_ref": "actor:metadata-enricher",
    "operation_ref": "op:metadata-enrich-001",
    "subject_ref": "obj:note-001",
    "input_refs": ["ref:input-note"],
    "output_refs": ["ref:output-note"]
  },
  "evidence": {
    "id": "evidence:demo-001",
    "subject_ref": "obj:note-001",
    "operation_ref": "op:metadata-enrich-001",
    "policy_ref": "policy:approved-metadata-v1",
    "references": [
      {
        "ref_id": "ref:input-note",
        "role": "input",
        "object_id": "obj:note-001",
        "digest": "sha256:<64 lowercase hex chars>",
        "locator": "urn:demo:note-001"
      },
      {
        "ref_id": "ref:output-note",
        "role": "output",
        "object_id": "obj:note-001-derived",
        "digest": "sha256:<64 lowercase hex chars>",
        "locator": "urn:demo:note-001-derived"
      }
    ],
    "artifacts": [
      {
        "artifact_id": "artifact:op-log-001",
        "type": "execution-log",
        "digest": "sha256:<64 lowercase hex chars>",
        "locator": "urn:demo:op-log-001"
      }
    ],
    "integrity": {
      "references_digest": "sha256:<64 lowercase hex chars>",
      "artifacts_digest": "sha256:<64 lowercase hex chars>",
      "statement_digest": "sha256:<64 lowercase hex chars>"
    }
  },
  "validation": {
    "id": "validation:demo-001",
    "evidence_ref": "evidence:demo-001",
    "provenance_ref": "prov:demo-001",
    "policy_ref": "policy:approved-metadata-v1",
    "validator": "agent-evidence validate-profile",
    "method": "schema+reference+consistency",
    "status": "verifiable"
  }
}
```
