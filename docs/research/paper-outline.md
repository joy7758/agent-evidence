# Paper / Technical Note Outline

## Working title

Agent Evidence Review Packs: Local, Verifiable, Reviewer-Facing Artifacts for
AI Agent Runs

## Abstract draft

AI agent systems increasingly produce execution traces, logs, tool-call
records, and framework-specific observability data. These artifacts help
operators debug systems, but they are often difficult to package for independent
post-execution review. `agent-evidence` explores a local-first evidence path
for AI agent operations: runtime evidence export, signed bundle verification,
structured capabilities metadata, and a reviewer-facing Review Pack. The v0.6.0
release introduces Review Pack V0.3, a local, offline, verify-first package
with stable reviewer checklist IDs, artifact inventory, conservative secret
scan status, and machine-readable error output for pack creation failures. This
technical note describes the artifact model, review boundary, limitations, and
research questions for portable agent-run accountability without claiming legal
non-repudiation, compliance certification, AI Act approval, or comprehensive
DLP.

## Problem statement

- Traces and logs are useful but often platform-bound.
- Reviewers need portable, verifiable post-execution artifacts.
- Agentic engineering needs both machine-readable and human-reviewable
  execution evidence.
- Evidence packaging must avoid turning narrow verification artifacts into
  broad governance or compliance claims.

## Contribution

The current project contributes:

- local evidence export for AI agent and service operations
- operation-accountability profile validation
- signed export bundle verification
- Review Pack V0.3 for reviewer-facing packaging
- agent-native discovery through capabilities metadata and generated metadata
  files
- explicit non-claims for legal, compliance, AI Act, governance, hosted-service,
  and DLP boundaries

## System overview

The paper can describe the system in layers:

1. CLI/core
2. operation-accountability profile and validator
3. runtime evidence records and exports
4. signed bundle verification
5. capabilities metadata
6. local OpenAPI wrapper
7. local MCP stdio tools
8. LangChain runnable path
9. OpenAI-compatible runnable path
10. Review Pack V0.3

The CLI remains the canonical local callable surface. OpenAPI and MCP are local
wrappers around existing behavior.

## Review Pack V0.3 section

The Review Pack section should cover:

- verified signed export bundle input
- public key input
- optional source summary input
- `manifest.json`, `receipt.json`, `findings.json`, and `summary.md`
- stable `RP-CHECK-*` reviewer checklist IDs
- `pack_creation_mode: local_offline`
- conservative `secret_scan_status`
- optional `--json-errors`
- fail-closed behavior

It should also state that Review Pack V0.3 is beta, local, offline, and not a
legal or compliance product.

## Evaluation plan

Evaluation can stay practical and reproducible:

- unit test suite
- LangChain smoke path
- OpenAI-compatible mock/offline smoke path
- signed export verification success
- tampered bundle fail-closed test
- bad public key fail-closed test
- non-empty output directory protection
- no private key copied into Review Pack
- configured secret sentinel has no hit
- no network during local/mock paths
- `--json-errors` smoke test
- docs and metadata consistency checks

## Limitations

The technical note must be explicit that the system is not:

- legal proof
- legal non-repudiation
- compliance certification
- AI Act approval
- a full AI governance platform
- hosted governance
- comprehensive DLP
- an official FDO standard
- a complete data-space connector

Review Pack V0.3 is a reviewer-facing artifact package. It supports review; it
does not replace judgment.

## Future work

Possible future work:

- Review Pack stabilization after external use
- AI Act Pack planning as a separate interpretation layer
- FDO / data-space mapping refinement
- broader integration evaluation
- privacy-preserving evidence packaging
- clearer reviewer workflows

Future work should remain staged. AI Act Pack should not be implemented until
the Review Pack evidence boundary and non-claims are stable.
