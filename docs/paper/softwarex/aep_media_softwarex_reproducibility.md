# AEP-Media Reproducibility Notes

## Installation Assumptions

Use Python 3.11+ from the repository root. The repository declares package metadata in `pyproject.toml` and provides the `agent-evidence` console script.

Typical setup:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

If the console script is not on `PATH`, use `./.venv/bin/agent-evidence`.

## Targeted Tests

```bash
./.venv/bin/python -m pytest tests/test_media_profile.py tests/test_media_bundle.py tests/test_media_time.py tests/test_media_evaluation.py tests/test_media_adapters.py -q
```

Prior report value from Mission 005: `38 passed, 1 warning`. Rerun before SoftwareX submission.

## Default Media Evaluation

```bash
./.venv/bin/agent-evidence run-media-evaluation --out demo/output/media_evaluation_demo
```

Expected high-level outcome from Mission 004: 18 cases, `unexpected=0`.

## Adapter-inclusive Evaluation

```bash
./.venv/bin/agent-evidence run-media-evaluation --out demo/output/media_evaluation_with_adapters --include-adapters
```

Expected high-level outcome from Mission 005: 26 cases, `unexpected=0`.

## Optional-tool Reporting Evaluation

```bash
./.venv/bin/agent-evidence run-media-evaluation --out demo/output/media_evaluation_with_tools --include-optional-tools
```

Expected high-level outcome from Mission 006: 23 cases, `unexpected=0`; missing optional tools are reported as skipped.

## Combined Adapter and Optional-tool Evaluation

```bash
./.venv/bin/agent-evidence run-media-evaluation --out demo/output/media_evaluation_combined --include-adapters --include-optional-tools
```

Expected high-level outcome from prior release materials: 31 cases, `unexpected=0`. Rerun before SoftwareX submission and record current output.

## Media Bundle Build and Verify

```bash
./.venv/bin/agent-evidence build-media-bundle examples/media/minimal-valid-media-evidence.json --out /tmp/aep-media-bundle-check
./.venv/bin/agent-evidence verify-media-bundle /tmp/aep-media-bundle-check
```

Expected outcome: bundle build passes and verification returns `ok: true`.

## Strict-time Bundle Build and Verify

```bash
./.venv/bin/agent-evidence build-media-bundle examples/media/time/minimal-valid-time-aware-media-evidence.json --out /tmp/aep-media-time-bundle-check
./.venv/bin/agent-evidence verify-media-bundle /tmp/aep-media-time-bundle-check --strict-time
```

Expected outcome: strict-time bundle verification returns `ok: true`.

## Release Pack

```bash
./.venv/bin/agent-evidence build-aep-media-release-pack --out /tmp/aep-media-release-pack
```

Expected outcome: release pack summary reports `PASS aep-media-release-pack@0.1`.

## Reproducibility Boundary

The fixture path does not require LinuxPTP, FFmpeg, ffprobe, or C2PA to be installed. Optional external tools may be detected when present, but tool absence is a skipped condition rather than a failure of the fixture-based research artifact.
