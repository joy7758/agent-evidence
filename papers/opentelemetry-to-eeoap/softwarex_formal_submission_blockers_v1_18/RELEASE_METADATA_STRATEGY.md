# Release Metadata Strategy

## Current Local Metadata State

OpenTelemetry-to-EEOAP-specific metadata drafts exist under:

`papers/opentelemetry-to-eeoap/softwarex_metadata_drafts_v1_8/`

They include local draft CFF, CodeMeta JSON, software metadata notes, artifact
availability, data availability, AI-assisted writing disclosure, and conflict /
funding declarations. They do not claim a DOI, public release URL, pushed tag,
or final release version.

The root `CITATION.cff` and root `codemeta.json` currently describe AEP-Media,
including AEP-Media release identifiers. They should not be treated as final
OpenTelemetry-to-EEOAP metadata.

## Why Root Metadata Should Not Be Overwritten Blindly

The repository contains multiple paper and artifact lines. Blindly replacing
root metadata with OpenTelemetry-to-EEOAP metadata would risk corrupting the
already documented AEP-Media citation surface and confusing readers about what
the repository-level release represents.

Root metadata should only change after deciding whether the public release is a
whole-repository release, a focused branch release, or a package-local archive.

## Candidate Strategy A: Focused Release Branch Updates Root Metadata

Description: create or keep a focused release branch for OpenTelemetry-to-EEOAP
and update root `CITATION.cff` / `codemeta.json` there to describe the
OpenTelemetry-to-EEOAP SoftwareX release.

Advantages:

- Aligns root metadata with a focused release snapshot.
- Gives SoftwareX a conventional repository-level metadata surface.
- Easier for GitHub/Zenodo automation if the full repository snapshot is used.

Risks:

- May obscure AEP-Media metadata in the release branch.
- Requires careful branch naming and release notes.
- Must not be merged back in a way that corrupts other paper lines.

Recommendation status: possible later, not now.

## Candidate Strategy B: Keep Root Metadata and Include Package Metadata

Description: keep root metadata as repository-level / AEP-Media metadata for
now, and include OpenTelemetry-to-EEOAP metadata under
`papers/opentelemetry-to-eeoap/` or the final support package.

Advantages:

- Safest for a multi-line repository.
- Avoids overwriting AEP-Media metadata.
- Matches the v1.7 and v1.8 local metadata strategy.

Risks:

- SoftwareX may prefer repository-level metadata if the full GitHub repository
  is the software distribution.
- The manuscript must clearly explain metadata scope.
- DOI/archive tooling may not automatically read package-local metadata.

Recommendation status: preferred until release scope is finalized.

## Candidate Strategy C: Release Artifact Archive With Independent Metadata

Description: create a final support package/archive that includes
OpenTelemetry-to-EEOAP metadata independent of root metadata.

Advantages:

- Cleanest if the final public artifact is a focused support package.
- Avoids root metadata conflict.
- Can include exact article draft, evidence, checksum, validation, CFF, and
  CodeMeta files.

Risks:

- Must still satisfy SoftwareX requirements around GitHub repository visibility.
- DOI and GitHub Release relationships must be clearly explained.
- Needs final clean-clone and checksum verification after package creation.

Recommendation status: strong companion strategy, especially if combined with
Candidate B.

## Recommended Release Metadata Strategy

Use a hybrid of Candidate B and Candidate C now:

1. Keep root metadata unchanged until release scope is formally decided.
2. Finalize OpenTelemetry-to-EEOAP metadata inside the focused package/support
   materials.
3. If a full focused release branch becomes the chosen public route, consider
   Candidate A only in that release branch.

This recommendation is provisional. No metadata changes are executed in v1.18.
