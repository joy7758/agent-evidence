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

## Review Pack V0.3 Smoke

- [ ] Run `python examples/langchain_minimal_evidence.py --output-dir ./tmp/langchain-minimal-evidence`
- [ ] Run `agent-evidence review-pack create --bundle ./tmp/langchain-minimal-evidence/langchain-evidence.bundle.json --public-key ./tmp/langchain-minimal-evidence/manifest-public.pem --summary ./tmp/langchain-minimal-evidence/summary.json --output-dir ./tmp/langchain-review-pack`
- [ ] Confirm `./tmp/langchain-review-pack/manifest.json` parses as JSON
- [ ] Confirm `./tmp/langchain-review-pack/receipt.json` contains `"ok": true`
- [ ] Confirm `./tmp/langchain-review-pack/findings.json` parses as JSON
- [ ] Confirm `review_pack_version` is `"0.3"` in Review Pack metadata
- [ ] Confirm `./tmp/langchain-review-pack/summary.md` includes:
      `RP-CHECK-001`, `Reviewer Checklist`, `Verification Details`,
      `Artifact Inventory`, `Findings`, `Secret and Private Key Boundary`,
      `Recommended Reviewer Actions`, `What This Does Not Prove`,
      `not comprehensive DLP`, and `local_offline`
- [ ] Confirm `manifest.json` and `receipt.json` include `secret_scan_status`
- [ ] Confirm `findings.json` severities are limited to `pass`, `warning`,
      `fail`, and `unknown`
- [ ] Confirm `manifest-private.pem` is not copied into the Review Pack
- [ ] Confirm the tampered bundle fail-closed test passes
- [ ] Confirm `--json-errors` returns machine-readable failure JSON for
      `review-pack create` failures
- [ ] Confirm no OpenAPI or MCP Review Pack endpoint/tool is exposed
- [ ] Remove `./tmp/langchain-minimal-evidence` and `./tmp/langchain-review-pack`
- [ ] Run the OpenAI-compatible mock Review Pack smoke if changing Review Pack packaging

## Secret and Promotion Checks

- [ ] Run an OpenAI-compatible secret sentinel check
- [ ] Run a Review Pack secret sentinel check
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
- [ ] Review Pack claims are limited to local/offline V0.3 reviewer packaging
- [ ] No comprehensive DLP claim
- [ ] No AI Act Pack claim

## Final Release Actions

- [ ] Confirm release version
- [ ] Confirm release date
- [ ] Confirm DOI handling
- [ ] Create GitHub release if approved
- [ ] Publish PyPI package if approved
- [ ] Verify installed package from published artifact
