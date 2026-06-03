# Agent Evidence SE Workflow Case Prototype v0.1.0-rc3

This release candidate repairs the rc2 packaging limitations identified by the Phase 33 post-release audit.

## Repair Scope

- Adds top-level release evidence documents: `CLAIM_BOUNDARY.md`, `ENVIRONMENT.md`, `REPRODUCIBILITY.md`, `ARCHIVE_NOTES.md`, and `AI_DISCLOSURE.md`.
- Corrects release metadata from rc2 to rc3.
- Replaces stale unrelated citation metadata with SE workflow case prototype metadata.
- Expands the selected SE workflow pytest suite into 28 meaningful checks over the case matrix, baseline counts, diagnostic codes, top-level release documents, and claim boundaries.
- Prepares a standalone installable release candidate package that includes package metadata and the minimal `agent_evidence` module required by the case runners.

## Evidence Summary

- Total case rows: 18.
- Valid rows: 3.
- Invalid rows: 15.
- Diagnostic match: 18/18.
- Schema-only missed invalid: 15.
- Log-only missed invalid: 15.
- Policy-only missed invalid: 13.

## Claim Boundary

These are representative reproducible SE workflow fixtures and case prototypes. This release candidate does not claim industrial real-world evaluation, production deployment, benchmark superiority, legal or compliance sufficiency, full FDO interoperability, or TSE v3 readiness.
