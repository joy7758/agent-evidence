# Runtime Evidence Export Contract

This note describes a minimal external-first callback-based export contract for a runtime evidence bundle.

The goal is to keep the exported shape small and stable enough to discuss across integrations. It is not a full runtime schema, not a tracing model, and not a formal standard.

## What this contract is

This contract is a small agreement about what a runtime evidence bundle should contain when a callback-based exporter writes it from an agent run.

The contract stays intentionally narrow. A runtime evidence bundle is treated as one bounded JSON payload with three top-level blocks:

- `bundle`
- `steps`
- `hashes`

That is enough to express a minimal run summary and to verify that the exported artifact did not change after export.

## Scope

This contract is in scope for:

- external-first callback-based export
- one runtime evidence bundle for one run, or one bounded slice of a run
- a minimal JSON shape centered on `bundle`, `steps`, and `hashes`
- simple offline validation and hash verification

## Non-goals

This contract does not try to define:

- a full tracing or observability schema
- token-level streaming records
- input and output payload schemas
- signatures, runtime actor identities, timestamps, provenance chains, or storage backends
- a final standard or a large interoperability profile

## Minimal bundle shape

For this contract, a runtime evidence bundle is a single JSON object with three top-level fields:

- `bundle`
- `steps`
- `hashes`

Minimal example:

```json
{
  "bundle": {
    "bundle_id": "bundle-minimal-001",
    "bundle_type": "runtime-evidence-bundle"
  },
  "steps": [
    {
      "step_id": "step-1",
      "step_type": "chain.start",
      "status": "completed"
    },
    {
      "step_id": "step-2",
      "step_type": "tool.end",
      "status": "completed"
    }
  ],
  "hashes": {
    "step_hash": "sha256:45839c366c0e2ccdb1f3c0f43a306a780416cdec4d55bf9bc298500fece7ce63",
    "bundle_hash": "sha256:3759d86c7ec22406a5e6c90540f30e59f27db44fa71cb61c164039d34dddd38b"
  }
}
```

This is deliberately small. A richer directory layout, manifest, or sidecar files may exist around it, but those are outside this contract.

## Minimal step record

The `bundle` block carries the minimal bundle identity and type:

- `bundle_id`: a stable identifier for the exported bundle
- `bundle_type`: the type label for the exported bundle

Each item in `steps` should be an object with three string fields:

- `step_id`: a stable identifier within the bundle
- `step_type`: a coarse event label such as `chain.start`, `tool.end`, or `handoff`
- `status`: a simple outcome such as `completed`, `failed`, or `cancelled`

Nothing else is required in the minimal contract. If an exporter wants to keep richer details, those can live in separate runtime-specific artifacts rather than inside this minimal bundle shape.

## Hash and integrity fields

The `hashes` block is the integrity layer for the runtime evidence bundle.

- `step_hash` is the SHA-256 digest of the deterministic JSON serialization of `steps`
- `bundle_hash` is the SHA-256 digest of the deterministic JSON serialization of:

```json
{
  "bundle": "...the exact bundle object...",
  "steps": "...the exact steps array...",
  "hashes": {
    "step_hash": "...the computed step_hash..."
  }
}
```

This avoids self-reference while still binding the runtime evidence bundle to its minimal identity block, the step content, and the declared `step_hash`.

For this contract, deterministic JSON serialization means:

- UTF-8 encoding
- object keys sorted lexicographically
- no reliance on whitespace
- array order preserved exactly as exported

Digest values should be written as `sha256:<64 lowercase hex chars>`.

## Minimal validation / verification flow

The minimal validation and verification flow is:

1. Load the runtime evidence bundle as JSON.
2. Check that `bundle` is an object, `steps` is an array, and `hashes` is an object.
3. Check that `bundle` contains `bundle_id` and `bundle_type`, and that each is a string.
4. Check that each step contains `step_id`, `step_type`, and `status`, and that each is a string.
5. Check that `hashes.step_hash` and `hashes.bundle_hash` match the `sha256:<64 lowercase hex chars>` format.
6. Recompute `step_hash` from the exported `steps`.
7. Recompute `bundle_hash` from the exported `bundle`, `steps`, and the recomputed `step_hash`.
8. Compare the recomputed values to the stored values.

If both hashes match, the runtime evidence bundle is internally consistent at this minimal level. If either hash differs, the bundle was changed, serialized differently, or exported incorrectly.

## Relationship to tracing / observability

This contract is not a tracing system and does not try to replace one.

Tracing and observability systems usually keep much richer runtime data: nested spans, timings, attributes, logs, streaming events, dashboards, and search. A runtime evidence bundle is the smaller exported artifact that can be carried outside that environment.

In practice, the `steps` block may be derived from callback events, span summaries, or trace records. The point of the contract is not to reproduce the full trace. The point is to stabilize the smallest external shape that still preserves a useful execution summary and a basic integrity check.

## Why this stays external-first for now

An external callback-based export path is the least invasive place to learn what shape stays stable across real runs.

This external-first approach helps because it:

- works without requiring runtime-core changes
- keeps the contract small while usage patterns are still being tested
- makes it easier to compare outputs across frameworks without forcing a shared internal model too early

If this shape proves useful over time, stronger guarantees or richer hooks can be discussed later. For now, the useful constraint is to keep the runtime evidence bundle minimal and easy to export.

## Current status

This is a callback-based experimental export contract for discussing a stable interface shape for a runtime evidence bundle.
