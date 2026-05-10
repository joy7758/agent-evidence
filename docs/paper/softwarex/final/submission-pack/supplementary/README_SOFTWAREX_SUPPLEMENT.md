# AEP-Media SoftwareX Supplement

This supplement supports the SoftwareX submission for AEP-Media.

## Contents

- `REPRODUCIBILITY.md`: commands for installing and reproducing the main validation paths.
- `CLAIM_BOUNDARY.md`: the explicit local-validation boundary and non-claims.
- `SOFTWARE_INVENTORY.md`: major software modules, specs, schemas, examples, demos, and reports.
- `EVALUATION_SUMMARY.md`: expected evaluation matrix outcomes from the release reports.
- `CHECKSUMS.sha256`: checksums for supplement files.
- `reports/`: selected AEP-Media mission and evaluation reports.
- `schemas/`: selected AEP-Media JSON schemas.
- `examples/`: selected valid and invalid media examples.
- `specs/`: selected AEP-Media profile and bundle specifications.

## Reproducibility Boundary

The baseline path uses local fixtures and does not require LinuxPTP, FFmpeg, ffprobe, or C2PA to be installed. Optional external tools can be reported when available, but their absence is not a failure of the fixture-based software artifact.

## Claim Boundary

AEP-Media supports local validation and fixture-based adapter ingestion. It does not claim legal admissibility, non-repudiation, trusted timestamping, real PTP proof, full MP4 PRFT parsing, real C2PA signature verification, chain of custody, production deployment, or proof that the original media capture event was truthful, authorized, or unmodified before packaging.
