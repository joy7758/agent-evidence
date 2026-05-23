# Release-Readiness Wording

## What Is Currently Ready

- Adapter source exists at `tools/opentelemetry_to_eeoap_adapter.py`.
- Broader package and validator source exists under `agent_evidence/`.
- Two valid OpenTelemetry-style fixtures exist.
- Four invalid diagnostic fixtures exist.
- Generated EEOAP statements and adapter reports are committed under
  `generated/`.
- Scoped tests exist and continue to pass.
- Local metadata drafts exist under
  `papers/opentelemetry-to-eeoap/softwarex_metadata_drafts_v1_8/`.
- SoftwareX route, preparation, article, and readiness documentation exists.

## What Is Not Yet Released

- No package-specific public release URL exists.
- No package-specific GitHub Release exists.
- No package-specific DOI exists.
- No package-specific release tag has been pushed.
- Final OpenTelemetry-to-EEOAP CFF and CodeMeta metadata are not public release
  metadata.
- Final SoftwareX support package has not been cut.

## What Local Tags Mean

The local tags `eeoap-v0.1-artifact` and `aep-v0.1-artifact` are local
immutable references for related artifacts. They are useful for internal
preparation, but they are not public release identifiers because they have not
been pushed or archived.

## What Version 0.5 Frozen Package Means

`papers/opentelemetry-to-eeoap/frozen_v0_5/` is a historical internal freeze. It
records early clean-clone and checksum evidence, but it predates the second
valid trace added in version 0.7. It should not be described as the final
SoftwareX release package.

## What Release-Candidate Branch Means

The `softwarex-otel-eeoap-release-candidate` branch is the current isolated
preparation surface. It contains the second valid trace, generated statements,
metadata drafts, SoftwareX article drafts, and release-readiness planning. It
is not yet a public release.

## What Must Happen Before Final SoftwareX Submission

- Decide and execute public release strategy.
- Create or identify final public release URL.
- Decide DOI/archive route.
- Decide GitHub Release route.
- Decide tag-push route.
- Finalize CFF and CodeMeta metadata.
- Refresh support package with current two-valid-trace evidence.
- Rerun clean-clone verification and checksum verification.
- Update artifact availability and references with public identifiers.

## What Must Not Be Claimed Now

- Public release exists.
- DOI exists.
- GitHub Release exists.
- Tags are pushed.
- Root metadata is final OpenTelemetry-to-EEOAP metadata.
- Version 0.5 frozen package is the final SoftwareX package.
- The package is production-ready or broadly OpenTelemetry-compatible.
