# Figure and Table Plan

## Figures

### Fig. 2

- Source file: `paper/tosem_cn/figures/fig2_profile_structure.mmd`
- Target role in paper:
  Concept figure for the minimal verifiable profile, with `operation` as the accountability center and `policy`, `provenance`, `evidence`, and `validation` as bound surrounding parts
- Current figure type:
  concept figure
- Still needs visual cleanup:
  yes
- Likely ACM/acmart formatting issue:
  Mermaid source must be exported to a stable figure format such as PDF or SVG; line weights, font sizing, and grayscale legibility should be checked after export

### Fig. 6

- Source file: `paper/tosem_cn/figures/fig6_validator_workflow.mmd`
- Target role in paper:
  Workflow figure for the two-layer validator path from input instance through structural checks, accountability checks, error classification, and pass/fail output
- Current figure type:
  workflow figure
- Still needs visual cleanup:
  yes
- Likely ACM/acmart formatting issue:
  Mermaid workflow nodes may become crowded after journal-column scaling; label shortening and landscape placement may be needed during export

### Fig. 7

- Source file: `paper/tosem_cn/figures/fig7_artifact_closure.mmd`
- Target role in paper:
  Artifact figure showing the reproducible closure from profile specification to release and DOI
- Current figure type:
  artifact figure
- Still needs visual cleanup:
  yes
- Likely ACM/acmart formatting issue:
  Linear pipeline diagrams can become too wide for standard journal layout; a wrapped or vertical export may be needed

## Tables

### Table 1

- Source file: `paper/tosem_cn/tables/table1_method_comparison.md`
- Target role in paper:
  Method-level qualitative comparison among ordinary logs, provenance-only, policy-only, audit-trail views, and the proposed method
- Current figure type:
  evaluation table
- Still needs visual cleanup:
  yes
- Likely ACM/acmart formatting issue:
  The number of comparison columns may exceed a narrow column width; the final layout may need `table*`, abbreviation, or column compaction

### Table 2

- Source file: `paper/tosem_cn/tables/table2_artifact_status.md`
- Target role in paper:
  Artifact-status table summarizing currently grounded repository assets
- Current figure type:
  evaluation table
- Still needs visual cleanup:
  yes
- Likely ACM/acmart formatting issue:
  Status phrasing should stay compact to avoid overlong cells in journal layout

### Table 3

- Source file: `paper/tosem_cn/tables/table3_validation_summary.md`
- Target role in paper:
  Evaluation table summarizing valid and invalid examples, expected outcomes, main error codes, and current evidence source
- Current figure type:
  evaluation table
- Still needs visual cleanup:
  yes
- Likely ACM/acmart formatting issue:
  File names and error codes may overrun standard column widths; line breaks or abbreviated headers may be required

### Table 4

- Source file: `paper/tosem_cn/tables/table4_portability_mini_matrix.md`
- Target role in paper:
  Evaluation table stabilizing the paper's limited portability claim
- Current figure type:
  evaluation table
- Still needs visual cleanup:
  yes
- Likely ACM/acmart formatting issue:
  Multi-clause cells may need aggressive shortening before LaTeX conversion to preserve readability

## Packaging Note

All current figure and table assets are content-complete enough for submission planning, but none of them are yet in final ACM/acmart-ready presentation form. The next packaging pass should convert figures first, then compact table wording where necessary to fit journal layout constraints.
