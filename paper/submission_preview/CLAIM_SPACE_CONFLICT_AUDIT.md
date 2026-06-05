# Claim-Space Conflict Audit

## Overall Verdict

Verdict: blocked for external submission; allowed for local preparation.

The current isolated paper-minimal preview is internally coherent, but it is
not cleared for any new external submission. The manuscript ledger records
`TSE-2026-05-0426` as `Under review / 审核中`, and that active TSE line shares
the same operation-accountability claim-space as this preview. The preview may
continue as local source preparation, local build review, and internal claim
mapping only.

## Current Preview Claim Extraction

| field | extracted claim |
| --- | --- |
| title | `Operation Accountability as a First-Class Verification Boundary for Machine-Actionable Object Systems` |
| research question | Can one operation accountability statement be expressed and checked as a bounded verification object? |
| object of study | one operation accountability statement |
| profile | Execution Evidence and Operation Accountability Profile v0.1 |
| artifact surface | JSON profile, JSON Schema, profile-aware validator, examples, demo, rerun script, and paper-minimal review package |
| evidence surface | one valid example, three controlled invalid examples, one metadata-enrichment demo, clean rerun, and package manifest/boundary metadata |
| examples count | 1 valid / 3 invalid / 1 demo |
| validator stages | schema conformance; reference closure; cross-field consistency; integrity digest recomputation |
| review package role | paper-minimal inspection package, not a standalone software release |

Source evidence:

- `paper/drafts/operation_accountability_boundary_full_v2.md`
- `paper/submission_preview/main_body_paper_minimal_v2.md`
- `paper/submission_preview/main_abstract_paper_minimal_v2.tex`
- `paper/submission_preview/FINAL_PREVIEW_PACKAGE_AUDIT.md`
- `docs/PAPER_BOUNDARY_FREEZE.md`
- `docs/PAPER_MAINLINE.md`
- `docs/REPRODUCE_PAPER_MINIMAL.md`

## Current Preview Non-Claims

The preview remains bounded by these non-claims:

- no registry design
- no multi-agent orchestration
- no full FDO interoperability
- no full cryptographic trust fabric
- no legal non-repudiation
- no production deployment
- no broad platform governance
- no broad runtime integration coverage
- no compliance approval

The preview also does not run or rely on AEP-Media, AI Act, Automaton,
LangChain, OpenAI Agents, or full-repository integration tests.

## Active Manuscript Status Extraction

`/Users/zhangbin/GitHub/MANUSCRIPT_STATUS.md` was accessible.

| line | title | venue / system | manuscript ID | current status | conflict relevance |
| --- | --- | --- | --- | --- | --- |
| TSE v2 / operation-accountability rebuilt | `Operation-Accountability Boundaries for Machine-Actionable Object Systems: A Profile and Validator` | IEEE TSE / ScholarOne | `TSE-2026-05-0426` | `Under review / 审核中`; active | highest relevance; same operation-accountability claim-space |
| CSI / EEOAP | `A Minimal Execution Evidence Profile for Validator-Checkable AI Agent Operation Records in FAIR Digital Object-Inspired Data-Space Settings` | Computer Standards & Interfaces / Editorial Manager | `CSI-D-26-00686` | submission confirmed / active processing | nearby execution-evidence and operation-record claim-space |
| AI Act / B4 | `Engineering Compliance Evidence for High-Risk AI Systems under the EU AI Act` | IEEE TSE / Research Exchange | `TSE-2026-04-0381` | `Under Review`; active | separate B4 compliance line, but active and must not be mixed |
| Digital Biosphere / Supercomputing | `The Digital Biosphere: Distributed Active FDO Metadata Mapping Architectures for Machine-Actionable Data Spaces and the Distillation of Neural Logic` | The Journal of Supercomputing / SNAPP | SNAPP submission-details ID recorded in ledger | `With editor`; active | low direct overlap; data-space/FDO wording needs caution |
| SQJ / execution-evidence journal v2 | `A Minimal Execution-Evidence Profile for Bounded Reviewability of Agentic Software Runs` | Software Quality Journal / SNAPP | `40461fd0-9e8e-439e-af4d-46da34b96e4c v1.1` | `Submission received`; Technical Check stage | nearby execution-evidence line; no new parallel route without separation |
| eScience2026 / FAIR evidence object | `A FAIR Evidence Object Layer for Auditable Agent Self-Improvement` | EasyChair / eScience2026 | submission 65 | received; needs tracking | adjacent AEP / evidence-object line |
| IJDC / AEEP | `AEEP v0.1.0: A Minimal Metadata Profile for Reviewing Primary-Operator AI Agent Execution Evidence` | IJDC / OJS | submission 1144 | acknowledgement recorded | adjacent AEP/AEEP profile line |

Status interpretation is conservative. `Submission received`, `With editor`,
`Under Review`, and `Under review / 审核中` are not acceptance, publication,
positive review, artifact-badge approval, DOI creation, or official standard
adoption.

## Active TSE Comparison

Compared line: `TSE-2026-05-0426`.

