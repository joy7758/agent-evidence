# Cross-environment verification protocol

## Purpose

The cross-environment gate checks whether the manuscript-facing public scientific workflow pack validates consistently across native operating systems, Python versions and the declared container image.

## Matrix

| Environment dimension | Values |
|---|---|
| Native OS | `ubuntu-latest`, `macos-latest` |
| Python | `3.11`, `3.12`, `3.13` |
| Container | `ghcr.io/joy7758/agent-evidence:ncs-v0.1` |

## Checks

Each environment runs:

1. public scientific workflow pack build;
2. repository strict validation through `agent-evidence validate-pack --pack <pack> --strict`;
3. paper-local strict validation through `scripts/validate_ncs_pack.py`;
4. public failure-matrix validation;
5. independent-checker agreement validation;
6. receipt-digest and agreement reporting.

## Current local result

The local cross-environment harness passes the repository validator, paper-local validator, public failure matrix and independent checker agreement checks. The local Docker run was not executed because Docker was not available or not running in this session.

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

The paper-local result file is:

`paper_packs/scientific_workflow_public/cross_environment_verification.json`

The active GitHub Actions workflow is:

`.github/workflows/ncs-cross-environment.yml`

The paper-local workflow copy is:

`paper-ncs-execution-evidence/.github/workflows/ncs-cross-environment.yml`

## Interpretation

The local result and native CI matrix establish agreement across macOS and Ubuntu runners for Python `3.11`, `3.12` and `3.13`. Container verification remains blocked until the declared GHCR image is published or made accessible to GitHub Actions.
