# Repository audit

## Snapshot

- Date/time: 2026-04-24 CST
- Current branch: `ncs-scientific-workflow-evidence`
- Dirty working tree files: see current `git status --short` during each command run

## Existing top-level `paper*` directories

- `paper`
- `paper-ncs-execution-evidence`

## Local ignore status

- Exact local ignore entry `paper-ncs-execution-evidence/` was removed from `.git/info/exclude`.
- Backup created at `.git/info/exclude.ncs-backup`.
- No broad `paper-*` ignore was removed.
- `paper-ncs-execution-evidence/` is now visible to `git status`.

## Discovered package manager

- `pyproject.toml`
- `setup.py`
- `Makefile`

## Discovered validator CLI candidates

- `validate-profile` (not installed as a standalone command in the current shell)
- `verify-bundle` (not installed as a standalone command in the current shell)
- `verify-export` (not installed as a standalone command in the current shell)
- `agent-evidence` (console entry point declared as `agent_evidence.cli.main:main`; not on PATH in the current shell)
- `.venv/bin/agent-evidence validate-profile <file>` (available)
- `.venv/bin/agent-evidence validate-pack --pack <dir> --strict` (available)
- `.venv/bin/agent-evidence verify-bundle --bundle-dir <dir>` (available)
- `.venv/bin/agent-evidence verify-export` (available)
- `scripts/verify_bundle.py`
- `scripts/verify_evidence_object.py`
- `scripts/run_profile_gate.py`

`validate-pack --pack <dir> --strict` is now implemented in the repository CLI.

## Repository source changes

- CLI source file discovered: `agent_evidence/cli/main.py`
- New validator module: `agent_evidence/validate_pack.py`
- CLI subcommand added: `agent-evidence validate-pack --pack <pack_dir> --strict`

## Command help summaries

- `validate-pack`: Click subcommand accepting `--pack` plus optional `--strict`; validates the native NCS pack contract and returns the NCS exit-code taxonomy.
- `validate-profile`: Click subcommand accepting one JSON profile file plus optional `--schema`; validates `execution-evidence-operation-accountability-profile@0.1`.
- `verify-bundle`: Click subcommand requiring `--bundle-dir`; validates an Agent Evidence Profile bundle directory, not an NCS scientific workflow pack.
- `verify-export`: Click subcommand for repository export bundles/archives, not an NCS scientific workflow pack.

## Repository validator integration status

| Command | Status | Reason |
|---|---|---|
| `.venv/bin/agent-evidence validate-pack --pack <pack> --strict` | strict-integrated | validates native NCS pack directories |
| `.venv/bin/agent-evidence validate-profile repo_compat/operation_accountability_statement.json` | advisory-integrated | validates a derived old-profile statement |
| `.venv/bin/agent-evidence validate-profile bundle.json` | not-compatible | NCS bundle is not the old operation-accountability schema |
| `.venv/bin/agent-evidence validate-profile repo_compat/ncs_bundle_view.json` | not-compatible | NCS bundle view intentionally preserves the NCS contract |
| `.venv/bin/agent-evidence verify-bundle --bundle-dir <pack>` | not-compatible | NCS pack is not an AEP bundle directory |

Observed probe exit codes:

- derived old-profile statement via `validate-profile`: `0`
- native NCS `bundle.json` via `validate-profile`: `1`
- `repo_compat/ncs_bundle_view.json` via `validate-profile`: `1`
- NCS pack directory via `verify-bundle --bundle-dir`: `1`
- `repo_validator_adapter.py`: `0`

Current `repo_validator_config.json` mode: `strict`.

`ncs_verify_pack.sh` now defaults to the repository validator when `.venv/bin/agent-evidence validate-pack` is available. `run_scientific_workflow_validation_matrix.sh` exercises the same strict validator and preserves the expected failure-taxonomy exit codes.

## Discovered schema files

- `agent_evidence/aep/schema_v0.1.json`
- `agent_evidence/schema/evidence.schema.json`
- `schema/execution-evidence-object.schema.json`
- `schema/execution-evidence-operation-accountability-profile-v0.1.schema.json`

## Discovered examples

- `examples/minimal-valid-evidence.json`
- `examples/invalid-missing-required.json`
- `examples/invalid-unclosed-reference.json`
- `examples/invalid-policy-link-broken.json`
- `examples/invalid-provenance-output-mismatch.json`
- `examples/invalid-validation-provenance-link-broken.json`
- `examples/valid-retention-review-evidence.json`
- `examples/valid-high-risk-payment-review-evidence.json`
- `examples/evidence-object-openai-run.json`
- `examples/fdo-style-execution-evidence-object.json`
- `examples/openai-agent-run.json`
- `examples/langchain_minimal_evidence.py`

## Discovered demo files

- `demo/run_operation_accountability_demo.py`
- `demo/scenario.md`
- `demo/expected-output.md`
- `demo/artifacts/minimal-profile-evidence.json`
- `demo/artifacts/validation-report.json`
- `demo/artifacts/input-object.json`
- `demo/artifacts/derived-object.json`
- `demo/artifacts/operation-log.json`

## Discovered tests

- `tests/test_aep_profile.py`
- `tests/test_cli.py`
- `tests/test_export.py`
- `tests/test_hashing.py`
- `tests/test_langchain_integration.py`
- `tests/test_operation_accountability_profile.py`
- `tests/test_serialization_security.py`
- `tests/test_sql_store.py`
- additional integration tests for AGT, Automaton, OpenAI Agents and Postgres

## Discovered CI workflows