| question | result |
| --- | --- |
| Same or nearby title? | Yes. The titles differ, but both center operation accountability boundaries for machine-actionable object systems. |
| Same core claim? | Yes. Both concern bounded operation-level reviewability and profile-aware validator evidence. |
| Same profile / validator / demo / review package? | Substantially overlapping. The active TSE ledger records a larger 3 valid / 7 invalid / 16 tests / 1 demo package; this preview is a narrower 1 valid / 3 invalid / 1 demo paper-minimal preview. |
| Same repository / artifact family? | Yes. Both are tied to the operation-accountability / EEOAP artifact family around `agent-evidence` and related local packages. |
| Is this preview merely local source preparation for an active claim-space? | Yes. It should be treated as local preparation only. |
| Duplicate submission risk if submitted externally now? | HIGH. |

Risk level: HIGH.

Required action: Do not submit this preview externally as a new manuscript while
`TSE-2026-05-0426` remains under review. If this preview is ever reused
externally, it must wait for the active decision or proceed only through a
proper venue mechanism such as replacement, withdrawal, revision, or a clearly
non-overlapping post-decision extension.

## AEP Comparison

Compared line: AEP / Agent Evidence Profile live-chain specimen.

| dimension | assessment |
| --- | --- |
| status | DCMI / AEP is rejected and closed in the ledger. |
| AEP object | runtime evidence bundle, live-chain specimen, offline verification, tamper failure, optional runtime provenance capture |
| current preview object | one operation accountability statement and profile-aware validator path |
| overlap object | evidence profile vocabulary and repository lineage |
| separation | AEP is bundle/live-chain oriented; this preview is statement-count and validator-stage oriented. |
| risk level | LOW if kept separate; MEDIUM if AEP live-chain specimen language is merged into the paper-minimal claim. |

Separation note: keep AEP as historical runtime-evidence lineage. Do not reuse
DCMI/AEP artifact status, DOI language, or live-chain specimen claims as
evidence for this preview.

## AEP-Media Comparison

Compared line: AEP-Media.

| dimension | assessment |
| --- | --- |
| status | SoftwareX and FSI:DI AEP-Media lines are recorded as rejected and closed in the current ledger summary. |
| AEP-Media object | local validation of time-aware media evidence bundles, media hashes, time traces, adapter ingestion, offline media bundle verification |
| current preview object | one operation accountability statement, EEOAP v0.1, validator stages, 1 valid / 3 invalid / 1 demo |
| overlap object | operation accountability terminology, repository, validator-style local checks |
| absent from preview | media artifacts, time-trace validation, LinuxPTP fixtures, FFmpeg/ffprobe fixtures, C2PA-like adapter ingestion, media bundle verification |
| risk level | LOW for duplicate submission while kept separate; MEDIUM historical confusion risk because the repository and some accountability vocabulary overlap. |

Separation note: do not import media evidence bundle claims, SoftwareX
artifact-package status, FSI:DI framing, media timing traces, or adapter
ingestion evidence into the current preview.

## AI Act Evidence Layer Comparison

Compared line: AI Act / B4.

| dimension | assessment |
| --- | --- |
| status | `TSE-2026-04-0381` is recorded as `Under Review`; EUSurvey contribution is recorded as public consultation evidence, not a publication. |
| AI Act object | high-risk AI compliance evidence line; runtime evidence bundle, operation accountability statement, and AI Act alignment manifest framing |
| current preview object | single operation accountability profile plus validator |
| overlap object | operation accountability statement vocabulary and evidence-review framing |
| separation | current preview does not contain an AI Act alignment manifest, legal/regulatory sufficiency claim, or compliance approval claim |
| risk level | MEDIUM, because a related TSE high-risk compliance line is active and the current preview must not be marketed as AI Act compliance evidence. |

Separation note: keep the AI Act line as B4 / high-risk compliance evidence.
This preview cannot be described as regulatory validation, legal sufficiency,
official compliance, or AI Act evidence-layer completion.

## Sovereign-pFDO Comparison

Compared line: Sovereign-pFDO / Scientific Reports.

| dimension | assessment |
| --- | --- |
| status | rejected and closed in the ledger. |
| Sovereign-pFDO object | protocol-driven distributed data governance and knowledge sovereignty framework |
| current preview object | one local operation accountability statement and validator |
| overlap object | FDO-adjacent language and machine-actionable object framing |
| separation | preview does not claim protocol-layer sovereignty, broad data governance, digital territory, hardware scalability, or legal-grade certainty |
| risk level | LOW if kept out of the preview; MEDIUM conceptual risk if broad protocol/governance narrative is reintroduced. |

Separation note: do not turn this preview into a Sovereign-pFDO or Digital
Biosphere argument. The current paper-minimal contribution is local,
statement-level, and validator-bounded.

## SoftwareX Comparison

Compared line: SoftwareX / AEP-Media.

