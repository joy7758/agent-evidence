# Agent Evidence

Agent Evidence is a minimal Python toolkit for capturing verifiable evidence
about autonomous agent execution. It provides structured evidence records,
deterministic hashing, append-only local storage, and a small CLI for
inspection and export.

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
pip install -e ".[dev,langchain]"
agent-evidence schema
```

## CLI examples

```bash
agent-evidence record \
  --store ./data/evidence.jsonl \
  --actor planner \
  --action tool_call \
  --input '{"task":"summarize"}' \
  --output '{"status":"ok"}'

agent-evidence list --store ./data/evidence.jsonl
agent-evidence show --store ./data/evidence.jsonl --index 0
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
