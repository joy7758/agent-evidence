# LangChain Minimal Evidence

## 1) What this example shows

This cookbook shows the smallest local-first LangChain path in this repository:

- capture LangChain runtime events through an external callback
- persist those events to a local JSONL store
- export a signed JSON `bundle`
- verify the exported `bundle` offline to produce a `receipt`
- write a reviewer-facing `summary`

The example stays outside LangGraph persistence and checkpointer internals.

## 2) Why callback/export-first

This repository now has one recommended LangChain wrapper:
`LangChainAdapter`.

It keeps the integration external, reviewable, and easy to adapt into another
LangChain app while still reusing the existing callback and export primitives.

The callback records runtime facts. The export step packages those records into
a portable artifact with a signed manifest summary. That is the smallest honest
surface here.

Recommended public API:

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

## 3) Minimal flow

```text
LangChain callback events
-> local JSONL evidence store
-> signed JSON bundle
-> receipt
-> summary
```

If you need detached anchoring, treat the signed bundle and manifest as an
external handoff point. That step is not verified by this repo today.

If you later add profile-level `validation.trust_bindings[]`, treat them as
optional pointers to an external trust source. They are not the same thing as
the manifest signatures verified by `verify-export`.

## 4) Prerequisites

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[langchain,signing]"
```

The commands below assume `agent-evidence` is available on `PATH`. If you are
using the repository virtualenv directly, run `.venv/bin/agent-evidence ...`.

No model API key is required. The example uses deterministic local runnables and
a mocked model callback event.

Tested on the repo's current local environment. On Python 3.14,
`langchain_core` may emit a non-blocking warning during example runs or
verification.

## 5) Run the example

From the repository root:

```bash
python examples/langchain_minimal_evidence.py
```

Or choose an explicit output directory:

```bash
python examples/langchain_minimal_evidence.py --output-dir ./tmp/langchain-minimal-evidence
```

The script uses `LangChainAdapter` to capture the run, signs the exported
bundle with a local Ed25519 demo key, writes a machine-readable `receipt`, and
writes a reviewer-facing `summary`.

## 6) Output artifacts

Primary outputs:

- `bundle`: `examples/artifacts/langchain-minimal-evidence/langchain-evidence.bundle.json`
- `receipt`: `examples/artifacts/langchain-minimal-evidence/receipt.json`
- `summary`: `examples/artifacts/langchain-minimal-evidence/summary.json`

Supporting files written by the same run:

- `examples/artifacts/langchain-minimal-evidence/runtime-events.jsonl`
- `examples/artifacts/langchain-minimal-evidence/langchain-evidence.manifest.json`
- `examples/artifacts/langchain-minimal-evidence/manifest-private.pem`
- `examples/artifacts/langchain-minimal-evidence/manifest-public.pem`

Notes:

- `runtime-events.jsonl` is the local append-only callback capture.
- `langchain-evidence.manifest.json` is a readable sidecar copy of the signed manifest.
- The generated private key is only for local demo use.

## 7) Verify

Run the offline verification command from the summary if you want to regenerate
or inspect the `receipt` directly:

```bash
agent-evidence verify-export \
  --bundle examples/artifacts/langchain-minimal-evidence/langchain-evidence.bundle.json \
  --public-key examples/artifacts/langchain-minimal-evidence/manifest-public.pem
```

You should get `ok: true` plus signature verification details.

That verification step covers the local signed export. It does not verify any
external trust anchor or transparency log entry.

## 8) Boundaries / what this is not

- This is not a LangGraph persistence or checkpointer integration.
- This is not a hosted tracing product.
- This is not a non-repudiation or WORM storage claim.
- Detached anchoring is an external handoff point in this repo, not something
  this example verifies today.
- If you need external anchoring, use the exported bundle digest and manifest as
  the handoff point to another system.
