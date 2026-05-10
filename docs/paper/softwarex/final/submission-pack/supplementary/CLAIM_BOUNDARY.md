# Claim Boundary

AEP-Media validates declared local evidence packages.

It checks:

- media profile structure;
- required fields;
- reference closure;
- media hashes;
- bundle-local paths;
- bundle checksums;
- declared time-trace references;
- trace summaries and thresholds;
- adapter-ingestion reports.

It does not claim:

- legal admissibility;
- non-repudiation;
- trusted timestamping;
- real PTP proof;
- full MP4 PRFT parsing;
- real C2PA signature verification;
- chain of custody;
- production deployment;
- proof that the original media capture event was truthful, authorized, or unmodified before packaging.
