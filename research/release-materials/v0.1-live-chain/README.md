# v0.1-live-chain

This specimen snapshot lives under `research/` and is not the canonical SDK entry surface.

This is the controlled public specimen for the first real AEP live chain.

Positioning:

- AEP is an integrity-verifiable evidence profile for autonomous agent runs, with offline verification and runtime provenance capture.
- This release is a standard specimen, not a non-repudiation system.

Canonical artifacts:

- Release note: [RELEASE_NOTE.md](RELEASE_NOTE.md)
- Schema: [schema_v0.1.json](../../../agent_evidence/aep/schema_v0.1.json)
- Verify CLI: [main.py](../../../agent_evidence/cli/main.py)
- LangChain exporter: [export_evidence.py](../../../integrations/langchain/export_evidence.py)
- Automaton exporter: [automaton.py](../../../agent_evidence/integrations/automaton.py)
- Live runbook: [LIVE_RUNBOOK.md](../../../integrations/automaton/LIVE_RUNBOOK.md)
- Boundary statement: [What-AEP-proves-and-what-it-does-not-prove.md](What-AEP-proves-and-what-it-does-not-prove.md)

Public fixtures:

- Live bundle without runtime root: [manifest.json](../../../tests/fixtures/agent_evidence_profile/valid/live-automaton-bundle/manifest.json)
- Live bundle with runtime root: [manifest.json](../../../tests/fixtures/agent_evidence_profile/valid/live-automaton-runtime-root-bundle/manifest.json)
- Tampered live bundle without runtime root: [manifest.json](../../../tests/fixtures/agent_evidence_profile/invalid/live-automaton-tampered-bundle/manifest.json)
- Tampered live bundle with runtime root: [manifest.json](../../../tests/fixtures/agent_evidence_profile/invalid/live-automaton-runtime-root-tampered-bundle/manifest.json)

Minimal verification surface:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,langchain,sql]"

agent-evidence verify-bundle \
  --bundle-dir tests/fixtures/agent_evidence_profile/valid/live-automaton-bundle

agent-evidence verify-bundle \
  --bundle-dir tests/fixtures/agent_evidence_profile/valid/live-automaton-runtime-root-bundle

python scripts/run_specimen_gate.py
```

Expected result:

- Both valid live bundles pass offline verification.
- Both tampered live bundles fail at integrity verification.
- The runtime-root specimen carries `source_runtime_version`, `source_runtime_commit`, and `source_runtime_dirty`.
- The release note and boundary statement define the specimen scope.
