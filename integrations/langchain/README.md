# LangChain Integration

This integration writes a digest-only Agent Evidence Profile bundle from one
LangChain run. It is an integrity-verifiable evidence bundle, not a hosted
tracing platform and not a court-grade non-repudiation claim.

The callback handler is narrowed to one integration point:

- `EvidenceCallbackHandler`
- default `digest_only=True`
- optional `omit_request` / `omit_response`
- no token-by-token bundle persistence

Run the demo:

```bash
python integrations/langchain/export_evidence.py
agent-evidence verify-bundle --bundle-dir integrations/langchain/langchain-evidence-bundle
```

Run the fixture gate:

```bash
python scripts/run_profile_gate.py
```