| dimension | assessment |
| --- | --- |
| ledger status | summary row records SoftwareX / AEP-Media as rejected and closed; an older detailed paragraph still says `SOFTX-D-26-00495` was active |
| SoftwareX object | reusable research software for offline validation of time-aware media evidence bundles |
| current preview object | paper-minimal operation-accountability profile and validator path |
| overlap object | same repository and local validator/review-package vocabulary |
| separation | current preview does not claim SoftwareX artifact status, AEP-Media release readiness, media-bundle validation, or software-publication scope |
| risk level | LOW for direct duplicate submission if treated as closed; MEDIUM ledger-hygiene and historical-confusion risk. |

Ledger hygiene note: the current table and supplemental rejection notes support
treating SoftwareX as rejected and closed, while an older detail paragraph still
contains stale active-submission wording. This audit does not edit the ledger,
but future ledger cleanup should reconcile that stale detail paragraph.

## Duplicate Submission Risk Matrix

| compared line | status | overlap object | overlap claim | overlap artifact | risk level | required action before external submission |
| --- | --- | --- | --- | --- | --- | --- |
| TSE v2 / `TSE-2026-05-0426` | `Under review / 审核中`; active | operation-accountability statement/profile/validator | same core operation-accountability review-boundary claim | same repository/artifact family; active TSE has larger evidence package | HIGH | Do not submit externally as a new manuscript while active. Wait for decision or use proper venue replacement/withdrawal/revision mechanism. |
| CSI / EEOAP / `CSI-D-26-00686` | submission confirmed / active processing | execution evidence profile and operation record | nearby validator-checkable operation-record claim | local-only profile/review-package family | MEDIUM | Do not create another EEOAP / operation-record submission without a clear non-overlap memo and active-status update. |
| AI Act / `TSE-2026-04-0381` | `Under Review`; active | operation accountability statement vocabulary | adjacent compliance-evidence framing | separate B4 high-risk evidence package | MEDIUM | Keep B4 compliance and paper-minimal profile separate; no AI Act claims in this preview. |
| AEP / DCMI | rejected and closed | runtime evidence bundle lineage | related evidence-profile lineage, not same statement-count claim | AEP live-chain specimen, different package | LOW | Preserve as historical lineage only; do not import live-chain specimen claims. |
| AEP-Media / FSI:DI | rejected and closed | media evidence bundle | adjacent media operation-accountability vocabulary | media/time-trace/adapters, absent from preview | LOW | Keep media bundle and adapter claims out of this preview. |
| SoftwareX / AEP-Media | rejected and closed in summary; stale detail text remains | research-software artifact in same repo | adjacent software-artifact claim | AEP-Media v0.1.0 release and supplement, not current preview | LOW to MEDIUM | Reconcile ledger wording before route decisions; do not cite SoftwareX status as current or as support for this preview. |
| Sovereign-pFDO | rejected and closed | FDO/governance framing | broad protocol/governance narrative, not current profile-validator claim | separate conceptual manuscript | LOW | Keep protocol/governance narrative out of the current paper-minimal path. |
| Digital Biosphere / Supercomputing | `With editor`; active | FDO/data-space wording | low direct overlap but adjacent vocabulary | separate metadata-mapping architecture line | LOW | Avoid broad FDO/data-space mapping claims in this preview. |

## Required Action Before Any External Submission

Because active TSE `TSE-2026-05-0426` exists and the current preview has HIGH
claim-space overlap with that operation-accountability manuscript:

- Do not submit this preview externally as a new manuscript while the active
  TSE manuscript remains under review.
- Treat this preview as local source preparation only.
- Wait for decision, withdraw/replace only through proper venue mechanism, or
  clearly prepare a non-overlapping extension after decision.
- Re-check `MANUSCRIPT_STATUS.md` before any route decision.
- If a future extension is prepared, create a separate extension memo that
  proves new title, new research question, new contribution, new evidence set,
  and non-overlapping artifact scope.

## Current Allowed Actions

Allowed now:

- local source cleanup
- local build audit
- local review package audit
- internal claim mapping
- preparing response materials if tied to the active submission
- ledger hygiene review
- no external submission

Not allowed now:

- new external submission of this preview
- replacing formal submission source files
- presenting this preview as cleared for official submission
- merging AEP-Media, AI Act, Sovereign-pFDO, SoftwareX, or AEP live-chain
  claims into the preview
- treating `Under review`, `Under Review`, `With editor`, or `Submission
  received` as acceptance, publication, or positive review

## Blocking Issues

- Active TSE `TSE-2026-05-0426` is under review and overlaps the current
  preview at the operation-accountability claim-space level.
- CSI / EEOAP and AI Act active-status entries add nearby-route caution, even
  though they are separate lines.

## Non-Blocking Issues

- SoftwareX status wording in the ledger has a stale detailed paragraph that
  conflicts with the current summary-row closed status.
- AEP-Media, Sovereign-pFDO, and AEP are separable from the current preview, but
  their historical terminology can confuse route decisions if imported.

## Suggested Next Codex Goal

Run a manuscript-ledger hygiene audit that reconciles stale SoftwareX status
wording and produces a route-control note for operation-accountability,
EEOAP/CSI, AI Act/B4, AEP, AEP-Media, and Sovereign-pFDO without modifying
paper sources or creating external submission materials.

## Suggested Commit Message

```text
Audit claim-space conflicts for submission preview
```
