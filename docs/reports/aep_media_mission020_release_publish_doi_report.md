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

Pending. This section will be finalized after staging and commit.

## 7. Commit Hash

Pending.

## 8. Tag Status

Pending.

## 9. GitHub Release URL

Pending.

## 10. Zenodo DOI Status

Pending.

No DOI will be guessed or invented.

## 11. SoftwareX Final Pack Status

Pending.

## 12. Current Readiness

Pending.

## 13. Remaining Blockers

Pending.

## 14. Next Action

Pending.
