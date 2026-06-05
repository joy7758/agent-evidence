# Agentic Impact Scorecard

## Purpose

This scorecard measures whether `agent-evidence` is becoming easier for
external coding agents and tool-using agents to discover, invoke, verify,
package, and cite.

It evaluates whether agent-facing documentation and metadata help agents move
through the existing consumption loop:

```text
discover project
-> inspect capabilities
-> choose CLI/core
-> run examples
-> verify exports
-> create Review Packs
-> inspect results
-> cite correctly
-> stop on verification failure
```

It does not measure:

- private agent usage
- individual users
- hidden agent behavior
- exact agent identity
- legal or compliance adoption

## Measurement Principles

- no telemetry
- no user tracking
- no private data
- no fake adoption claims
- no star-count-only evaluation
- use public or authorized data only
- combine indirect signals with reproducible agent task tests

The scorecard is a manual evaluation tool. It is not automation, not a
dashboard, not a GitHub Actions workflow, and not a release gate.

## Metric Categories

### A. Discovery Metrics

Discovery metrics estimate whether external readers or agents can find the
agent-facing surfaces.

Examples:

- GitHub repository views
- GitHub unique visitors
- popular paths
- popular referrers
- agent-facing docs appearing in popular paths

Agent-facing paths to watch:

- `AGENTS.md`
- `CLAUDE.md`
- `llms.txt`
- `llms-full.txt`
- `agent-index.json`
- `docs/for-agents.md`
- `docs/cookbooks/agentic_engineering_consumption_loop.md`
- `docs/cookbooks/review_pack_minimal.md`
- `docs/callable-surfaces.md`
- `docs/how-to-cite.md`

### B. Installation / Invocation Metrics

Installation and invocation metrics estimate whether the package is being
retrieved or cloned after agent-facing docs changes.

Examples:

- PyPI downloads
- PyPI downloads by version
- GitHub clones
- release downloads if available
- latest-version adoption trend

### C. Agent Task Success Metrics

Task success metrics measure whether agents can complete controlled manual
tasks without human correction.

Measure whether agents can:

- discover the project
- inspect capabilities
- identify CLI/core as canonical
- run the LangChain path
- run the OpenAI-compatible mock path
- run `verify-export`
- create a Review Pack
- inspect manifest / receipt / findings / summary
- handle failed verification correctly
- cite the project correctly
- avoid overclaims

### D. External Signal Metrics

External signal metrics look for public evidence that others are referencing or
trying to use the project.

Examples:

- GitHub code search mentions
- public issues / PRs mentioning `agent-evidence`
- public docs or blog mentions
- DOI / citation mentions if available
- real dependents if visible

These signals are weak unless they are source-backed and specific. Do not
convert mentions into adoption claims.

## Agentic Impact Scorecard

| Category | Metric | Source | Frequency | Interpretation | Caution |
| --- | --- | --- | --- | --- | --- |
| Discovery | GitHub views | GitHub traffic API | Weekly | More views may indicate better discovery. | Views do not identify agents or prove adoption. |
| Discovery | GitHub clones | GitHub traffic API | Weekly | More unique cloners may indicate trial or integration interest. | Clones may be human, CI, mirrors, or bots. |
| Discovery | Top paths | GitHub traffic API | Weekly | Agent-facing paths appearing here suggests docs are being found. | Popular paths are aggregate traffic, not intent. |
| Discovery | Top referrers | GitHub traffic API | Weekly | Referrers can show where discovery begins. | Referrers do not prove endorsement or use. |
| Installation | PyPI downloads | PyPIStats / PyPI BigQuery | Weekly | Download trend may show installation interest. | Downloads include CI, mirrors, caches, and retries. |
| Installation | Version-specific downloads | PyPIStats / PyPI BigQuery | Weekly | Latest-version share can show whether users move to current surfaces. | Version downloads do not prove agent use. |
| Task success | Agent task success rate | Manual task evaluation | Monthly | Higher scores suggest clearer agent-facing paths. | Controlled tests are not real-world adoption. |
| External signals | External mentions | GitHub search / public web sources | Quarterly | Specific public references may show external awareness. | Mentions do not equal adoption. |
| External signals | Citation / DOI signals | Zenodo / public citation sources | Quarterly | Correct DOI usage suggests citation clarity. | Citation counts can lag and may be incomplete. |
| Boundary quality | Overclaim incidents | Manual review of issues, PRs, reports, and task tests | Monthly | Fewer overclaims suggests better boundary discipline. | Absence of observed incidents is not proof of zero incidents. |

## Agent Task Success Scoring

Score each task:

- `0` = fail
- `1` = partial / needs human correction
- `2` = success

Task groups:

- discovery
- capability inspection
- invocation
- verification
- Review Pack creation
- failure handling
- citation
- boundary discipline

Score:

```text
Agent Task Success Rate = observed points / maximum points
```

Report both the total score and the main failure point. A high score means the
current agent-facing materials are easier to use in a controlled evaluation. It
does not prove adoption.

## Interpretation Guide

Signals that suggest improvement:

- agent-facing docs appear in popular paths
- latest PyPI version downloads increase
- unique cloners increase after agent-facing docs changes
- agents complete more tasks without human correction
- fewer overclaim errors
- correct DOI/citation use increases

Signals that do not prove impact:

- stars alone
- one-off social mention
- private claim without evidence
- agent hallucinated recommendation
- fake adopter signal

## Baseline and Cadence

Recommended cadence:

- weekly GitHub/PyPI public metric snapshot
- monthly agent task success evaluation
- quarterly external signal review

Treat the first complete snapshot as the baseline. Compare later snapshots
against the baseline only when collection method, date range, and scope are
documented.

## Manual Collection Commands

These commands are manual examples, not automated telemetry.

GitHub traffic:

```bash
gh api repos/joy7758/agent-evidence/traffic/views
gh api repos/joy7758/agent-evidence/traffic/clones
gh api repos/joy7758/agent-evidence/traffic/popular/paths
gh api repos/joy7758/agent-evidence/traffic/popular/referrers
```

PyPI:

```bash
python -m pip install pypistats
pypistats recent agent-evidence
pypistats overall agent-evidence
pypistats python_major agent-evidence
```

External search:

```bash
gh search code "\"agent-evidence\""
gh search code "\"agent-evidence review-pack\""
gh search code "\"review-pack create\""
```

## Boundaries

- no telemetry
- no private tracking
- no private-source scraping
- no user profiling
- no automatic promotion
- no fake adoption
- no legal/compliance interpretation
- no claim of legal non-repudiation
- no claim of compliance certification
- no claim of AI Act approval
