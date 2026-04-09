# TOSEM Submission Package Outline

## 1. Title / Abstract / Keywords

- Source: `paper/tosem_en/00_title_abstract_keywords.md`
- Current status: stable English front package available
- Packaging note: still needs ACM metadata fields such as CCS concepts, author block, and publication-oriented front-matter formatting

## 2. Main Sections

- Introduction: `paper/tosem_en/01_introduction.md`
- Contributions and scope boundary: `paper/tosem_en/02_contributions_and_scope.md`
- Methods / profile / validator: `paper/tosem_en/04_methods_profile_and_validator.md`
- Evaluation: `paper/tosem_en/05_evaluation.md`
- Related work: `paper/tosem_en/06_related_work.md`
- Discussion / limits / threats: `paper/tosem_en/07_discussion_limits_threats.md`
- Conclusion: `paper/tosem_en/08_conclusion.md`
- Packaging note: these sections already form a coherent full draft in `paper/tosem_en/manuscript_en.md`, but still need template-aware merging and section-level formatting decisions

## 3. Figures

- Fig. 2: profile structure
- Fig. 6: validator workflow
- Fig. 7: artifact closure
- Packaging note: all current figure sources are Mermaid files and will need export into submission-ready figure assets with stable captions and numbering

## 4. Tables

- Table 1: method comparison
- Table 2: artifact status
- Table 3: validation summary
- Table 4: portability mini-matrix
- Packaging note: all current table sources are Markdown tables and will need conversion into acmart-compatible table environments or equivalent layout decisions

## 5. Artifact Availability Note

- Source: `submission/artifact-availability.md`
- Current status: aligned to repository release `v0.2.0` and Zenodo DOI `10.5281/zenodo.19334062`
- Packaging note: still needs placement and wording decisions inside the final submission template

## 6. References Plan

- Source planning file: `paper/submission_tosem/reference_plan.md`
- Current status: citation categories are clear, but the manuscript still lacks an actual bibliography set

## 7. Remaining Submission Blockers

- Core citations are not yet selected and integrated into the manuscript
- Mermaid figures are not yet exported into submission-ready assets
- Markdown tables are not yet mapped into acmart-ready table layouts
- CCS concepts and ACM front-matter metadata are still placeholders
- No acmart-based main submission file exists yet
