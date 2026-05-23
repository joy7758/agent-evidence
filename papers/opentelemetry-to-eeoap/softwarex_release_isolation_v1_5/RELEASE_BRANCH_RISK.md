# Release Branch Risk

## Risks If Release Is Prepared From the Current Dirty Worktree

- Unrelated AEP-Media manuscript and submission-pack changes could be staged
  accidentally.
- Untracked `pd-oap`, `tmp`, `paper-ncs-execution-evidence`, and paper draft
  files could leak into release artifacts.
- Root citation metadata currently points to AEP-Media and could be confused
  with the OpenTelemetry-to-EEOAP package.
- Dirty worktree state makes release checks harder to reproduce and explain to
  reviewers.
- A release cut from the dirty tree would blur the boundary between
  OpenTelemetry-to-EEOAP and other ongoing paper/software lines.

## Why the Isolated Worktree Is Safer

- It starts from the exact v1.4 route-analysis commit.
- It has a clean `git status --short` before v1.5 documentation.
- It contains only committed repository files plus the new v1.5 documentation
  added on the release-candidate branch.
- It allows scoped tests, validator checks, and checksum checks without touching
  the original dirty worktree.
- It provides a clear place for the next SoftwareX preparation checklist.

## Remaining Blockers Before Public Release

- Decide whether to push `softwarex-otel-eeoap-release-candidate`.
- Decide whether to push `eeoap-v0.1-artifact` and `aep-v0.1-artifact`.
- Decide whether to create a new OpenTelemetry-to-EEOAP public release tag.
- Decide whether to create an archive or DOI.
- Resolve `README.md` / `LICENSE.txt` / `repo/src` expectations.
- Prepare package-specific `CITATION.cff` and `codemeta.json`.
- Build final SoftwareX support material with checksums.
- Re-run clean-clone and scoped tests against the final release candidate.

No tag was pushed.
No DOI was created.
No GitHub Release was created.
No venue formatting was performed.
