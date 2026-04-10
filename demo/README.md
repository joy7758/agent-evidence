# Minimal Demo

This demo is the smallest runnable path in the current Agent Evidence / AEP
v0.1 package surface.

It is part of the current primary entry for this repository, not the historical
`Execution Evidence Object` prototype surface.

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

For system context, start with
[digital-biosphere-architecture](https://github.com/joy7758/digital-biosphere-architecture).
For historical naming surfaces, see [docs/lineage.md](../docs/lineage.md).
