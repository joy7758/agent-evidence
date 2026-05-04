# Review Pack V0.3 White Paper Index

## Purpose

This document identifies the canonical repository white paper draft for Review
Pack V0.3 and organizes the supporting research materials around it.

It is a repository white paper index. It is not a submission package, not a
Zenodo technical report, not an arXiv or workshop submission, and not AI Act
Pack. It does not add implementation scope or publication claims.

## Current Recommendation

Canonical draft:

- [Review Pack V0.3 Technical Note V3](review-pack-v0.3-technical-note-v3.md)

Supporting background:

- [Review Pack V0.3 Technical Note V2](review-pack-v0.3-technical-note-v2.md)
- [Review Pack V0.3 Submission Plan](review-pack-v0.3-submission-plan.md)
- [Operation Accountability Profile](operation-accountability-profile.md)
- [FDO / Data-Space Mapping](fdo-data-space-mapping.md)
- [Strategic Positioning](../strategic-positioning.md)
- [Review Pack Minimal Cookbook](../cookbooks/review_pack_minimal.md)

The current recommendation is to treat V3 as the canonical repository white
paper draft. No immediate V3.1 is required. A Zenodo technical report should
wait until one more refinement cycle. arXiv and workshop submission remain
deferred.

## Reading Order

1. [Strategic Positioning](../strategic-positioning.md)
   - Start here to understand the project boundary after v0.6.0: local
     evidence export, validation, verification, and review packaging.
2. [Review Pack V0.3 Technical Note V3](review-pack-v0.3-technical-note-v3.md)
   - Read this as the canonical technical note draft and repository white
     paper seed.
3. [Review Pack Minimal Cookbook](../cookbooks/review_pack_minimal.md)
   - Use this to connect the white paper claims to the runnable local Review
     Pack path.
4. [Operation Accountability Profile](operation-accountability-profile.md)
   - Read this for the research framing around post-execution operation
     accountability.
5. [FDO / Data-Space Mapping](fdo-data-space-mapping.md)
   - Read this for the conceptual mapping to digital-object and data-space
     language without official standard or connector claims.
6. [Review Pack V0.3 Submission Plan](review-pack-v0.3-submission-plan.md)
   - Read this before external sharing to check target readers, contribution
     framing, figures, evaluation evidence, and claims boundaries.

## Target Readers

Primary readers:

- AI agent framework engineers should take away how Review Pack V0.3 packages
  signed runtime evidence into local markdown and JSON artifacts that humans
  and tool-using agents can inspect.
- Platform reliability / audit engineers should take away the verify-first,
  fail-closed flow, artifact inventory, reviewer checklist, and operational
  boundaries.

Secondary readers:

- FDO / data-space researchers should take away a conceptual mapping between
  evidence bundles, manifests, receipts, and review packages as portable
  digital-object-style artifacts.
- AI governance researchers should take away that Review Pack V0.3 is a
  bounded evidence and review layer that could support later interpretation,
  not a compliance product.
- Standards-oriented reviewers should take away that Operation Accountability
  Profile remains research framing, not an official standard.

## Canonical Thesis

Review Pack V0.3 turns a verified signed AI agent evidence bundle into a
local, offline, fail-closed, markdown/JSON reviewer-facing package that can be
inspected by humans and tool-using agents without relying on hosted tracing
platforms or making legal/compliance claims.

## Contribution Checklist

The white paper contribution framing should stay limited to exactly four
implemented contributions:

1. A local verify-first / fail-closed Review Pack artifact model for signed
   agent evidence bundles.
2. A dual human/agent review surface: `summary.md` plus `manifest.json`,
   `receipt.json`, and `findings.json`.
3. Stable `RP-CHECK-*` reviewer checklist IDs and bounded findings/severity
   model.
4. Conservative safety boundaries: no private key copying, no network
   requirement, limited `secret_scan_status`, and no legal/compliance/DLP
   overclaim.

Do not add adoption, benchmark, legal, compliance, governance-platform, or
official-standard claims to this contribution list.

## External Sharing Checklist

- [x] canonical draft selected
- [x] abstract selected
- [x] contribution list stable
- [x] figures reviewed
- [x] evaluation evidence table present
- [x] claims / non-claims reviewed
- [x] no invented benchmarks
- [x] no adoption metrics claimed
- [x] no legal/compliance claims
- [x] no AI Act approval claim
- [x] DOI strategy understood
- [x] version context clear: `agent-evidence` v0.6.0, Review Pack V0.3

Before any external publication package, re-run this checklist and verify that
the current repository state still matches the note.

## Citation / DOI Note

The current DOI strategy is:

- primary project DOI: `10.5281/zenodo.19334061`
- v0.6.0 exact version DOI: `10.5281/zenodo.20013667`

Use the concept DOI for the evolving project. Use the exact version DOI when
the goal is exact v0.6.0 reproduction. Do not invent a future DOI. Do not
replace the concept DOI with a version DOI for general project citation.

## Claims and Non-Claims

| Claim area | Allowed wording | Forbidden wording |
| --- | --- | --- |
| Legal non-repudiation | Review Pack V0.3 preserves verification status for local review. | Review Pack proves legal non-repudiation. |
| Compliance certification | Review Pack V0.3 can support later compliance-oriented interpretation. | Review Pack is compliance certification. |
| AI Act approval | AI Act Pack remains future planning only. | Review Pack provides AI Act approval. |
| Official FDO standard | FDO mapping is conceptual research framing. | Review Pack is an official FDO standard or official FDO profile. |
| Full AI governance platform | Review Pack V0.3 is a local reviewer-facing evidence package. | Review Pack is a full AI governance platform. |
| Comprehensive DLP | `secret_scan_status` records configured sentinel checks and limitations. | Review Pack guarantees all secrets are absent or proves comprehensive DLP. |
| Hosted/remote review service | Review Pack V0.3 is local and offline. | Review Pack is a hosted review service or remote review service. |

Use this table when reviewing abstracts, diagrams, release-facing prose, or
external sharing language.

## Next Writing Step

Recommended next phase:

```text
P50 Review Pack V0.3 white paper polish planning
```

P50 should decide whether to prepare a V3.1 draft, refine diagrams, select the
final abstract for external sharing, and decide whether and when to create a
Zenodo technical report. arXiv and workshop submission should remain deferred.

Do not make AI Act Pack implementation the next step.

## Deferred Work

- Zenodo technical report
- arXiv / workshop submission
- AI Act Pack planning
- Chinese summary
- figure redraw
- related-work citation selection

These are future planning items. They should not be treated as current
implementation, release, or submission work.

## Non-Goals

This index does not add:

- code
- release work
- legal/compliance claims
- AI Act Pack
- PDF/HTML/dashboard output
- remote service
- OpenAPI/MCP/schema/core changes
