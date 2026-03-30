# Operation Accountability Statement Examples

These examples target
`execution-evidence-operation-accountability-profile@0.1` and are intended to
produce one validation report per file.

## Files

- `minimal-valid-evidence.json`
  - Passes schema, reference closure, policy/provenance/evidence consistency,
    and integrity recomputation.
- `invalid-missing-required.json`
  - Fails because `validation.method` is intentionally removed.
  - Main broken rule: required field completeness.
- `invalid-unclosed-reference.json`
  - Fails because the operation output reference points to `ref:missing-output`,
    which is not defined in `evidence.references`.
  - Main broken rule: reference closure.
- `invalid-policy-link-broken.json`
  - Fails because `evidence.policy_ref` points to `policy:stale-metadata-v1`
    instead of the declared `policy.id`.
  - Main broken rule: policy/evidence link consistency.

## Validate

```bash
agent-evidence validate-profile examples/minimal-valid-evidence.json
agent-evidence validate-profile examples/invalid-missing-required.json
agent-evidence validate-profile examples/invalid-unclosed-reference.json
agent-evidence validate-profile examples/invalid-policy-link-broken.json
```
