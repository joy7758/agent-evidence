# Release Metadata Implementation Plan

## Current State

The OpenTelemetry-to-EEOAP SoftwareX route has a verified local support package,
clean-clone verification, template-style manuscript drafts, author-confirmed
metadata, and finalized declaration wording. It still has no public release URL,
DOI, GitHub Release, pushed release tag, final release version, final public
metadata, or final public references.

The root `CITATION.cff` and root `codemeta.json` currently describe AEP-Media,
not OpenTelemetry-to-EEOAP. Local OpenTelemetry-to-EEOAP metadata drafts exist
under `papers/opentelemetry-to-eeoap/softwarex_metadata_drafts_v1_8/`, but they
are not final public release metadata.

## Confirmed Public Metadata

- Author: Bin Zhang / Zhang Bin
- ORCID: `https://orcid.org/0009-0002-8861-1481`
- Affiliation: Independent Researcher, China
- Corresponding author email: `joy7759@gmail.com`
- Support contact strategy: GitHub Issues
- License: Apache-2.0
- Funding: this research received no specific grant from any funding agency in
  the public, commercial, or not-for-profit sectors.
- Conflict of interest: the author declares no known competing financial
  interests or personal relationships that could have appeared to influence the
  work reported in this paper.
- Acknowledgements: None.
- Keywords: OpenTelemetry; EEOAP; agent telemetry; operation accountability;
  execution evidence; validation; reproducibility

## Unresolved Release Metadata

- Final public repository or release URL.
- Final support issue URL.
- DOI.
- Final release version.
- Final release tag.
- GitHub Release.
- Pushed tags.
- Final public CFF and CodeMeta metadata.
- Final references.
- Final SoftwareX metadata table values.
- Final clean-clone and checksum verification after metadata changes.

## Metadata Files That Can Be Prepared Later

- Package-local `CITATION_OTEL_EEOAP.cff`.
- Package-local `codemeta-otel-eeoap.json`.
- Package-local `SOFTWARE_METADATA.md`.
- Package-local `ARTIFACT_AVAILABILITY.md`.
- Support package `METADATA/` copies.
- SoftwareX manuscript metadata table.
- Final references file.

## Metadata Files That Must Not Be Changed Yet

- Root `CITATION.cff`.
- Root `codemeta.json`.
- Root `README.md`.
- Root `LICENSE`.
- Root `pyproject.toml`.
- Existing versioned SoftwareX directories from v1.15 through v1.22.

## Release Sequence Dependency

1. Decide package-local metadata content and provisional release/tag naming.
2. Prepare package-local release metadata drafts.
3. Build a final release-candidate support package that includes the metadata.
4. Run checksum, validator, scoped pytest, and clean-clone verification.
5. Create and push a focused release-candidate tag only if approved.
6. Create GitHub Release only if approved and only after validation.
7. Create or link DOI only if approved and only after public release artifacts
   are stable.
8. Update manuscript references and SoftwareX metadata table after public URLs
   and DOI exist.

## Recommended Implementation Path

1. Keep root `CITATION.cff` and root `codemeta.json` unchanged for now.
2. Prepare OpenTelemetry-to-EEOAP-specific release metadata under the
   paper/package path.
3. Create a final release-candidate support package after metadata is updated.
4. Run checksum, validator, scoped pytest, and clean-clone checks.
5. Only then create or push a release tag if approved.
6. Only then create GitHub Release and DOI if approved.
7. Update manuscript references and metadata table after release URLs exist.

No release action is executed in version 1.23.
