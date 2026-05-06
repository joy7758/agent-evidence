# Historical Lineage

Agent Evidence / AEP v0.1 is the current primary entry surface in this
repository. This note gathers the earlier naming layers and historical prototype
surfaces so the main README can stay focused on the current package path.

## Current Primary Path

- Agent Evidence = the concrete execution-evidence entry point for the Digital Biosphere Architecture
- Current package = `Execution Evidence and Operation Accountability Profile v0.1`
- System context = [digital-biosphere-architecture](https://github.com/joy7758/digital-biosphere-architecture)
- Walkthrough = [verifiable-agent-demo](https://github.com/joy7758/verifiable-agent-demo)
- Post-execution review = [aro-audit](https://github.com/joy7758/aro-audit)
- Execution-integrity upstream surface = [fdo-kernel-mvk](https://github.com/joy7758/fdo-kernel-mvk), which can hand off a local MVK `audit_bundle.json` bridge bundle into the Agent Evidence verification and packaging path

## Execution Evidence Object

Before the current v0.1 package path, this repository used `Execution Evidence
Object` as the main top-level framing for a standards prototype.

Historical assets retained in the repository:

- `spec/execution-evidence-object.md`
- `schema/execution-evidence-object.schema.json`
- `examples/evidence-object-openai-run.json`
- `scripts/verify_evidence_object.py`
- `scripts/demo_execution_evidence_object.py`
- `docs/architecture/execution-evidence-object.md`
- `docs/architecture/execution-evidence-object-one-page.md`

Historical top-level wording retained from the older README surface:

- English: `This repository now includes a standards proposal prototype for an Execution Evidence Object.`
- Chinese: `这个仓库现在包含一个“执行证据对象”的标准提案原型。`

Historical prototype commands:

```bash
python3 scripts/verify_evidence_object.py examples/evidence-object-openai-run.json
python3 scripts/demo_execution_evidence_object.py
```

These surfaces are preserved as lineage material, not as the current primary
entry.

## Agent Evidence Profile Legacy Surface

Later repository copies used `Agent Evidence Profile` or `AEP` as the
top-of-page label for the bundle-verification path before the current package
structure was tightened around the v0.1 handoff package.

Historical assets retained from that surface:

- `release/v0.1-live-chain/README.md`
- `release/v0.1-live-chain/What-AEP-proves-and-what-it-does-not-prove.md`
- `release/v0.1-live-chain/RELEASE_NOTE.md`
- `scripts/run_profile_gate.py`

Historical specimen DOI:

- https://doi.org/10.5281/zenodo.19055948

This legacy surface still matters for provenance and reproducibility, but the
current primary README entry is the v0.1 package path under `spec/`, `schema/`,
`examples/`, `demo/`, and `docs/STATUS.md`.

## Older FDO Mapping Wording

Earlier public-facing copies sometimes presented the repository primarily
through `Execution Evidence Object` and FDO-facing wording. That history is
retained, but it is now subordinate to the current Agent Evidence / AEP v0.1
entry surface.

Relevant historical files:

- `docs/fdo-mapping/execution-evidence-to-fdo.md`
- `docs/fdo-mapping/minimal-fdo-object-example.md`
- `docs/outreach/public-positioning.md`

Current interpretation:

- FDO mapping remains useful supporting material
- Agent Evidence / AEP v0.1 remains the current primary entry surface
- System-level interpretation remains in `digital-biosphere-architecture`
