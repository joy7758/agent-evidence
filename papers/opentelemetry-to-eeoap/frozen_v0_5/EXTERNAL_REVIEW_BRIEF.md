# External Review Brief

## One-sentence Summary

This package demonstrates a bounded adapter path from OpenTelemetry-style agent telemetry to EEOAP-compatible portable operation evidence.

## Problem

Runtime telemetry can describe what happened inside an agent system, but it does not automatically become a portable operation evidence object that another party can validate.

## What This Package Demonstrates

This package demonstrates that one valid OpenTelemetry-style agent trace can be transformed into an EEOAP-compatible operation accountability statement. The generated statement passes the existing EEOAP validator.

It also includes four invalid traces that expose controlled adapter diagnostics:

- `missing_agent_span`
- `unresolved_tool_span`
- `broken_parent_span_relation`
- `missing_operation_name`

## What Is Inside The Frozen Package

- `paper_v0_4.md`
- `references_draft.md`
- `artifact_freeze_note.md`
- `submission_checklist.md`
- `claim_boundary.md`
- `evaluation_summary.md`
- `reviewer_positioning.md`
- `README.md`
- `MANIFEST.md`
- `FREEZE_STATUS.md`
- `NEXT_ACTIONS.md`
- `CHECKSUMS.sha256`
- `CLEAN_CLONE_VERIFICATION.md`
- `EXTERNAL_REVIEW_BRIEF.md`

## How To Reproduce

Check out commit:

```text
393aded70f9e3230ac93fb277476d8a8fc2cfb6e
```

Run the scoped adapter test:

```sh
pytest tests/test_opentelemetry_to_eeoap_adapter.py -q
```

Run checksum verification:

```sh
sha256sum -c papers/opentelemetry-to-eeoap/frozen_v0_5/CHECKSUMS.sha256
```

or:

```sh
shasum -a 256 -c papers/opentelemetry-to-eeoap/frozen_v0_5/CHECKSUMS.sha256
```

## Relationship To OpenTelemetry

OpenTelemetry supplies the telemetry-side source structure. This package uses OpenTelemetry-style agent trace fields as the source for the adapter. It does not claim full OpenTelemetry implementation compatibility.

## Relationship To EEOAP

EEOAP supplies the target evidence object and existing validator. This package does not create a new EEOAP profile and does not modify the EEOAP schema.

## Relationship To AEP

AEP focuses on runtime evidence bundles and integrity-verifiable evidence packaging. This package focuses on span-to-operation-evidence transformation.

## What This Does Not Claim

- no legal accountability proof
- no full runtime reconstruction
- no general OpenTelemetry implementation compatibility
- no cross-framework generality
- no agent-output correctness
- no production readiness
- no new profile claim

## Why This Matters

This package gives a small, reproducible bridge between agent telemetry and portable operation evidence. It can serve as a baseline for later real-runtime integrations and as a reviewable artifact for evidence-layer research.

## Suggested Reviewer Questions

- Does the mapping preserve enough provenance to support later review?
- Are the failure diagnostics meaningful and bounded?
- Is the adapter doing more than field copying?
- Is the non-claim boundary clear?
- What additional runtime fixture would strengthen the next version?
