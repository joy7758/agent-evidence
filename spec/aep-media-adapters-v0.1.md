# AEP-Media Adapters v0.1: Adapter-Only Ingestion Interfaces for LinuxPTP, FFmpeg PRFT, and C2PA-like Metadata

## 1. Purpose

AEP-Media Adapters v0.1 defines fixture-first ingestion interfaces for external-tool-style outputs. The adapters normalize LinuxPTP-style logs, ffprobe PRFT-style timing metadata, and C2PA-like manifest metadata into local artifacts that can be referenced by the existing AEP-Media profile, bundle, strict-time validation, and evaluation pack.

## 2. Adapter-only Scope

The adapters perform ingestion and normalization. They do not create a trusted external anchor, hardware proof, or legal evidence system. Reproducible tests use local fixtures and Python stdlib-compatible parsing.

## 3. LinuxPTP-style Trace Ingestion

The LinuxPTP adapter reads `ptp4l` or `phc2sys` style log lines, extracts offset, delay, sample time, and state, and writes an `aep-media-time-trace@0.1` JSON artifact. When the fixture does not contain UTC timestamps, the adapter may synthesize a stable fixture time window.

## 4. FFmpeg PRFT-style Timing Metadata Ingestion

The FFmpeg adapter reads ffprobe-style JSON and normalizes PRFT and timecode indicators into `aep-media-ffmpeg-prft-metadata@0.1`. This is not a direct MP4 box parser. A missing PRFT marker returns `ffmpeg_prft_not_found`.

## 5. C2PA-like Manifest Metadata Ingestion

The C2PA adapter reads C2PA-like manifest JSON and normalizes manifest id, claim generator, ingredients, assertions, and declared signature status into `aep-media-c2pa-manifest-metadata@0.1`. Fixture `declared_valid` is not equivalent to real C2PA signature verification.

## 6. Adapter Report Model

Each adapter writes an `aep-media-adapter-ingestion-report@0.1` report with adapter identity, source metadata, normalized output hash and size, claim boundary, issues, and PASS/FAIL summary.

## 7. Integration with AEP-Media Profile

Normalized adapter outputs can be included as AEP-Media artifacts. LinuxPTP output is referenced as `role=clock_trace`. FFmpeg timing metadata is referenced as `role=other`. C2PA-like metadata can be referenced by `provenance.c2pa_manifest_ref` as local manifest metadata.

## 8. Integration with Strict-time Bundle Verification

Adapter-generated LinuxPTP-style time traces can satisfy strict-time validation if the generated artifact hash, reference closure, time window, summary, and thresholds validate.

## 9. Optional External Smoke Paths

The FFmpeg and C2PA adapters expose optional external-tool flags. The evaluation command also exposes `--include-optional-tools`, which probes tool availability for `ptp4l`, `phc2sys`, `ffmpeg`, `ffprobe`, and `c2pa`.

These paths are environment-dependent and are not required for reproducible tests. The optional LinuxPTP path records version availability only; it does not automatically start `ptp4l` or `phc2sys`, because those processes require a real interface or PTP hardware clock and can affect host clock behavior.

## 10. Non-claims

- This adapter layer does not prove real PTP synchronization.
- This adapter layer does not verify hardware clock discipline.
- This adapter layer does not parse MP4 boxes directly in v0.1.
- This adapter layer does not prove that FFmpeg PRFT is present unless the supplied ffprobe output indicates it.
- This adapter layer does not create or verify real C2PA signatures by default.
- C2PA-like fixture ingestion is not equivalent to C2PA signature verification.
- Optional external tool smoke paths are environment-dependent and are not required for reproducible tests.
- The current claim is adapter ingestion plus local validation only.

## 11. Example Commands

```bash
agent-evidence ingest-linuxptp-trace examples/media/adapters/linuxptp/ptp4l-sample.log --out /tmp/aep-linuxptp-clock-trace.json
agent-evidence ingest-ffmpeg-prft examples/media/adapters/ffmpeg/ffprobe-prft-sample.json --out /tmp/aep-ffmpeg-prft-metadata.json
agent-evidence ingest-c2pa-manifest examples/media/adapters/c2pa/c2pa-manifest-valid-like.json --out /tmp/aep-c2pa-manifest-metadata.json
agent-evidence run-media-evaluation --out /tmp/aep-media-evaluation-with-adapters --include-adapters
agent-evidence run-media-evaluation --out /tmp/aep-media-evaluation-with-tools --include-optional-tools
```

## 12. Future Work

- Parse captured linuxptp traces from real deployments.
- Add an FFmpeg PRFT extraction adapter with pinned command capture.
- Add a C2PA CLI verification adapter with explicit signature result capture.
- Add external timestamping or transparency-log publication as a separate claim layer.
