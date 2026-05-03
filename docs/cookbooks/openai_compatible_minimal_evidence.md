# OpenAI-Compatible Minimal Evidence

## 1) What this example shows

This cookbook shows the smallest provider-agnostic OpenAI-compatible path in
this repository:

- configure an OpenAI-compatible runtime through `api_key`, `base_url`, and
  `model`
- run a deterministic mock/offline chat-completion flow by default
- persist runtime evidence events to a local JSONL store
- export a signed JSON evidence bundle
- verify the exported bundle offline with a public key

The path is intentionally provider-agnostic. It is not specific to OpenAI,
Zhipu GLM, or another compatible provider.

## 2) Five-minute copy/paste path

From a local checkout:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[openai-compatible,signing]"

python examples/openai_compatible_minimal_evidence.py \
  --output-dir ./tmp/openai-compatible-minimal-evidence \
  --mock

agent-evidence verify-export \
  --bundle ./tmp/openai-compatible-minimal-evidence/openai-compatible-evidence.bundle.json \
  --public-key ./tmp/openai-compatible-minimal-evidence/manifest-public.pem

python -m json.tool ./tmp/openai-compatible-minimal-evidence/summary.json

rm -rf ./tmp/openai-compatible-minimal-evidence
```

No external API key is required. The default path uses deterministic local
mock behavior and makes no outbound network calls.

## 3) Provider configuration

The compatible provider configuration is deliberately small:

- `OPENAI_COMPATIBLE_API_KEY`
- `OPENAI_COMPATIBLE_BASE_URL`
- `OPENAI_COMPATIBLE_MODEL`

The mock path does not require any of these variables. A live provider call is
available only when explicitly requested with `--live`, and tests do not use
that mode.

Live mode fails before any provider call when `api_key`, `base_url`, or `model`
is missing. The error is machine-readable and uses the code
`invalid_provider_config`.

Provider examples are configuration examples only:

| Provider | `base_url` | `model` | Notes |
| --- | --- | --- | --- |
| OpenAI | `https://api.openai.com/v1` | provider model name | Use live mode only when explicitly enabled. |
| Zhipu GLM | `<provider OpenAI-compatible endpoint>/v1` | provider model name | Configure through `base_url`; no provider-specific core logic. |
| Other compatible provider | `<provider-compatible-endpoint>/v1` | provider model name | Must support OpenAI-compatible chat completions semantics. |

Example live invocation shape:

```bash
export OPENAI_COMPATIBLE_API_KEY="..."
export OPENAI_COMPATIBLE_BASE_URL="https://example-compatible-endpoint/v1"
export OPENAI_COMPATIBLE_MODEL="some-model"

python examples/openai_compatible_minimal_evidence.py \
  --output-dir ./tmp/openai-compatible-minimal-evidence \
  --live
```

## 4) Why mock/export-first

The default mock path verifies the evidence capture and export shape without
requiring a provider account, a network connection, or provider-specific core
logic. It records digest-only request and response evidence, exports a signed
bundle, and verifies that bundle through the existing CLI/core behavior.

CLI/core behavior remains canonical. This cookbook does not change the OpenAPI
or MCP wrappers and does not introduce new evidence semantics.

Tests exercise the mock path only. They do not call real providers, do not
require real API keys, and check that provider secret sentinels are not written
to runtime events, bundle JSON, manifest JSON, or summary output.

## 5) Minimal flow

```text
OpenAI-compatible chat-completion event
-> local JSONL evidence store
-> signed JSON bundle
-> offline verify
```

If you need detached anchoring, treat the signed bundle and manifest as an
external handoff point. That step is not verified by this repo today.

## 6) Output artifacts

By default the script writes:

- `examples/artifacts/openai-compatible-minimal-evidence/runtime-events.jsonl`
- `examples/artifacts/openai-compatible-minimal-evidence/openai-compatible-evidence.bundle.json`
- `examples/artifacts/openai-compatible-minimal-evidence/openai-compatible-evidence.manifest.json`
- `examples/artifacts/openai-compatible-minimal-evidence/manifest-private.pem`
- `examples/artifacts/openai-compatible-minimal-evidence/manifest-public.pem`
- `examples/artifacts/openai-compatible-minimal-evidence/summary.json`

Notes:

- `runtime-events.jsonl` is the local append-only evidence capture.
- `openai-compatible-evidence.bundle.json` is the portable export artifact.
- `openai-compatible-evidence.manifest.json` is a readable sidecar copy of the signed manifest.
- The generated private key is only for local demo use.
- Request and response payloads are represented by digests in the demo evidence.
- Provider API keys and authorization-like values are not written into the
  runtime store, export bundle, manifest, or summary artifacts.

## 7) Verify

Run the offline verification command from the summary:

```bash
agent-evidence verify-export \
  --bundle examples/artifacts/openai-compatible-minimal-evidence/openai-compatible-evidence.bundle.json \
  --public-key examples/artifacts/openai-compatible-minimal-evidence/manifest-public.pem
```

You should get `ok: true` plus signature verification details.

## 8) Boundaries / what this is not

- This is not provider-specific core logic.
- This is not a Zhipu-specific adapter.
- This is not a Review Pack commercial feature.
- This is not an AI Act Pack.
- This is not a hosted tracing product.
- This is not a full AI governance platform.
- This is not a non-repudiation or WORM storage claim.
- This does not change OpenAPI or MCP behavior.
- Detached anchoring is an external handoff point in this repo, not something
  this example verifies today.
