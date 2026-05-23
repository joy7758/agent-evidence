# Tag Target Decision

Purpose: decide the future target for
`opentelemetry-to-eeoap-softwarex-rc-v1.0`.

## Candidate A: Version 1.25 Support Package Commit

Commit: `a03f6455d87bcf67987c7ba1e4297a224de70976`

Advantages:

- Contains the current version 1.25 support package.
- Contains copied article, metadata, evidence, validation commands, and
  checksum file.
- Checksum, CodeMeta JSON, validator, and scoped pytest results were recorded
  in the package.

Risks:

- Does not include the later version 1.26 clean-clone verification documents.
- A reviewer would need a separate commit to see the clean-clone verification
  result.

What the tag would include:

- Version 1.25 support package.
- Version 1.24 package-local metadata drafts copied into the support package.
- Version 1.22 declaration-finalized manuscript copy.

What it would exclude:

- Version 1.26 clean-clone verification.
- Version 1.27 tag preparation plan.

Suitability for release-candidate tag: partial.

Recommendation: do not use this commit as the RC tag target now because it
excludes the clean-clone verification evidence.

## Candidate B: Version 1.26 Clean-Clone Verification Commit

Commit: `94a2a796929e48142f804ab8cc5cec8e120f76c5`

Advantages:

- Contains version 1.25 support package.
- Contains version 1.26 clean-clone verification showing the support package is
  reproducible from a clean checkout.
- Verification passed for checksum, CodeMeta JSON, validator checks, scoped
  pytest, privacy check, and final clean git status.

Risks:

- Does not include this version 1.27 tag preparation plan.
- Local tag target choice and tag command safety checks would remain outside
  the tagged state.

What the tag would include:

- Version 1.25 support package.
- Version 1.26 clean-clone verification documentation.

What it would exclude:

- Version 1.27 tag preparation plan.

Suitability for release-candidate tag: mostly suitable if no tag planning
documentation needs to be part of the tagged state.

Recommendation: acceptable fallback if the tag preparation plan is treated as
out-of-band. Not preferred because the current route is making tag preparation
part of the audited trail.

## Candidate C: Future Commit After Version 1.27 Plan Or Later Release Metadata Updates

Commit: TODO after this version 1.27 plan is committed, unless a later metadata
or template update is made before local tag creation.

Advantages:

- Includes the version 1.25 support package.
- Includes the version 1.26 clean-clone verification.
- Includes this version 1.27 tag target, naming, creation, and push safety plan.
- Keeps the tag decision itself inside the auditable repository history.

Risks:

- The concrete commit hash is not known until this plan is committed.
- If additional release metadata or template updates occur before tag creation,
  this target should be superseded by a later verified commit.

What the tag would include:

- Version 1.25 support package.
- Version 1.26 clean-clone verification.
- Version 1.27 tag preparation plan.

What it would exclude:

- Any future release metadata changes after v1.27.
- Public release URLs, DOI, GitHub Release, and pushed tag state, which do not
  exist yet.

Suitability for release-candidate tag: suitable for the next local annotated RC
tag if no additional release metadata or template changes are made before tag
creation.

Recommendation: use this path.

## Recommended Future Tag Target

Use the version 1.27 plan commit created by this task as the future local RC tag
target, provided no additional release metadata, template, or support-package
changes are made before tag creation.

If any release metadata, support package, template, checksum, or validation
material changes before tag creation, choose the later updated commit and rerun
the required checks before creating the local tag.

Do not create the tag in version 1.27.
