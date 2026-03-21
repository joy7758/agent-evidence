# Agent Evidence Root Inventory

Pre-refactor root inventory snapshot for `agent-evidence`:

- `agent_evidence/`
- `docs/`
- `examples/`
- `integrations/`
- `schema/`
- `spec/`
- `scripts/`
- `tests/`
- `poster/`
- `proposal/`
- `release/`
- `roadmap/`
- `speaking/`
- `submission/`
- `outreach/`
- `setup.py`

Primary boundary issues:

- research and release material competed with the SDK package surface
- conference specimen assets dominated the README entry path
- runtime evidence capture risked being confused with the downstream audit control plane
- packaging still exposed both `pyproject.toml` and `setup.py`
