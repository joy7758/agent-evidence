# Contributing

`agent-evidence` is intentionally narrow. It packages AI agent and service
operation evidence into local, verifiable artifacts and keeps validation,
offline verification, signed export metadata, receipts, and review packs inside
that boundary.

## Good Contribution Types

Good contributions include:

- validator correctness fixes
- schema clarification
- valid and invalid examples
- offline verification improvements
- signed export safety checks
- review pack improvements
- documentation that improves agent discovery, citation, or reuse
- tests for CLI behavior and bundle verification

## Out-of-Scope Changes

Please do not broaden this repository into:

- a full agent platform
- hosted APIs
- remote MCP services
- hidden telemetry
- automatic promotion
- reputation automation
- legal compliance claims
- official FDO standard claims

OpenAPI and MCP work must stay local, thin, and aligned with existing
validation/export logic unless a separate maintainer-approved plan changes that
boundary.

## Development Setup

Create a local environment and install development dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Run the main checks:

```bash
pytest -q
ruff check .
ruff format --check .
python scripts/generate_agent_index.py --check
python scripts/generate_llms_full.py --check
git diff --check
```

For quick CLI smoke checks:

```bash
agent-evidence validate-profile examples/minimal-valid-evidence.json
agent-evidence capabilities --json
```

## Pull Request Checklist

Before opening a pull request:

- keep the patch focused on one behavior, documentation, metadata, or safety
  concern
- add or update tests for validator, CLI, export, or bundle-verification
  behavior when behavior changes
- update examples when schema or validation expectations change
- cite affected EEOAP clauses and include protocol-gate validation results
  when protocol, evidence, validator, workflow, example, or PR metadata changes
- update generated agent metadata when source discovery files change
- update `DEVELOPMENT_LEDGER.md` and `DEVELOPMENT_LEDGER.jsonl` for meaningful
  behavior, metadata, policy, or agent-facing discovery changes
- preserve claim boundaries from `AGENTS.md`, `llms.txt`,
  `docs/project-facts.md`, and `README.md`
- avoid committing secrets, private keys, sensitive runtime evidence, or
  production review packs

## Maintainer Review Focus

Maintainers should focus review on:

- whether the change stays inside the current evidence packaging and
  verification boundary
- validator correctness and schema compatibility
- manifest, hash, and bundle path handling
- signed export metadata safety
- JSON, CSV, and XML export safety
- offline verification receipts and review-pack clarity
- dependency and GitHub Actions permission changes
- whether docs or metadata introduce unsupported legal, compliance, AI Act, FDO
  standard, hosted-service, or adoption claims
