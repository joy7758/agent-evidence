# AEP-Media v0.1.0

## Scope

Reusable research software for offline validation of time-aware media evidence bundles.

## Included Functionality

- AEP-Media evidence profile validator
- offline media bundle builder and verifier
- strict declared time-trace validator
- LinuxPTP-style trace ingestion adapter
- FFmpeg PRFT-style metadata ingestion adapter
- C2PA-like manifest ingestion adapter
- evaluation runner with default, adapter-inclusive, optional-tool, and combined matrices
- release/submission pack tooling
- examples, schemas, specs, demos, tests, and reports

## Verification Summary

- targeted tests: `48 passed, 1 warning`
- SoftwareX/readiness tests: `23 passed, 1 warning`
- full tests: `155 passed, 1 skipped, 15 warnings`
- evaluation default: `18 cases, unexpected=0`
- evaluation adapters: `26 cases, unexpected=0`
- evaluation optional tools: `23 cases, unexpected=0`
- evaluation combined: `31 cases, unexpected=0`
- release pack: `PASS aep-media-release-pack@0.1`

## Claim Boundary

AEP-Media supports local validation and fixture-based adapter ingestion. It does not claim legal admissibility, non-repudiation, trusted timestamping, real PTP proof, full MP4 PRFT parsing, real C2PA signature verification, chain of custody, or production deployment.

## Citation

Zenodo DOI: `10.5281/zenodo.20107097`.

Record: <https://zenodo.org/records/20107097>.
