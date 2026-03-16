# Execution Evidence to FDO

## Evidence bundle identity

An execution evidence bundle should be treated as a bounded object instance
rather than only as an internal runtime export.

The bounded identity comes from:

- `object_type`
- `run_id`
- `agent_framework`
- hash-linked integrity material

## Persistent identifier placeholder

The current prototype does not assign a production identifier.

A standards-facing placeholder can be represented as:

`pid:pending/execution-evidence-object/<run_id>`

This keeps the mapping discussion concrete without claiming registry-level
allocation.

## Metadata layer

The metadata layer is formed from contextual runtime information such as:

- execution context
- agent framework
- timestamp
- step summaries

This is the descriptive surface that helps an external reader interpret the
object.

## Integrity layer

The integrity layer is formed from:

- `action_hash`
- `trace_hash`
- `proof_hash`

These fields allow the object to be checked as a stable evidence artifact
rather than as an unstructured log dump.

## Provenance reference

Provenance-oriented reading comes from the agent and runtime origin fields,
especially:

- the framework origin
- run identity
- actor or agent references carried in the surrounding context

## Mapping Table

| Execution Evidence Field | FDO Concept |
| --- | --- |
| `run_id` | persistent identifier placeholder |
| `object_type` | object class marker |
| `steps` | object element set |
| `hashes.action_hash` | integrity reference |
| `hashes.trace_hash` | integrity reference |
| `hashes.proof_hash` | verification proof surface |
| `context` | metadata block |
| `agent_framework` | provenance entity / runtime source |

Examples:

- `event_id` -> object element
- `trace_hash` -> integrity reference
- `context` -> metadata block
- `agent_id` -> provenance entity

## Diagram Description

Agent Run
→ Evidence Bundle
→ Digital Object
→ FDO Registry

This diagram is intended as an interpretation path, not as a claim of formal
registry integration.
