# Bibliography Completion Audit

## Overall Verdict

Status: PASS.

Recovered bibliography entry count: 7.

Still missing bibliography key count: 0.

Readiness verdict: ready for layout patch.

The seven previously missing BibTeX entries were recovered from existing
repository reference text and normalized into
`paper/submission_preview/references_paper_minimal_v2.bib`. No web search was
used, no citation key was renamed, and no formal source file was modified.

## Recovered Entries

| key | status | source | entry handling | confidence |
| --- | --- | --- | --- | --- |
| `acm2020artifactbadging` | recovered | `docs/paper/softwarex/final/aep_media_softwarex_final_manuscript.md:187`; `docs/paper/aep_media_tse_submission_high_revision.md:262` | normalized | high |
| `dona2018doip` | recovered | `docs/paper/aep_media_tse_submission_high_revision.md:272`; `docs/paper/softwarex/final/aep_media_softwarex_final_manuscript.md:195` | normalized | high |
| `kahn2006framework` | recovered | `docs/paper/aep_media_tse_submission_high_revision.md:270`; `docs/paper/softwarex/final/aep_media_softwarex_final_manuscript.md:193` | normalized | high |
| `slsaBuildProvenance` | recovered | `docs/paper/aep_media_tse_submission_high_revision.md:268` | normalized | medium |
| `slsaProvenance` | recovered | `docs/paper/softwarex/final/aep_media_softwarex_final_manuscript.md:191` | normalized | medium |
| `soilandreyes2024evaluating` | recovered | `docs/paper/aep_media_tse_submission_high_revision.md:274` | normalized | high |
| `torresarias2019intoto` | recovered | `docs/paper/softwarex/final/aep_media_softwarex_final_manuscript.md:189`; `docs/paper/aep_media_tse_submission_high_revision.md:264` | normalized | high |

Normalization means that the local reference text contained enough metadata to
write a BibTeX entry with the existing citation key. The source text was not
invented or expanded beyond the recorded bibliographic fields.

## Still Missing Entries

| key | status | required action |
| --- | --- | --- |
| none | none | none |

## Sources Checked

Repository BibTeX files checked:

```text
paper/submission_tosem/references.bib
paper/submission_tosem/acmart/references.bib
paper/submission_preview/references_paper_minimal_v2.bib
```

Repository reference-text sources used:

```text
docs/paper/softwarex/final/aep_media_softwarex_final_manuscript.md
docs/paper/aep_media_tse_submission_high_revision.md
```

No external network lookup was used.

## Git History Search Summary

Exact BibTeX-entry search in git history found no existing `.bib` entries for
the seven missing keys. Historical text search confirmed these reference
families in tracked manuscript/reference text, which was used as the recovery
source. No branch checkout, reset, or old-file restoration was performed.

## Citation Coverage Result

| metric | value |
| --- | ---: |
| citation key count | 19 |
| matched bibliography entry count | 19 |
| missing bibliography key count | 0 |

Recovered keys:

```text
acm2020artifactbadging
dona2018doip
kahn2006framework
slsaBuildProvenance
slsaProvenance
soilandreyes2024evaluating
torresarias2019intoto
```

## PDF Build Result

Build command:

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

| item | value |
| --- | --- |
| TeX generation result | passed |
| PDF compile result | passed |
| skip reason | none |
| PDF path | `paper/submission_preview/build/main_wrapper_paper_minimal_v2.pdf` |
| PDF page count | 6 |
| PDF file size | 106470 bytes |
| overfull hbox warnings | 11 |
| underfull hbox warnings | 25 |
| unresolved citation warnings in final log | 0 |
| unresolved reference warnings in final log | 0 |

The preview `.bib` includes a preamble bootstrap so the existing preview build
chain emits bibliography entries without modifying the preview body, wrapper,
or build script. The next layout pass should handle visible markdown-style
citation markers in the generated PDF.

## Reproduction Result

The paper-minimal rerun was executed in a temporary clone to avoid modifying
the current repository's `artifacts/` directory.

```text
bash scripts/reproduce_paper_minimal.sh
ok: true
git_commit: a1a6630
```

Observed case results:

- `valid_minimal`: pass
- `invalid_missing_required`: pass, `schema_violation`
- `invalid_unclosed_reference`: pass, `unresolved_output_ref`
- `invalid_policy_link_broken`: pass, `unresolved_evidence_policy_ref`
- `demo_metadata_enrichment`: pass

## Pytest Result

```text
./.venv/bin/python -m pytest tests/test_operation_accountability_profile.py tests/test_cli.py tests/test_review_pack_paper_minimal.py -q
26 passed, 1 warning
```

## Ruff Result

```text
./.venv/bin/ruff check agent_evidence/review_pack agent_evidence/cli/main.py tests/test_review_pack_paper_minimal.py
All checks passed!
```

## Scope Boundary Result

| check | result |
| --- | --- |
| `agent_evidence/` modified | false |
| `tests/` modified | false |
| `examples/` modified | false |
| `demo/` modified | false |
| `README.md` modified | false |
| `main_body.md` modified | false |
| `main_wrapper.tex` modified | false |
| `submission/` modified | false |
| `paper/drafts/operation_accountability_boundary_full_v2.md` modified | false |
| build output selected for commit | false |
| unrelated staged files touched | false |

## Suggested Next Codex Goal

```text
Patch isolated submission-preview layout and citation rendering without
touching formal source files.
```

## Suggested Commit Message

```text
Complete submission preview bibliography from local sources
```
