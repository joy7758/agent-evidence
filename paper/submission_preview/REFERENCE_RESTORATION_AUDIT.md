# Reference Restoration Audit

## Overall Verdict

Readiness verdict: ready for bibliography completion.

Citation keys were restored to the isolated submission preview without changing
the paper-minimal claim boundary. Matched BibTeX entries were copied only from
existing repository `.bib` files. Seven restored citation keys still lack
reliable local BibTeX entries, so PDF generation is intentionally skipped after
TeX generation until bibliography completion is done.

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

Matched bibliography entry count: 12.

Matched entries were copied from existing repository BibTeX files:

- `paper/submission_tosem/references.bib`
- `paper/submission_tosem/acmart/references.bib`

Matched keys:

```text
atkinson2019profiles
herschel2017surveyprovenance
hu2014abac
iannella2018odrl
kent2006sp80092
knublauch2017shacl
moreau2013provdm
oliner2012loganalysis
schneier1999secureauditlogs
simmhan2005provenance
wright2022jsonschema
wright2022jsonschemavalidation
```

No BibTeX entries were fabricated.

## Missing BibTeX Entries

Missing bibliography key count: 7.

Missing keys are tracked in
`paper/submission_preview/MISSING_REFERENCES_PAPER_MINIMAL_V2.md`.

```text
acm2020artifactbadging
dona2018doip
kahn2006framework
slsaBuildProvenance
slsaProvenance
soilandreyes2024evaluating
torresarias2019intoto
```

## Files Changed

Changed files in this restoration pass:

- `paper/submission_preview/main_body_paper_minimal_v2.md`
- `paper/submission_preview/references_paper_minimal_v2.bib`
- `paper/submission_preview/citation_keys_paper_minimal_v2.txt`
- `paper/submission_preview/MISSING_REFERENCES_PAPER_MINIMAL_V2.md`
- `paper/submission_preview/BUILD_PREVIEW_AUDIT.md`
- `paper/submission_preview/PDF_LAYOUT_AND_REFERENCE_AUDIT.md`
- `paper/submission_preview/source_map_paper_minimal_v2.md`
- `paper/submission_preview/REFERENCE_RESTORATION_AUDIT.md`

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

The restoration only reconnects existing preview sentences to local citation
keys and local bibliography tracking. It does not add a new claim family.

## Build Result

Build command:

```bash
bash paper/submission_preview/build_preview.sh
```

Observed result:

```text
generated: paper/submission_preview/build/main_body_paper_minimal_v2.tex
citation_key_count: 19
matched_bibliography_entry_count: 12
missing_bibliography_key_count: 7
WARNING: bibliography incomplete; PDF generation skipped.
missing keys written to: paper/submission_preview/build/missing_citation_keys.txt
```

TeX generation result: passed.

PDF compile result: skipped.

Skip reason: bibliography incomplete.

This skip is intentional. The preview should not generate a PDF with unresolved
citations and should not be marked ready for official source conversion.

## Reproduction Result

Status: PASS.

The paper-minimal rerun was executed in a temporary clone to avoid modifying
the current repository's `artifacts/` directory.

```text
bash scripts/reproduce_paper_minimal.sh
ok: true
git_commit: 47117a1
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

Recommended fourteenth goal:

```text
Complete submission-preview bibliography entries for the seven missing keys
from existing reliable source material, without web search and without
fabricating BibTeX metadata.
```

## Suggested Commit Message

```text
Restore submission preview citations and bibliography tracking
```
