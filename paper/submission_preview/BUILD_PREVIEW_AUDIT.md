# Build Preview Audit

## Verdict

Status: ready for commit.

Reference readiness verdict: ready for layout patch.

## Citation And Bibliography

| metric | value |
| --- | ---: |
| citation key count | 19 |
| matched bibliography entry count | 19 |
| missing bibliography key count | 0 |

The preview body contains 19 restored citation keys, and all 19 now have local
BibTeX entries in `references_paper_minimal_v2.bib`. Seven entries were
normalized from existing repository reference text with source provenance
recorded in `BIBLIOGRAPHY_COMPLETION_AUDIT.md`; no web search was used.

## Build Results

| check | result |
| --- | --- |
| TeX generation result | passed |
| PDF compile result | passed |
| skip reason | none |
| PDF path | `paper/submission_preview/build/main_wrapper_paper_minimal_v2.pdf` |
| PDF page count | 6 |
| PDF file size | 106470 bytes |

Observed command:

```bash
bash paper/submission_preview/build_preview.sh
```

Observed output summary:

```text
generated: paper/submission_preview/build/main_body_paper_minimal_v2.tex
citation_key_count: 19
matched_bibliography_entry_count: 19
missing_bibliography_key_count: 0
generated: paper/submission_preview/build/main_wrapper_paper_minimal_v2.pdf
```

Final LaTeX log summary:

| warning type | count |
| --- | ---: |
| overfull hbox | 11 |
| underfull hbox | 25 |
| unresolved citation warnings in final log | 0 |
| unresolved reference warnings in final log | 0 |

The preview `.bib` includes a BibTeX preamble bootstrap so the current
`pandoc --from=gfm` preview path emits the bibliography without modifying the
preview body, wrapper, or build script. This is a preview-build compatibility
measure only. The next layout pass should still replace visible markdown-style
citation markers in the generated PDF with normal rendered citations.

## Boundary Checks

| check | result |
| --- | --- |
| official sources overwritten | false |
| `submission/` modified | false |
| claim boundary changed | false |
