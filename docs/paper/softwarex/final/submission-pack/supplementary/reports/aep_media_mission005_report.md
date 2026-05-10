# AEP-Media Mission 005 Report

## 1. Mission 005 Goal

Mission 005 adds adapter-only ingestion interfaces for LinuxPTP-style traces, FFmpeg PRFT-style timing metadata, and C2PA-like manifest metadata. The goal is to show how external-tool-style outputs can enter the existing AEP-Media profile, bundle, strict-time, and evaluation workflows without claiming real external anchoring.

## 2. Adapter-only Boundary

The current claim is fixture ingestion plus local validation. Mission 005 does not prove real PTP synchronization, hardware clock discipline, MP4 box parsing, FFmpeg ground truth, C2PA signature verification, trusted timestamping, non-repudiation, legal admissibility, or complete compliance.

## 3. New Files

- `agent_evidence/adapters/linuxptp.py`
- `agent_evidence/adapters/ffmpeg_prft.py`
- `agent_evidence/adapters/c2pa_manifest.py`
- `agent_evidence/media_adapter_evaluation.py`
- `schema/aep_media_adapter_report_v0_1.schema.json`
- `spec/aep-media-adapters-v0.1.md`
- `examples/media/adapters/`
- `demo/run_media_adapter_demo.py`
- `tests/test_media_adapters.py`
- `docs/reports/aep_media_adapter_evaluation_tables.md`
- `docs/reports/aep_media_adapter_claim_boundary.md`

## 4. CLI Commands

```bash
agent-evidence ingest-linuxptp-trace <input_log> --out <out_json>
agent-evidence ingest-ffmpeg-prft <input> --out <out_json>
agent-evidence ingest-c2pa-manifest <input_manifest_json> --out <out_json>
agent-evidence run-media-evaluation --out <dir> --include-adapters
```

## 5. Fixture-based Test Results

- `./.venv/bin/python -m pytest tests/test_media_profile.py tests/test_media_bundle.py tests/test_media_time.py tests/test_media_evaluation.py tests/test_media_adapters.py -q`: `38 passed, 1 warning`
- `./.venv/bin/python -m pytest -q`: `115 passed, 1 skipped, 15 warnings`
- `./.venv/bin/python demo/run_media_adapter_demo.py`: `PASS aep-media-adapters@0.1 demo`
- `./.venv/bin/agent-evidence run-media-evaluation --out /tmp/aep-media-evaluation-default`: `PASS aep-media-evaluation@0.1 cases=18 unexpected=0`
- `./.venv/bin/agent-evidence run-media-evaluation --out /tmp/aep-media-evaluation-with-adapters --include-adapters`: `PASS aep-media-evaluation@0.1 cases=26 unexpected=0 adapters=included`

The fixture path does not require linuxptp, ffmpeg, ffprobe, or c2pa to be installed.

## 6. Optional External Tool Behavior

External tool paths are optional smoke paths only. If `ffprobe` or `c2pa` is unavailable, the adapters report explicit tool availability issues for those optional paths. The reproducible tests do not depend on external tools.

## 7. Adapter Evaluation Matrix

The adapter evaluation contains eight cases: two valid LinuxPTP-style logs, one invalid empty LinuxPTP log, valid and missing-PRFT ffprobe-style JSON, valid-like and invalid-signature-like C2PA manifests, and one adapter-backed strict-time bundle. The local run reported `case_count: 8`, `matched_count: 8`, and `unexpected_count: 0`.

## 8. Integration with Evaluation Pack

Default `run-media-evaluation` remains the Mission 004 18-case pack. Passing `--include-adapters` appends adapter cases and adds the `adapter_ingestion` category.

## 9. Non-claims

This mission only demonstrates adapter ingestion and local validation. It does not turn the project into a real PTP, FFmpeg, C2PA, legal evidence, or external anchoring system.

## 10. Next Mission Proposal

Mission 006, if needed, should remain optional smoke integration: captured linuxptp log ingestion, ffprobe command capture, and C2PA CLI verification capture with explicit environment metadata and no change to the current claim boundary.
