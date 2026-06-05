# Final Preview Package Audit

## Overall Verdict

Readiness verdict: ready for claim-space conflict audit.

The isolated submission preview is internally consistent enough for the next
claim-space conflict audit. It is not cleared for official submission, formal
source replacement, or creation of a new external submission.

## Build Result

Observed command:

```bash
bash paper/submission_preview/build_preview.sh
```

| item | value |
| --- | --- |
| TeX generation result | passed |
| PDF compile result | passed |
| PDF path | `paper/submission_preview/build/main_wrapper_paper_minimal_v2.pdf` |
| PDF page count | 6 |
| PDF file size | 106275 bytes |
| citation key count | 19 |
| matched BibTeX entry count | 19 |
| missing bibliography key count | 0 |
| undefined citation count | 0 |
| undefined reference count | 0 |
| bibliography warning count | 0 |

## Layout Result

| warning type | count | classification |
| --- | ---: | --- |
| overfull hbox | 1 | non-blocking |
| underfull hbox | 20 | non-blocking |

The only remaining overfull warning is the known small path overflow in the
demo command text. The remaining underfull warnings are paragraph-quality
warnings. Layout risk classification: non-blocking.

## Reference Closure Result

Reference closure result: PASS.

| check | result |
| --- | --- |
| citation keys listed | 19 |
| matched BibTeX entries | 19 |
| missing bibliography keys | 0 |
| `references_paper_minimal_v2.bib` nonempty | true |
| undefined citations in final log | 0 |
| undefined references in final log | 0 |

## Source Isolation Result

Source isolation result: PASS.

| check | result |
| --- | --- |
| `main_body.md` modified | false |
| `main_wrapper.tex` modified | false |
| `submission/` modified | false |
| `paper/drafts/operation_accountability_boundary_full_v2.md` modified | false |
| preview source files modified in this audit | false |
| formal source files overwritten | false |
| `paper/submission_preview/build/` treated as generated output | true |

The preview remains isolated under `paper/submission_preview/`. Generated build
output was used only as audit evidence and should not be selected for commit.

## Scope Boundary Result

Scope boundary result: PASS.

The preview remains limited to:

- one operation accountability statement
- Execution Evidence and Operation Accountability Profile v0.1
- profile-aware validator
- one valid example
- three controlled invalid examples
- metadata-enrichment demo
- clean rerun
- paper-minimal review package

The validator-stage surface remains limited to:

- schema conformance
- reference closure
- cross-field consistency
- integrity digest recomputation

The non-claims remain present:

- no registry design
- no multi-agent orchestration
- no full FDO interoperability
- no full cryptographic trust fabric
- no legal non-repudiation
- no production deployment
- no broad platform governance
- no broad runtime integration coverage
- no compliance approval

Adjacent workstreams are not promoted into the preview's main contribution:
AEP-Media, AI Act, SoftwareX, and Sovereign-pFDO remain outside this preview
claim boundary. Strict forbidden phrase scan result: PASS.

## Review Package Result

Review package result: PASS.

Observed command:

```bash
./.venv/bin/agent-evidence review-pack create \
  --paper-minimal \
  --out /tmp/review-pack-paper-minimal-final-preview.zip
```

| item | value |
| --- | --- |
| CLI result | passed |
| CLI `ok` | true |
| package path | `/tmp/review-pack-paper-minimal-final-preview.zip` |
| resolved output path | `/private/tmp/review-pack-paper-minimal-final-preview.zip` |
| package SHA-256 | `fa5e1010ebc1388b6d7ab62318616a8d18458f675b7a8ba91d6344b4a8e56dc7` |
| package git commit | `dd95057` |
| manifest entry count | 17 |
| zip file count | 18 |
| manifest hash mismatches | 0 |
| manifest verification issues | 0 |
| `MANIFEST.json` self-listed | false |
| `CLAIM_BOUNDARY.md` includes `no compliance approval` as a non-claim | true |
| `PACKAGE_INFO.json` has `paper_minimal: true` | true |
| `PACKAGE_INFO.json` includes `no compliance approval` in `non_claims` | true |
| included examples | 1 valid and 3 controlled invalid examples |
| reproduce script executable | true |

`REPRODUCE.md` identifies the package as a paper-minimal inspection package.
`CLAIM_BOUNDARY.md` states that the package is not a complete standalone
software release.

## Reproduction Result

Reproduction result: PASS.

The rerun was executed in a temporary clone under `/tmp`, so the current
repository's `artifacts/` directory was not used as audit output.

| item | value |
| --- | --- |
| temporary clone HEAD | `dd95057` |
| rerun command | `bash scripts/reproduce_paper_minimal.sh` |
| summary `ok` | true |
| `valid_minimal` | pass |
| `invalid_missing_required` | pass, `schema_violation` |
| `invalid_unclosed_reference` | pass, `unresolved_output_ref` |
| `invalid_policy_link_broken` | pass, `unresolved_evidence_policy_ref` |
| `demo_metadata_enrichment` | pass |

## Pytest Result

Pytest result: PASS.

Observed command:

```bash
./.venv/bin/python -m pytest \
  tests/test_operation_accountability_profile.py \
  tests/test_cli.py \
  tests/test_review_pack_paper_minimal.py \
  -q
```

Observed result:

```text
26 passed, 1 warning
```

The warning is the existing Python 3.14 / Pydantic V1 compatibility warning
emitted by `langchain_core`.

## Ruff Result

Ruff result: PASS.

Observed command:

```bash
./.venv/bin/ruff check \
  agent_evidence/review_pack \
  agent_evidence/cli/main.py \
  tests/test_review_pack_paper_minimal.py
```

Observed result:

```text
All checks passed!
```

## External Submission Caution

External submission caution: ACTIVE.

The manuscript ledger is readable at `/Users/zhangbin/GitHub/MANUSCRIPT_STATUS.md`.
It records active TSE submission `TSE-2026-05-0426` with status
`Under review / 审核中` for `Operation-Accountability Boundaries for
Machine-Actionable Object Systems: A Profile and Validator`.

This preview is not cleared for new external submission until a separate
claim-space conflict audit is completed.

## Blocking Issues

- No blocking issue was found for the final preview package audit itself.
- New external submission remains blocked until the claim-space conflict audit
  resolves the active `TSE-2026-05-0426` overlap risk.

## Non-Blocking Issues

- One small overfull hbox warning remains.
- Twenty underfull hbox warnings remain.
- The active TSE ledger entry requires the next audit before any external route
  decision.

## Suggested Next Codex Goal

Run the claim-space conflict audit by reading `MANUSCRIPT_STATUS.md` and
comparing this preview against active TSE, AEP-Media, AI Act, SoftwareX, and
Sovereign-pFDO boundaries. Do not replace formal source files and do not create
a new external submission during that audit.

## Suggested Commit Message

```text
Audit final submission preview package readiness
```
