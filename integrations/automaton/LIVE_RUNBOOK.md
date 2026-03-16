# Automaton Live AEP Runbook

## Live data minimum

- Run a real Automaton process in an isolated `HOME`, so the runtime writes to
  `<isolated-home>/.automaton/`.
- Required for export: `state.db`.
- Recommended for fuller evidence: `.git` state repo in the same directory.
- Optional sections such as policy rows, transaction rows, on-chain rows, or
  registry rows may be absent; export should degrade instead of aborting.

## Export command

```bash
agent-evidence export automaton \
  --state-db /tmp/agent-evidence-live-home/.automaton/state.db \
  --repo /tmp/agent-evidence-live-home/.automaton \
  --runtime-root /tmp/automaton-ref \
  --out /tmp/agent-evidence-live-bundle

agent-evidence verify-bundle \
  --bundle-dir /tmp/agent-evidence-live-bundle
```

## Degradation behavior

- Missing SQLite tables: bundle still exports, `manifest.json` records the gap in
  `omitted_sections`.
- Empty but present sections: bundle still exports, `manifest.json` records the
  gap in `export_warnings`.
- Missing git history, registry entry, or on-chain refs: verify still runs and
  the bundle remains integrity-verifiable; only the corresponding references and
  warnings degrade.
- Omitting `--runtime-root`: export still succeeds, but runtime version,
  commit, and dirty-state fields degrade to `null` with warnings.
