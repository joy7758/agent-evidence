# Expected Output

## Valid Example

Command:

```bash
agent-evidence validate-profile examples/minimal-valid-evidence.json
```

Expected summary:

- JSON output includes `"ok": true`
- `issue_count` is `0`
- `summary` contains one `PASS execution-evidence-operation-accountability-profile@0.1 ...` line

## Invalid Examples

### Missing required field

Command:

```bash
agent-evidence validate-profile examples/invalid-missing-required.json
```

Expected summary:

- JSON output includes `"ok": false`
- primary error code: `schema_violation`
- failure reason: `validation.method` is missing

### Unclosed reference

Command:

```bash
agent-evidence validate-profile examples/invalid-unclosed-reference.json
```

Expected summary:

- JSON output includes `"ok": false`
- primary error code: `unresolved_output_ref`
- failure reason: `operation.output_refs[0]` points to `ref:missing-output`

### Broken policy link

Command:

```bash
agent-evidence validate-profile examples/invalid-policy-link-broken.json
```

Expected summary:

- JSON output includes `"ok": false`
- primary error code: `unresolved_evidence_policy_ref`
- failure reason: `evidence.policy_ref` does not resolve to `policy.id`

## Demo Script

Command:

```bash
python3 demo/run_operation_accountability_demo.py
```

Main output shape:

1. `Step 1: object load or creation`
2. `Step 2: profile precheck`
3. `Step 3: operation call`
4. `Step 4: evidence generation`
5. `Step 5: validator verification`
6. `Step 6: output verification result`

Expected end state:

- one `PASS execution-evidence-operation-accountability-profile@0.1 ...` line
- `demo/artifacts/minimal-profile-evidence.json` exists
- `demo/artifacts/validation-report.json` exists

## Error Code Reference

- `schema_violation`: required field or field shape does not satisfy the schema
- `unresolved_output_ref`: an operation output ref does not resolve to `evidence.references[].ref_id`
- `unresolved_evidence_policy_ref`: `evidence.policy_ref` does not resolve to `policy.id`
