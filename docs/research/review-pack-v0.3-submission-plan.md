# Review Pack V0.3 Submission Plan

This document plans the next writing and publication path for the Review Pack
V0.3 technical note. It is a planning document, not an actual submission
package, final paper draft, release plan, or publication record.

## Purpose

Review Pack V0.3 is implemented in `agent-evidence` v0.6.0 and documented in
the current technical note draft. The next step is to decide how that note
should become externally shareable without expanding the project's claims.

This plan defines the target format, reader profile, abstract variants,
contribution framing, figure plan, evaluation evidence, related-work
categories, and claims boundary for the next writing step.

## Recommended Target Format

The recommended path is:

1. Repository white paper / technical note first.
2. Zenodo technical report later after one refinement cycle.
3. arXiv and workshop submission deferred.

This order is intentional. Review Pack V0.3 is stable enough to explain as an
implemented technical artifact, but the current evidence is not yet broad
enough for a full system paper. The strongest immediate output is a sober
repository technical note that can be reviewed, cited informally, and refined.

Zenodo can become appropriate after one more refinement cycle because it gives
the technical note a citable archival record. arXiv or workshop submission
should wait until the related-work positioning, figures, and evaluation
presentation are mature enough to avoid overclaiming.

AI Act Pack and compliance interpretation are intentionally deferred. The
technical note should explain Review Pack as an evidence and review layer, not
as a legal, compliance, or governance product.

## Target Readers

Primary readers:

- AI agent framework engineers: should understand how Review Pack packages
  signed runtime evidence into local markdown and JSON artifacts that agents
  and humans can inspect.
- Platform reliability / audit engineers: should understand the fail-closed
  verification path, artifact inventory, reviewer checklist, and operational
  boundaries.

Secondary readers:

- FDO / data-space researchers: should see how evidence bundles, manifests,
  receipts, and review packages can be discussed as portable digital-object
  style artifacts without claiming official profile status.
- AI governance researchers: should see Review Pack as a bounded evidence
  layer that could support later interpretation, not as compliance
  certification.
- Standards-oriented reviewers: should see the Operation Accountability
  Profile as research framing and not an official standard.

## Refined Title and Subtitle

Main title:

```text
Agent Evidence Review Packs:
Local, Verifiable, Reviewer-Facing Artifacts for AI Agent Runs
```

Alternative subtitles:

- A Local Review Layer for Signed AI Agent Evidence Bundles
- Portable Post-Execution Artifacts for Human and Agent Review
- Markdown and JSON Review Packages for Verifiable Agent Runs

The main title should stay unchanged for the next draft.

## Abstract Variants

### A. 100-word abstract

AI agent runs often leave traces, logs, and tool-call records that are useful
to operators but hard to hand to independent reviewers. This technical note
presents Review Pack V0.3 in `agent-evidence` v0.6.0: a local, offline,
verify-first, fail-closed package generated from a verified signed evidence
bundle. The pack combines human-readable summary material with
machine-readable manifest, receipt, and findings JSON. It adds stable reviewer
checklist IDs, conservative `secret_scan_status`, `local_offline` creation
metadata, and opt-in JSON failure output. The goal is portable post-execution
review, not legal proof, compliance certification, AI Act approval, official
standard status, hosted governance, or comprehensive DLP.

### B. 150-word abstract

AI agent systems commonly produce traces, logs, and tool-call records, but
these artifacts are often bound to platforms or operator workflows rather than
packaged for independent post-execution review. This technical note presents
Review Pack V0.3, implemented in `agent-evidence` v0.6.0, as a local,
offline, verify-first, fail-closed artifact package for AI agent runs. Review
Pack V0.3 transforms a verified signed evidence bundle into a small
reviewer-facing directory containing `summary.md`, `manifest.json`,
`receipt.json`, `findings.json`, and copied public evidence artifacts. It adds
stable `RP-CHECK-*` reviewer checklist IDs, `local_offline` creation metadata,
conservative `secret_scan_status`, and opt-in JSON error output for tool
callers. The contribution is a bounded review layer for humans and agents,
grounded in existing validation tests and smoke paths. It supports portable
inspection without claiming legal non-repudiation, compliance certification,
AI Act approval, official FDO status, full governance automation, hosted
review, or comprehensive DLP.

### C. 250-word abstract

AI agent systems increasingly produce execution traces, logs, tool-call
records, and framework-specific observability data. These artifacts can help
operators debug runs, but they are often platform-bound and difficult to
package for independent review after execution. This technical note presents
Review Pack V0.3, implemented in `agent-evidence` v0.6.0, as a local,
offline, verify-first, fail-closed package for AI agent run evidence. Starting
from a verified signed evidence bundle, Review Pack V0.3 produces a small
markdown and JSON directory: `summary.md` for human review, `manifest.json`
for package metadata and inventory, `receipt.json` for verification and
packaging state, `findings.json` for bounded findings, and copied public
evidence artifacts. V0.3 adds stable `RP-CHECK-*` reviewer checklist IDs,
`pack_creation_mode: local_offline`, conservative `secret_scan_status`, and
opt-in `--json-errors` for machine-readable failure handling. The note
positions these artifacts as a practical bridge between runtime evidence,
operation accountability, and agent-native inspection. Evaluation is based on
existing smoke and regression checks: LangChain and OpenAI-compatible mock
paths, tampered bundle and bad public key fail-closed tests, no private key
copying, secret sentinel checks, no network behavior, JSON error output, and
generated metadata consistency. The contribution remains intentionally narrow.
Review Pack V0.3 is not legal proof, compliance certification, AI Act
approval, an official FDO standard, a complete governance platform, a hosted
review service, or comprehensive DLP. It is best read as a technical artifact
model and review workflow seed, not as a regulatory product.

