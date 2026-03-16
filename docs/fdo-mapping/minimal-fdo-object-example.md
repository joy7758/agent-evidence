# Minimal FDO-style Object Example

This note explains the smallest FDO-style object example in this repository:

- [examples/fdo-style-execution-evidence-object.json](../../examples/fdo-style-execution-evidence-object.json)

## What comes from the Execution Evidence Object

The embedded payload is the Execution Evidence Object itself.

It carries:

- the execution `steps`
- the runtime `context`
- the `agent_framework`
- the integrity-linked `hashes`
- the run `timestamp`

## What represents FDO-style object identity

The FDO-style identity layer is expressed through:

- `object_id`
- `object_type`
- `pid_placeholder`
- `metadata`

These fields give the evidence object a readable outer identity instead of
leaving it as only a runtime export payload.

## What represents integrity and provenance binding

Integrity binding is carried by:

- `integrity.action_hash`
- `integrity.trace_hash`
- `integrity.proof_hash`

Provenance binding is carried by:

- `provenance.agent_id`
- `provenance.runtime_source`
- `provenance.derived_from`

## Why this example matters

This example shows the difference between:

- the Execution Evidence Object as the bounded evidence payload
- the FDO-style wrapper as the object-facing identity, integrity, and
  provenance surface

That is the practical bridge between the current prototype and FDO-oriented
object discussion.
