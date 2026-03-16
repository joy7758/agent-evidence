# Conformance Profile Draft

## Required fields

- `object_type`
- `agent_framework`
- `run_id`
- `steps`
- `hashes.action_hash`
- `hashes.trace_hash`
- `hashes.proof_hash`
- `context`
- `timestamp`

## Optional fields

Optional fields may include:

- additional step summaries
- extended runtime metadata
- policy-oriented references
- wrapper-level FDO-style identity fields

## Integrity requirements

- the object must pass schema validation
- `action_hash` must be recomputable from `steps`
- `trace_hash` must be recomputable from the bounded runtime payload
- `proof_hash` must be recomputable from `action_hash` and `trace_hash`

## Provenance requirements

- the runtime source must be represented
- the run identity must be represented
- provenance-oriented fields must distinguish runtime origin from object wrapper
  identity

## Portability requirements

- exporters from different frameworks must emit the same core required fields
- verification must not depend on framework-specific tooling
- the object must remain readable after export outside the original runtime
