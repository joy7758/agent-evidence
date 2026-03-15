# Agent Evidence

Agent Evidence is a minimal Python toolkit for capturing verifiable evidence
about autonomous agent execution. It provides structured evidence records,
deterministic hashing, append-only local storage, and a small CLI for
inspection and export.

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
- `previous_event_hash`
- `event_hash`
- `chain_hash`

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
