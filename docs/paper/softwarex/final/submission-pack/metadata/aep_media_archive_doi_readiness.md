# AEP-Media Archive and DOI Readiness

Date: 2026-05-10

## Current DOI Status

- AEP-Media-specific release DOI: `10.5281/zenodo.20107097`.
- Zenodo record: <https://zenodo.org/records/20107097>.
- GitHub release: <https://github.com/joy7758/agent-evidence/releases/tag/aep-media-v0.1.0>.

Interpretation: the AEP-Media release archive DOI is confirmed for SoftwareX-facing citation metadata.

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

No archive DOI action remains. Use the confirmed DOI above in SoftwareX metadata.

## Readiness Result

Archive/DOI readiness: READY.

Reason: the AEP-Media-specific release DOI is confirmed.

## Mission 019 Update

Mission 019 prepared a local release candidate for `aep-media-v0.1.0`, refreshed AEP-Media citation/archive metadata, and generated a release command preview. Because `AEP_MEDIA_PUBLISH_RELEASE` was not set to `1`, no tag was pushed and no GitHub release or Zenodo archive DOI was created.

Mission 020 published the release and confirmed DOI `10.5281/zenodo.20107097`.
