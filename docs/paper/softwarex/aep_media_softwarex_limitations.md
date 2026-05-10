# AEP-Media Limitations and Claim Boundary

## Current Claim

AEP-Media claims local validation and fixture-based adapter ingestion for time-aware media evidence bundles. It checks whether a declared local evidence package is internally consistent, portable, and reproducible.

## Non-claims

AEP-Media does not claim:

- legal admissibility;
- non-repudiation;
- trusted timestamping;
- real PTP proof;
- full MP4 PRFT parser;
- real C2PA signature verification;
- production deployment;
- chain of custody;
- complete regulatory compliance;
- broad forensic sufficiency;
- proof that the original media capture event was truthful, authorized, or unmodified before packaging.

## Adapter Boundary

The adapter layer ingests LinuxPTP-style, FFmpeg PRFT-style, and C2PA-like metadata into AEP-Media report formats. It separates fixture ingestion, optional external-tool reporting, and local validation. It should not be interpreted as proof that real external systems were used unless a future environment-specific report records those tool runs.

## Evaluation Boundary

The current evaluation is a bounded conformance-oriented artifact evaluation. It exercises validation surfaces, controlled invalid examples, tamper cases, and expected failure codes. It is not a field deployment study, user study, performance benchmark, or legal-evidence assessment.

## Submission Boundary

For SoftwareX, the paper should present AEP-Media as reusable research software. It should not reframe the artifact as a general media-authenticity platform, legal evidence system, non-repudiation system, or production assurance product.
