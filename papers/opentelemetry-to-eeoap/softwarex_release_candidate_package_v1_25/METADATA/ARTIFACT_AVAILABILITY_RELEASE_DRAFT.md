# Artifact Availability Release Draft

Purpose: draft artifact availability wording for the OpenTelemetry-to-EEOAP
SoftwareX route. This is not final public-release wording.

## Current Local State

The OpenTelemetry-to-EEOAP materials are currently local to the
`softwarex-otel-eeoap-release-candidate` branch. The relevant local artifacts
include:

- adapter source: `tools/opentelemetry_to_eeoap_adapter.py`
- synthetic trace fixtures: `examples/opentelemetry/`
- generated EEOAP-compatible statements and adapter reports: `generated/`
- scoped tests: `tests/test_opentelemetry_to_eeoap_adapter.py`
- release-candidate support package:
  `papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_15/`
- template and clean-clone verification documentation under
  `papers/opentelemetry-to-eeoap/`

The related EEOAP and AEP local tags are `eeoap-v0.1-artifact` and
`aep-v0.1-artifact`. They are local only and have not been pushed.

## Intended Future Release State

After approval and final checks, the public release should cite a verified
release tag, GitHub Release URL, support package, and DOI if one is created.
The version 1.24 metadata drafts should first be incorporated into an updated
release-candidate support package and rechecked.

## Generated Statements And Adapter Reports

The release materials should include generated statements and adapter reports
for:

- `valid-agent-trace`
- `valid-agent-workflow-trace`

Both valid generated statements must continue to pass the validator with
`ok=true` and `issue_count=0` before public release.

## What Remains TODO

- final release URL
- final release tag
- final GitHub Release URL
- final Zenodo DOI URL, if created
- final public support issue URL
- final checksum verification after metadata updates
- final clean-clone verification after metadata updates

## Pre-Release Wording

The OpenTelemetry-to-EEOAP artifacts are currently maintained in a local
release-candidate branch and package-local support materials. No public
OpenTelemetry-to-EEOAP release URL, DOI, GitHub Release, or pushed release tag
is claimed in this draft. Final artifact availability wording will be updated
after the release package is verified and public identifiers exist.

## Post-Release Wording Template

The OpenTelemetry-to-EEOAP software release is available at TODO: final GitHub
Release URL, with source state identified by TODO: final release tag. The
release support package includes synthetic trace fixtures, generated
EEOAP-compatible statements, adapter reports, metadata files, checksums, and
validation documentation. The archived release DOI is TODO: final DOI if
created. The project support route is TODO: final GitHub Issues URL.

Warning: do not use the post-release wording until the release URL, tag, support
URL, and DOI status are real.
