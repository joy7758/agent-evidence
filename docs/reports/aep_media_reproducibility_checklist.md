# AEP-Media Reproducibility Checklist

## Environment Setup

- Use the repository virtual environment when available.
- Run commands from the repository root.
- The evaluation uses local declared-demo fixtures only.

## Command List

```bash
./.venv/bin/python -m pytest tests/test_media_profile.py tests/test_media_bundle.py tests/test_media_time.py tests/test_media_evaluation.py -q

./.venv/bin/agent-evidence validate-media-profile examples/media/minimal-valid-media-evidence.json
./.venv/bin/agent-evidence build-media-bundle examples/media/minimal-valid-media-evidence.json --out /tmp/aep-media-bundle-check
./.venv/bin/agent-evidence verify-media-bundle /tmp/aep-media-bundle-check

./.venv/bin/agent-evidence validate-media-time-profile examples/media/time/minimal-valid-time-aware-media-evidence.json
./.venv/bin/agent-evidence build-media-bundle examples/media/time/minimal-valid-time-aware-media-evidence.json --out /tmp/aep-media-time-bundle-check
./.venv/bin/agent-evidence verify-media-bundle /tmp/aep-media-time-bundle-check --strict-time

./.venv/bin/agent-evidence run-media-evaluation --out demo/output/media_evaluation_demo

./.venv/bin/python demo/run_media_evaluation_demo.py
```

## Expected Outputs

- media profile valid example passes;
- media bundle build and verify pass;
- strict time valid example passes;
- evaluation summary reports `unexpected_count: 0`;
- evaluation matrix contains at least 18 matched cases.

## Troubleshooting

- If bare `python` lacks `pytest`, use `./.venv/bin/python`.
- If `agent-evidence` is not in `PATH`, use `./.venv/bin/agent-evidence`.
