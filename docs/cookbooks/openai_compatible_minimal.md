# OpenAI-Compatible Minimal

## 1) What these examples show

This cookbook shows two thin configuration examples built on the real
`OpenAICompatibleAdapter` wrapper:

- default OpenAI-compatible configuration
- alternate `base_url` configuration

Both examples keep the provider client outside core evidence logic and preserve
the same primary outputs used elsewhere in this repository:

- `bundle`
- `receipt`
- `summary`

Manifest sidecars, keys, and runtime JSONL remain supporting files only.

## 2) Prerequisites

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[signing]"
pip install openai
```

These examples are local example surfaces, not tests. They make live provider
calls when you run them.

## 3) Recommended wrapper

Both examples use the same C1 wrapper:

```python
from agent_evidence.integrations.openai_compatible import OpenAICompatibleAdapter

adapter = OpenAICompatibleAdapter.for_output_dir(
    output_dir="./artifacts/openai-compatible-run",
    provider_label="openai",
    model="gpt-4.1-mini",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://api.openai.com/v1",
)

response = adapter.record_call(
    operation="chat.completions.create",
    request={"model": "gpt-4.1-mini", "messages": [...]},
    invoke=lambda: client.chat.completions.create(...),
)

artifacts = adapter.finalize()
```

The examples change configuration only. They do not introduce a second export
path or provider-specific branching into core.

## 4) Default configuration example

Environment:

```bash
export OPENAI_API_KEY=...
export OPENAI_MODEL=${OPENAI_MODEL:-gpt-4.1-mini}
```

Run:

```bash
python examples/openai_compatible/basic_export.py
```

This example:

- uses `provider_label="openai"`
- relies on the SDK default base URL
- records one `chat.completions.create` call
- writes `bundle`, `receipt`, and `summary`

## 5) Alternate base_url example

Environment:

```bash
export OPENAI_API_KEY=...
export OPENAI_COMPAT_BASE_URL=...
export OPENAI_COMPAT_PROVIDER_LABEL=...
export OPENAI_MODEL=${OPENAI_MODEL:-gpt-4.1-mini}
```

Run:

```bash
python examples/openai_compatible/alternate_base_url.py
```

This example:

- uses the same `OpenAICompatibleAdapter`
- changes only `base_url` and `provider_label`
- keeps the same `bundle` / `receipt` / `summary` output contract

## 6) Output artifacts

Primary outputs:

- `bundle`
- `receipt`
- `summary`

Supporting files written by the same run:

- manifest sidecar
- verification key
- local signing key
- runtime JSONL capture

## 7) Boundaries

- no CLI changes
- no schema changes
- no `README.md` or `docs/quickstart.md` changes
- no `openai_agents` path merge or rename
- no provider-specific business logic in core
