# PDF Layout and Reference Readiness Audit

## Overall Verdict

Submission readiness verdict: ready for layout patch.

The isolated submission preview now has restored citation keys and complete
local bibliography coverage. The build generates TeX and PDF from the preview
source with no missing bibliography keys. It is ready for a layout-focused pass,
not for formal source replacement.

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
| PDF file size | 106470 bytes |
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

| warning type | count | interpretation |
| --- | ---: | --- |
| overfull hbox | 11 | non-blocking layout risk |
| underfull hbox | 25 | non-blocking layout risk |
| undefined citation | 0 | no unresolved citation in final log |
| undefined reference | 0 | no unresolved cross-reference in final log |
| missing file warning | 0 | final build has a generated `.bbl` |
| bibliography warning | 0 | final build has bibliography entries |

The preview `.bib` uses a preamble bootstrap to make the current GFM-to-LaTeX
preview path emit bibliography entries without modifying the preview body,
wrapper, or build script. The generated PDF still shows markdown-style citation
markers in body text; that is a layout/source-preview issue for the next pass,
not a bibliography-completion blocker.

Most severe layout snippets from the build log:

| rank | log evidence |
| ---: | --- |
| 1 | `Overfull hbox (355.25523pt too wide) ... lines 489--507` |
| 2 | `Overfull hbox (288.0pt too wide) ... lines 226--226` |
| 3 | `Overfull hbox (180.0pt too wide) ... lines 429--429` |
| 4 | `Overfull hbox (180.0pt too wide) ... lines 429--429` |
| 5 | `Overfull hbox (168.0pt too wide) ... lines 429--429` |
| 6 | `Overfull hbox (156.0pt too wide) ... lines 429--429` |
| 7 | `Overfull hbox (107.16507pt too wide) ... lines 435--450` |
| 8 | `Overfull hbox (61.39897pt too wide) ... lines 267--273` |
| 9 | `Overfull hbox (36.0pt too wide) ... lines 429--429` |
| 10 | `Overfull hbox (24.0pt too wide) ... lines 170--170` |

Underfull warnings are concentrated around validator explanation paragraphs and
long code/path fragments. The overfull warnings are more important for the next
layout pass because they indicate visible line-width overflow from long command
strings, paths, and tables.

Layout risk classification: non-blocking for bibliography completion.

Rationale: the PDF builds successfully and has no unresolved citations or
cross-references in the final log. The remaining risk is visible formatting and
preview citation rendering quality, not missing bibliography metadata.

## Reference Readiness Summary

Completion update:

| item | restored result | completion result |
| --- | ---: | ---: |
| citation key count | 19 | 19 |
| matched bibliography entry count | 12 | 19 |
| missing bibliography key count | 7 | 0 |
| real BibTeX entry count | 12 | 19 |
| Related Work section present | yes | yes |
| Related Work citation keys present | yes | yes |

Updated reference readiness verdict: ready for layout patch.

The preview now has citation keys restored from local source material and full
local BibTeX coverage. The seven previously missing entries were recovered from
existing repository reference text and are documented in
`BIBLIOGRAPHY_COMPLETION_AUDIT.md`.

Historical pre-restoration state:

| item | result |
| --- | ---: |
| citation key count | 0 |
| matched bibliography entry count | 0 |
| missing bibliography key count | 0 |
| real BibTeX entry count | 0 |
| Related Work section present | yes |
| Related Work citation keys present | no |

Reference readiness classification before restoration: blocking for
submission-quality related work, non-blocking for build.

After restoration and bibliography completion, the remaining work is layout
quality and preview citation rendering, not reference recovery.

## Claim Boundary Result

Claim boundary result: PASS.

The preview remains within the paper-minimal path: one operation accountability
statement, Execution Evidence and Operation Accountability Profile v0.1, one
profile-aware validator path, one valid example, three controlled invalid
examples, one metadata-enrichment demo, one rerun path, and one review package.

Adjacent surfaces are not used as main claims. Compliance approval appears only
as a non-claim. No broad platform, legal assurance, deployment, or complete
interoperability claim is introduced by the PDF build or bibliography preview.

## Source Isolation Result

Source isolation result: PASS.

| check | result |
| --- | --- |
| `main_body.md` modified | false |
| `main_wrapper.tex` modified | false |
| `submission/` modified | false |
| preview body modified in this audit | false |
| preview abstract modified in this audit | false |
| preview wrapper modified in this audit | false |
| build output committed | false |
| `paper/submission_preview/build/` ignored | true |

The preview remains isolated under `paper/submission_preview/`. Build output is
generated under `paper/submission_preview/build/`, which is ignored by the
existing repository ignore rule for `build/`.

## Blocking Issues

No bibliography-completion blockers remain.

This is still not a signal to replace formal source files. The preview needs a
layout pass and citation-rendering cleanup before any formal-source decision.

## Non-Blocking Issues

1. PDF layout has 11 overfull hbox warnings and 25 underfull hbox warnings.
2. The most severe overfull warnings are caused by long commands, paths, and
   preview tables.
3. The generated PDF still displays markdown-style citation markers because the
   preview GFM conversion path does not render them as numeric citations.

## Verification

Paper-minimal rerun was executed in a temporary clone to avoid modifying the
current repository's `artifacts/` directory.

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

Recommended fifteenth goal:

```text
Patch the isolated submission preview layout and citation rendering only under
paper/submission_preview, without replacing formal source files.
```

The next pass should focus on long commands, long paths, tables, and
markdown-style citation marker rendering.

## Suggested Commit Message

```text
Complete submission preview bibliography from local sources
```
