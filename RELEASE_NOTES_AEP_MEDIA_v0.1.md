# AEP-Media v0.1 Release Notes

## 1. What Is Included

- Minimal AEP-Media evidence profile.
- Offline media evidence bundle build and verify commands.
- Strict declared time-trace validation.
- LinuxPTP-style, FFmpeg PRFT-style, and C2PA-like adapter ingestion.
- Optional external-tool detection.
- Evaluation evidence pack and release pack generator.
- Paper scaffold and final claim boundary.

## 2. Missions Completed

- Mission 001: media evidence profile.
- Mission 002: offline bundle and tamper matrix.
- Mission 003: strict time trace validation.
- Mission 004: evaluation evidence pack.
- Mission 005: adapter-only ingestion.
- Mission 006: optional external-tool detection.
- Mission 007: release pack and manuscript scaffold.

## 3. Evaluation Summary

- Default evaluation: 18 cases, expected `unexpected=0`.
- Adapter-inclusive evaluation: at least 26 cases, expected `unexpected=0`.
- Optional-tool evaluation: at least 23 cases, expected `unexpected=0`, with missing tools skipped.

## 4. Adapter Support

Adapters ingest LinuxPTP-style logs, ffprobe PRFT-style JSON, and C2PA-like manifests into local metadata that can be carried in AEP-Media statements and bundles.

## 5. Optional External Tools

Optional external-tool probes detect ptp4l, phc2sys, ffmpeg, ffprobe, and c2pa. Missing tools are recorded as skipped, not fixture-path failures.

## 6. Claim Boundary

AEP-Media v0.1 supports local validation, fixture ingestion, offline bundle checks, strict declared time-trace checks, and optional-tool detection. It does not claim legal admissibility, non-repudiation, trusted timestamping, production deployment, broad forensic coverage, real PTP proof, full MP4 PRFT parsing, or real C2PA signature verification in the current environment.

## 7. Reproducibility Commands

```bash
./.venv/bin/python -m pytest tests/test_media_profile.py tests/test_media_bundle.py tests/test_media_time.py tests/test_media_evaluation.py tests/test_media_adapters.py tests/test_media_release_pack.py -q

./.venv/bin/agent-evidence run-media-evaluation --out /tmp/aep-media-evaluation-default

./.venv/bin/agent-evidence run-media-evaluation --out /tmp/aep-media-evaluation-with-adapters --include-adapters

./.venv/bin/agent-evidence run-media-evaluation --out /tmp/aep-media-evaluation-with-tools --include-optional-tools

./.venv/bin/agent-evidence build-aep-media-release-pack --out /tmp/aep-media-release-pack
```

## 8. Known Limitations

- No real PTP hardware validation in current environment.
- No real FFmpeg PRFT smoke result because tool unavailable.
- No real C2PA verification result because tool unavailable.
- No production deployment.
- No legal evidence claim.

## 9. Next Work

- Run optional tool path on a Linux host with LinuxPTP.
- Run ffprobe on a real PRFT-bearing MP4.
- Run c2pa CLI on a real signed asset.
- Keep these as separate environment-dependent evidence appendices.
