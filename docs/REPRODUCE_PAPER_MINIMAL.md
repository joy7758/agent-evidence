# Reproduce Paper Minimal

This is the minimal paper-facing rerun path for the operation-accountability
profile boundary.

## Scope

The rerun validates:

- `examples/minimal-valid-evidence.json`
- `examples/invalid-missing-required.json`
- `examples/invalid-unclosed-reference.json`
- `examples/invalid-policy-link-broken.json`
- `demo/run_operation_accountability_demo.py`

It does not run AEP-Media, AI Act, Automaton, LangChain, OpenAI Agents, or
full-repository integration tests.

## Command

Run from the repository root:

```bash
bash scripts/reproduce_paper_minimal.sh
```

## Expected Results

Expected command outcomes:

| Command | Expected exit | Expected result |
| --- | ---: | --- |
| `agent-evidence validate-profile examples/minimal-valid-evidence.json` | 0 | `ok: true` |
| `agent-evidence validate-profile examples/invalid-missing-required.json` | non-zero | `schema_violation` |
| `agent-evidence validate-profile examples/invalid-unclosed-reference.json` | non-zero | `unresolved_output_ref` |
| `agent-evidence validate-profile examples/invalid-policy-link-broken.json` | non-zero | `unresolved_evidence_policy_ref` |
| `python demo/run_operation_accountability_demo.py` | 0 | `PASS execution-evidence-operation-accountability-profile@0.1` |

## Output

The script writes command outputs and the rerun summary under:

```text
artifacts/paper-minimal-rerun/
```

The summary file is:

```text
artifacts/paper-minimal-rerun/summary.json
```

The summary records:

- timestamp
- Python version
- git commit
- command
- expected exit
- observed exit
- expected primary code
- observed result

## Claim Boundary

Passing this rerun only supports the paper-minimal claim that the repository has
a bounded, independently rerunnable validation path for one operation
accountability profile. It does not prove production readiness, legal
non-repudiation, compliance approval, official FDO adoption, semantic
correctness, or broad governance-platform coverage.
