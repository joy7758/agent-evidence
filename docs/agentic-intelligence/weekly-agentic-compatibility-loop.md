# Weekly Agentic Compatibility Intelligence Loop

## Purpose

This loop reviews public changes in agentic engineering ecosystems and
recommends safe compatibility updates for `agent-evidence`.

It supports:

- agent discovery
- machine-readable metadata
- callable surfaces
- cookbook clarity
- Review Pack invocation
- citation and attribution
- failure handling
- boundary clarity

It does not:

- auto-modify the repository
- auto-create pull requests
- auto-publish releases
- auto-promote `agent-evidence`
- fabricate adopter, support, or recommendation signals

## Human Decision Model

The system performs analysis. The system produces recommendations. Humans
decide whether to act.

Every accepted change must go through a separate reviewed pull request. No
recommendation is binding, and no weekly report is authorization to change
code, publish, register, promote, or alter project claims.

## Weekly Cadence

Use a weekly review window:

1. collect legitimate public sources
2. extract evidence-backed changes
3. map each change to `agent-evidence` surfaces
4. classify the recommended action
5. assign priority and risk
6. identify No-Go items
7. send the report to human review
8. create a separate pull request only when approved

## Email Notification

Weekly reminders and report notifications can be delivered through GitHub Issue
notifications. See
`docs/agentic-intelligence/email-notification-protocol.md`.

The notification issue is a reminder and human decision prompt. It does not
auto-generate reports, auto-create pull requests, change repository behavior,
publish releases, or promote the project.

## Public Source Categories

Use only legitimate public sources:

- official docs
- official changelogs
- official blogs
- public GitHub releases
- public standards/spec pages
- public SDK/API docs

Candidate monitored areas:

- OpenAI / Codex agent behavior and docs
- Anthropic / Claude Code behavior and docs
- Google / Gemini agent tooling
- GitHub Copilot coding agent
- Cursor
- Windsurf / Cascade
- Replit / other coding-agent IDE workflows
- MCP ecosystem changes
- OpenAPI / tool-calling conventions
- `AGENTS.md` / `llms.txt` conventions
- software citation / attribution practices for AI agents

These are monitoring categories, not guaranteed weekly changes.

## Weekly Analysis Workflow

For each source-backed observation:

1. summarize the observed change
2. record evidence links
3. map the possible impact to `agent-evidence`
4. classify the action type
5. assign priority
6. identify risk
7. list No-Go items
8. recommend the next action
9. require a human decision

Separate observation from recommendation. Do not convert weak signals into
project claims.

## Impact Categories

- discovery metadata
- `AGENTS.md` / `llms.txt`
- capabilities JSON
- callable surfaces
- MCP compatibility
- OpenAPI compatibility
- docs / cookbooks
- Review Pack invocation
- citation / attribution
- security / privacy boundary
- release / packaging

## Recommendation Types

- no action
- watch
- docs-only candidate
- metadata-only candidate
- test-only candidate
- code-affecting candidate
- release-affecting candidate
- reject / no-go

## Priority Scale

- P0 urgent
- P1 high
- P2 normal
- P3 watch

## Risk Scale

- low
- medium
- high
- no-go

## Decision Gates

These gates apply to every recommendation:

- no automatic code changes
- no automatic release
- no automatic registry publication
- no automatic promotion
- no fake adopter claims
- no private-source scraping
- no credentials or secrets collection
- no private user data collection
- human approval required before pull request
- separate pull request required for every approved change

If a recommendation fails any gate, mark it `reject / no-go`.

## Relationship to the Agentic Consumption Loop

The weekly intelligence loop keeps
`docs/cookbooks/agentic_engineering_consumption_loop.md` current as external
agent tooling changes.

The consumption loop is the current external-agent path through discovery,
capability inspection, runnable evidence generation, signed export
verification, Review Pack creation, failure handling, citation, and
attribution. Weekly compatibility analysis should improve that path only when
public evidence shows a real compatibility need.

## Example Outcomes

- If a coding agent changes how it discovers `AGENTS.md`, recommend a
  docs/metadata review.
- If an MCP convention changes, recommend compatibility review, not immediate
  implementation.
- If official docs add a new citation convention, recommend attribution docs
  review.
- If a trend is rumor-only, mark it `reject / no-go`.

## No-Go Examples

- adding provider-specific core logic based on rumor
- claiming support for a new agent platform without testing
- adding registry publication because it is trending
- creating `ADOPTERS.md` without real adoption
- asking agents to star, follow, fork, or promote the project
- changing OpenAPI or MCP behavior without implementation and tests
