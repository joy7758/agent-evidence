# AEP-Media Final Reproducibility Checklist

## 1. Environment

Use the repository virtual environment. The fixture-only path does not require LinuxPTP, FFmpeg, ffprobe, or C2PA CLI.

## 2. Install

Install project dependencies into `.venv` if they are not already present.

## 3. Run Core Tests

```bash
./.venv/bin/python -m pytest tests/test_media_profile.py tests/test_media_bundle.py tests/test_media_time.py tests/test_media_evaluation.py tests/test_media_adapters.py -q

./.venv/bin/python -m pytest -q
```

## 4. Run Default Evaluation

```bash
./.venv/bin/agent-evidence run-media-evaluation --out /tmp/aep-media-evaluation-default
```

## 5. Run Adapter Evaluation

```bash
./.venv/bin/agent-evidence run-media-evaluation --out /tmp/aep-media-evaluation-with-adapters --include-adapters
```

## 6. Run Optional-tool Evaluation

```bash
./.venv/bin/agent-evidence run-media-evaluation --out /tmp/aep-media-evaluation-with-tools --include-optional-tools
```

## 7. Build Release Pack

```bash
./.venv/bin/agent-evidence build-aep-media-release-pack --out /tmp/aep-media-release-pack

./.venv/bin/python demo/build_aep_media_release_pack.py
```

## 8. Expected Outputs

- Default evaluation: 18 cases, unexpected=0.
- Adapter evaluation: at least 26 cases, unexpected=0.
- Optional-tool evaluation: at least 23 cases, unexpected=0; missing external tools are skipped.
- Release pack: `release-summary.json`, `claim-boundary.md`, `artifact-inventory.json`, `checksums.sha256`, and paper scaffold.

## 9. Troubleshooting

- If bare python lacks pytest, use `.venv`.
- If `agent-evidence` is not in PATH, use `./.venv/bin/agent-evidence`.
- If ffmpeg, ffprobe, c2pa, or LinuxPTP tools do not exist, optional tools are skipped and fixture-only reproducibility is unaffected.
- On macOS, do not directly run ptp4l or phc2sys clock discipline commands unless there is a clear Linux PTP environment and an explicit run window.
