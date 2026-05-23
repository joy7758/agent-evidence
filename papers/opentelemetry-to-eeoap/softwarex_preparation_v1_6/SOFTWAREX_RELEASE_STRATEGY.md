# SoftwareX Release Strategy

This file analyzes release and tag strategy. It does not execute any release
operation.

## Current Local Tags

- `eeoap-v0.1-artifact`
  - local annotated tag
  - target commit: `96f444b7ed39b39fe9f47e428af835952e843cb0`
  - pushed: no
- `aep-v0.1-artifact`
  - local annotated tag
  - target commit: `af2b90c14587718a8ed6982131ba9c98e3274054`
  - pushed: no

## Why Local Tags Are Insufficient for Final SoftwareX Submission

Local tags stabilize the author's local citation references, but reviewers and
editors cannot resolve them unless they are pushed or archived. SoftwareX needs
a publicly inspectable software distribution and a persistent retrieval path.
The current local tags are useful internal anchors, not final public artifact
identifiers.

## Candidate Release Artifacts

Possible release artifacts:

- A focused OpenTelemetry-to-EEOAP release tag in this repository.
- A SoftwareX supplement package containing fixtures, generated statements,
  adapter reports, frozen documentation, and checksums.
- Public GitHub Release assets after branch cleanliness is confirmed.
- DOI archive only after the exact release payload is frozen.

## Proposed Tag Strategy

Do not push the existing local tags yet. First decide the software object:

- Option A: OpenTelemetry-to-EEOAP as part of the broader `agent-evidence`
  software release.
- Option B: OpenTelemetry-to-EEOAP as a focused subpackage/release candidate
  within `agent-evidence`.
- Option C: OpenTelemetry-to-EEOAP as a paper supplement with local source paths
  and exact commit references.

After that decision, create a package-specific release candidate tag only if it
has a clear target and final support-material scope.

## Proposed Archive Strategy

Archive only after:

- metadata strategy is fixed;
- release payload is frozen;
- clean-clone and checksum evidence is regenerated;
- the article availability statement matches the actual public state.

The archive should not be created from the original dirty worktree.

## What Should Not Be Released Yet

- Current root `CITATION.cff`, because it describes AEP-Media.
- Current root `codemeta.json`, because it describes AEP-Media.
- Any unrelated AEP-Media manuscript or submission-pack changes.
- `pd-oap`, `tmp`, or local paper-draft directories.
- A DOI archive before OpenTelemetry-to-EEOAP release scope is decided.

## Risks of Pushing Tags Too Early

- Public references may point to the wrong software object.
- AEP-Media metadata may be mistaken for OpenTelemetry-to-EEOAP metadata.
- Reviewers may see local paper-preparation commits rather than a clean software
  release.
- A tag push can be hard to correct without creating confusing replacement
  tags.

## Recommended Release Sequence

1. Finish SoftwareX preparation checklist.
2. Decide whether the repository should expose OpenTelemetry-to-EEOAP as part
   of the main `agent-evidence` release or as a focused subpackage release.
3. Update citation metadata only if the route is confirmed.
4. Run clean-clone checks.
5. Create release candidate tag.
6. Only then consider GitHub Release or DOI archive.
