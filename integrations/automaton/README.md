# Automaton Exporter

This exporter is a Conway-neutral, read-only sidecar path for producing an AEP
bundle from Automaton runtime artifacts.

Inputs:

- `state.db`
- git history
- on-chain reference rows already persisted by the runtime

Outputs:

- `manifest.json`
- `records.jsonl`
- `fdo-stub.json`
- `erc8004-validation-stub.json`

Preferred command:

```bash
agent-evidence export automaton \
  --state-db /path/to/state.db \
  --repo /path/to/automaton/state/repo \
  --runtime-root /path/to/automaton-checkout \
  --out ./automaton-aep-bundle

agent-evidence verify-bundle --bundle-dir ./automaton-aep-bundle
```

Thin wrapper script:

```bash
python integrations/automaton/export_evidence.py \
  --state-db /path/to/state.db \
  --repo /path/to/automaton/state/repo \
  --runtime-root /path/to/automaton-checkout \
  --out ./automaton-aep-bundle
```

This path is read-only. It does not patch the Automaton runtime and it does not
claim non-repudiation. A live isolated-home export path has been validated; the
CLI entry remains experimental while the live data contract settles.

See `integrations/automaton/LIVE_RUNBOOK.md` for the minimal live export path.
