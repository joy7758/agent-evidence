# AEP-Media Zenodo Release Plan

Date: 2026-05-10

## Goal

Prepare an AEP-Media-specific archive suitable for SoftwareX submission if the existing repository DOI does not point to the exact intended AEP-Media release.

## Proposed Release Title

`AEP-Media: Reusable Research Software for Offline Validation of Time-Aware Media Evidence Bundles`

## Proposed Version / Tag

`aep-media-v0.1`

If the repository maintainers prefer semver alignment with the package version, use the next repository tag and make the release notes clearly identify the AEP-Media artifact.

## Metadata

- Creator: Bin Zhang
- ORCID: `0009-0002-8861-1481`
- Repository: `https://github.com/joy7758/agent-evidence`
- License: Apache-2.0
- Upload type: software
- Keywords: media evidence, operation accountability, research software, provenance, offline validation, evidence bundle, time trace, reproducibility

## Files to Include

- source code for `agent_evidence`
- AEP-Media specs under `spec/`
- AEP-Media schemas under `schema/`
- media examples and fixtures under `examples/media/`
- media demos under `demo/`
- AEP-Media tests under `tests/`
- AEP-Media reports under `docs/reports/`
- SoftwareX manuscript and supplementary materials under `docs/paper/softwarex/`
- `README.md`
- `LICENSE`
- `CITATION.cff`
- `.zenodo.json`

## Files to Exclude

- virtual environments
- bytecode caches
- unrelated historical staging packs
- local temporary outputs
- editor/system files
- unrelated paper workspaces

## Required Actions

1. Confirm the repository is public.
2. Create a clean tag for the AEP-Media release.
3. Generate release notes that identify AEP-Media as the release focus.
4. Archive the release with Zenodo.
5. Record the resulting DOI in `CITATION.cff`, README, and SoftwareX metadata if it differs from the existing repository DOI.

## Important Boundary

Do not invent a DOI. Until an AEP-Media-specific archive exists, SoftwareX materials should state that the repository DOI exists and the AEP-Media-specific release DOI is pending confirmation.
