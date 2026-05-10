# AEP-Media SoftwareX Supplementary File S1

This is Supplementary file S1 for the SoftwareX submission for AEP-Media v0.1.0.

## Release and Archive

- Repository: <https://github.com/joy7758/agent-evidence>
- GitHub release: <https://github.com/joy7758/agent-evidence/releases/tag/aep-media-v0.1.0>
- Zenodo DOI: `10.5281/zenodo.20107097`
- Zenodo record: <https://zenodo.org/records/20107097>
- License: Apache-2.0

## Contents

- `REPRODUCIBILITY.md`: commands for installing and reproducing the main validation paths.
- `CLAIM_BOUNDARY.md`: the explicit local-validation boundary and non-claims.
- `SOFTWARE_INVENTORY.md`: major software modules, specs, schemas, examples, demos, and reports.
- `EVALUATION_SUMMARY.md`: final v0.1.0 evaluation and test outcomes.
- `CHECKSUMS.sha256`: checksums for supplement files.
- `reports/`: selected validation, reproducibility, claim-boundary, and DOI confirmation reports.
- `schemas/`: selected AEP-Media JSON schemas.
- `examples/`: selected valid and invalid media examples.
- `specs/`: selected AEP-Media profile and bundle specifications.

## Reproducibility Boundary

The baseline path uses local fixtures and does not require LinuxPTP, FFmpeg, ffprobe, or C2PA to be installed. Optional external tools can be reported when available, but their absence is not a failure of the fixture-based software artifact.

## v0.1.0 Validation Summary

- targeted AEP-Media tests: 48 passed, 1 warning;
- SoftwareX/readiness tests: 23 passed, 1 warning;
- full test suite: 155 passed, 1 skipped, 15 warnings;
- default evaluation: 18 cases, `unexpected=0`;
- adapter-inclusive evaluation: 26 cases, `unexpected=0`;
- optional-tool reporting evaluation: 23 cases, `unexpected=0`;
- combined adapter and optional-tool evaluation: 31 cases, `unexpected=0`;
- release pack: `PASS aep-media-release-pack@0.1`.

## Claim Boundary

AEP-Media supports local validation and fixture-based adapter ingestion. It does not claim legal admissibility, non-repudiation, trusted timestamping, real PTP proof, full MP4 PRFT parsing, real C2PA signature verification, chain of custody, production deployment, broad forensic sufficiency, or proof that the original media capture event was truthful, authorized, or unmodified before packaging.
