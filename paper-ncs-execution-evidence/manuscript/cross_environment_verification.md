# Cross-environment verification protocol

## Purpose

The cross-environment gate checks whether the manuscript-facing public scientific workflow pack validates consistently across native operating systems, Python versions and a clean CI container image built from the current checkout.

## Matrix

| Environment dimension | Values |
|---|---|
| Native OS | `ubuntu-latest`, `macos-latest` |
| Python | `3.11`, `3.12`, `3.13` |
| Container | local CI image built from `paper-ncs-execution-evidence/docker/Dockerfile.ncs-ci` |

## Checks

Each environment runs:

1. public scientific workflow pack build;
2. repository strict validation through `agent-evidence validate-pack --pack <pack> --strict`;
3. paper-local strict validation through `scripts/validate_ncs_pack.py`;
4. public failure-matrix validation;
5. independent-checker agreement validation;
6. receipt-digest and agreement reporting.

## Current local result

The local cross-environment harness records repository validator, paper-local validator, public failure matrix, independent checker agreement and container-result status. Container verification writes `container_verification_result.json` only when the Docker validation actually runs.

Container verification now builds an ephemeral image from the current checkout using `python:3.12-slim`. It does not require `ghcr.io/joy7758/agent-evidence:ncs-v0.1` for CI success. The GHCR image remains an optional pull path for future immutable releases.

## Remote CI result

GitHub Actions run `24881392886` was triggered from branch `ncs-scientific-workflow-evidence`.

Native environments passed:

- `ubuntu-latest`, Python `3.11`
- `ubuntu-latest`, Python `3.12`
- `ubuntu-latest`, Python `3.13`
- `macos-latest`, Python `3.11`
- `macos-latest`, Python `3.12`
- `macos-latest`, Python `3.13`

The container environment did not initialize because GitHub Actions could not pull `ghcr.io/joy7758/agent-evidence:ncs-v0.1`; Docker pull failed with exit code `1`.

That blocker is addressed by the local-image CI path. A future release should publish an immutable OCI image digest before submission.

The data source license remains a separate submission blocker.

The paper-local result file is:

`paper_packs/scientific_workflow_public/cross_environment_verification.json`

The active GitHub Actions workflow is:

`.github/workflows/ncs-cross-environment.yml`

The paper-local workflow copy is:

`paper-ncs-execution-evidence/.github/workflows/ncs-cross-environment.yml`

## Interpretation

The native CI matrix establishes agreement across macOS and Ubuntu runners for Python `3.11`, `3.12` and `3.13`. Container agreement is now tested through a locally built CI image rather than an unavailable registry image.
