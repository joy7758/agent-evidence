# AEP-Media Paper Evaluation Tables

This document records the paper-ready evaluation framing for AEP-Media. The generated pack writes the full machine-readable matrix to `evaluation-matrix.json` and the Markdown table to `evaluation-matrix.md`.

## Summary Table

category | cases | expected pass | expected fail | interpretation
--- | ---: | ---: | ---: | ---
media_profile | 4 | 1 | 3 | base media evidence objects validate or fail with controlled codes
media_bundle | 6 | 2 | 4 | bundles build, verify offline, and detect tamper/path escape
media_time | 8 | 2 | 6 | strict declared time traces validate and time tampering emits time-specific codes

## Required Case Families

case family | expected result
--- | ---
valid profile | pass
invalid profile missing `time_context` | fail with `missing_time_context`
invalid profile broken media hash | fail with `media_hash_mismatch`
invalid profile unresolved policy ref | fail with `unresolved_policy_ref`
valid bundle build and verify | pass
tampered bundle artifact | fail with checksum or media hash code
tampered bundle statement | fail with profile-specific code
path escape bundle | fail with `bundle_path_escape`
valid strict-time profile and bundle | pass
strict-time missing trace ref | fail with `missing_clock_trace_ref`
strict-time offset threshold | fail with `clock_offset_threshold_exceeded`
strict-time window mismatch | fail with `clock_trace_window_mismatch`

## Paper-ready Interpretation

The evaluation supports three bounded claims. First, a minimal media evidence object can be validated for structure, reference closure, local media hashes, and declared time context. Second, the same object can be packaged into an offline bundle whose contents can be reverified and whose controlled tampering cases fail. Third, declared or synthetic time evidence can be checked as a referenced trace artifact, including coverage windows, offset thresholds, and summary recomputation. The evaluation does not test real PTP, FFmpeg PRFT extraction, or C2PA signature verification.
