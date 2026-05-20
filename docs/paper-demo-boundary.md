# Paper Demo Boundary

Keywords: EEOAP, execution evidence, operation accountability, validator, FDO-style mapping, paper_case.

## Scenario

The `examples/paper_case/` demo models one local AI agent operation: an aggregate-only analysis over an FDO-style dataset descriptor. The operation emits an aggregate summary object and binds that output to a declared content hash. The policy denies row-level records, personal data, raw prompts, and unredacted logs.

## Files

- `examples/paper_case/fdo-dataset.json` describes the input object in an FDO-style shape for discussion.
- `examples/paper_case/policy-aggregate-only.json` describes the aggregate-only policy.
- `examples/paper_case/agent-operation.json` records actor, action, subject, output, timestamp, policy, and provenance notes.
- `examples/paper_case/evidence-valid.json` is the valid EEOAP evidence object.
- `examples/paper_case/evidence-invalid-tampered-output.json` changes the output digest and leaves integrity binding stale so tampering is detectable.
- `examples/paper_case/expected-validator-pass.json` and `examples/paper_case/expected-validator-fail.json` document expected outcomes.

## Validation Path

Run:

```bash
make paper-demo
```

The Makefile target calls `scripts/reproduce_paper_demo.sh`. The script prefers the local `agent-evidence validate-profile` command when available and also runs a local Python check that loads the paper_case files, verifies required artifacts, checks the valid EEOAP profile, and confirms the tampered output digest does not match the operation output hash.

## PASS and FAIL Meaning

`PASS valid evidence bundle` means the valid paper_case object is structurally valid, internally bound, integrity-checkable, and aligned with the operation output hash.

`FAIL tampered output hash mismatch` is an expected negative result. It means the tampered case was rejected because the output reference hash no longer matches the operation output hash and its stale integrity binding is detectable.

## ZKP Boundary

ZKP is not implemented in this paper_case demo. It remains future work for privacy-preserving selective disclosure. The current version is deliberately simpler: ordinary JSON evidence, references, and hashes that can be inspected offline.
