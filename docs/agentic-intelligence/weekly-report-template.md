# Weekly Agentic Compatibility Report Template

## Week / Date

- Week:
- Report date:

## Reviewer

- Reviewer:
- Review mode: manual, human-reviewed

## Sources Reviewed

List only legitimate public sources. Prefer official docs, official
changelogs, official blogs, public GitHub releases, public standards/spec
pages, and public SDK/API docs.

| Source | Observed change | Evidence link | Agent-evidence impact | Recommendation | Priority | Risk | Human decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |

## Observed Changes

Record source-backed observations. Separate facts from interpretation.

- Observation:
- Evidence:
- Notes:

## Impact Assessment

Map each observation to one or more `agent-evidence` surfaces:

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

## Affected Agent-Evidence Surfaces

- Surface:
- Current project behavior:
- Possible compatibility impact:

## Recommendation

Choose one:

- no action
- watch
- docs-only candidate
- metadata-only candidate
- test-only candidate
- code-affecting candidate
- release-affecting candidate
- reject / no-go

Recommended action:

```text

```

## Email Notification Summary

Use this section when a GitHub Issue notification is created for the weekly
report.

- Issue title:
- Top recommendations:
- Human decision needed:

Decision checklist:

- [ ] no action / watch
- [ ] docs-only candidate
- [ ] metadata-only candidate
- [ ] test-only candidate
- [ ] code-affecting PR needs separate planning
- [ ] reject / no-go

## Priority

Choose one:

- P0 urgent
- P1 high
- P2 normal
- P3 watch

Rationale:

```text

```

## Risk

Choose one:

- low
- medium
- high
- no-go

Risk notes:

```text

```

## Evidence / Source Links

Every recommendation should cite or link to a public source.

- Source:
- Link:
- Date accessed:

## No-Go Checks

Confirm:

- [ ] no automatic code changes
- [ ] no automatic pull request
- [ ] no automatic release
- [ ] no automatic registry publication
- [ ] no automatic promotion
- [ ] no fake adopter claims
- [ ] no private-source scraping
- [ ] no credentials, secrets, or private user data collected
- [ ] no unsupported official partnership, adoption, or compliance claim
- [ ] no OpenAPI/MCP/schema/core change without a separate plan and tests

## Human Decision

Choose one:

- no action
- watch
- approved for docs-only PR
- approved for metadata-only PR
- approved for test-only PR
- approved for code PR planning
- approved for release planning
- rejected / no-go

Decision notes:

```text

```

## Follow-Up PRs, If Any

- PR:
- Scope:
- Approval reference:
- Verification required:
