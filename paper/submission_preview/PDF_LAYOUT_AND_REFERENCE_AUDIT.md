# PDF Layout and Reference Readiness Audit

## Overall Verdict

Submission readiness verdict: ready for reference restoration.

The isolated submission preview can generate TeX and PDF. The PDF build is not
blocked. However, the preview is not ready for official source conversion
because the body contains a Related Work section but zero citation keys and zero
real bibliography entries. The next step should restore citations and local
bibliography entries from existing source material without expanding the paper
scope.

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
| PDF file size | 85770 bytes |
| LaTeX log path | `paper/submission_preview/build/main_wrapper_paper_minimal_v2.log` |

Build output summary:

```text
generated: paper/submission_preview/build/main_body_paper_minimal_v2.tex
citation_key_count: 0
matched_bibliography_entry_count: 0
missing_bibliography_key_count: 0
generated: paper/submission_preview/build/main_wrapper_paper_minimal_v2.pdf
```

## Layout Warnings Summary

| warning type | count | interpretation |
| --- | ---: | --- |
| overfull hbox | 11 | non-blocking layout risk |
| underfull hbox | 21 | non-blocking layout risk |
| undefined citation | 0 | no unresolved citation at build time |
| undefined reference | 0 | no unresolved cross-reference at build time |
| missing file warning | 1 | expected missing `.bbl` in zero-citation build |
| bibliography warning | 1 | expected missing `.bbl` in zero-citation build |

The single `.bbl` warning is not a build blocker in this preview because the
body has zero citation commands. It should not be interpreted as bibliography
readiness for submission.

Most severe layout snippets from the build log:

| rank | log evidence |
| ---: | --- |
| 1 | `Overfull hbox (355.25523pt too wide) ... lines 479--497` |
| 2 | `Overfull hbox (288.0pt too wide) ... lines 221--221` |
| 3 | `Overfull hbox (180.0pt too wide) ... lines 419--419` |
| 4 | `Overfull hbox (180.0pt too wide) ... lines 419--419` |
| 5 | `Overfull hbox (168.0pt too wide) ... lines 419--419` |
| 6 | `Overfull hbox (156.0pt too wide) ... lines 419--419` |
| 7 | `Overfull hbox (107.16507pt too wide) ... lines 425--440` |
| 8 | `Overfull hbox (61.39897pt too wide) ... lines 261--267` |
| 9 | `Overfull hbox (36.0pt too wide) ... lines 419--419` |
| 10 | `Overfull hbox (24.0pt too wide) ... lines 166--166` |

Underfull warnings are concentrated around validator explanation paragraphs and
long code/path fragments. The overfull warnings are more important for the next
layout pass because they indicate visible line-width overflow from long command
strings, paths, and tables.

Layout risk classification: non-blocking.

Rationale: the PDF builds successfully and has no undefined citations or
undefined cross-references. The remaining risk is visible formatting quality,
not build failure.

## Reference Readiness Summary

| item | result |
| --- | ---: |
| citation key count | 0 |
| matched bibliography entry count | 0 |
| missing bibliography key count | 0 |
| real BibTeX entry count | 0 |
| Related Work section present | yes |
| Related Work citation keys present | no |

Reference readiness classification: blocking for submission-quality related
work, non-blocking for build.

The preview compiles because there are no citation commands to resolve. That is
not enough for submission preparation. The Related Work section discusses
external bodies of work, but the preview currently has no formal citation keys.
Unless the citations were intentionally removed as a venue-specific decision,
the preview should not advance to official source conversion.

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

1. Submission-quality references are not ready: citation key count is 0 while a
   Related Work section is present.

This is not a build blocker. It is a blocker for official source conversion.

## Non-Blocking Issues

1. PDF layout has 11 overfull hbox warnings and 21 underfull hbox warnings.
2. The most severe overfull warnings are caused by long commands, paths, and
   preview tables.
3. The zero-citation build naturally has no `.bbl` file; this is non-blocking
   for build but reinforces that reference restoration should happen before
   official conversion.

## Verification

Paper-minimal rerun was executed in a temporary clone to avoid modifying the
current repository's `artifacts/` directory.

```text
bash scripts/reproduce_paper_minimal.sh
ok: true
git_commit: 5c3c48e
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

Recommended thirteenth goal:

```text
Restore submission-preview citations and local bibliography from existing known
source materials without web search and without expanding scope.
```

The restoration should use existing repository or prior-source material only,
and should not fabricate BibTeX entries.

## Suggested Commit Message

```text
Audit submission preview layout and references
```
