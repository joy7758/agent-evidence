# Origin AEP Spec Release Kit v0.1

Status: local experimental protocol-candidate package.

This kit is a deterministic local review artifact. It does not claim external standard-body adoption, legal compliance, external certification, publication acceptance, production readiness, or vendor endorsement.

## Validate

```bash
python3 spec_release_v0_1/validator/spec_validator.py spec_release_v0_1/examples/github_pr_example.json
python3 -m json.tool spec_release_v0_1/schema/canonical_schema_v0_1.json
```

Affected clauses: EEOAP-001, EEOAP-002, EEOAP-003, EEOAP-004, EEOAP-005.
