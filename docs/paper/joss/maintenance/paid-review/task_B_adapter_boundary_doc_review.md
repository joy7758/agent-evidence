# Task B: Adapter Boundary Documentation Review

## Goal

Review `docs/aep-media/adapter-boundaries.md` for clarity, unsupported-claim
risk, and practical usefulness to a new user.

## Required Scope

The reviewer should inspect:

- LinuxPTP-style trace ingestion boundary;
- FFmpeg PRFT-style metadata ingestion boundary;
- C2PA-like manifest ingestion boundary;
- required fields;
- optional fields;
- unknown-field behavior;
- missing-field behavior;
- unsupported or out-of-scope claims.

The reviewer should cross-check the documentation against the current adapter
fixtures and tests where possible.

## Deliverable

Open one GitHub issue or PR that improves clarity. Suitable deliverables
include:

- wording changes that make boundaries more explicit;
- a small table clarifying required and optional fields;
- a correction where docs imply unsupported behavior;
- a short note explaining how unknown or missing fields are reported.

## Acceptance Criteria

The work is accepted if it:

- reduces ambiguity for a new user;
- preserves the existing claim boundary;
- avoids unsupported claims about real external verification;
- is limited to documentation unless a separate implementation issue is opened;
- includes enough context for maintainers to review the change.

## Boundaries

Do not claim real PTP proof, full MP4 PRFT parsing, real C2PA signature
verification, legal sufficiency, chain of custody, or production deployment.
The adapter layer remains a local fixture-ingestion and report-normalization
surface unless a future documented external verifier changes that boundary.
