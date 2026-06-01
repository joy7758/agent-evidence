# README Agent Discoverability Patch Plan

Date: 2026-06-02

## Goal

Make the GitHub landing path clear for humans, LLMs, and coding agents:

`README.md -> llms.txt -> docs/aep-media/agent-index.md -> mobile-video walkthrough -> external review issue body`

## Patch Scope

Add a short README section near the AEP-Media section:

```markdown
## Agent-readable project entry points

- `llms.txt`: compact project map for LLMs and coding agents.
- `docs/aep-media/agent-index.md`: command-oriented index for reviewers and agents.
- `docs/aep-media/mobile-video-walkthrough.md`: fresh-clone reproduction path.
- `docs/aep-media/adapter-boundaries.md`: adapter ingestion boundaries and non-claims.
- `paper/paper.md`: JOSS software paper draft.
```

Also add direct links under the existing AEP-Media entry-point list:

- `docs/aep-media/agent-index.md`
- `llms.txt`

## docs/aep-media README Sync

Update `docs/aep-media/README.md` to link:

- `agent-index.md`
- root `llms.txt`
- mobile-video walkthrough
- adapter boundaries
- external reproducibility review task

## Scoping Rule

Do not rewrite the whole README. Do not change implementation code. Do not
create GitHub issues. Do not submit to JOSS.

Because `docs/aep-media/README.md`, `mobile-video-walkthrough.md`, and
`adapter-boundaries.md` are linked by the README and `llms.txt`, include them in
the scoped discoverability commit to avoid broken GitHub links.
