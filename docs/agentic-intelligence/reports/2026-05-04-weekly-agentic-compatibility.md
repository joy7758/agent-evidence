# Weekly Agentic Compatibility Report: 2026-05-04

## Week / Date

- Week: 2026-05-04 to 2026-05-10
- Report date: 2026-05-04
- Review type: first manual baseline report after the weekly agentic
  compatibility loop was added

## Reviewer

- Reviewer: Codex, under human-directed review
- Review mode: manual, source-backed, human decision required

## Sources Reviewed

Only official or public specification sources were reviewed.

| Source | Observed change or current-state signal | Evidence link | Agent-evidence impact | Recommendation | Priority | Risk | Human decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OpenAI Codex docs | Codex is positioned for software-engineering work and documents repository guidance through `AGENTS.md`. | [OpenAI Codex](https://developers.openai.com/codex/), [AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md) | Reinforces the value of `AGENTS.md` plus a copy/paste consumption loop. | no action | P3 watch | low | pending |
| GitHub Copilot coding agent docs | Copilot coding agent works through GitHub task and pull-request workflows. | [GitHub Copilot coding agent](https://docs.github.com/en/copilot/using-github-copilot/coding-agent/about-assigning-tasks-to-copilot) | Current docs already require human-reviewed PRs; no automatic PR behavior should be added. | no action | P3 watch | low | pending |
| VS Code Copilot custom instructions | VS Code documents custom instructions and includes support for repository instructions such as `AGENTS.md`. | [VS Code custom instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions) | Current `AGENTS.md` remains an appropriate agent-facing instruction surface. | watch | P3 watch | low | pending |
| Anthropic Claude Code docs | Claude Code emphasizes repository understanding, terminal/file operations, and project memory files such as `CLAUDE.md`. | [Claude Code overview](https://docs.anthropic.com/en/docs/claude-code/overview), [Claude Code memory](https://docs.anthropic.com/en/docs/claude-code/memory) | `agent-evidence` may later benefit from a small provider-neutral instruction crosswalk or a minimal `CLAUDE.md` pointer, but not in this report. | docs-only candidate | P2 normal | medium | pending |
| Google Gemini CLI docs | Gemini CLI is an open-source AI agent for terminal-based development workflows. | [Gemini CLI](https://cloud.google.com/gemini/docs/codeassist/gemini-cli) | Reinforces keeping CLI/core canonical and runnable paths copy/pasteable. | no action | P3 watch | low | pending |
| Gemini API function calling docs | Gemini supports function calling as a structured tool-use pattern. | [Gemini function calling](https://ai.google.dev/gemini-api/docs/function-calling) | Supports continued clarity around callable surfaces without adding provider-specific behavior. | watch | P3 watch | low | pending |
| Windsurf Cascade docs | Windsurf documents `AGENTS.md` as an automatically discovered instruction file for agentic coding workflows. | [Windsurf AGENTS.md](https://docs.windsurf.com/windsurf/cascade/agents-md) | Confirms `AGENTS.md` should remain concise and authoritative. | no action | P3 watch | low | pending |
| Replit Agent docs | Replit Agent provides software-building workflows from prompts and project context. | [Replit Agent](https://docs.replit.com/replitai/agent) | No immediate compatibility change; keep runnable paths explicit and offline-capable. | watch | P3 watch | low | pending |
| MCP specification | MCP defines a shared protocol for applications to provide tools and context to LLMs. | [MCP introduction](https://modelcontextprotocol.io/docs/getting-started/intro), [MCP specification](https://modelcontextprotocol.io/specification) | Current local stdio read-only / verify-first MCP boundary remains appropriate. | watch | P3 watch | medium | pending |
| OpenAPI specification | OpenAPI remains the standard source for describing HTTP APIs. | [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) | Current local OpenAPI thin wrapper remains a documentation and local-callable surface, not a hosted API claim. | no action | P3 watch | low | pending |
| `llms.txt` convention | `llms.txt` is a public convention for guiding LLM-readable project context. | [llms.txt](https://llmstxt.org/) | Current `llms.txt` and `llms-full.txt` remain useful agent-facing metadata surfaces. | watch | P3 watch | low | pending |
| `AGENTS.md` convention | `AGENTS.md` is a public convention for repository agent instructions. | [AGENTS.md](https://agents.md/) | Current `AGENTS.md` aligns with cross-agent instruction trends. | no action | P3 watch | low | pending |

## Observed Changes

This first report is a baseline review. It does not assert that every source
changed during this exact week. It records current public signals that affect
agentic discovery, invocation, citation, and boundary clarity.

### Observation 1: Repository instruction files are now a core agent surface

OpenAI Codex, VS Code Copilot, Windsurf, and the public `AGENTS.md`
convention all make repository-level agent instructions a practical discovery
surface.

Evidence:

- [OpenAI Codex AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md)
- [VS Code custom instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)
- [Windsurf AGENTS.md](https://docs.windsurf.com/windsurf/cascade/agents-md)
- [AGENTS.md](https://agents.md/)

Notes:

- `agent-evidence` already has `AGENTS.md`.
- P55 added the agentic engineering consumption loop and linked it from
  agent-facing docs.
- No immediate file change is required.

### Observation 2: CLI-oriented agent workflows remain important

OpenAI Codex, Claude Code, Google Gemini CLI, and Replit Agent all reinforce
the importance of repository context, terminal workflows, file edits, and
test-running behavior.

Evidence:

- [OpenAI Codex](https://developers.openai.com/codex/)
- [Claude Code overview](https://docs.anthropic.com/en/docs/claude-code/overview)
- [Gemini CLI](https://cloud.google.com/gemini/docs/codeassist/gemini-cli)
- [Replit Agent](https://docs.replit.com/replitai/agent)

Notes:

- `agent-evidence` should keep CLI/core canonical.
- The P55 cookbook already gives copy/paste paths for capability inspection,
  evidence generation, `verify-export`, Review Pack creation, and citation.

### Observation 3: Claude Code may justify a future instruction crosswalk

Claude Code documents project memory through `CLAUDE.md`. That does not mean
`agent-evidence` should immediately add provider-specific files, but it is a
source-backed compatibility item to review.

Evidence:

- [Claude Code memory](https://docs.anthropic.com/en/docs/claude-code/memory)

Notes:

- This is a `docs-only candidate`, not an implementation approval.
- Any future work should remain a minimal pointer or crosswalk, not
  provider-specific core logic.

### Observation 4: MCP and OpenAPI should remain bounded callable surfaces

MCP and OpenAPI remain important tool/context and HTTP-description surfaces,
but this report found no source-backed reason to change `agent-evidence`
behavior this week.

Evidence:

- [MCP introduction](https://modelcontextprotocol.io/docs/getting-started/intro)
- [MCP specification](https://modelcontextprotocol.io/specification)
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)

Notes:

- Current project boundary remains: CLI/core is canonical.
- OpenAPI remains a local thin wrapper.
- MCP remains local stdio read-only / verify-first.
- Review Pack remains CLI-created and is not exposed through OpenAPI/MCP in
  the current release.

### Observation 5: LLM-readable context remains useful, but no format change is needed

The public `llms.txt` convention continues to support compact LLM-readable
project context. `agent-evidence` already maintains `llms.txt` and generated
`llms-full.txt`.

Evidence:

- [llms.txt](https://llmstxt.org/)

Notes:

- No metadata change is required this week.
- Continue running generator drift checks for `agent-index.json` and
  `llms-full.txt`.

## Impact Assessment

| Observation | Affected surfaces | Compatibility impact |
| --- | --- | --- |
| Repository instruction files are core agent surfaces | `AGENTS.md`, `docs/for-agents.md`, consumption loop cookbook | Current state is strong; keep watch. |
| CLI-oriented workflows remain important | CLI/core, examples, cookbooks, tests | Current state is strong; no behavior change needed. |
| Claude Code memory uses `CLAUDE.md` | agent-facing instructions | Possible future docs-only crosswalk; human review required. |
| MCP and OpenAPI remain important surfaces | MCP docs, OpenAPI wrapper, callable-surface docs | Watch; do not change behavior without separate plan and tests. |
| LLM-readable context remains useful | `llms.txt`, `llms-full.txt`, `agent-index.json` | Continue metadata drift checks. |

## Affected Agent-Evidence Surfaces

- discovery metadata: `AGENTS.md`, `llms.txt`, `llms-full.txt`,
  `agent-index.json`
- capabilities JSON: `agent-evidence capabilities --json`
- callable surfaces: CLI/core, local OpenAPI wrapper, local MCP tools
- docs / cookbooks:
  `docs/cookbooks/agentic_engineering_consumption_loop.md`
- Review Pack invocation: CLI-created Review Pack path
- citation / attribution: `docs/how-to-cite.md`, `ATTRIBUTION.md`,
  `CITATION.cff`, `codemeta.json`
- security / privacy boundary: no secrets, no private key copying, no private
  data collection, no promotion behavior
- release / packaging: no release action recommended

## Recommendations

| Recommendation | Type | Priority | Risk | Rationale | Human decision |
| --- | --- | --- | --- | --- | --- |
| Keep the P55 consumption loop as the canonical external-agent path. | no action | P3 watch | low | It already covers discovery, capability inspection, CLI invocation, verification, Review Pack creation, failure stop, and citation. | pending |
| Plan, but do not implement yet, a provider-instruction crosswalk for Claude Code / `CLAUDE.md` compatibility. | docs-only candidate | P2 normal | medium | Claude Code uses project memory files; a future minimal pointer may help without provider-specific core logic. | pending |
| Continue watching MCP and OpenAPI conventions without changing behavior. | watch | P3 watch | medium | MCP/OpenAPI are relevant, but no source-backed urgent change requires implementation this week. | pending |
| Keep `llms.txt`, `llms-full.txt`, and `agent-index.json` generation checks as-is. | no action | P3 watch | low | Current metadata surfaces already support external-agent discovery. | pending |
| Reject automatic promotion, registry publication, or fake adopter signals. | reject / no-go | P0 urgent | no-go | These actions violate the weekly loop and source policy. | pending |

## Priority

- Highest active priority: P2 normal
- Reason: the only concrete candidate is a future docs-only instruction
  crosswalk for Claude Code-style project memory. It is useful but not urgent.

## Risk

- Overall risk: low for this report
- Main watch risk: medium for provider-specific instruction files, because
  adding many provider-specific entrypoints could fragment the canonical agent
  path.
- Mitigation: keep `AGENTS.md` and the consumption loop canonical; use only
  minimal pointers if a later PR is approved.

## Evidence / Source Links

Accessed on 2026-05-04:

- [OpenAI Codex](https://developers.openai.com/codex/)
- [OpenAI Codex AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md)
- [GitHub Copilot coding agent](https://docs.github.com/en/copilot/using-github-copilot/coding-agent/about-assigning-tasks-to-copilot)
- [VS Code Copilot custom instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)
- [Claude Code overview](https://docs.anthropic.com/en/docs/claude-code/overview)
- [Claude Code memory](https://docs.anthropic.com/en/docs/claude-code/memory)
- [Gemini CLI](https://cloud.google.com/gemini/docs/codeassist/gemini-cli)
- [Gemini API function calling](https://ai.google.dev/gemini-api/docs/function-calling)
- [Windsurf AGENTS.md](https://docs.windsurf.com/windsurf/cascade/agents-md)
- [Replit Agent](https://docs.replit.com/replitai/agent)
- [MCP introduction](https://modelcontextprotocol.io/docs/getting-started/intro)
- [MCP specification](https://modelcontextprotocol.io/specification)
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [llms.txt](https://llmstxt.org/)
- [AGENTS.md](https://agents.md/)

## No-Go Checks

- [x] no automatic code changes
- [x] no automatic pull request
- [x] no automatic release
- [x] no automatic registry publication
- [x] no automatic promotion
- [x] no automatic star/follow/fork request
- [x] no fake adopter claims
- [x] no private-source scraping
- [x] no credentials, secrets, or private user data collected
- [x] no unsupported official partnership, adoption, or compliance claim
- [x] no OpenAPI/MCP/schema/core change without a separate plan and tests
- [x] no legal non-repudiation claim
- [x] no compliance certification claim
- [x] no AI Act approval claim
- [x] no full AI governance platform claim

## Human Decision

Pending. This report is advisory only.

Human decision options:

- no action
- watch
- approved for docs-only PR
- approved for metadata-only PR
- approved for test-only PR
- approved for code PR planning
- approved for release planning
- rejected / no-go

## Follow-Up PRs, If Any

None created automatically.

Possible future follow-up, if human-approved:

- P59 docs-only planning: provider-instruction crosswalk for Claude Code /
  `CLAUDE.md` compatibility, without changing code behavior or making
  provider-specific support claims.

## Top 3 Recommendations

1. Keep `docs/cookbooks/agentic_engineering_consumption_loop.md` as the
   canonical external-agent journey.
2. Plan a small docs-only review of Claude Code / `CLAUDE.md` compatibility,
   but do not implement it without human approval.
3. Continue watching MCP, OpenAPI, `AGENTS.md`, and `llms.txt` conventions
   without changing repository behavior this week.

## Items Explicitly Rejected

- automatic repository changes
- automatic pull requests
- automatic releases
- automatic registry publication
- automatic star/follow/fork/promotion instructions
- fake adoption or adopter claims
- provider-specific core logic based only on trend monitoring
- Review Pack exposure through OpenAPI/MCP without a separate plan and tests
- AI Act Pack implementation
- legal non-repudiation, compliance certification, or AI Act approval claims

## Next Weekly Review Date

2026-05-11
