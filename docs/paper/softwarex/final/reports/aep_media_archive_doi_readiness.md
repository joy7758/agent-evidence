# AEP-Media Archive and DOI Readiness

Date: 2026-05-10

## Current DOI Status

- `CITATION.cff` records repository DOI `10.5281/zenodo.19334062`.
- The current GitHub releases include repository-level releases, including `v0.2.1`.
- No confirmed AEP-Media-specific release DOI was found during Mission 018.

Interpretation: the repository has citation metadata, but SoftwareX final submission should still confirm or create an AEP-Media-focused release archive before claiming a software artifact DOI for this specific component.

## Proposed AEP-Media Release

- Proposed release tag: `aep-media-v0.1.0`
- Proposed release title: `AEP-Media v0.1: Offline Validation of Time-Aware Media Evidence Bundles`
- Repository: `https://github.com/joy7758/agent-evidence`
- License: Apache-2.0
- Creator: Bin Zhang
- ORCID: `0009-0002-8861-1481`

## Proposed Archive Contents

- Source repository snapshot.
- AEP-Media specs under `spec/`.
- AEP-Media schemas under `schema/`.
- Media examples and fixtures under `examples/media/`.
- Media demos under `demo/`.
- AEP-Media tests under `tests/`.
- SoftwareX manuscript and supplementary materials under `docs/paper/softwarex/`.
- Release pack and evaluation reports under `docs/reports/`.
- `README.md`, `LICENSE`, `CITATION.cff`, and `.zenodo.json`.

## Exclusions

Do not include:

- virtual environments;
- bytecode caches;
- local temporary outputs;
- old journal staging packs;
- unrelated paper workspaces;
- files containing local absolute paths.

## Action Required

1. Create a clean AEP-Media release tag.
2. Archive the release through Zenodo or an equivalent archival repository.
3. Record the resulting AEP-Media-specific DOI in `CITATION.cff`, README, SoftwareX metadata, and the SoftwareX manuscript.
4. Do not invent a DOI before the archive exists.

## Readiness Result

Archive/DOI readiness: NEAR READY.

Reason: repository-level DOI metadata exists, but an AEP-Media-specific release DOI is not yet confirmed.

## Mission 019 Update

Mission 019 prepared a local release candidate for `aep-media-v0.1.0`, refreshed AEP-Media citation/archive metadata, and generated a release command preview. Because `AEP_MEDIA_PUBLISH_RELEASE` was not set to `1`, no tag was pushed and no GitHub release or Zenodo archive DOI was created.

Current result remains NEAR READY.