- `.github/workflows/ci.yml`
- `.github/workflows/prototype-check.yml`
- `.github/workflows/ncs-cross-environment.yml`
- `paper-ncs-execution-evidence/.github/workflows/ncs-cross-environment.yml`

## Cross-environment verification

Configured matrix:

- native OS: `ubuntu-latest`, `macos-latest`
- Python: `3.11`, `3.12`, `3.13`
- container: local CI image built from `paper-ncs-execution-evidence/docker/Dockerfile.ncs-ci`
- optional pull image: `ghcr.io/joy7758/agent-evidence:ncs-v0.1`

Workflow files:

- active GitHub Actions workflow: `.github/workflows/ncs-cross-environment.yml`
- paper-local manuscript artifact copy: `paper-ncs-execution-evidence/.github/workflows/ncs-cross-environment.yml`

Each environment builds the public Drosophila small RNA-seq pack, runs the repository strict validator, runs the paper-local validator, runs the public failure matrix and runs independent-checker agreement.

Previous container blocker:

- `ghcr.io/joy7758/agent-evidence:ncs-v0.1` failed to pull with Docker exit code `1`.

Resolution:

- CI no longer requires the unavailable GHCR image.
- The container job builds `agent-evidence-ncs-ci:local` from the current checkout and runs the same validation commands inside Docker.
- `ghcr.io/joy7758/agent-evidence:ncs-v0.1` remains an optional non-default pull path controlled by `NCS_CONTAINER_PULL_IMAGE=1`.

Local cross-environment harness:

- command: `bash paper-ncs-execution-evidence/scripts/run_cross_environment_verification.sh`
- repository strict validator exit code: `0`
- paper-local validator exit code: `0`
- public failure matrix exit code: `0`
- independent checker agreement exit code: `0`
- local Docker container status: `not-run`
- result file: `paper-ncs-execution-evidence/paper_packs/scientific_workflow_public/cross_environment_verification.json`

Previous remote GitHub Actions status:

- run id: `24881392886`
- trigger: push to `ncs-scientific-workflow-evidence`
- native Ubuntu/Python matrix: PASS for Python `3.11`, `3.12`, `3.13`
- native macOS/Python matrix: PASS for Python `3.11`, `3.12`, `3.13`
- container matrix: FAIL before validation because `ghcr.io/joy7758/agent-evidence:ncs-v0.1` could not be pulled
- container failure reason: Docker pull failed with exit code `1` during GitHub Actions container initialization

Latest remote GitHub Actions status:

- run id: `24882352219`
- run URL: `https://github.com/joy7758/agent-evidence/actions/runs/24882352219`
- trigger: push to `ncs-scientific-workflow-evidence`
- conclusion: PASS
- native Ubuntu/Python matrix: PASS for Python `3.11`, `3.12`, `3.13`
- native macOS/Python matrix: PASS for Python `3.11`, `3.12`, `3.13`
- container local-build job: PASS
- container validation path: built `agent-evidence-ncs-ci:local` from `paper-ncs-execution-evidence/docker/Dockerfile.ncs-ci`, installed the current checkout and ran the public pack validator, public failure matrix and independent-checker agreement
- immutable OCI release digest: TODO before submission

## NCS verifier connection

`ncs_verify_pack.sh` defaults to the repository validator:

```bash
.venv/bin/agent-evidence validate-pack --pack <pack> --strict
```

It falls back to the paper-local validator only when no repository `validate-pack` command is available. The repository validator adapter is now strict via `repo_validator_config.json`.

The manuscript-facing scientific workflow pack is `paper_packs/scientific_workflow_public/`, built from Zenodo DOI `10.5281/zenodo.826906`. The earlier smoke pack remains a regression fixture.

## Public dataset source metadata

- DOI: `10.5281/zenodo.826906`
- Zenodo API snapshot: present
- DataCite API snapshot: present
- Compact verification record: present
- Source metadata verification status: PASS
- License status: verified
- License id: `cc-by-4.0`
- License title: `Creative Commons Attribution 4.0`
- License URL: `https://creativecommons.org/licenses/by/4.0`
- License source: `Zenodo API / DataCite API`
- Local file MD5 verification: pass for six FASTQ inputs
- Zenodo file MD5 verification: pass for six FASTQ inputs
- Dataset source manifest license TODO: resolved
- Boundary: GTN tutorial content license is not used as a substitute for Zenodo/DataCite data-file license metadata

## Gaps blocking NCS submission

| Gap | Current status | Required for NCS | Next action |
|---|---|---|---|
| scientific workflow smoke pack | DONE | executable local FASTQ fixture + deterministic outputs + receipt | keep as smoke gate |
| strict repository validator | DONE | native `validate-pack --pack --strict` | keep |
| public scientific dataset pack | DONE | public dataset + deterministic outputs + receipt | keep matrix green |
| failure injection public matrix | DONE | deterministic FAIL codes | keep matrix green |
| independent checker | DONE | agreement table | keep agreement table current |
| native cross-environment matrix | DONE | Ubuntu/macOS plus Python 3.11-3.13 | keep CI green |
| container verification | DONE | Docker validation from local CI image | keep CI green |
| dataset license/source metadata | DONE | source license verified before submission | keep source metadata verification current |
| immutable OCI release digest | TODO | reproducible image reference before submission | publish release image |
| manuscript results extraction | TODO | figure-data tables and text | extract results |
| baseline comparison | draft | accurate comparison section | refine |
| related manuscripts disclosure | draft | final statuses | update manually |
