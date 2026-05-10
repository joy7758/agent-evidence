# AEP-Media Time Trace v0.1: Declared Time Evidence for Media Evidence Validation

## 1. Purpose

AEP-Media Time Trace v0.1 defines a declared or synthetic clock trace artifact that can be referenced from an AEP-Media evidence statement and checked by a strict time validator. The purpose is to make the time layer inspectable: a statement can bind its `time_context` to a local `clock_trace` media artifact, and the validator can check trace hash, reference closure, time-window coverage, sample validity, summary recomputation, and thresholds.

This is a strict validation layer on top of the base AEP-Media Profile v0.1. It is not a hardware clock proof.

## 2. Time Trace Structure

A time trace JSON object contains:

- `profile`: fixed identity, `aep-media-time-trace@0.1`.
- `trace_id`: local trace identifier.
- `trace_type`: `declared_ptp_trace`, `declared_system_clock_trace`, or `synthetic_time_trace`.
- `collection`: declared collection source, collector, and collection start/end UTC timestamps.
- `sync`: declared source, sync status, optional PTP-like fields.
- `thresholds`: maximum acceptable absolute offset and jitter values in nanoseconds.
- `samples`: one or more timestamped offset samples.
- `summary`: declared sample count, maximum absolute offset, maximum jitter, and threshold result.

## 3. Relationship To AEP-Media Profile

The base AEP-Media Profile keeps `time_context.clock_trace_refs` optional. Strict time validation makes it required without changing the base profile. Every strict-time statement must:

- include a non-empty `time_context.clock_trace_refs`;
- resolve each referenced id to `media.artifacts[].id`;
- use `role: "clock_trace"` for each referenced trace artifact;
- keep clock trace artifact paths local to the statement or bundle;
- keep primary media artifacts bound to `time_context.id`.

## 4. Strict Time Validation Checks

The strict validator performs the base media profile validation first and then applies time-specific checks:

- clock trace reference presence and closure;
- clock trace artifact role, file presence, hash, and JSON parse;
- clock trace profile identity and schema conformance;
- collection window coverage of the statement time context;
- non-empty samples, parseable sample timestamps, non-decreasing sample order, numeric offsets, and valid states;
- summary recomputation for sample count, max absolute offset, max jitter, and `within_threshold`;
- threshold checks for offset and jitter;
- primary media time binding.

## 5. Error Codes

Representative strict-time error codes include:

- `missing_clock_trace_ref`
- `unresolved_clock_trace_ref`
- `invalid_clock_trace_artifact_role`
- `clock_trace_artifact_not_found`
- `clock_trace_hash_mismatch`
- `clock_trace_profile_mismatch`
- `clock_trace_parse_error`
- `clock_trace_window_mismatch`
- `invalid_clock_trace_samples`
- `clock_trace_summary_mismatch`
- `clock_offset_threshold_exceeded`
- `clock_jitter_threshold_exceeded`
- `missing_media_time_context_ref`
- `media_time_context_mismatch`

## 6. Non-claims

- This profile does not perform real PTP synchronization.
- This profile does not verify hardware clock discipline.
- This profile does not parse real MP4 PRFT boxes in v0.1.
- This profile does not verify trusted timestamps.
- This profile does not create or verify real C2PA signatures.
- This profile validates declared or synthetic time trace artifacts only.
- It should not be interpreted as legal-grade timing proof.

## 7. Future Integration Points

- linuxptp ptp4l / phc2sys trace ingestion
- FFmpeg PRFT extraction
- GStreamer GstPtpClock capture metadata
- C2PA manifest signing and verification
- external timestamping or transparency log anchoring

## 8. Example Commands

```bash
agent-evidence validate-media-time-profile examples/media/time/minimal-valid-time-aware-media-evidence.json
agent-evidence validate-media-time-profile examples/media/time/invalid-clock-offset-threshold.json
agent-evidence build-media-bundle examples/media/time/minimal-valid-time-aware-media-evidence.json --out /tmp/aep-media-time-bundle-check
agent-evidence verify-media-bundle /tmp/aep-media-time-bundle-check --strict-time
python demo/run_media_time_demo.py
```
