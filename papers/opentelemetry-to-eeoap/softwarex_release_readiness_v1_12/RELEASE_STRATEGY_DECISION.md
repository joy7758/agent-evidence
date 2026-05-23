# Release Strategy Decision

This file evaluates possible release strategies without executing any release
action.

## Option A: Main Repository Release

Description:
Release OpenTelemetry-to-EEOAP as part of the broader `agent-evidence`
repository.

Advantages:

- Matches the current repository organization.
- Keeps adapter, validator, examples, and generated outputs in one public
  source tree.
- Avoids maintaining a separate repository.

Risks:

- Root metadata currently describes AEP-Media.
- The repository contains multiple paper lines and out-of-scope materials.
- SoftwareX reviewers may find the software object ambiguous.

Effect on root metadata:
Likely requires root metadata updates or a release-specific metadata strategy.

Effect on SoftwareX submission:
Could work if the article clearly identifies the adapter path, release tag, and
support package, but it has higher ambiguity risk.

Recommendation:
Not the preferred first choice for this package unless repository-level release
scope is intentionally broad.

## Option B: Focused Release-Candidate Branch Release

Description:
Use the clean `softwarex-otel-eeoap-release-candidate` branch as the basis for a
focused OpenTelemetry-to-EEOAP release.

Advantages:

- Matches the current isolated worktree process.
- Allows focused release notes, support files, and metadata without disturbing
  active unrelated work.
- Keeps the adapter inside its real repository context while reducing release
  ambiguity.

Risks:

- Root metadata mismatch still needs final handling.
- The source layout remains `tools/`, not `repo/src`.
- A branch release still needs a public tag/archive/DOI decision.

Effect on root metadata:
Can defer root metadata overwrite until release scope is confirmed; local
OpenTelemetry-to-EEOAP metadata drafts can support the template-readiness stage.

Effect on SoftwareX submission:
Best fit for the current route because the paper can describe a focused release
candidate and later replace TODOs with final public identifiers.

Recommendation:
Preferred provisional strategy.

## Option C: Archive Only Frozen/Release-Candidate Package

Description:
Archive a focused support package rather than the full repository release.

Advantages:

- Gives a compact, citation-ready artifact.
- Avoids confusing unrelated repository content.
- Can include checksums, generated statements, reports, and documentation.

Risks:

- SoftwareX expects an open-source software distribution, not only a paper
  supplement.
- A package-only archive may hide source context or installation path.
- Needs careful mapping back to the public code repository.

Effect on root metadata:
May avoid root metadata edits, but final article still needs software citation
metadata.

Effect on SoftwareX submission:
Useful as supplementary archive, but not sufficient alone if SoftwareX requires
the software repository itself to be public and reusable.

Recommendation:
Use only as a supplement to Option B, not as the sole release strategy.

## Option D: Defer Release Until After SoftwareX Editorial Feedback

Description:
Keep all release fields as TODO until after initial editorial or external
feedback.

Advantages:

- Avoids premature release of a package that may need format or metadata
  changes.
- Reduces risk of pushing wrong tags or DOI metadata.

Risks:

- SoftwareX submission likely needs a public software version before formal
  submission.
- Reviewers may treat unresolved release state as a readiness failure.

Effect on root metadata:
No immediate effect.

Effect on SoftwareX submission:
Acceptable for pre-review, not acceptable for final submission.

Recommendation:
Acceptable until template-readiness stage, but not beyond formal submission.

## Recommended Release Strategy

Use Option B as the provisional strategy: prepare a focused release-candidate
branch release for OpenTelemetry-to-EEOAP, with Option C as a supplementary
archive if needed.

Do not execute the release yet. The next step should update wording and
template-readiness materials so they consistently describe this provisional
strategy without claiming pushed tags, DOI, GitHub Release, or public archive.
