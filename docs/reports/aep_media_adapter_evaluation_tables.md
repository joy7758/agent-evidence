# AEP-Media Adapter Evaluation Tables

## Summary

category | cases | expected pass | expected fail | claim
--- | ---: | ---: | ---: | ---
adapter_ingestion | 8 | 5 | 3 | fixture ingestion plus local validation

## Cases

case_id | expected | primary success/failure condition
--- | --- | ---
adapter_linuxptp_ptp4l_valid | pass | ptp4l-style fixture normalizes to time trace
adapter_linuxptp_phc2sys_valid | pass | phc2sys-style fixture normalizes to time trace
adapter_linuxptp_empty_invalid | fail | `linuxptp_no_samples`
adapter_ffmpeg_prft_valid | pass | PRFT-style marker detected
adapter_ffmpeg_prft_missing_invalid | fail | `ffmpeg_prft_not_found`
adapter_c2pa_manifest_valid_like | pass | declared-valid C2PA-like metadata ingested
adapter_c2pa_manifest_invalid_signature_like | fail | `c2pa_signature_invalid_declared`
adapter_backed_strict_time_bundle_valid | pass | adapter-backed statement validates and strict-time bundle verifies

## Interpretation

The adapter matrix demonstrates that fixture-style external outputs can be normalized into AEP-Media artifacts and used by existing validation surfaces. No external tool is required for reproducible tests, and no real external verification claim is made.
