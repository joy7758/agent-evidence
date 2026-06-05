# LangChain Minimal Evidence

## 1) What this example shows

This cookbook shows the smallest local-first LangChain path in this repository:

- capture LangChain runtime events through an external callback
- persist those events to a local JSONL store
- export a signed JSON evidence bundle
- verify the exported bundle offline with a public key

The example stays outside LangGraph persistence and checkpointer internals.

## 2) Five-minute copy/paste path

From a local checkout:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[langchain,signing]"

python examples/langchain_minimal_evidence.py --output-dir ./tmp/langchain-minimal-evidence

agent-evidence verify-export \
  --bundle ./tmp/langchain-minimal-evidence/langchain-evidence.bundle.json \
  --public-key ./tmp/langchain-minimal-evidence/manifest-public.pem

python -m json.tool ./tmp/langchain-minimal-evidence/summary.json

rm -rf ./tmp/langchain-minimal-evidence
```

No external API key is required. The example uses deterministic local behavior
and mocked callback events.

## 3) Why callback/export-first

This repository already has a thin LangChain callback surface and a separate
signed export surface. Reusing those two pieces keeps the integration external,
reviewable, and easy to adapt into another LangChain app.

The callback records runtime facts. The export step packages those records into
a portable artifact with a signed manifest summary. That is the smallest honest
surface here.

CLI/core behavior remains canonical. This cookbook does not change the OpenAPI
or MCP wrappers and does not introduce new evidence semantics.

## 4) Minimal flow

```text
LangChain callback events
-> local JSONL evidence store
-> signed JSON bundle
-> offline verify
```

If you need detached anchoring, treat the signed bundle and manifest as an
external handoff point. That step is not verified by this repo today.

## 5) Prerequisites

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[langchain,signing]"
```

No model API key is required. The example uses deterministic local runnables and
a mocked model callback event.

Tested on the repo's current local environment. On Python 3.14,
`langchain_core` may emit a non-blocking warning during example runs or
verification.

## 6) Run the example

From the repository root:

```bash
python examples/langchain_minimal_evidence.py
```

Or choose an explicit output directory:

```bash
python examples/langchain_minimal_evidence.py --output-dir ./tmp/langchain-minimal-evidence
```

The script generates the run artifacts, signs the exported bundle with a local
Ed25519 demo key, runs an API-level verification pass, and writes a summary.

## 7) Output artifacts

By default the script writes:

- `examples/artifacts/langchain-minimal-evidence/runtime-events.jsonl`
- `examples/artifacts/langchain-minimal-evidence/langchain-evidence.bundle.json`
- `examples/artifacts/langchain-minimal-evidence/langchain-evidence.manifest.json`
- `examples/artifacts/langchain-minimal-evidence/manifest-private.pem`
- `examples/artifacts/langchain-minimal-evidence/manifest-public.pem`
- `examples/artifacts/langchain-minimal-evidence/summary.json`

Notes:

- `runtime-events.jsonl` is the local append-only callback capture.
- `langchain-evidence.bundle.json` is the portable export artifact.
- `langchain-evidence.manifest.json` is a readable sidecar copy of the signed manifest.
- The generated private key is only for local demo use.

## 8) Verify

Run the offline verification command from the summary:

```bash
agent-evidence verify-export \
  --bundle examples/artifacts/langchain-minimal-evidence/langchain-evidence.bundle.json \
  --public-key examples/artifacts/langchain-minimal-evidence/manifest-public.pem
```

You should get `ok: true` plus signature verification details.

## 9) Boundaries / what this is not

- This is not a LangGraph persistence or checkpointer integration.
- This is not a Review Pack commercial feature.
- This is not a hosted tracing product.
- This is not a full AI governance platform.
- This is not a non-repudiation or WORM storage claim.
- This does not change OpenAPI or MCP behavior.
- Detached anchoring is an external handoff point in this repo, not something
  this example verifies today.
- If you need external anchoring, use the exported bundle digest and manifest as
  the handoff point to another system.
