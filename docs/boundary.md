# Agent Evidence Boundary

`agent-evidence` is the capture substrate for semantic execution events.

## What this repo does

- capture runtime-side evidence events
- persist append-only evidence chains
- export bundles for later review
- provide schema and profile contracts for stored envelopes
- expose adapters for runtime integrations

## What this repo does not do

- run the audit control plane
- own bounded review or conformance workflows
- replace the architecture hub
- act as the walkthrough demo repository

## Relation to ARO Audit

- `agent-evidence` = capture substrate
- `aro-audit` = review, verify, export, and conformance plane
- evidence capture happens close to runtime
- audit review happens downstream after evidence is available
