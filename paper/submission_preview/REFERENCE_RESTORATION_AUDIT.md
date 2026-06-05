# Reference Restoration Audit

## Overall Verdict

Readiness verdict: bibliography completed; ready for layout patch.

Citation keys remain restored in the isolated submission preview without
changing the paper-minimal claim boundary. The original 12 matched BibTeX
entries remain present, and the seven previously missing entries now have local
BibTeX coverage documented in `BIBLIOGRAPHY_COMPLETION_AUDIT.md`.

## Restored Citation Keys

Restored citation key count: 19.

```text
acm2020artifactbadging
atkinson2019profiles
dona2018doip
herschel2017surveyprovenance
hu2014abac
iannella2018odrl
kahn2006framework
kent2006sp80092
knublauch2017shacl
moreau2013provdm
oliner2012loganalysis
schneier1999secureauditlogs
simmhan2005provenance
slsaBuildProvenance
slsaProvenance
soilandreyes2024evaluating
torresarias2019intoto
wright2022jsonschema
wright2022jsonschemavalidation
```

## Matched BibTeX Entries

Matched bibliography entry count: 19.

The first 12 matched entries came from existing repository BibTeX files:

- `paper/submission_tosem/references.bib`
- `paper/submission_tosem/acmart/references.bib`

The seven completion entries were normalized from existing repository reference
text, not from web search. Their provenance is recorded in
`BIBLIOGRAPHY_COMPLETION_AUDIT.md`.

Completed keys:

```text
acm2020artifactbadging
dona2018doip
kahn2006framework
slsaBuildProvenance
slsaProvenance
soilandreyes2024evaluating
torresarias2019intoto
```

No BibTeX entries were fabricated.

## Missing BibTeX Entries

Missing bibliography key count: 0.

`paper/submission_preview/MISSING_REFERENCES_PAPER_MINIMAL_V2.md` now records
all seven previously missing keys as recovered.

## Files Changed

Changed files in the original restoration pass:

- `paper/submission_preview/main_body_paper_minimal_v2.md`
- `paper/submission_preview/references_paper_minimal_v2.bib`
- `paper/submission_preview/citation_keys_paper_minimal_v2.txt`
- `paper/submission_preview/MISSING_REFERENCES_PAPER_MINIMAL_V2.md`
- `paper/submission_preview/BUILD_PREVIEW_AUDIT.md`
- `paper/submission_preview/PDF_LAYOUT_AND_REFERENCE_AUDIT.md`
- `paper/submission_preview/source_map_paper_minimal_v2.md`
- `paper/submission_preview/REFERENCE_RESTORATION_AUDIT.md`

Changed files in the bibliography-completion pass:

- `paper/submission_preview/references_paper_minimal_v2.bib`
- `paper/submission_preview/MISSING_REFERENCES_PAPER_MINIMAL_V2.md`
- `paper/submission_preview/BUILD_PREVIEW_AUDIT.md`
- `paper/submission_preview/PDF_LAYOUT_AND_REFERENCE_AUDIT.md`
- `paper/submission_preview/source_map_paper_minimal_v2.md`
- `paper/submission_preview/REFERENCE_RESTORATION_AUDIT.md`
- `paper/submission_preview/BIBLIOGRAPHY_COMPLETION_AUDIT.md`

## Scope Boundary Check

| check | result |
| --- | --- |
| official source files overwritten | false |
| `main_body.md` modified | false |
| `main_wrapper.tex` modified | false |
| `submission/` modified | false |
| paper-minimal example count changed | false |
| validator stages changed | false |
| non-claims changed | false |
| adjacent surfaces promoted to mainline | false |

The restoration and completion passes only reconnect preview sentences to local
citation keys and local bibliography entries. They do not add a new claim
family.

## Build Result

Build command:

```bash
bash paper/submission_preview/build_preview.sh
```

Observed result:

```text
generated: paper/submission_preview/build/main_body_paper_minimal_v2.tex
citation_key_count: 19
matched_bibliography_entry_count: 19
missing_bibliography_key_count: 0
generated: paper/submission_preview/build/main_wrapper_paper_minimal_v2.pdf
```

TeX generation result: passed.

PDF compile result: passed.

PDF path: `paper/submission_preview/build/main_wrapper_paper_minimal_v2.pdf`.

PDF page count: 6.

PDF file size: 106470 bytes.

The preview `.bib` includes a preamble bootstrap so the current preview
conversion path emits bibliography entries without changing the preview body,
wrapper, or build script. The next layout pass should address visible
markdown-style citation markers in the generated PDF.

## Reproduction Result

Status: PASS.

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

Status: PASS.

```text
./.venv/bin/python -m pytest tests/test_operation_accountability_profile.py tests/test_cli.py tests/test_review_pack_paper_minimal.py -q
26 passed, 1 warning
```

## Ruff Result

Status: PASS.

```text
./.venv/bin/ruff check agent_evidence/review_pack agent_evidence/cli/main.py tests/test_review_pack_paper_minimal.py
All checks passed!
```

## Suggested Next Codex Goal

Recommended fifteenth goal:

```text
Patch isolated submission-preview layout and citation rendering without
touching formal source files.
```

## Suggested Commit Message

```text
Complete submission preview bibliography from local sources
```
