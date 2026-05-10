# AEP-Media Mission 018 CLI and Archive Readiness Report

Date: 2026-05-10

## 1. Initial Failure Snapshot

Baseline targeted AEP-Media pytest result:

- `44 passed, 2 failed, 1 warning`

Failing tests:

- `tests/test_media_evaluation.py::test_cli_run_media_evaluation`
- `tests/test_media_release_pack.py::test_cli_build_aep_media_release_pack`

Baseline full pytest result:

- `148 passed, 5 failed, 1 skipped, 15 warnings`

Additional full-suite failures:

- `tests/test_media_submission_pack.py::test_cli_build_aep_media_submission_pack`
- `tests/test_media_ieee_word_pack.py::test_cli_build_ieee_word_pack`
- `tests/test_media_high_revision_pack.py::test_cli_build_high_revision_pack`

Missing command names:

- `run-media-evaluation`
- `build-aep-media-release-pack`
- `build-aep-media-submission-pack`
- `build-aep-media-ieee-word-pack`
- `build-aep-media-high-revision-pack`

Initial `agent-evidence --help` listed only the core agent evidence commands and did not expose the AEP-Media commands documented by README and tests.

## 2. Root Cause

The AEP-Media implementation modules and internal evaluation functions were present and working, but their entry points were not registered in the Click CLI. The issue was command wiring, not profile validation, bundle verification, strict-time validation, adapter parsing, or evaluation semantics.

## 3. Files Changed

Code:

- `agent_evidence/cli/main.py`

Tests:

- `tests/test_media_cli_registration.py`

Documentation and readiness reports:

- `docs/paper/softwarex/final/reports/aep_media_archive_doi_readiness.md`
- `docs/paper/softwarex/final/reports/repository_readiness_audit.md`
- `docs/reports/aep_media_mission017_softwarex_final_pack_report.md`
- `docs/reports/aep_media_mission018_cli_archive_readiness_report.md`
- `docs/STATUS.md`
- `plans/implementation-plan.md`

## 4. CLI Commands Registered

Mission 018 registers existing AEP-Media functionality without duplicating validator logic:

- `validate-media-profile`
- `build-media-bundle`
- `verify-media-bundle`
- `validate-media-time-profile`
- `ingest-linuxptp-trace`
- `ingest-ffmpeg-prft`
- `ingest-c2pa-manifest`
- `run-media-evaluation`
- `build-aep-media-release-pack`
- `build-aep-media-submission-pack`
- `build-aep-media-ieee-word-pack`
- `build-aep-media-high-revision-pack`

The capabilities payload command list was updated to match the registered Click command surface.

## 5. CLI Smoke Test Results

Passed:

- `agent-evidence validate-media-profile examples/media/minimal-valid-media-evidence.json`
- `agent-evidence build-media-bundle examples/media/minimal-valid-media-evidence.json --out /tmp/aep-media-cli-bundle-check`
- `agent-evidence verify-media-bundle /tmp/aep-media-cli-bundle-check`
- `agent-evidence validate-media-time-profile examples/media/time/minimal-valid-time-aware-media-evidence.json`
- `agent-evidence build-media-bundle examples/media/time/minimal-valid-time-aware-media-evidence.json --out /tmp/aep-media-cli-time-bundle-check`
- `agent-evidence verify-media-bundle /tmp/aep-media-cli-time-bundle-check --strict-time`
- `agent-evidence ingest-linuxptp-trace examples/media/adapters/linuxptp/ptp4l-sample.log --out /tmp/aep-media-cli-linuxptp-trace.json`
- `agent-evidence ingest-ffmpeg-prft examples/media/adapters/ffmpeg/ffprobe-prft-sample.json --out /tmp/aep-media-cli-ffmpeg-prft.json`
- `agent-evidence ingest-c2pa-manifest examples/media/adapters/c2pa/c2pa-manifest-valid-like.json --out /tmp/aep-media-cli-c2pa-manifest.json`

## 6. Targeted Pytest Result

Command:

```bash
./.venv/bin/python -m pytest tests/test_media_profile.py tests/test_media_bundle.py tests/test_media_time.py tests/test_media_adapters.py tests/test_media_evaluation.py tests/test_media_release_pack.py tests/test_media_cli_registration.py -q
```

Result:

- `48 passed, 1 warning`

## 7. SoftwareX / Readiness Test Result

Command:

```bash
./.venv/bin/python -m pytest tests/test_media_submission_pack.py tests/test_media_ieee_word_pack.py tests/test_media_high_revision_pack.py -q
```

Result:

- `23 passed, 1 warning`

## 8. Full Pytest Result

Command:

```bash
./.venv/bin/python -m pytest -q
```

Result:

- `155 passed, 1 skipped, 15 warnings`

The remaining warnings are dependency/runtime deprecation warnings and do not indicate an AEP-Media CLI blocker.

## 9. Evaluation CLI Results

Passed:

- Default evaluation: `PASS aep-media-evaluation@0.1 cases=18 unexpected=0`
- Adapter-inclusive evaluation: `PASS aep-media-evaluation@0.1 cases=26 unexpected=0 adapters=included`
- Optional-tool reporting evaluation: `PASS aep-media-evaluation@0.1 cases=23 unexpected=0 optional_tools=included`
- Combined adapter and optional-tool evaluation: `PASS aep-media-evaluation@0.1 cases=31 unexpected=0 adapters=included optional_tools=included`

## 10. Release Pack CLI Result

Passed:

- `PASS aep-media-release-pack@0.1`

## 11. DOI / Archive Readiness

Observed:

- `CITATION.cff` records repository DOI `10.5281/zenodo.19334062`.
- `.zenodo.json` contains AEP-Media-focused archive metadata.
- GitHub releases exist for the repository.

Current blocker:

- No confirmed AEP-Media-specific release DOI was found.

Result:

- Archive/DOI readiness: NEAR READY.
- Do not claim SoftwareX final READY until the AEP-Media release archive DOI is confirmed or created.

## 12. Red-Line Scan Result

Mission 018 keeps AEP-Media claims bounded:

- no positive legal-evidence claim;
- no positive non-repudiation claim;
- no positive trusted timestamping claim;
- no positive real PTP proof claim;
- no positive full MP4 PRFT parser claim;
- no positive real C2PA signature verification claim;
- no positive production deployment claim;
- no positive chain-of-custody claim.

Repository docs created in this mission avoid local home absolute paths.

## 13. SoftwareX Readiness After Mission 018

SoftwareX readiness: NEAR READY.

Reason:

- CLI blocker is fixed.
- Targeted tests pass.
- Full test suite passes.
- Evaluation CLI and release pack CLI pass.
- AEP-Media-specific release DOI/archive confirmation remains pending.

## 14. Remaining Blockers

1. Confirm or create an AEP-Media-specific archive DOI.
2. Update SoftwareX metadata and manuscript with that DOI when available.
3. Perform final human review of SoftwareX template output before upload.

## 15. Next Mission Recommendation

Mission 019 should prepare the AEP-Media release archive and complete the SoftwareX final submission metadata after a real archive DOI exists.
