# Recommended Metadata Strategy

## Recommendation

Hybrid:

- Option B now.
- Possible Option C later if the SoftwareX route is confirmed and a focused
  release branch needs root-level metadata.

## Reason

Root metadata currently represents AEP-Media:

- `CITATION.cff` names AEP-Media, version `aep-media-v0.1.0`, and DOI
  `10.5281/zenodo.20107097`.
- `codemeta.json` names AEP-Media and points to the AEP-Media DOI and release.

Changing root metadata too early risks corrupting or confusing other paper
lines. The OpenTelemetry-to-EEOAP package is currently a SoftwareX route
candidate, not a public release. A paper-local OpenTelemetry-to-EEOAP-specific
metadata note is safer before release.

If the SoftwareX route is confirmed, a focused release branch can later adjust
root metadata or release metadata so that the final public software object,
release tag, citation, and availability statement all agree.

## Minimal Next Metadata Artifacts

Create these later, but not in this task:

- `papers/opentelemetry-to-eeoap/CITATION_OTEL_EEOAP.cff`
- `papers/opentelemetry-to-eeoap/codemeta-otel-eeoap.json`
- `papers/opentelemetry-to-eeoap/SOFTWARE_METADATA.md`
- `papers/opentelemetry-to-eeoap/ARTIFACT_AVAILABILITY.md`

These files should be treated as draft metadata until release scope, tag push,
and archive strategy are finalized.

## What Not To Do Yet

- Do not overwrite root `CITATION.cff`.
- Do not overwrite root `codemeta.json`.
- Do not push tags.
- Do not create DOI.
- Do not create GitHub Release.
- Do not submit.
