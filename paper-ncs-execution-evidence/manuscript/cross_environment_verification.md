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

The paper-local result file is:

`paper_packs/scientific_workflow_public/cross_environment_verification.json`

The active GitHub Actions workflow is:

`.github/workflows/ncs-cross-environment.yml`

The paper-local workflow copy is:

`paper-ncs-execution-evidence/.github/workflows/ncs-cross-environment.yml`

## Interpretation

The local result establishes that both validators and the checker agree on the current machine. The CI workflow defines the manuscript-facing cross-environment gate. Remote GitHub Actions results must be recorded after the branch is pushed and the workflow completes.
