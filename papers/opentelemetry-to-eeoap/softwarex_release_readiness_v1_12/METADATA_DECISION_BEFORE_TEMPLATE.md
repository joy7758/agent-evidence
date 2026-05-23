# Metadata Decision Before Template Conversion

## Current Metadata State

- Root `CITATION.cff` describes AEP-Media, version `aep-media-v0.1.0`, DOI
  `10.5281/zenodo.20107097`, and the AEP-Media release.
- Root `codemeta.json` describes AEP-Media and points to the same AEP-Media
  release and DOI.
- OpenTelemetry-to-EEOAP-specific metadata drafts exist under
  `papers/opentelemetry-to-eeoap/softwarex_metadata_drafts_v1_8/`.
- Those drafts do not claim a DOI, pushed tag, public release URL, or GitHub
  Release.

## What the SoftwareX Article Should Say Now

The article should state that:

- root metadata currently belongs to another artifact line, AEP-Media;
- OpenTelemetry-to-EEOAP has local draft metadata only;
- final public release metadata is pending;
- DOI, GitHub Release, pushed tags, and release URLs are TODO before formal
  submission;
- the article is a SoftwareX route draft, not a released package record.

## What Must Be Updated After Release

- Final software version.
- Public repository/release URL.
- Release tag.
- DOI or archive URL if one is created.
- Final CFF and CodeMeta metadata.
- Final artifact availability statement.
- Final references for EEOAP and AEP artifacts.

## Recommended Metadata Handling Before Template Conversion

Do not edit root `CITATION.cff` before template conversion.

Do not edit root `codemeta.json` before template conversion.

Use the local OpenTelemetry-to-EEOAP metadata drafts as supporting material and
explicitly state that final public release metadata is pending. This avoids
corrupting AEP-Media metadata while keeping the OpenTelemetry-to-EEOAP
SoftwareX draft honest about release readiness.

## Decision

Proceed with local metadata drafts and explicit TODOs. Root metadata changes
should wait until the release object is decided.
