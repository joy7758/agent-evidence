# LangChain Integration

The single recommended LangChain entry point in this repository is
`LangChainAdapter` in `agent_evidence.integrations.langchain`.

Current recommended public API:

```python
from agent_evidence.integrations.langchain import LangChainAdapter

adapter = LangChainAdapter.for_output_dir(
    "./artifacts/langchain-run",
    digest_only=True,
    omit_request=False,
    omit_response=False,
)

callbacks = [adapter.callback_handler()]
artifacts = adapter.finalize()
```

This adapter keeps the current quickstart path on one surface:

- callback capture through `EvidenceCallbackHandler`
- JSON `bundle` export
- machine-readable `receipt`
- reviewer-facing `summary`

Supporting files such as the manifest sidecar, local keys, and runtime JSONL
remain supporting materials, not additional primary outputs.

Primary runnable example:

```bash
python examples/langchain_minimal_evidence.py
```

See also:

- `examples/langchain_minimal_evidence.py`
- `docs/cookbooks/langchain_minimal_evidence.md`

## Alternate / secondary path

The older AEP bundle directory path remains available as an alternate surface.
It is not the recommended starting point for the current LangChain-first flow.

Alternate commands:

```bash
python integrations/langchain/export_evidence.py
agent-evidence verify-bundle --bundle-dir integrations/langchain/langchain-evidence-bundle
```

Use that alternate path only if you specifically need the older bundle-directory
shape. The recommended LangChain entry point for current docs and examples is
still `LangChainAdapter` producing `bundle`, `receipt`, and `summary`.

## Fixture gate

Run the existing fixture gate:

```bash
python scripts/run_profile_gate.py
```
