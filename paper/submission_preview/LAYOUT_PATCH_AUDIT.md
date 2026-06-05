# Layout Patch Audit

## Overall Verdict

Status: PASS.

Readiness verdict: ready for final preview package audit.

The layout pass reduced the isolated preview PDF from 11 overfull hbox warnings
to 1 and from 25 underfull hbox warnings to 20 while preserving citation
coverage, bibliography coverage, example count, validator stages, and the
paper-minimal claim boundary.

## Before Layout Warning Summary

Observed before this pass:

| warning type | count |
| --- | ---: |
| overfull hbox | 11 |
| underfull hbox | 25 |
| unresolved citation warnings in final log | 0 |
| unresolved reference warnings in final log | 0 |

Major causes:

- long shell commands in verbatim blocks
- visible markdown-style citation markers in generated TeX
- long command strings in preview tables
- long package path strings in preview tables

## After Layout Warning Summary

Observed after this pass:

| warning type | count |
| --- | ---: |
| overfull hbox | 1 |
| underfull hbox | 20 |
| unresolved citation warnings in final log | 0 |
| unresolved reference warnings in final log | 0 |

Remaining overfull warning:

```text
Overfull hbox (6.0pt too wide) ... demo/run_operation_accountability_demo.py
```

The remaining underfull warnings are paragraph-quality warnings around
validator explanations, package description text, and compact invalid-case
phrasing. They do not block the preview build.

## Files Changed

- `paper/submission_preview/main_body_paper_minimal_v2.md`
- `paper/submission_preview/main_wrapper_paper_minimal_v2.tex`
- `paper/submission_preview/build_preview.sh`
- `paper/submission_preview/BUILD_PREVIEW_AUDIT.md`
- `paper/submission_preview/PDF_LAYOUT_AND_REFERENCE_AUDIT.md`
- `paper/submission_preview/source_map_paper_minimal_v2.md`
- `paper/submission_preview/LAYOUT_PATCH_AUDIT.md`

## Patch Actions

| warning source | likely cause | patch action |
| --- | --- | --- |
| validation command block | long shell command | wrapped command with line continuation |
| review package command block | long shell command | wrapped command with line continuation |
| visible citation markers | preview conversion emitted markdown-style markers | switched preview conversion to citation-aware markdown and normalized to `\cite{...}` |
| expected-outcomes table | full command strings in table cells | replaced command strings with stable case identifiers while keeping full commands above the table |
| table overflow | long cells and package paths | scaled preview tables to page width and used compact table text |
| wrapper package support | paragraph-column tables and scaling need standard support packages | added `array`, `calc`, and `graphicx` |

## Remaining Warnings

| remaining warning | count | disposition |
| --- | ---: | --- |
| small demo path overfull | 1 | non-blocking |
| validator explanation underfull paragraphs | 11 | non-blocking |
| package description underfull paragraphs | 4 | non-blocking |
| invalid-case explanation underfull paragraphs | 5 | non-blocking |

## Boundary Checks

| check | result |
| --- | --- |
| claim boundary changed | false |
| citation keys changed | false |
| bibliography changed | false |
| official sources overwritten | false |
| `main_body.md` modified | false |
| `main_wrapper.tex` modified | false |
| `submission/` modified | false |
| example count changed | false |
| validator stages changed | false |
| review package boundary changed | false |
| adjacent surfaces promoted to mainline | false |

## PDF Build Result

```text
bash paper/submission_preview/build_preview.sh
generated: paper/submission_preview/build/main_body_paper_minimal_v2.tex
citation_key_count: 19
matched_bibliography_entry_count: 19
missing_bibliography_key_count: 0
generated: paper/submission_preview/build/main_wrapper_paper_minimal_v2.pdf
```

| item | value |
| --- | --- |
| PDF compile result | passed |
| PDF page count | 6 |
| PDF file size | 106275 bytes |
| citation key count | 19 |
| missing bibliography key count | 0 |

## Reproduction Result

The paper-minimal rerun was executed in a temporary clone to avoid modifying
the current repository's `artifacts/` directory.

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

## Suggested Next Codex Goal

```text
Run the final isolated preview package audit for build output, source map,
citation coverage, bibliography coverage, claim boundary, and TSE conflict
guard without replacing formal source files.
```

## Suggested Commit Message

```text
Patch submission preview layout warnings
```
