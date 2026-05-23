# Frozen Package Update Decision

## Situation

The version 0.5 frozen package under
`papers/opentelemetry-to-eeoap/frozen_v0_5/` is an internally frozen package. It
contains clean-clone verification, checksum verification, claim boundary
material, reviewer notes, and an external review brief.

However, version 0.5 predates the version 0.7 second valid trace. The current
SoftwareX evidence story includes:

- two valid OpenTelemetry-style traces;
- four invalid diagnostic traces;
- two generated EEOAP-compatible statements;
- validator passes for both valid generated statements;
- later SoftwareX route, metadata, and article materials.

## Should SoftwareX Cite Version 0.5?

Version 0.5 can be cited as a historical freeze and early reproducibility
checkpoint. It should not be presented as the final SoftwareX release package
because it does not include the second valid trace evidence point.

## Is a New Frozen Package Needed Before Template Conversion?

Not necessarily. Template conversion can proceed if the article clearly states
that version 0.5 is historical support material and that final release-candidate
support packaging remains TODO.

## Is a New Frozen Package Needed Before Formal Submission?

Yes, or an equivalent final release-candidate package is needed. Formal
submission should not rely on a frozen package that predates the current
evaluation story.

## Options

- No update before template conversion.
- Create version 1.12 or later release-candidate frozen package before template
  conversion.
- Defer frozen package update until release candidate finalization.

## Decision

Defer frozen package update until release candidate finalization.

## Reason

The immediate blocker is wording, not packaging. A template-readiness draft
should clarify that `frozen_v0_5/` is historical and that a final
release-candidate package must be cut before formal submission. Cutting a new
package now would risk mixing planning documents with final release artifacts
before metadata and release strategy are fixed.
