# SoftwareX Requirement Map

Official source checked:

- SoftwareX Guide for Authors, ScienceDirect:
  <https://www.sciencedirect.com/journal/softwarex/publish/guide-for-authors>
- Fresh verification date: 2026-05-23.

| SoftwareX requirement or expectation | Current package status | Evidence source | Gap | Action needed |
|---|---|---|---|---|
| Short descriptive software paper | `paper_v1_0_submission_candidate.md` exists as a journal-style candidate. | `papers/opentelemetry-to-eeoap/paper_v1_0_submission_candidate.md` | Current draft is method-paper shaped, not SoftwareX-template shaped. | Rewrite as a short software article after route approval. |
| 3000-word limit | Current v1.0 candidate is about 3692 words. | `wc -w papers/opentelemetry-to-eeoap/paper_v1_0_submission_candidate.md` | Over the SoftwareX word limit. | Compress to below 3000 words excluding permitted metadata sections. |
| Open-source software distribution | Repository has source, tests, fixtures, generated outputs, and reproducibility notes. | `agent_evidence/`, `tools/`, `tests/`, `examples/opentelemetry/`, `generated/`, `frozen_v0_5/` | OpenTelemetry-to-EEOAP package is not yet cut as a public release candidate. | Prepare a clean release branch/package before submission. |
| Public GitHub repository | Remote is `https://github.com/joy7758/agent-evidence.git`. | `git remote -v` | Current OpenTelemetry-to-EEOAP branch/tags are local in this analysis. | Decide whether and when to push branch/tag or cut release. |
| Permanent software version link | Local immutable tags exist for EEOAP/AEP references. | `artifact_tagging_v1_3/TAG_RECORDS.md` | OpenTelemetry-to-EEOAP package does not yet have a pushed tag, release, archive, or DOI. | Decide public release/tag/archive strategy. |
| README.md | Root `README.md` exists and explains the broader `agent-evidence` package. | `README.md` | It is not focused on the OpenTelemetry-to-EEOAP adapter package. | Add or prepare SoftwareX-facing README material in a clean release branch. |
| LICENSE.txt or recognized open-source license | Root `LICENSE` exists and is Apache-2.0. `pyproject.toml` also declares `Apache-2.0`. | `LICENSE`, `pyproject.toml` | Official SoftwareX guidance names `LICENSE.txt`; this repo has `LICENSE`. | Either add `LICENSE.txt` in release branch or confirm `LICENSE` is acceptable. |
| Source code in `repo/src` | Source lives under `agent_evidence/`; adapter script lives under `tools/`. No `src/` directory was found. | `find . -maxdepth 2 -type d -name src -print` | SoftwareX guidance explicitly asks for source in `repo/src`. | Decide whether to restructure, create a release package with `src/`, or ask editorial office. |
| Software citation / persistent identifier | Root `CITATION.cff` and `codemeta.json` currently describe AEP-Media, not OpenTelemetry-to-EEOAP. | `CITATION.cff`, `codemeta.json` | No OpenTelemetry-to-EEOAP-specific software citation metadata. | Create package-specific citation metadata after release strategy is chosen. |
| Support material | Frozen package, clean-clone verification, checksums, adapter reports, generated statements, and external review brief exist. | `papers/opentelemetry-to-eeoap/frozen_v0_5/`, `generated/` | v0.5 support material predates v0.7 second trace; not yet cut as final SoftwareX supplement. | Build a final support-material package after release branch is clean. |
| Metadata table | Not prepared in SoftwareX form. | `paper_v1_0_submission_candidate.md`, v0.9 route notes | Missing SoftwareX metadata table. | Draft SoftwareX metadata table from `pyproject.toml`, tag records, and repository URL. |
| Data availability statement | Not final for SoftwareX. | v1.0 artifact availability note | Needs venue-specific wording. | Add data/software availability statement in SoftwareX draft. |
| Generative AI use declaration | Not final for SoftwareX. | v1.1 blockers and official guidance | Needs disclosure in the required manuscript location. | Draft declaration before venue formatting. |
| Conflict of interest declaration | Not final. | v1.1 blockers and official guidance | Missing submission-ready declaration. | Prepare final declaration. |
| Funding statement | Not final. | v1.1 blockers and official guidance | Missing submission-ready statement. | Prepare final funding statement. |
| Highlights | Not prepared in SoftwareX form. | Current manuscript files | Missing concise SoftwareX highlights. | Draft 3-5 highlights after article scope is fixed. |
| Graphical abstract optional | Not prepared. | Official guide mentions graphical abstract as a writing/formatting item. | Optional; may help but not required for route decision. | Defer unless the selected submission path benefits from it. |
| Article template requirement | Not venue-formatted. | Official SoftwareX guide | SoftwareX requires journal-specific templates. | Do not template until final route and release strategy are chosen. |

## Interpretation

The current package fits SoftwareX better than JSS/IST because the strongest
contribution is runnable research software with reproducibility evidence. It is
not yet SoftwareX-ready because the release state, source layout, citation
metadata, public artifact identifiers, and 3000-word template adaptation remain
open.
