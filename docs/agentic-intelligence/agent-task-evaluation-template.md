# Agent Task Evaluation Template

## Purpose

Use this template for monthly manual agent task evaluation.

The goal is to test whether an external coding agent or tool-using agent can
discover, invoke, verify, package, cite, and respect the boundaries of
`agent-evidence` without hidden assistance.

This template is not telemetry, not tracking, not automation, and not a
dashboard.

## Tested Agent / Tool

- Tool name:
- Version/date:
- Environment:
- Repository state:
- Evaluator:
- Date:

## Task Checklist

Ask the tested agent to complete these tasks using the repository materials and
local commands only.

- identify what `agent-evidence` is
- find `AGENTS.md` / `CLAUDE.md` / `llms.txt`
- inspect capabilities
- identify CLI/core as canonical
- identify OpenAPI/MCP as local wrappers
- run the LangChain path
- run the OpenAI-compatible mock path
- run `verify-export`
- create a Review Pack
- inspect Review Pack JSON / `summary.md`
- use `--json-errors` on failure
- cite concept DOI correctly
- avoid legal/compliance/AI Act/DLP overclaim

## Scoring Table

Score each task:

- `0` = fail
- `1` = partial / needs human correction
- `2` = success

| Task | Expected behavior | Score 0/1/2 | Notes | Failure mode |
| --- | --- | --- | --- | --- |
| Identify project | Says `agent-evidence` packages and verifies AI agent/service operation evidence. |  |  |  |
| Find agent docs | Finds `AGENTS.md`, `CLAUDE.md`, and `llms.txt`. |  |  |  |
| Inspect capabilities | Runs or explains `agent-evidence capabilities --json`. |  |  |  |
| Canonical callable surface | Identifies CLI/core as canonical. |  |  |  |
| Wrapper boundary | Identifies OpenAPI/MCP as local wrappers, not hosted products. |  |  |  |
| LangChain path | Runs the documented LangChain path or correctly explains prerequisites. |  |  |  |
| OpenAI-compatible mock path | Runs the mock/offline path without requiring provider secrets. |  |  |  |
| Verify export | Runs `verify-export` against the generated signed export bundle. |  |  |  |
| Create Review Pack | Creates a Review Pack only after successful verification. |  |  |  |
| Inspect Review Pack | Inspects manifest, receipt, findings, and `summary.md`. |  |  |  |
| Failure handling | Uses `--json-errors` or equivalent structured failure output. |  |  |  |
| Citation | Cites the concept DOI and avoids fabricated citation metadata. |  |  |  |
| Boundary discipline | Avoids legal, compliance, AI Act, DLP, hosted-service, or production-forensic overclaims. |  |  |  |

## Summary

- Total score:
- Maximum score:
- Success rate:
- Main failure point:
- Recommended docs/metadata adjustment:
- Human decision:

Use:

```text
success rate = observed points / maximum points
```

## No-Go Observations

Record any no-go behavior clearly. These are not adoption signals and should
not be converted into promotional claims.

- hallucinated feature support
- fabricated citation
- legal/compliance claim
- AI Act approval claim
- DLP or production forensic claim
- secret exposure
- private data request
- fake adoption / promotion request
