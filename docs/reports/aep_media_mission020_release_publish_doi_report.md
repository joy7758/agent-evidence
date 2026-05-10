# AEP-Media Mission 020 Release Publish and DOI Report

Date: 2026-05-10

## 1. Release Authorization Status

The user authorized direct operation for the release flow after the guarded Mission 020 attempt stopped without publication.

## 2. Initial Release Safety Snapshot

- Branch: `docs/link-mvk-bridge`
- Pre-release latest commit: `0bb307e Stabilize docs link check DOI excludes`
- Repository: `joy7758/agent-evidence`
- Visibility: public
- License: Apache-2.0
- GitHub CLI: authenticated as `joy7758`
- Existing `aep-media-v0.1.0` release before publication: not found

The working tree contains broad AEP-Media mission work plus unrelated untracked material. Release staging is restricted to AEP-Media, SoftwareX, citation, archive, CLI, test, report, and readiness files.

## 3. Pre-Publish Tests

- Targeted AEP-Media tests: `48 passed, 1 warning`
- SoftwareX/readiness tests: `23 passed, 1 warning`
- Full pytest: `155 passed, 1 skipped, 15 warnings`
- Ruff: `All checks passed!`
- `git diff --check`: passed

## 4. Pre-Publish Evaluation

- Default evaluation: `PASS aep-media-evaluation@0.1 cases=18 unexpected=0`
- Adapter-inclusive evaluation: `PASS aep-media-evaluation@0.1 cases=26 unexpected=0 adapters=included`
- Optional-tool reporting evaluation: `PASS aep-media-evaluation@0.1 cases=23 unexpected=0 optional_tools=included`
- Combined evaluation: `PASS aep-media-evaluation@0.1 cases=31 unexpected=0 adapters=included optional_tools=included`
- Release pack: `PASS aep-media-release-pack@0.1`

## 5. Red-Line Scan

Status: PASS.

Release-facing materials and release candidate archive passed the red-line scan.

## 6. Staged Files Summary

The release-readiness commit staged AEP-Media, SoftwareX, citation, archive,
CLI, tests, reports, examples, schemas, specs, and release-candidate materials.
The unrelated paper workspace was not staged.

## 7. Commit Hash

`1c344e3 Prepare AEP-Media v0.1.0 SoftwareX release`

## 8. Tag Status

Published tag: `aep-media-v0.1.0`

## 9. GitHub Release URL

<https://github.com/joy7758/agent-evidence/releases/tag/aep-media-v0.1.0>

## 10. Zenodo DOI Status

DOI pending.

Zenodo search did not confirm an AEP-Media-specific DOI immediately after the
GitHub release was created. No DOI was guessed or invented.

## 11. SoftwareX Final Pack Status

SoftwareX final pack exists and remains synchronized with the release-candidate
state, except that the AEP-Media-specific DOI is still pending.

## 12. Current Readiness

NEAR READY.

## 13. Remaining Blockers

- Confirm Zenodo GitHub integration for `joy7758/agent-evidence`.
- Wait for or reprocess the `aep-media-v0.1.0` Zenodo archive.
- Copy the exact DOI into citation and SoftwareX-facing metadata.
- Regenerate the final SoftwareX submission pack after DOI sync.

## 14. Next Action

Run a DOI sync mission after Zenodo publishes the AEP-Media v0.1.0 archive DOI.
