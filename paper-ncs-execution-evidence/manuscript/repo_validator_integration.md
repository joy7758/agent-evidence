# Repository validator integration

## Previous status

The repository validator integration was advisory only. The NCS pack generated a
derived `repo_compat/operation_accountability_statement.json` artifact that
passed the existing `validate-profile` command, but the native NCS pack contract
was not validated by the repository CLI.

## New status

Current integration mode: `strict`.

The repository CLI now exposes native NCS pack validation:

```bash
.venv/bin/agent-evidence validate-pack --pack paper-ncs-execution-evidence/paper_packs/scientific_workflow --strict
```

This command validates the native NCS pack directory, including `manifest.json`,
`bundle.json`, `receipt.json`, `summary.json`, `expected_digest.txt`, policy,
provenance, input/output artifacts, evidence artifacts, digest linkage, temporal
ordering and outcome linkage.

## Commands Discovered

| Command | Discovery result | Help/source summary | Native input contract |
|---|---|---|---|
| `validate-profile` | not installed as standalone command in shell | not available on PATH | not tested directly |
| `verify-bundle` | not installed as standalone command in shell | not available on PATH | not tested directly |
| `verify-export` | not installed as standalone command in shell | not available on PATH | not tested directly |
| `agent-evidence` | console entry point declared; `.venv/bin/agent-evidence` exists | Click group in `agent_evidence/cli/main.py` | repository CLI |
| `.venv/bin/agent-evidence validate-profile` | available | validates one operation-accountability profile JSON file | `execution-evidence-operation-accountability-profile@0.1` JSON statement |
| `.venv/bin/agent-evidence verify-bundle` | available | verifies an Agent Evidence Profile bundle directory offline | AEP bundle directory, not NCS pack |
| `.venv/bin/agent-evidence verify-export` | available | verifies repository export bundle/archive forms | exported repository bundle/archive, not NCS pack |
| `.venv/bin/agent-evidence validate-pack` | available | validates native NCS pack directories | NCS pack directory |

## Compatibility Matrix

| Command | Native NCS pack | Derived compatibility artifact | Integration status |
|---|---:|---:|---|
| `validate-pack --pack <pack> --strict` | Yes | Not needed | `strict-integrated` |
| `validate-profile` | No | Yes, `repo_compat/operation_accountability_statement.json` | `advisory-integrated` |
| `verify-bundle` | No | No | `not-compatible` |
| `verify-export` | No | No | `not-compatible` |

## Tested Command Lines

| Command | Observed exit code | Interpretation |
|---|---:|---|
| `.venv/bin/agent-evidence validate-pack --pack paper-ncs-execution-evidence/paper_packs/scientific_workflow --strict` | 0 | native NCS valid pack passes |
| `.venv/bin/agent-evidence validate-pack --pack paper-ncs-execution-evidence/paper_packs/scientific_workflow/failures/tampered_input --strict` | 2 | expected digest mismatch |
| `.venv/bin/agent-evidence validate-pack --pack paper-ncs-execution-evidence/paper_packs/scientific_workflow/failures/tampered_output --strict` | 2 | expected digest mismatch |
| `.venv/bin/agent-evidence validate-pack --pack paper-ncs-execution-evidence/paper_packs/scientific_workflow/failures/missing_policy --strict` | 5 | expected policy linkage failure |
| `.venv/bin/agent-evidence validate-pack --pack paper-ncs-execution-evidence/paper_packs/scientific_workflow/failures/broken_evidence_link --strict` | 11 | expected reference resolution failure |
| `.venv/bin/agent-evidence validate-pack --pack paper-ncs-execution-evidence/paper_packs/scientific_workflow/failures/version_mismatch --strict` | 4 | expected version/profile mismatch |
| `.venv/bin/agent-evidence validate-pack --pack paper-ncs-execution-evidence/paper_packs/scientific_workflow/failures/temporal_inconsistency --strict` | 6 | expected temporal inconsistency |
| `.venv/bin/agent-evidence validate-pack --pack paper-ncs-execution-evidence/paper_packs/scientific_workflow/failures/outcome_unverifiable --strict` | 7 | expected outcome unverifiable |
| `.venv/bin/agent-evidence validate-profile paper-ncs-execution-evidence/paper_packs/scientific_workflow/repo_compat/operation_accountability_statement.json` | 0 | advisory-compatible derived old-profile statement |
| `.venv/bin/agent-evidence validate-profile paper-ncs-execution-evidence/paper_packs/scientific_workflow/bundle.json` | 1 | native NCS bundle is not the old profile schema |
| `.venv/bin/agent-evidence verify-bundle --bundle-dir paper-ncs-execution-evidence/paper_packs/scientific_workflow` | 1 | NCS pack is not an AEP bundle directory |

## Current Decision

The strict repository validator is now the manuscript-facing validator for the
NCS smoke pack. `ncs_verify_pack.sh` defaults to repository validation when
`.venv/bin/agent-evidence validate-pack` is available, and the scientific
workflow matrix exercises the same strict validator.

The `repo_compat/` artifacts remain useful as an advisory bridge to the older
operation-accountability profile, but they are no longer the strict validation
surface for the NCS pack.
