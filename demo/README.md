# Minimal Demo

This demo implements one policy-constrained metadata enrichment path.

Flow:

1. load one source object
2. run a minimal profile precheck
3. apply one constrained operation
4. generate one operation accountability statement
5. validate the statement with the profile-aware validator
6. write artifacts and one validation report for review

Run:

```bash
python3 demo/run_operation_accountability_demo.py
```

Artifacts are written under `demo/artifacts/`.
