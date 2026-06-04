# Submission Preview Audit

## Verdict

Preview readiness verdict: generated as an isolated submission source preview.

The full v2 audit verdict is: ready to convert into submission source.

Blocking issue count for this preview: 0.

Non-blocking issue count for this preview: 0.

## Scope Check

| check | result |
| --- | --- |
| source preview generated without overwriting official source | PASS |
| `main_body.md` untouched | PASS |
| `main_wrapper.tex` untouched or absent | PASS |
| `submission/` untouched | PASS |
| preview files confined to `paper/submission_preview/` | PASS |
| source body derived from `operation_accountability_boundary_full_v2.md` | PASS |
| title and abstract removed from preview body | PASS |
| abstract extracted into standalone TeX fragment | PASS |
| wrapper generated as an independent preview wrapper | PASS |

## Evidence Boundary

The example count remains:

- 1 valid example
- 3 controlled invalid examples
- 1 metadata-enrichment demo

The validator stages remain four:

- schema conformance
- reference closure
- cross-field consistency
- integrity digest recomputation

The non-claims remain:

- no registry design
- no multi-agent orchestration
- no full FDO interoperability
- no full cryptographic trust fabric
- no legal non-repudiation
- no production deployment
- no broad platform governance
- no broad runtime integration coverage
- no compliance approval

The review package remains an inspection package, not a standalone software
distribution.

## Adjacent-Surface Check

AEP-Media, AI Act, and Sovereign-pFDO are not used as main claims in the
preview manuscript body, abstract, or wrapper.

## Preview Build Check

Build command:

```bash
bash paper/submission_preview/build_preview.sh
```

Status: PASS for source preview generation.

Observed result:

```text
generated: paper/submission_preview/build/main_body_paper_minimal_v2.tex
WARNING: bibliography file submission/58_references_tse.bib was not found; PDF generation skipped.
build_preview_exit: 0
```

The configured wrapper still uses `submission/58_references_tse` as the
bibliography target. The current checkout does not contain
`submission/58_references_tse.bib`, so PDF generation was skipped after the
temporary TeX body was generated. No output was written to `dist/`, `tmp/`, or
`artifacts/`.

## Mainline Verification

Rerun command:

```bash
bash scripts/reproduce_paper_minimal.sh
```

Status: PASS in a temporary clone.

Observed summary:

```text
ok: true
git_commit: 18385d3
valid_minimal: pass
invalid_missing_required: pass, schema_violation
invalid_unclosed_reference: pass, unresolved_output_ref
invalid_policy_link_broken: pass, unresolved_evidence_policy_ref
demo_metadata_enrichment: pass
```

Pytest command:

```bash
./.venv/bin/python -m pytest tests/test_operation_accountability_profile.py tests/test_cli.py tests/test_review_pack_paper_minimal.py -q
```

Status: PASS.

Observed result:

```text
26 passed, 1 warning
```

Ruff command:

```bash
./.venv/bin/ruff check agent_evidence/review_pack agent_evidence/cli/main.py tests/test_review_pack_paper_minimal.py
```

Status: PASS.

Observed result:

```text
All checks passed!
```

## Preview File Checks

Observed structural checks:

```text
all_expected_files_present: true
abstract_words: 195
body_words: 3094
abstract_env_absent: true
body_title_abstract_absent: true
readme_no_overwrite_phrase: true
```

Forbidden expansion phrase check:

```text
strict_forbidden_phrase_rg_exit: 1
```

The strict forbidden phrase search found no expansion phrasing in the preview
directory.
