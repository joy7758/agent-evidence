# Operation Accountability Statement Examples

These examples target
`execution-evidence-operation-accountability-profile@0.1` and are intended to
produce one validation report per file.

## Files

- `minimal-valid-evidence.json`
  - Passes schema, reference closure, policy/provenance/evidence consistency,
    and integrity recomputation.
- `valid-retention-review-evidence.json`
  - Passes the same profile checks in a second context:
    one dataset package subject, two input references, and one retention decision output.
  - Main value: second-context validity evidence for the same minimal profile.
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
- `invalid-provenance-output-mismatch.json`
  - Fails because `provenance.output_refs` points to `ref:input-note`
    instead of matching `operation.output_refs`.
  - Main broken rule: provenance/operation cross-field binding consistency.
- `invalid-validation-provenance-link-broken.json`
  - Fails because `validation.provenance_ref` points to
    `prov:missing-metadata-enrich-001`, which is not defined locally.
  - Main broken rule: validation/provenance reference closure.

## Validate

```bash
agent-evidence validate-profile examples/minimal-valid-evidence.json
agent-evidence validate-profile examples/valid-retention-review-evidence.json
agent-evidence validate-profile examples/invalid-missing-required.json
agent-evidence validate-profile examples/invalid-unclosed-reference.json
agent-evidence validate-profile examples/invalid-policy-link-broken.json
agent-evidence validate-profile examples/invalid-provenance-output-mismatch.json
agent-evidence validate-profile examples/invalid-validation-provenance-link-broken.json
```
