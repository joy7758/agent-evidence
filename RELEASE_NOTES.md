# Release Notes

## v0.6.0 Review Pack V0.3 Release Prep

This release-prep entry prepares `agent-evidence` v0.6.0 after Review Pack
V0.3 was merged and post-merge audited. It does not publish a GitHub Release,
TestPyPI package, or PyPI package by itself.

### Added

- Review Pack V0.3 reviewer-facing stabilization:
  - stable `RP-CHECK-*` reviewer checklist IDs
  - `pack_creation_mode: local_offline`
  - `Secret and Private Key Boundary` summary section
  - conservative `secret_scan_status`
  - optional `--json-errors` for `review-pack create` failures
- Review Pack manifest and receipt clarity fields for reviewers and agents:
  - `review_pack_version`
  - `pack_creation_mode`
  - `verification_ok`
  - `record_count`
  - `signature_count`
  - `verified_signature_count`
  - `included_artifacts`
  - `artifact_inventory`
  - `reviewer_checklist`
  - `secret_scan_status`
  - `non_claims`
- Structured Review Pack failure output remains opt-in and limited to
  `agent-evidence review-pack create --json-errors`.

### Safety Boundaries

- Review Pack V0.3 is local and offline.
- Review Pack creation verifies signed exports before packaging.
- Review Pack creation fails closed when verification fails.
- Review Pack creation does not mutate source artifacts.
- Review Pack creation does not copy private keys.
- Review Pack creation does not add telemetry.
- Review Pack creation does not change OpenAPI or MCP behavior.
- Review Pack creation does not change canonical schema or core validation.
- `secret_scan_status` is not comprehensive DLP and does not prove all possible
  secrets are absent.
- No legal non-repudiation, court-grade proof, or regulatory certification
  claim is made.
- Review Pack V0.3 is not compliance certification.
- Review Pack V0.3 is not AI Act approval.
- Review Pack V0.3 is not a full AI governance assessment.
- `agent-evidence` is not a full AI governance platform.

### Non-Goals

- No AI Act Pack.
- No PDF or HTML report generator.
- No dashboard.
- No hosted or remote review service.
- No remote MCP.
- No MCP registry publication.
- No OpenAPI or MCP Review Pack exposure.
- No GitHub Pages or `ADOPTERS.md`.
- No canonical schema rewrite.
- No core validation rewrite.
- No old NCS/media work.

### Release Actions Still Required

- Confirm final v0.6.0 release authorization.
- Confirm GitHub release body.
- Confirm PyPI/TestPyPI publication intent.
- Confirm Zenodo behavior after GitHub release.
- Confirm v0.6.0 installed-package smoke after publication.

## v0.5.0 Review Pack V0.2 Release

This release entry records `agent-evidence` v0.5.0 after Review Pack V0.2 was
merged, post-merge audited, and published to GitHub, Zenodo, TestPyPI, and PyPI.

### Added

- Review Pack V0.2 reviewer-facing summary improvements:
  - reviewer checklist
  - verification details table
  - artifact inventory table
  - findings table
  - recommended reviewer actions
  - `What This Does Not Prove` section
- Review Pack manifest and receipt clarity fields for reviewers and agents:
  - `review_pack_version`
  - `verification_ok`
  - `record_count`
  - `signature_count`
  - `verified_signature_count`
  - `included_artifacts`
  - `artifact_inventory`
  - `non_claims`
- Refined bounded findings taxonomy for local review packages.
- Explicit tampered bundle fail-closed coverage.

### Safety Boundaries

- Review Pack V0.2 is local and offline.
- Review Pack creation verifies signed exports before packaging.
- Review Pack creation fails closed when verification fails.
- Review Pack creation does not mutate source artifacts.
- Review Pack creation does not copy private keys.
- Review Pack creation does not add telemetry.
- Review Pack creation does not change OpenAPI or MCP behavior.
- Review Pack creation does not change canonical schema or core validation.
- No legal non-repudiation, court-grade proof, or regulatory certification
  claim is made.
- Review Pack V0.2 is not compliance certification.
- Review Pack V0.2 is not AI Act approval.
- Review Pack V0.2 is not a full AI governance assessment.
- `agent-evidence` is not a full AI governance platform.

### Non-Goals

- No AI Act Pack.
- No PDF or HTML report generator.
- No dashboard.
- No hosted or remote review service.
- No remote MCP.
- No MCP registry publication.
- No OpenAPI or MCP Review Pack exposure.
- No GitHub Pages or `ADOPTERS.md`.
- No canonical schema rewrite.
- No core validation rewrite.
- No old NCS/media work.

### Release Status

- GitHub Release v0.5.0: completed.
- Zenodo v0.5.0 archive: completed.
- TestPyPI v0.5.0 publication: completed.
- PyPI v0.5.0 publication: completed.
- v0.5.0 clean install smoke: completed.
- This docs-only post-release correction does not publish a new package.

## v0.4.0 Review Pack Release Prep

This release-prep entry prepares `agent-evidence` v0.4.0 after Review Pack
V0.1 was merged.

### Added

