# Build Preview Audit

## Verdict

Status: ready for commit.

## Citation And Bibliography

| metric | value |
| --- | ---: |
| citation key count | 19 |
| matched bibliography entry count | 12 |
| missing bibliography key count | 7 |

The preview body now contains restored citation keys. Matched entries were
copied only from existing repository BibTeX files. Missing keys are tracked in
`MISSING_REFERENCES_PAPER_MINIMAL_V2.md`; no BibTeX entries were fabricated.

## Build Results

| check | result |
| --- | --- |
| TeX generation result | passed |
| PDF compile result | skipped |
| skip reason | bibliography incomplete |

Observed command:

```bash
bash paper/submission_preview/build_preview.sh
```

Observed output summary:

```text
generated: paper/submission_preview/build/main_body_paper_minimal_v2.tex
citation_key_count: 19
matched_bibliography_entry_count: 12
missing_bibliography_key_count: 7
WARNING: bibliography incomplete; PDF generation skipped.
missing keys written to: paper/submission_preview/build/missing_citation_keys.txt
```

Missing keys:

```text
acm2020artifactbadging
dona2018doip
kahn2006framework
slsaBuildProvenance
slsaProvenance
soilandreyes2024evaluating
torresarias2019intoto
```

The current build is not acceptable for final submission because restored
citations still have missing bibliography entries. This is an intentional
skip, not a TeX generation failure.

## Boundary Checks

| check | result |
| --- | --- |
| official sources overwritten | false |
| `submission/` modified | false |
| claim boundary changed | false |
