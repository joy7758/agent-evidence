# AEP v0.1 Live-Chain Specimen

## Subtitle

An integrity-verifiable evidence profile specimen for autonomous agent runs

## Artifact DOI

https://doi.org/10.5281/zenodo.19055948

## What this release is

This release packages the first public, reproducible live-chain specimen of AEP (Agent Evidence Profile).

## What it proves

- real runtime export
- offline verification pass
- tamper detection fail path
- runtime provenance capture with optional `--runtime-root`

## What it does not prove

- not a non-repudiation system
- no external signing / anchoring by default
- strength depends on capture boundary and anchoring model

See the boundary statement: [What-AEP-proves-and-what-it-does-not-prove.md](What-AEP-proves-and-what-it-does-not-prove.md)

## What this release contains

- AEP schema
- verify CLI
- LangChain exporter
- Automaton exporter
- LIVE_RUNBOOK
- public valid / invalid fixtures
- specimen gate

## How to reproduce

```bash
python scripts/run_specimen_gate.py
python -m pytest -q
agent-evidence verify-bundle --bundle-dir <fixture-or-exported-bundle>
```

## Release positioning

AEP is an integrity-verifiable evidence profile specimen for autonomous agent runs, with offline verification, tamper detection, and optional runtime provenance capture.
