# Mission 022 Metadata Parity Audit

## Canonical Release Metadata

- Title: AEP-Media: Reusable Research Software for Offline Validation of Time-Aware Media Evidence Bundles
- Software name: AEP-Media
- Version: `aep-media-v0.1.0`
- DOI: `10.5281/zenodo.20107097`
- Repository: <https://github.com/joy7758/agent-evidence>
- GitHub release: <https://github.com/joy7758/agent-evidence/releases/tag/aep-media-v0.1.0>
- Zenodo record: <https://zenodo.org/records/20107097>
- License: Apache-2.0
- Author: Bin Zhang
- ORCID: 0009-0002-8861-1481
- Email: joy7759@gmail.com

## Files Audited

- `CITATION.cff`
- `.zenodo.json`
- `codemeta.json`
- `README.md`
- `docs/how-to-cite.md`
- `docs/paper/softwarex/final/release/notes/aep-media-v0.1.0-release-notes.md`
- `docs/paper/softwarex/final/aep_media_softwarex_final_manuscript.md`
- `docs/paper/softwarex/final/submission-pack/metadata/softwarex_submission_metadata.md`

## Result

Metadata parity result: PASS.

The audited files use the same release version, DOI, repository URL, GitHub
release URL, Zenodo record URL, license, author identity, ORCID, and contact
email where the target metadata format supports or naturally carries those
fields.

## Notes

- `CITATION.cff` records the title, author, ORCID, email, affiliation, version,
  DOI, license, repository-code, and GitHub release URL.
- `.zenodo.json` records the title, creator, ORCID, license, version,
  repository URL, GitHub release URL, and DOI relationship. The creator is
  represented as `Zhang, Bin`, which is equivalent to `Bin Zhang` in Zenodo
  metadata.
- `codemeta.json` records the software name, title, DOI, repository URL,
  GitHub release URL, Zenodo record URL, license, version, author, ORCID,
  email, and affiliation.
- `README.md`, `docs/how-to-cite.md`, release notes, manuscript metadata, and
  submission metadata all expose the DOI and release location needed for
  SoftwareX review.

No DOI, release tag, author identity, or license mismatch was found.
