# Agent Evidence

Capture autonomous agent execution as verifiable semantic events with JSONL,
SQLite, and PostgreSQL storage backends.

[![CI](https://github.com/joy7758/agent-evidence/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/joy7758/agent-evidence/actions/workflows/ci.yml)
![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)
![Semantic Events](https://img.shields.io/badge/semantic%20events-v2.0.0-1f6feb)
![Storage](https://img.shields.io/badge/storage-JSONL%20%7C%20SQLite%20%7C%20Postgres-0a7b83)
![Status](https://img.shields.io/badge/status-experimental-orange)

Agent Evidence is a minimal Python toolkit for capturing verifiable evidence
about autonomous agent execution. It provides structured evidence records,
deterministic hashing, append-only local storage, signed export bundles, and a
small CLI for inspection and export.

The toolkit now supports two storage modes:

- append-only local JSONL files
- SQLAlchemy-backed SQLite/PostgreSQL databases

The current model treats each record as a semantic event envelope:

- `event.event_type` is framework-neutral, such as `chain.start` or `tool.end`
- `event.context.source_event_type` preserves the raw framework event name
- `hashes.previous_event_hash` links to the prior event
- `hashes.chain_hash` provides a cumulative chain tip for integrity checks

## Why this shape

The project is organized so evidence capture stays modular:

- `agent_evidence`: core models and recorder logic
- `agent_evidence/crypto`: canonical hashing and chain helpers
- `agent_evidence/storage`: append-only local storage backends
- `agent_evidence/integrations`: adapters for external agent frameworks
- `agent_evidence/cli`: command-line entrypoints
- `agent_evidence/schema`: JSON schema for persisted envelopes
- `examples`: executable usage examples
- `tests`: baseline regression coverage

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,langchain,sql]"
agent-evidence schema
```

## CLI examples

```bash
agent-evidence record \
  --store ./data/evidence.jsonl \
  --actor planner \
  --event-type tool.call \
  --input '{"task":"summarize"}' \
  --output '{"status":"ok"}' \
  --context '{"source":"cli","component":"tool"}'

agent-evidence list --store ./data/evidence.jsonl
agent-evidence show --store ./data/evidence.jsonl --index 0
agent-evidence verify --store ./data/evidence.jsonl
```

SQL stores use a SQLAlchemy URL instead of a file path:

```bash
agent-evidence record \
  --store sqlite+pysqlite:///./data/evidence.db \
  --actor planner \
  --event-type tool.call \
  --context '{"source":"cli","component":"tool"}'

agent-evidence query \
  --store sqlite+pysqlite:///./data/evidence.db \
  --event-type tool.call \
  --source cli

agent-evidence query \
  --store sqlite+pysqlite:///./data/evidence.db \
  --span-id tool-1 \
  --parent-span-id root \
  --offset 0 \
  --limit 50

agent-evidence query \
  --store sqlite+pysqlite:///./data/evidence.db \
  --previous-event-hash <event-hash> \
  --event-hash-from <lower-bound-hash> \
  --event-hash-to <upper-bound-hash>

agent-evidence export \
  --store ./data/evidence.jsonl \
  --format json \
  --output ./exports/evidence.bundle.json

agent-evidence export \
  --store ./data/evidence.jsonl \
  --format csv \
  --output ./exports/evidence.csv \
  --manifest-output ./exports/evidence.csv.manifest.json \
  --private-key ./keys/manifest-private.pem \
  --key-id evidence-demo

agent-evidence export \
  --store ./data/evidence.jsonl \
  --format json \
  --output ./exports/evidence.multisig.json \
  --required-signatures 2 \
  --required-signature-role approver=1 \
  --required-signature-role attestor=1 \
  --signer-config ./keys/operations-q2.signer.json \
  --signer-config ./keys/compliance-q1.signer.json

agent-evidence verify-export \
  --bundle ./exports/evidence.bundle.json \
  --public-key ./keys/manifest-public.pem

agent-evidence verify-export \
  --bundle ./exports/evidence.multisig.json \
  --keyring ./keys/manifest-keyring.json

agent-evidence verify-export \
  --bundle ./exports/evidence.multisig.json \
  --keyring ./keys/manifest-keyring.json \
  --required-signature-role approver=1
```

## Development

```bash
make install
make test
make lint
make hooks
```

The repository includes a `.pre-commit-config.yaml` with baseline whitespace,
JSON, and Ruff checks.

For PostgreSQL support, install the extra driver dependencies:

```bash
pip install -e ".[dev,postgres]"
```

## Semantic event model

Each persisted record follows this shape:

```json
{
  "schema_version": "2.0.0",
  "event": {
    "event_id": "...",
    "timestamp": "2026-03-16T00:00:00+00:00",
    "event_type": "tool.end",
    "actor": "search-tool",
    "inputs": {},
    "outputs": {},
    "context": {
      "source": "langchain",
      "component": "tool",
      "source_event_type": "on_tool_end",
      "span_id": "...",
      "parent_span_id": null,
      "ancestor_span_ids": [],
      "name": "search-tool",
      "tags": ["langchain", "tool"],
      "attributes": {}
    },
    "metadata": {}
  },
  "hashes": {
    "event_hash": "...",
    "previous_event_hash": "...",
    "chain_hash": "..."
  }
}
```

`event_type` is the stable semantic layer. `source_event_type` keeps the
original callback or trace event for lossless debugging.

## LangChain integration

Agent Evidence supports two integration paths for current LangChain runtimes:

- callback handlers for live capture during execution
- stream event adapters for `Runnable.astream_events(..., version="v2")`

Example callback usage:

```python
from agent_evidence import EvidenceRecorder, LocalEvidenceStore
from agent_evidence.integrations import EvidenceCallbackHandler
from langchain_core.runnables import RunnableLambda

store = LocalEvidenceStore("data/evidence.jsonl")
recorder = EvidenceRecorder(store)
handler = EvidenceCallbackHandler(recorder)

chain = RunnableLambda(lambda text: text.upper()).with_config({"run_name": "uppercase"})
result = chain.invoke(
    "hello",
    config={"callbacks": [handler], "metadata": {"session_id": "demo"}},
)
```

Example stream event capture:

```python
import asyncio

from agent_evidence import EvidenceRecorder, LocalEvidenceStore
from agent_evidence.integrations import record_langchain_event
from langchain_core.runnables import RunnableLambda

async def main() -> None:
    store = LocalEvidenceStore("data/evidence.jsonl")
    recorder = EvidenceRecorder(store)
    chain = RunnableLambda(lambda text: text[::-1]).with_config({"run_name": "reverse"})

    async for event in chain.astream_events("hello", version="v2"):
        record_langchain_event(recorder, event)

asyncio.run(main())
```

Both integration paths normalize LangChain callback names such as
`on_chain_start` and `on_tool_end` into semantic event types such as
`chain.start` and `tool.end`.

## Verification

Use the CLI to validate the chain after capture:

```bash
agent-evidence verify --store ./data/evidence.jsonl
```

This recomputes each `event_hash`, checks `previous_event_hash`, and validates
the cumulative `chain_hash`.

## SQL storage

`SqlEvidenceStore` persists the semantic event envelope into a relational table
while keeping indexed columns for efficient filtering:

- `event_type`
- `actor`
- `timestamp`
- `source`
- `component`
- `span_id`
- `parent_span_id`
- `previous_event_hash`
- `event_hash`
- `chain_hash`

The query interface supports:

- semantic filters such as `event_type`, `actor`, `source`, and `component`
- chain traversal via `previous_event_hash`
- span-scoped inspection with `span_id` and `parent_span_id`
- time windows via `since` and `until`
- lexicographic hash windows via `event_hash_from/to` and `chain_hash_from/to`
- pagination via `offset` and `limit`

Hash window filters operate on fixed-width lowercase SHA-256 hex digests, so
lexicographic ranges map cleanly to digest ordering for indexed lookups.

The store accepts standard SQLAlchemy URLs, for example:

- `sqlite+pysqlite:///./data/evidence.db`
- `postgresql+psycopg://user:password@localhost:5432/agent_evidence`

## Migration

You can migrate existing JSONL evidence into SQLite or PostgreSQL:

```bash
agent-evidence migrate \
  --source ./data/evidence.jsonl \
  --target sqlite+pysqlite:///./data/evidence.db
```

The `query` command works across both local and SQL stores, although SQL stores
are preferable once record volume grows beyond simple local inspection.

## Bundle export

Agent Evidence supports two export shapes:

- JSON bundles containing `records`, `manifest`, and one or more detached signatures
- CSV artifacts plus a JSON sidecar manifest

Both formats include a manifest with:

- `artifact_digest` for the exported bytes
- ordered event-hash and chain-hash list digests
- first/last event hashes and latest chain hash
- export filters used to produce the artifact

Each signature can also carry:

- `key_id` and `key_version` for key rotation
- `signer` and `role` for audit attribution
- `signed_at` and arbitrary JSON metadata

Manifests can also carry threshold policies:

- `signature_policy.minimum_valid_signatures` for `N-of-M`
- `signature_policy.minimum_valid_signatures_by_role` for role thresholds such
  as `{"approver": 1, "attestor": 1}`

If neither is present, verification defaults to requiring every signature in
the artifact to validate. If only role thresholds are present, the effective
total threshold defaults to the sum of those role requirements.

Manifest signing uses Ed25519 PEM keys. To enable signing outside the dev
environment:

```bash
pip install -e ".[signing]"
```

Example key generation with OpenSSL:

```bash
openssl genpkey -algorithm Ed25519 -out ./keys/manifest-private.pem
openssl pkey -in ./keys/manifest-private.pem -pubout -out ./keys/manifest-public.pem
```

Signer config files let you attach multiple signatures during export. Example
`operations-q2.signer.json`:

```json
{
  "private_key": "./operations-q2-private.pem",
  "key_id": "operations",
  "key_version": "2026-q2",
  "signer": "Operations Bot",
  "role": "approver",
  "metadata": {
    "environment": "prod"
  }
}
```

To embed signature policy in the exported manifest, pass:

- `--required-signatures N` for a global `N-of-M` rule
- `--required-signature-role <role>=<count>` one or more times for role rules

`verify-export` will honor the manifest policy by default, or you can override
the global threshold and role thresholds at verification time with the same
flags.

Keyrings let `verify-export` resolve rotated keys by `key_id` and
`key_version`. Example `manifest-keyring.json`:

```json
{
  "keys": [
    {
      "key_id": "operations",
      "key_version": "2026-q1",
      "public_key": "./operations-q1-public.pem"
    },
    {
      "key_id": "operations",
      "key_version": "2026-q2",
      "public_key": "./operations-q2-public.pem"
    }
  ]
}
```

When you export CSV, Agent Evidence writes the CSV artifact and a manifest
sidecar such as `evidence.csv.manifest.json`. `verify-export` validates the
manifest summary, exported artifact digest, and every signature it can resolve
from a provided public key or keyring.

## PostgreSQL integration validation

For a repeatable real-database validation path, use the bundled Docker-backed
integration script:

```bash
make install-postgres
make test-postgres
```

This starts a temporary PostgreSQL container, exports
`AGENT_EVIDENCE_POSTGRES_URL`, and runs `tests/test_postgres_integration.py`
against the live database.
