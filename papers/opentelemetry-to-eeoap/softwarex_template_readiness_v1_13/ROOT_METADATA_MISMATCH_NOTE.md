# Root Metadata Mismatch Note

## Current Root Metadata

The root `CITATION.cff` currently describes AEP-Media, including the
`aep-media-v0.1.0` version and AEP-Media DOI.

The root `codemeta.json` also describes AEP-Media and points to the AEP-Media
release and DOI.

## Why These Files Are Not Final OpenTelemetry-to-EEOAP Metadata

OpenTelemetry-to-EEOAP is a separate SoftwareX route candidate inside the same
repository. Using AEP-Media root metadata as if it were OpenTelemetry-to-EEOAP
metadata would misidentify the software object.

## Local Metadata Drafts

OpenTelemetry-to-EEOAP-specific metadata drafts exist under:

- `papers/opentelemetry-to-eeoap/softwarex_metadata_drafts_v1_8/CITATION_OTEL_EEOAP.cff`
- `papers/opentelemetry-to-eeoap/softwarex_metadata_drafts_v1_8/codemeta-otel-eeoap.json`
- `papers/opentelemetry-to-eeoap/softwarex_metadata_drafts_v1_8/SOFTWARE_METADATA.md`

These files are local drafts, not public release metadata.

## Deferred Decision

The final release metadata decision is deferred until the OpenTelemetry-to-EEOAP
release object is fixed. The likely options remain focused branch release,
supplementary archive, or broader repository release with clear package
scoping.

## Boundary

No root metadata file was changed in this task.
