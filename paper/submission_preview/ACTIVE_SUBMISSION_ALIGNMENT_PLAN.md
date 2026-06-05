# Active Submission Alignment Plan

## Current Status Summary

Plan verdict: blocked for external submission; allowed for local preparation.

| item | current status |
| --- | --- |
| current HEAD commit | `54b46f8` |
| active TSE manuscript | `TSE-2026-05-0426` |
| active TSE status | active TSE under review: `Under review / 审核中` |
| active TSE title | `Operation-Accountability Boundaries for Machine-Actionable Object Systems: A Profile and Validator` |
| preview readiness | local build, reference closure, review package, reproduction, pytest, and ruff checks were recorded as passing in the final preview package audit |
| claim-space audit verdict | `blocked for external submission; allowed for local preparation` |
| preview package status | local source preview and local inspection package only |

The current preview is not an external submission package. It must be handled as
local source preparation while `TSE-2026-05-0426` remains active.

## Active Submission Relationship

The current preview and active `TSE-2026-05-0426` belong to the same
operation-accountability / profile-validator claim-space.

The current preview should be treated only as:

- local source cleanup
- future revision candidate
- response material
- internal consistency evidence
- artifact reproducibility preparation

The current preview should not be submitted as a new manuscript to any external
venue while the active TSE manuscript remains under review.

## Allowed Local Actions

Allowed now:

- local source cleanup
- local PDF preview build
- local review package validation
- local response preparation
- reviewer-question mapping
- artifact reproducibility hardening
- ledger hygiene audit
- no external submission

These actions are internal preparation actions. They do not change the external
status of the active TSE manuscript.

## Disallowed Actions

Disallowed now:

- no new external submission
- no upload to another venue
- no replacement of official submission source without decision or formal venue mechanism
- no claim expansion
- no merging AEP-Media into this preview
- no merging AI Act evidence-layer claims into this preview
- no merging Sovereign-pFDO protocol or governance claims into this preview
- no declaring the preview cleared for official-submission use

These restrictions remain in force until the active submission status changes
and the manuscript ledger is rechecked.

## Future Decision Branches

### A. If Active TSE Decision Is Reject

If `TSE-2026-05-0426` is rejected, the current preview can become a candidate
for a later independent route, but only after a fresh gate review.

Required work:

- update cover letter history
- update response history
- prepare a novelty statement
- refresh the claim-space conflict audit
- review duplicate submission risk again
- rebuild any source, artifact, and PDF packages from the final chosen route
- obtain final human approval before any external action

### B. If Active TSE Decision Is Revise / Resubmit

If `TSE-2026-05-0426` receives a revise or resubmit decision, the current
preview can serve as a revision source base.

Required work:

- generate a reviewer-response map
- map each reviewer concern to source sections, examples, validator behavior,
  and artifact evidence
- preserve the active TSE manuscript ID and correspondence history
- use the proper TSE revision mechanism
- keep the preview out of any separate external route

### C. If Active TSE Decision Is Accept

If `TSE-2026-05-0426` is accepted, the current preview should be treated as
archival and post-acceptance cleanup material.

Required work:

- align archive notes with the accepted version
- preserve the accepted manuscript as the version-governing route
- avoid duplicate publication of the same claim-space
- require a substantial extension memo before any later manuscript derived from
  this material
- prove a different contribution boundary before any later external route

## Claim-Space Separation Map

| line | core claim | current status | relationship to preview | allowed treatment |
| --- | --- | --- | --- | --- |
| active TSE operation accountability paper | operation-accountability boundaries for machine-actionable object systems; profile and validator | `TSE-2026-05-0426`; active TSE under review | same operation-accountability / profile-validator claim-space | primary external route; use preview only as local preparation or future formal-response material |
| current paper-minimal preview | one operation accountability statement; EEOAP v0.1; profile-aware validator; 1 valid / 3 invalid / 1 demo; review package | local preview only | narrower local preparation surface for the active claim-space | local cleanup, build checks, review-package validation, response planning |
| AEP runtime evidence line | runtime evidence bundle, live-chain specimen, offline verification, tamper failure | DCMI/AEP line rejected and closed in ledger | historical runtime-evidence lineage, not the current statement-count paper | background only; do not import live-chain specimen status or DOI claims |
| AEP-Media line | local validation of time-aware media evidence bundles with media hashes, timing traces, and adapters | SoftwareX/FSI:DI AEP-Media lines recorded as rejected and closed in current summary | adjacent media evidence line with repository and terminology overlap | keep separate; no media/time-trace/adapter claims in the preview |
| AI Act evidence layer line | high-risk AI compliance evidence and AI Act alignment framing | `TSE-2026-04-0381` recorded as `Under Review`; EUSurvey contribution recorded separately | separate B4 compliance line with operation-accountability vocabulary overlap | keep separate; no compliance approval, certification, or legal sufficiency claim |
| Sovereign-pFDO line | protocol-driven distributed data governance and knowledge sovereignty | rejected and closed in ledger | broad conceptual/governance line, not the paper-minimal validator path | background only; no protocol sovereignty or broad governance expansion |
| SoftwareX line | AEP-Media reusable research software for offline media evidence validation | summary row says rejected and closed; older detail text contains stale active wording | adjacent software-artifact line in same repository, not the current preview | treat as ledger hygiene issue; do not use SoftwareX status as preview support |

## Required Pre-Submission Gates

Before any external route is reconsidered, all gates below must be closed:

- active submission decision known
- claim-space conflict audit refreshed
- `MANUSCRIPT_STATUS.md` ledger cleaned
- duplicate submission risk reviewed
- venue-specific policy checked
- source package regenerated
- artifact package regenerated
- final PDF rebuilt
- final human approval

Until these gates are closed, the only valid route is local preparation.

## Ledger Hygiene Note

The claim-space conflict audit found a ledger hygiene issue:

- the SoftwareX / AEP-Media summary row records the line as rejected and closed
- an older SoftwareX detail paragraph still contains stale active-submission
  wording

This plan does not modify `/Users/zhangbin/GitHub/MANUSCRIPT_STATUS.md`.
A later ledger hygiene patch should reconcile the summary table and detailed
evidence bullets together.

## Recommended Next Codex Goal

Prepare ledger hygiene audit for `MANUSCRIPT_STATUS.md` without changing
manuscript files.

## Suggested Commit Message

```text
Plan active-submission alignment for paper-minimal preview
```
