# Release Checklist

Use this checklist before publishing a GitHub or PyPI release.

## Core Checks

- [ ] `pytest -q`
- [ ] `ruff check`
- [ ] `ruff format --check`
- [ ] `agent-evidence capabilities --json | python -m json.tool`
- [ ] `python scripts/generate_agent_index.py --check`
- [ ] `python scripts/generate_llms_full.py --check`

## Metadata Validation

- [ ] `CITATION.cff` parses as YAML
- [ ] `codemeta.json` parses as JSON
- [ ] `agent-index.json` parses as JSON
- [ ] `DEVELOPMENT_LEDGER.jsonl` parses as JSONL
- [ ] `pyproject.toml`, `CITATION.cff`, `codemeta.json`,
      `docs/project-facts.md`, `agent-index.json`, and `llms-full.txt` agree
      on the current version
- [ ] Primary DOI is the Zenodo concept DOI
- [ ] Exact release DOI is documented only in release-specific context
- [ ] PyPI and GitHub release notes are consistent

## Local OpenAPI Smoke

- [ ] `agent-evidence serve --help`
- [ ] Start local server on `127.0.0.1`
- [ ] `GET /healthz`
- [ ] `GET /v1/capabilities`
- [ ] Confirm OpenAPI remains local-only and thin over CLI/core

## MCP Smoke

- [ ] `agent-evidence mcp --transport stdio --help`
- [ ] `python -m agent_evidence.mcp.server --help`
- [ ] Confirm MCP remains stdio-only
- [ ] Confirm MCP has no prompts, remote registry publication, telemetry,
      shell tools, write tools, upload/sign tools, or GitHub automation tools

## LangChain Smoke

- [ ] Run `python examples/langchain_minimal_evidence.py --output-dir ./tmp/langchain-minimal-evidence`
- [ ] Run `agent-evidence verify-export --bundle ./tmp/langchain-minimal-evidence/langchain-evidence.bundle.json --public-key ./tmp/langchain-minimal-evidence/manifest-public.pem`
- [ ] Confirm `verify-export` returns `"ok": true`
- [ ] Remove `./tmp/langchain-minimal-evidence`

## OpenAI-Compatible Smoke

- [ ] Run `python examples/openai_compatible_minimal_evidence.py --output-dir ./tmp/openai-compatible-minimal-evidence --mock`
- [ ] Run `agent-evidence verify-export --bundle ./tmp/openai-compatible-minimal-evidence/openai-compatible-evidence.bundle.json --public-key ./tmp/openai-compatible-minimal-evidence/manifest-public.pem`
- [ ] Confirm `verify-export` returns `"ok": true`
- [ ] Remove `./tmp/openai-compatible-minimal-evidence`

## Secret and Promotion Checks

- [ ] Run an OpenAI-compatible secret sentinel check
- [ ] Confirm fake provider API keys do not appear in generated artifacts
- [ ] Confirm `Authorization` headers are not serialized into artifacts
- [ ] Check no automatic star/follow/fork/promotion language exists in
      release-facing metadata
- [ ] Check no provider secret leaks exist in committed artifacts

## Documentation Checks

- [ ] Documentation link check if available
- [ ] No stale statement that MCP is unavailable
- [ ] No claim of official FDO standard status
- [ ] No legal non-repudiation claim
- [ ] No full AI governance platform claim
- [ ] No remote MCP or hosted OpenAPI product claim
- [ ] No Review Pack or AI Act Pack claim

## Final Release Actions

- [ ] Confirm release version
- [ ] Confirm release date
- [ ] Confirm DOI handling
- [ ] Create GitHub release if approved
- [ ] Publish PyPI package if approved
- [ ] Verify installed package from published artifact
