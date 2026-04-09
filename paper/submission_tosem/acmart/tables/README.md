# Table Assets

This directory contains the current LaTeX table assets for the acmart scaffold.

## Source Markdown Tables

- `paper/tosem_cn/tables/table1_method_comparison.md`
- `paper/tosem_cn/tables/table2_artifact_status.md`
- `paper/tosem_cn/tables/table3_validation_summary.md`
- `paper/tosem_cn/tables/table4_portability_mini_matrix.md`

## Generated LaTeX Table Assets

- `table1_method_comparison.tex`
- `table2_artifact_status.tex`
- `table3_validation_summary.tex`
- `table4_portability_mini_matrix.tex`

## Manual Cleanup Still Recommended

- Table 1 is the densest table and is the most likely to need one more readability pass if final page-count pressure becomes high.
- Table 3 should be rechecked once final copyediting settles, because file names and error codes are naturally width-sensitive.
- Table 4 is structurally stable, but its prose cells should be rechecked after the final compile to confirm that the “supports / does not support” contrast remains easy to scan.
