# SoftwareX Preparation Checklist

| Item | Status | Evidence | Action required | Priority |
|---|---|---|---|---|
| Decide public release strategy | blocked | v1.4 route analysis; v1.5 isolation notes | Choose whether OpenTelemetry-to-EEOAP is released as part of `agent-evidence`, as a focused subpackage/release, or as supplemental artifact material. | P0 |
| Decide whether and when to push `eeoap-v0.1-artifact` tag | blocked | Local tag exists; not pushed | Push only after final citation/release strategy is approved. | P0 |
| Decide whether and when to push `aep-v0.1-artifact` tag | blocked | Local tag exists; not pushed | Push only after final citation/release strategy is approved. | P0 |
| Create OpenTelemetry-to-EEOAP software release tag candidate | not started | No package-specific release tag exists | Define candidate tag name and target commit after metadata strategy is fixed. | P0 |
| Create or update artifact availability statement | partial | v1.0 artifact note; v1.4/v1.5 docs | Rewrite for SoftwareX with exact public availability state. | P0 |
| Update software citation strategy | blocked | `CITATION.cff` is AEP-Media-specific | Decide whether to use root metadata, subpackage metadata, or a paper-local citation note. | P0 |
| Resolve OpenTelemetry-to-EEOAP-specific `CITATION.cff` or equivalent citation note | blocked | Root `CITATION.cff` exists but describes AEP-Media | Create a strategy before editing metadata. | P0 |
| Resolve OpenTelemetry-to-EEOAP-specific `codemeta.json` or equivalent metadata note | blocked | Root `codemeta.json` exists but describes AEP-Media | Create a strategy before editing metadata. | P0 |
| Ensure root README clearly points to OpenTelemetry-to-EEOAP adapter path | partial | Root `README.md`; adapter docs under `papers/` | Add focused pointer later, only after release scope is decided. | P0 |
| Decide how to handle no `repo/src` layout | blocked | Source is under `agent_evidence/`; adapter is under `tools/`; no `src/` directory | Choose whether to restructure, create a release package layout, or ask SoftwareX editorial office. | P0 |
| Produce 3000-word SoftwareX article draft | not started | v1.0 manuscript is about 3692 words | Compress into SoftwareX structure after metadata/release scope is fixed. | P0 |
| Final references | partial | v0.9 references; local tags in v1.3 | Update with final public tag/archive/DOI state. | P0 |
| Final AI-assisted writing disclosure | not started | v1.4 noted requirement | Draft according to final venue wording. | P0 |
| Conflict of interest declaration | not started | v1.4 noted requirement | Prepare final statement. | P0 |
| Funding statement | not started | v1.4 noted requirement | Prepare final statement. | P0 |
| Data availability statement | not started | v1.4 noted requirement | Prepare data/software availability statement after release scope. | P0 |
| Final clean-clone verification after release candidate | not started | v1.5 isolated worktree verification exists | Re-run after final package/release-candidate changes. | P1 |
| Checksum regeneration for final package | not started | v0.5 checksum exists; final package not cut | Generate final checksums after final support package is built. | P1 |
| Final validator rerun for both generated statements | partial | v1.5 validator pass for both statements | Re-run immediately before final release/submission. | P1 |
| Final scoped pytest rerun | partial | v1.5 scoped tests passed before and after docs | Re-run after metadata/release package work. | P1 |
| Repository hygiene note | partial | v1.4/v1.5 notes disclose dirty original worktree | Write final release-specific hygiene note. | P1 |
| Final proofreading | not started | Manuscript not yet SoftwareX-shaped | Proofread after article draft and declarations exist. | P1 |
| Graphical abstract | not started | Optional in v1.4 analysis | Defer unless SoftwareX preparation benefits from it. | P2 |
| Highlights polishing | not started | Skeleton exists in v1.4 | Polish after article draft exists. | P2 |
| Optional workflow diagram | not started | Existing conceptual materials exist elsewhere | Defer until article shape is fixed. | P2 |
| Optional SoftwareX metadata table polishing | not started | v1.4 skeleton exists | Polish after metadata strategy is fixed. | P2 |

## Checklist Interpretation

The next blocker is not the article text. The next blocker is metadata and
release-scope strategy: the repository already has citation metadata, but it
currently points to AEP-Media rather than OpenTelemetry-to-EEOAP. Drafting the
SoftwareX article before resolving that could create the wrong software object.