- Review Pack V0.1 local reviewer-facing packaging:
  - `agent-evidence review-pack create`
  - `manifest.json`
  - `receipt.json`
  - `findings.json`
  - `summary.md`
  - `artifacts/evidence.bundle.json`
  - `artifacts/manifest-public.pem`
  - optional `artifacts/summary.json`
- Review Pack cookbook:
  - `docs/cookbooks/review_pack_minimal.md`
- Review Pack tests for:
  - LangChain example pack creation
  - OpenAI-compatible mock pack creation
  - fail-closed verification behavior
  - no private key copying
  - no secret leakage
  - no network calls
  - boundary language in reviewer summaries

### Safety Boundaries

- Review Pack V0.1 is local and offline.
- Review Pack creation verifies signed exports before packaging.
- Review Pack creation does not mutate source artifacts.
- Review Pack creation does not copy private keys.
- Review Pack creation does not add telemetry.
- Review Pack creation does not change OpenAPI or MCP behavior.
- Review Pack creation does not change canonical schema or core validation.
- No legal non-repudiation, court-grade proof, or regulatory certification
  claim is made.
- `agent-evidence` is not a full AI governance platform.

### Non-Goals

- No AI Act Pack.
- No PDF or HTML report generator.
- No hosted review service.
- No remote MCP.
- No MCP registry publication.
- No GitHub Pages or `ADOPTERS.md`.
- No canonical schema rewrite.
- No core validation rewrite.
- No old NCS/media work.

### Release Actions Still Required

- Confirm final v0.4.0 release authorization.
- Confirm GitHub release body.
- Confirm PyPI/TestPyPI publication intent.
- Confirm Zenodo behavior after GitHub release.
- Confirm v0.4.0 installed-package smoke after publication.

## v0.3.1 Metadata-Only Patch Prep

This metadata-only patch prepares `agent-evidence` v0.3.1 after GitHub Release
v0.3.0 was archived by Zenodo.

### Changed

- Primary project citation now uses the Zenodo concept DOI:
  `10.5281/zenodo.19334061`.
- The exact v0.3.0 version DOI is documented for release-specific citation:
  `10.5281/zenodo.19998176`.
- The exact v0.3.1 version DOI is documented for release-specific citation:
  `10.5281/zenodo.19998690`.
- Release metadata, citation guidance, generated agent metadata, and release
  readiness docs are aligned on version `0.3.1`.

### Scope

- Metadata-only patch.
- No code behavior changes.
- No OpenAPI, MCP, schema, or core validation changes.
- No PyPI/TestPyPI release was made for `0.3.0`.

## v0.3.0 Release Prep

This release-prep entry summarizes the agent-native discovery and local
callable-surface work merged after v0.2.0. This file prepares the repository
for a v0.3.0 release; it does not publish the release by itself.

### Added

- Agent-native discovery surfaces:
  - `AGENTS.md`
  - `llms.txt`
  - `llms-full.txt`
  - `agent-index.json`
  - `agent-index.schema.json`
  - `docs/for-agents.md`
- Citation, attribution, and recommendation-policy metadata:
  - `CITATION.cff`
  - `codemeta.json`
  - `ATTRIBUTION.md`
  - `RECOMMENDATION_POLICY.md`
  - `docs/how-to-cite.md`
- Development ledger and metadata validation workflow.
- `agent-evidence capabilities --json` for machine-readable callable-surface
  metadata.
- Generated agent metadata checks for `agent-index.json` and `llms-full.txt`.
- Local OpenAPI thin wrapper:
  - `openapi.yaml`
  - `agent-evidence serve --host 127.0.0.1 --port 8765`
  - local endpoints for health, capabilities, profile validation, and bundle
    verification.
- Local MCP stdio read-only / verify-first wrapper:
  - `agent-evidence mcp --transport stdio`
  - fixed tools: `list_capabilities`, `list_schemas`, `validate_profile`,
    `verify_bundle`
  - fixed read-only resources under `agent-evidence://`.
- LangChain 5-minute runnable path with offline/mock behavior and
  `verify-export` coverage.
- OpenAI-compatible minimal evidence path with mock/offline default behavior.
- OpenAI-compatible hardening tests for live configuration errors,
  no-network mock behavior, and no provider-secret leakage into artifacts.

### Safety Boundaries

- No telemetry is added.
- No automatic star, follow, fork, recommendation, or promotion mechanism is added.
- No legal non-repudiation, court-grade proof, or regulatory certification
  claim is made.
- `agent-evidence` is not a full AI governance platform.
- The CLI/core remains canonical; local OpenAPI and MCP surfaces are wrappers.
- OpenAPI is local-only and is not a hosted API product.
- MCP is local stdio only and is not a remote or registry-published service.

### Non-Goals

- No remote MCP.
- No MCP registry publication.
- No GitHub Pages or `ADOPTERS.md`.
- No Review Pack commercial feature.
- No AI Act Pack.
- No canonical schema rewrite.
- No core validation rewrite.
- No old NCS/media work.

### Release Actions Still Required

- Confirm final version and release date.
- Confirm whether the existing DOI remains the concept/repository DOI or
  whether release-specific archive metadata should be added after publication.
- Create the GitHub release if approved.
- Publish to PyPI if approved.
- Confirm release notes and package metadata after publication.
