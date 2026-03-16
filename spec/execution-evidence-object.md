# Execution Evidence Object

## Purpose

Execution Evidence Object defines a bounded evidence artifact for autonomous
agent runs.

The goal is to turn runtime activity into a portable object that can be
reviewed, verified, and discussed as a standards-oriented artifact rather than
only as a toolkit export.

## Object Identity

The object is identified as an `execution-evidence-object`.

Each object instance should carry:

- a stable `object_type`
- the originating `agent_framework`
- a `run_id` that scopes the runtime session
- a `timestamp` for export time

## Evidence Structure

The core structure is intentionally small:

- object identity fields
- ordered execution `steps`
- grouped `hashes`
- runtime `context`

This keeps the object readable enough for architecture discussion and concrete
enough for validation.

## Integrity Verification

Integrity is expressed through three hash surfaces:

- `action_hash` for the exported execution steps
- `trace_hash` for the bounded run context
- `proof_hash` for the integrity link between action and trace material

The exact verification path is demonstrated by the prototype script under
`scripts/verify_evidence_object.py`.

## Runtime Export

The object is intended to be exported after runtime execution completes.

It does not replace detailed tracing or full observability systems.

Instead, it provides a compact execution evidence object that can be carried
between runtime, review, and standards-oriented discussion.

## FDO Compatibility

The object is designed to be readable as a candidate Digital Object surface:

- object identity maps to object-level identity
- context maps to metadata
- hashes map to integrity references
- runtime origin maps to provenance-oriented interpretation

This repository treats the Execution Evidence Object as a standards proposal
prototype rather than a finalized standard.