## Contribution List

Keep exactly four contributions:

1. A local verify-first / fail-closed Review Pack artifact model for signed
   agent evidence bundles.
2. A dual human/agent review surface: `summary.md` plus `manifest.json`,
   `receipt.json`, and `findings.json`.
3. Stable `RP-CHECK-*` reviewer checklist IDs and bounded findings/severity
   model.
4. Conservative safety boundaries: no private key copying, no network
   requirement, limited `secret_scan_status`, and no legal/compliance/DLP
   overclaim.

Do not add broader governance, compliance, adoption, or benchmark claims to the
contribution list.

## Figure Plan

| Figure | Purpose | What it should show | Status |
| --- | --- | --- | --- |
| Evidence export to Review Pack flow | Explain the core pipeline. | Runtime events -> signed export bundle -> verify -> Review Pack. | Present in v2; keep and polish labels. |
| Review Pack artifact layout | Show the concrete output package. | `manifest.json`, `receipt.json`, `findings.json`, `summary.md`, and `artifacts/`. | Present in v2; keep, but redraw cleanly before external publication. |
| Agent-native surface context | Place Review Pack among callable surfaces. | CLI/core, capabilities metadata, local OpenAPI, local MCP, and Review Pack. | Present in v2; simplify so it does not imply OpenAPI/MCP Review Pack exposure. |
| Operation Accountability Profile conceptual model | Connect the note to research framing. | Operation, actor/agent, runtime event, evidence record, verification result, reviewer-facing package. | Present in v2; keep as conceptual figure or appendix figure. |

Figures should remain explanatory. They should not imply remote services,
compliance workflows, or official standard status.

## Evaluation Evidence Plan

Use only existing validation evidence:

- LangChain Review Pack smoke
- OpenAI-compatible mock Review Pack smoke
- tampered bundle fail-closed test
- bad public key fail-closed test
- no private key copied
- secret sentinel no hit
- no network behavior
- `--json-errors` smoke
- generated metadata checks
- docs / release metadata consistency checks

Do not invent benchmark numbers, user counts, adoption metrics, comparative
performance claims, or external certification results.

The next technical note draft should present this evidence as a small table:

| Evidence item | What it supports | Boundary |
| --- | --- | --- |
| Smoke paths | The package can be produced from supported local examples. | Not a benchmark. |
| Fail-closed tests | Bad public keys and tampered bundles do not produce successful packs. | Does not prove all failure modes. |
| Secret sentinel checks | Configured sentinel values are not serialized into generated packs. | Not comprehensive DLP. |
| No private key copied | Private key artifacts are excluded from Review Pack output. | Does not assess external storage. |
| Metadata checks | Generated agent-facing metadata stays consistent. | Not an adoption claim. |

## Related Work Categories

Full citation selection is future work. The current categories are:

- agent tracing and observability platforms
- agent framework callback / event systems
- verifiable software artifacts
- software citation and metadata
- FDO / digital object metadata
- data-space accountability workflows
- AI governance tooling

The next writing cycle should choose specific citations only after the note
settles its target format.

## Claims and Non-Claims

| Claim type | Allowed wording | Forbidden wording |
| --- | --- | --- |
| Legal non-repudiation | Review Pack preserves verification status for review. | Review Pack provides legal non-repudiation or court-grade proof. |
| Compliance certification | Review Pack can support later compliance-oriented interpretation. | Review Pack is compliance certification. |
| AI Act approval | AI Act Pack remains future planning only. | Review Pack provides AI Act approval. |
| Official FDO standard | FDO mapping is conceptual research framing. | Review Pack is an official FDO standard or official FDO profile. |
| Full AI governance platform | Review Pack is a bounded reviewer-facing package. | Review Pack is a full AI governance platform. |
| Comprehensive DLP | `secret_scan_status` records configured sentinel checks and limitations. | Review Pack proves comprehensive DLP or proves all possible secrets are absent. |
| Hosted/remote review service | Review Pack is local and offline. | Review Pack is a hosted review service or remote review service. |

This table should be reused during future abstract, figure, and submission
review.

## Recommended Next Writing Step

Recommended next step:

```text
P47 docs-only drafting:
Review Pack V0.3 technical note v3
```

Purpose of v3:

- compress v2
- choose one abstract
- polish figures
- strengthen contribution framing
- add an evaluation evidence table
- keep boundaries explicit

Do not recommend immediate arXiv submission, workshop submission, AI Act Pack,
or new feature implementation.

## Readiness Checklist Before External Publication

- [ ] final abstract chosen
- [ ] contribution list stabilized
- [ ] diagrams redrawn cleanly
- [ ] evaluation evidence table added
- [ ] related work citations selected
- [ ] non-claims reviewed
- [ ] no invented metrics
- [ ] no legal/compliance overclaim
- [ ] version/release references checked
- [ ] DOI strategy checked

## Risks

- Overclaiming Review Pack as a compliance product.
- Overstating `secret_scan_status` as comprehensive DLP.
- Confusing Operation Accountability Profile with an official standard.
- Submitting too early before related work is mature.
- Turning the technical note into product marketing.
- Letting AI Act Pack language enter before the evidence layer is stable.

## Recommendation

Go for P47 technical note v3 drafting.

No-Go for AI Act Pack, arXiv submission, workshop submission, or new feature
implementation at this stage.
