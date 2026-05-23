# Template Conversion Readiness Check

| Readiness item | Status | Evidence | Action before template conversion | Action before formal submission |
|---|---|---|---|---|
| Article draft | ready | `softwarex_article_draft_v1_13_readiness.md` | Use this draft as template source. | Final proofread after template conversion. |
| Word count | ready | `WORD_COUNT_NOTE.md`: `2258` total words, `1835` approximate body words | No action before template conversion. | Recount final template text. |
| Metadata table | partial | Metadata table in v1.13 draft | Keep unresolved public-release fields as TODOs. | Fill version, release URL, DOI/archive, docs, and contact fields. |
| Artifact availability wording | ready for draft | `ARTIFACT_AVAILABILITY_WORDING.md` | Use draft wording with explicit TODOs. | Replace with final public artifact statement. |
| Root metadata mismatch wording | ready | `ROOT_METADATA_MISMATCH_NOTE.md` | State root metadata describes AEP-Media. | Finalize release metadata or exception. |
| Source layout wording | ready | `SOURCE_LAYOUT_NOTE.md` | State adapter lives under `tools/`, package under `agent_evidence/`. | Decide whether explanation is enough or layout change is required. |
| Frozen package status wording | ready | `FROZEN_PACKAGE_STATUS_NOTE.md` | State v0.5 is historical internal freeze. | Create final release-candidate support package. |
| Declarations | partial | v1.8 draft declarations and v1.13 article | Keep draft wording. | Adapt to venue policy. |
| References | partial | v1.13 references | Keep TODO release references. | Replace with final release/archive identifiers. |
| Release strategy | partial | v1.12 release strategy | Use focused release-candidate branch as provisional strategy. | Execute public release/archive decision. |
| Tag push | deferred | local tags exist | No action before template conversion. | Decide and push only if selected. |
| DOI | deferred | no DOI exists | No action before template conversion. | Create only if archive route is selected. |
| GitHub Release | deferred | no GitHub Release exists | No action before template conversion. | Create only after release package is final. |
| Final clean-clone verification | deferred | historical and v1.5 checks exist | No action before template conversion. | Rerun on final release candidate. |

## Assessment

Template conversion can proceed after v1.13. The readiness draft is within the
SoftwareX word target and the remaining unresolved items are formal-submission
release actions, not template-conversion blockers. Release execution remains
deferred.
