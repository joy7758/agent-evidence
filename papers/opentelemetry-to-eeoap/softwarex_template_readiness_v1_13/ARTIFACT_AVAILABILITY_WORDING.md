# Artifact Availability Wording

## Short Version

The OpenTelemetry-to-EEOAP artifacts are currently available in the local
release-candidate branch. Generated EEOAP statements, adapter reports, fixtures,
tests, metadata drafts, and SoftwareX preparation materials are committed
repository artifacts. Public release URL, pushed tags, DOI, and GitHub Release
remain TODO before formal submission.

## Long Version

The OpenTelemetry-to-EEOAP package is currently prepared in the
`softwarex-otel-eeoap-release-candidate` branch. It contains adapter source at
`tools/opentelemetry_to_eeoap_adapter.py`, fixtures under
`examples/opentelemetry/`, generated EEOAP statements and adapter reports under
`generated/`, scoped tests under `tests/`, and SoftwareX preparation materials
under `papers/opentelemetry-to-eeoap/`.

The version 0.5 frozen package under `papers/opentelemetry-to-eeoap/frozen_v0_5/`
is a historical internal freeze. It includes clean-clone and checksum evidence,
but it predates the version 0.7 second valid trace. The forward path for formal
submission is a release-candidate support package derived from the current
branch, not the historical frozen package alone.

Local EEOAP and AEP artifact tags exist, but they have not been pushed or
archived. No DOI or GitHub Release has been created. Final artifact availability
wording must be updated after public release, archive, pushed tag, or DOI
creation.

## Current Draft Wording

Artifacts are currently local to the repository and release-candidate branch.
Generated statements and adapter reports are committed repository artifacts.
The version 0.5 frozen package is historical support material. Local EEOAP/AEP
tags exist but are not pushed or archived. No DOI or GitHub Release has been
created. TODO: replace this draft with the final public artifact availability
statement before submission.

## TODOs Before Final Submission

- Create or select the public release URL.
- Decide whether a GitHub Release is created.
- Decide whether a DOI/archive is created.
- Decide whether local EEOAP/AEP artifact tags are pushed.
- Create final OpenTelemetry-to-EEOAP release tag or immutable public reference.
- Create final release-candidate support package.
- Rerun clean-clone verification.
- Regenerate final checksums.
- Update references to final public identifiers.

## Update After DOI/GitHub Release/Tag Push

Replace TODO placeholders with:

- public repository URL;
- release tag URL;
- GitHub Release URL if created;
- DOI/archive URL if created;
- final checksum location;
- final clean-clone verification location.

## Warning

Do not claim public release, public archive, pushed tags, GitHub Release, or DOI
until those actions actually exist.
