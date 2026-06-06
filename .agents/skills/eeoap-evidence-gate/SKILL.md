---
name: eeoap-evidence-gate
description: Use this repo-local skill when agent-evidence work touches EEOAP evidence gates, operation accountability statements, protocol metadata, validators, examples, PR templates, CI checks, or agent-readable project instructions.
---

# EEOAP Evidence Gate Skill

## Purpose

Use this skill when a task affects agent evidence, operation accountability statements, protocol metadata, validators, examples, PR templates, CI checks, or agent-readable project instructions.

EEOAP means Execution Evidence and Operation Accountability Profile.

This skill helps agents cite the relevant EEOAP clauses and run the existing evidence-gate checks before reporting completion.

## When to use

Use this skill when modifying:

- AGENTS.md
- llms.txt
- docs/AGENT_VALUE.md
- docs/CLAIM_SCOPE.md
- docs/QUICKSTART_FOR_AGENTS.md
- docs/protocol/
- protocol/manifest.json
- protocol/clause-index.json
- scripts/check_protocol_citations.py
- examples/
- demo/
- .github/pull_request_template.md
- .github/workflows/

## Required reading

Before changing relevant files, read:

- docs/protocol/profile.md
- docs/protocol/clauses.md
- docs/protocol/citation-guide.md
- docs/CLAIM_SCOPE.md
- docs/QUICKSTART_FOR_AGENTS.md
- protocol/manifest.json
- protocol/clause-index.json

## Required checks

Run:

```bash
python3 -m json.tool protocol/manifest.json
python3 -m json.tool protocol/clause-index.json
python3 scripts/check_protocol_citations.py
agent-evidence validate-profile examples/minimal-valid-evidence.json
```

If the `agent-evidence` command is unavailable, use:

```bash
.venv/bin/agent-evidence validate-profile examples/minimal-valid-evidence.json
```

## Required report

In the final task summary, report:

- affected EEOAP clauses;
- files changed;
- validation commands run;
- validator result;
- any known deviations.

## Claim limits

Do not claim:

- legal compliance;
- external certification;
- standard-body adoption;
- publication acceptance;
- deployment robustness;
- external validation;
- submitted, accepted, certified, standardized, or published status.

## Forbidden actions

Do not:

- invent new EEOAP clauses;
- change protocol claim scope;
- modify branch protection;
- tag or release;
- upload to any portal;
- touch PaperProof / C1;
- merge PR #84.
