# PDF Layout and Reference Readiness Audit

## Overall Verdict

Submission readiness verdict: ready for final preview package audit.

The isolated submission preview now builds a 6-page PDF with complete local
bibliography coverage and a substantially reduced layout-warning surface. The
remaining warning set is non-blocking and should be checked once more during
the final preview package audit. This is still local preview preparation, not a
formal-source replacement or submission action.

## PDF Build Result

Build command:

```bash
bash paper/submission_preview/build_preview.sh
```

Observed result:

| item | value |
| --- | --- |
| TeX generation result | passed |
| PDF compile result | passed |
| PDF path | `paper/submission_preview/build/main_wrapper_paper_minimal_v2.pdf` |
| PDF page count | 6 |
| PDF file size | 106275 bytes |
| LaTeX log path | `paper/submission_preview/build/main_wrapper_paper_minimal_v2.log` |

Build output summary:

```text
generated: paper/submission_preview/build/main_body_paper_minimal_v2.tex
citation_key_count: 19
matched_bibliography_entry_count: 19
missing_bibliography_key_count: 0
generated: paper/submission_preview/build/main_wrapper_paper_minimal_v2.pdf
```

## Layout Warnings Summary

| warning type | before layout patch | after layout patch | interpretation |
| --- | ---: | ---: | --- |
| overfull hbox | 11 | 1 | one small non-blocking path overflow remains |
| underfull hbox | 25 | 20 | remaining warnings are paragraph-quality warnings |
| undefined citation | 0 | 0 | no unresolved citation in final log |
| undefined reference | 0 | 0 | no unresolved cross-reference in final log |
| missing file warning | 0 | 0 | final build has a generated `.bbl` |
| bibliography warning | 0 | 0 | final build has bibliography entries |

The layout pass replaced visible markdown-style citation markers in generated
TeX with numeric citation commands, wrapped long shell commands, shortened
table-facing case labels, and scaled preview tables. The only remaining
overfull warning is a 6pt overflow on the demo script path in the appendix
command block.

Remaining warnings:

| warning class | count | status |
| --- | ---: | --- |
| `Overfull hbox (6.0pt too wide) ... demo/run_operation_accountability_demo.py` | 1 | non-blocking |
| validator explanation underfull paragraphs | 11 | non-blocking |
| package description underfull paragraphs | 4 | non-blocking |
| invalid-case explanation underfull paragraphs | 5 | non-blocking |

Layout risk classification: non-blocking.

Rationale: the PDF builds successfully, citations resolve in the final log, the
page count remains 6, and the severe table and long-command overflows are gone.

## Reference Readiness Summary

| item | result |
| --- | ---: |
| citation key count | 19 |
| matched bibliography entry count | 19 |
| missing bibliography key count | 0 |
| real BibTeX entry count | 19 |
| Related Work section present | yes |
| Related Work citation keys present | yes |

Reference readiness verdict: complete for preview package audit.

No citation key was added, removed, or renamed in the layout pass. The
bibliography database was not modified.

## Claim Boundary Result

Claim boundary result: PASS.

The preview remains within the paper-minimal path: one operation accountability
statement, Execution Evidence and Operation Accountability Profile v0.1, one
profile-aware validator path, one valid example, three controlled invalid
examples, one metadata-enrichment demo, one rerun path, and one review package.

Adjacent surfaces are not used as main claims. Compliance approval appears only
as a non-claim. No broad platform, legal assurance, deployment, or complete
interoperability claim is introduced by the layout pass.

## Source Isolation Result

Source isolation result: PASS.

| check | result |
| --- | --- |
| `main_body.md` modified | false |
| `main_wrapper.tex` modified | false |
| `submission/` modified | false |
| formal source files overwritten | false |
| build output selected for commit | false |
| `paper/submission_preview/build/` ignored | true |

The preview remains isolated under `paper/submission_preview/`. Build output is
generated under `paper/submission_preview/build/`, which is ignored by the
existing repository ignore rule for `build/`.

## Verification

Paper-minimal rerun was executed in a temporary clone to avoid modifying the
current repository's `artifacts/` directory.

```text
bash scripts/reproduce_paper_minimal.sh
ok: true
git_commit: 348cc31
```

Observed case results:

- `valid_minimal`: pass
- `invalid_missing_required`: pass, `schema_violation`
- `invalid_unclosed_reference`: pass, `unresolved_output_ref`
- `invalid_policy_link_broken`: pass, `unresolved_evidence_policy_ref`
- `demo_metadata_enrichment`: pass

Pytest result:

```text
./.venv/bin/python -m pytest tests/test_operation_accountability_profile.py tests/test_cli.py tests/test_review_pack_paper_minimal.py -q
26 passed, 1 warning
```

Ruff result:

```text
./.venv/bin/ruff check agent_evidence/review_pack agent_evidence/cli/main.py tests/test_review_pack_paper_minimal.py
All checks passed!
```

## Suggested Next Codex Goal

Recommended sixteenth goal:

```text
Run the final isolated preview package audit for build output, source map,
citation coverage, bibliography coverage, claim boundary, and TSE conflict
guard without replacing formal source files.
```

## Suggested Commit Message

```text
Patch submission preview layout warnings
```
