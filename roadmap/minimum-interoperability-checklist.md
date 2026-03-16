# Minimum Interoperability Checklist

Use this checklist when evaluating whether a framework export is compatible with
the current specimen profile.

## Object shape

- exports `object_type` as `execution-evidence-object`
- exports `agent_framework`
- exports `run_id`
- exports `steps` as an array
- exports `context` as an object
- exports `timestamp`

## Integrity

- exports `action_hash`
- exports `trace_hash`
- exports `proof_hash`
- passes hash recomputation with the shared verification logic

## Portability

- object can be saved as standalone JSON
- object can be verified outside the original runtime
- object does not require framework-private state to be interpreted

## Provenance

- runtime source is explicit
- run identity is explicit
- agent or actor reference is available when appropriate

## FDO-style readiness

- object can be wrapped with identity metadata
- integrity fields can be surfaced outside the payload
- provenance fields can be surfaced outside the payload
