# LangChain Integration

This integration writes a digest-only Agent Evidence Profile bundle from one
LangChain run. It is an integrity-verifiable evidence bundle, not a hosted
tracing platform and not a court-grade legal-proof claim.

## Five-Minute Runnable Path

Start with the cookbook:

```text
docs/cookbooks/langchain_minimal_evidence.md
```

The canonical minimal example is:

```bash
python examples/langchain_minimal_evidence.py --output-dir ./tmp/langchain-minimal-evidence
agent-evidence verify-export \
  --bundle ./tmp/langchain-minimal-evidence/langchain-evidence.bundle.json \
  --public-key ./tmp/langchain-minimal-evidence/manifest-public.pem
```

This path is offline/mock by default. It uses deterministic local runnables and
mocked callback events, so it does not require an external model API key.

## Callback Surface

The callback handler is narrowed to one integration point:

- `EvidenceCallbackHandler`
- default `digest_only=True`
- optional `omit_request` / `omit_response`
- no token-by-token bundle persistence

## Lower-Level Bundle Directory Demo

This integration also includes a smaller bundle-dir demo for callback-handler
coverage:

```bash
python integrations/langchain/export_evidence.py
agent-evidence verify-bundle --bundle-dir integrations/langchain/langchain-evidence-bundle
```

Run the fixture gate:

```bash
python scripts/run_profile_gate.py
```
