# Software Metadata

## Software Name

OpenTelemetry-to-EEOAP Adapter: Transforming Agent Telemetry into Portable
Operation Evidence

## Short Name

OpenTelemetry-to-EEOAP Adapter

## Provisional Version

TODO: assign release version before external submission.

Suggested internal placeholder: `otel-eeoap-adapter-v0.1.0-rc`

## Authorship

- Bin Zhang
- ORCID: `https://orcid.org/0009-0002-8861-1481`

TODO: confirm final public affiliation and contact metadata before external
submission.

## Repository Status

The current metadata drafts are local to the release-candidate branch:

- Branch: `softwarex-otel-eeoap-release-candidate`
- Current baseline before v1.8: `7414eaf2e42d984f8567db4d548429038b4e29a1`
- Worktree: `/tmp/agent-evidence-softwarex-otel-eeoap-rc`

No public release URL, DOI, GitHub Release, or pushed tag is claimed in these
metadata drafts.

## License Status

The repository has a root Apache-2.0 `LICENSE`. The metadata drafts use the
SPDX identifier `Apache-2.0`.

TODO: verify whether final SoftwareX packaging requires a `LICENSE.txt` copy or
whether root `LICENSE` is sufficient.

## Source Path

- Adapter: `tools/opentelemetry_to_eeoap_adapter.py`

## Test Path

- Scoped adapter tests: `tests/test_opentelemetry_to_eeoap_adapter.py`

## Example Path

- OpenTelemetry-style fixtures: `examples/opentelemetry/`
- Valid fixtures:
  - `examples/opentelemetry/valid-agent-trace.json`
  - `examples/opentelemetry/valid-agent-workflow-trace.json`
- Invalid fixtures:
  - `examples/opentelemetry/invalid-missing-agent-span.json`
  - `examples/opentelemetry/invalid-unresolved-tool-span.json`
  - `examples/opentelemetry/invalid-broken-parent-span.json`
  - `examples/opentelemetry/invalid-missing-operation-name.json`

## Generated Evidence Path

- `generated/valid-agent-trace-eeoap-statement.json`
- `generated/valid-agent-trace-adapter-report.json`
- `generated/valid-agent-workflow-trace-eeoap-statement.json`
- `generated/valid-agent-workflow-trace-adapter-report.json`

## Related Artifacts

- EEOAP local tag:
  - tag: `eeoap-v0.1-artifact`
  - tag object: `f4270a575517f987dcd45d8ef80a7d30d808f39f`
  - target commit: `96f444b7ed39b39fe9f47e428af835952e843cb0`
  - public status: not pushed, not archived
- AEP local tag:
  - tag: `aep-v0.1-artifact`
  - tag object: `a58aa33501252b26acde085fed3dfa0104e255a0`
  - target commit: `af2b90c14587718a8ed6982131ba9c98e3274054`
  - public status: not pushed, not archived

## Citation Status

This directory includes local draft citation metadata:

- `CITATION_OTEL_EEOAP.cff`
- `codemeta-otel-eeoap.json`

These files are not final release metadata. They do not claim a DOI, public
release URL, or pushed tag.

## Unresolved Release Fields

- Final public repository URL.
- Final release tag.
- Final release version.
- Final release date.
- DOI or archive decision.
- Final artifact availability statement.
- Final data availability statement.
- Final AI-assisted writing disclosure.
- Final conflict of interest and funding declarations.

## No Public Release Yet

- DOI: not created.
- GitHub Release: not created.
- Tag push: not performed.

## Difference From Root AEP-Media Metadata

The root `CITATION.cff` and root `codemeta.json` describe AEP-Media
v0.1.0. They should not be used as OpenTelemetry-to-EEOAP metadata.

These v1.8 metadata drafts describe a separate OpenTelemetry-to-EEOAP adapter
package candidate for a possible SoftwareX route.
