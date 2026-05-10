# Reproducibility

Run commands from the repository root.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Targeted AEP-Media Tests

```bash
./.venv/bin/python -m pytest tests/test_media_profile.py tests/test_media_bundle.py tests/test_media_time.py tests/test_media_adapters.py tests/test_media_evaluation.py tests/test_media_release_pack.py -q
```

## Evaluation Commands

```bash
./.venv/bin/agent-evidence run-media-evaluation --out /tmp/aep-media-softwarex-eval-default
./.venv/bin/agent-evidence run-media-evaluation --out /tmp/aep-media-softwarex-eval-adapters --include-adapters
./.venv/bin/agent-evidence run-media-evaluation --out /tmp/aep-media-softwarex-eval-optional --include-optional-tools
./.venv/bin/agent-evidence run-media-evaluation --out /tmp/aep-media-softwarex-eval-combined --include-adapters --include-optional-tools
```

## Expected Outcomes

- Default evaluation: 18 cases, `unexpected=0`.
- Adapter-inclusive evaluation: 26 cases, `unexpected=0`.
- Optional-tool reporting evaluation: 23 cases, `unexpected=0`.
- Combined adapter and optional-tool evaluation: 31 cases, `unexpected=0`.

These are local conformance and reporting checks. They do not require LinuxPTP, FFmpeg, ffprobe, or C2PA for the fixture-based path.
