# AEP-Media Repository Readiness Audit for SoftwareX

Date: 2026-05-10

## Repository

- Repository URL: `https://github.com/joy7758/agent-evidence`
- Git remote: `https://github.com/joy7758/agent-evidence.git`
- GitHub visibility check: PUBLIC
- GitHub license check: Apache-2.0
- HTTP check: GitHub returned HTTP 200 for the repository URL.

Result: PASS.

## License

Files checked:

- `LICENSE`
- `pyproject.toml`
- `README.md`

Observed:

- `LICENSE` contains Apache License 2.0.
- `pyproject.toml` declares `license = "Apache-2.0"`.
- README exposes the repository and DOI.

Result: PASS.

## README

Before Mission 017, the README described `agent-evidence` but did not clearly expose the AEP-Media path. Mission 017 adds a concise section:

`AEP-Media: time-aware media evidence validation`

The section includes:

- purpose;
- install command;
- media profile validation command;
- bundle build/verify command;
- strict-time command;
- evaluation command;
- adapter-only boundary note;
- non-claims summary;
- links to specs, schemas, examples, demos, and reports.

Result: PASS after README update.

## Installation

Package metadata:

- package name: `agent-evidence`
- primary package: `agent_evidence`
- Python: 3.11+
- console script: `agent-evidence = "agent_evidence.cli.main:main"`

Recommended install command:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Result: PASS.

## Tests

Relevant test files observed:

- `tests/test_media_profile.py`
- `tests/test_media_bundle.py`
- `tests/test_media_time.py`
- `tests/test_media_adapters.py`
- `tests/test_media_evaluation.py`
- `tests/test_media_release_pack.py`
- `tests/test_media_submission_pack.py`
- `tests/test_media_ieee_word_pack.py`
- `tests/test_media_high_revision_pack.py`

Result: PASS.

## Examples

Observed:

- `examples/media/minimal-valid-media-evidence.json`
- controlled invalid examples under `examples/media/`
- strict-time examples under `examples/media/time/`
- adapter fixtures under `examples/media/adapters/`

Result: PASS.

## Specs and Schemas

Observed specs:

- `spec/aep-media-profile-v0.1.md`
- `spec/aep-media-bundle-v0.1.md`
- `spec/aep-media-time-trace-v0.1.md`
- `spec/aep-media-adapters-v0.1.md`

Observed schemas:

- `schema/aep_media_profile_v0_1.schema.json`
- `schema/aep_media_bundle_v0_1.schema.json`
- `schema/aep_media_time_trace_v0_1.schema.json`
- `schema/aep_media_adapter_report_v0_1.schema.json`

Result: PASS.

## Demos

Observed:

- `demo/run_media_evidence_demo.py`
- `demo/run_media_bundle_demo.py`
- `demo/run_media_time_demo.py`
- `demo/run_media_adapter_demo.py`
- `demo/run_media_evaluation_demo.py`
- release/submission pack builders under `demo/`

Result: PASS.

## DOI / Archive

Observed:

- `CITATION.cff` exists and records AEP-Media DOI `10.5281/zenodo.20107097`.
- `.zenodo.json` contains AEP-Media-specific metadata.
- GitHub release `aep-media-v0.1.0` exists.
- Zenodo record `20107097` exists.

Status:

- AEP-Media-specific archive DOI confirmed.
- DOI: `10.5281/zenodo.20107097`.

Result: READY.

## Overall Readiness

Repository readiness: READY.

Remaining blockers:

- Final SoftwareX submission pack review by the author before upload.

## Mission 018 Refresh

Mission 018 fixed the AEP-Media CLI registration blocker. The documented AEP-Media commands are now exposed by `agent-evidence --help`, and the targeted AEP-Media tests, SoftwareX/readiness tests, full pytest suite, media evaluation CLI commands, and release pack CLI command pass.

Current result:

- Targeted AEP-Media tests: `48 passed, 1 warning`
- SoftwareX/readiness tests: `23 passed, 1 warning`
- Full pytest: `155 passed, 1 skipped, 15 warnings`
- Default evaluation: `18 cases, unexpected=0`
- Adapter-inclusive evaluation: `26 cases, unexpected=0`
- Optional-tool reporting evaluation: `23 cases, unexpected=0`
- Combined evaluation: `31 cases, unexpected=0`

Repository readiness is READY after DOI confirmation and DOI-synchronized
SoftwareX pack refresh.
