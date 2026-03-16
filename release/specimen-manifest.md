# Reproducible Conference Specimen Manifest

This manifest freezes the current Execution Evidence Object specimen as the
conference baseline.

## Canonical prototype files

- `spec/execution-evidence-object.md`
- `schema/execution-evidence-object.schema.json`
- `proposal/execution-evidence-object-proposal.md`
- `docs/architecture/execution-evidence-object.md`
- `docs/architecture/execution-evidence-object-one-page.md`
- `docs/fdo-mapping/execution-evidence-to-fdo.md`
- `docs/fdo-mapping/minimal-fdo-object-example.md`
- `docs/outreach/public-positioning.md`

## Canonical example files

- `examples/minimal-evidence-object.json`
- `examples/evidence-object-openai-run.json`
- `examples/fdo-style-execution-evidence-object.json`

## Canonical demo entrypoints

- `scripts/verify_evidence_object.py`
- `scripts/demo_execution_evidence_object.py`
- `integrations/openai-agents/export_evidence.py`
- `integrations/langchain/export_evidence.py`
- `integrations/crewai/export_evidence.py`

## Verification commands

```bash
python3 scripts/verify_evidence_object.py examples/evidence-object-openai-run.json
python3 scripts/demo_execution_evidence_object.py
python3 -m py_compile \
  scripts/verify_evidence_object.py \
  scripts/demo_execution_evidence_object.py \
  integrations/openai-agents/export_evidence.py \
  integrations/langchain/export_evidence.py \
  integrations/crewai/export_evidence.py
```

## Expected outputs

- `verify_evidence_object.py` prints `VERIFY_OK`
- `demo_execution_evidence_object.py` prints:
  - `Loaded object`
  - `Schema validation`
  - `Integrity check`
  - `Provenance summary`
  - `FDO mapping summary`
  - `Final result`
- `py_compile` finishes with no output and exit status `0`
