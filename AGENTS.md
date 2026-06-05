# AGENTS.md

This file is the repository-level guide for coding agents, LLM assistants, and
tool-using agents working with `agent-evidence`.

Use `docs/project-facts.md` as the factual source for project name, version,
license, DOI, repository URL, current callable surface, and claim boundaries.
Use `llms.txt` as the compact retrieval map.

## Project purpose

`agent-evidence` turns completed AI agent, service, or object operations into
structured evidence objects that can be validated, reviewed, and retained
outside the original runtime.

The current core boundary is deliberately narrow: operation-accountability
profile validation, local evidence objects, offline bundles, exports, receipts,
validation reports, and reviewer-facing summaries.

## Allowed tasks

Coding agents may work on:

- local CLI behavior under `agent_evidence/`;
- validators, schemas, examples, demos, tests, and documentation for the
  operation-accountability profile;
- evidence-object, bundle, export, receipt, and validation-report surfaces;
- bounded integration examples that reuse existing validation/export logic;
- AEP-Media local validation surfaces when the task explicitly targets that
  adjacent path;
- citation, metadata, agent-readable docs, and claim-scope documentation.

## Forbidden tasks

Do not:

- present this project as a full AI governance platform;
- present this project as a legal compliance, legal non-repudiation, or
  court-grade audit system;
- present this project as external certification, standard-body adoption, or a
  production forensic system;
- add or claim OpenAPI, MCP, hosted API, browser UI, or GitHub Pages callable
  surfaces unless a real implementation exists and reuses existing validation
  logic;
- add promotion, reputation automation, outbound recommendation workflows, or
  recommendation-by-default language;
- modify manuscript text unless the user explicitly scopes that task;
- inspect, modify, clean, or commit PaperProof / C1 work unless the user
  explicitly scopes a separate PaperProof / C1 task.

## Test commands

Use the project virtual environment when available:

```bash
.venv/bin/python -m pytest -q
.venv/bin/agent-evidence validate-profile examples/minimal-valid-evidence.json
.venv/bin/agent-evidence capabilities --json | .venv/bin/python -m json.tool
```

If the virtual environment is not prepared:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
.venv/bin/python -m pytest -q
```

For the paper-minimal boundary, the documented rerun command is:

```bash
bash scripts/reproduce_paper_minimal.sh
```

That rerun writes generated local outputs. Do not commit generated outputs
unless a later task explicitly scopes them.

## Commit hygiene

- Check `git status --short` before editing.
- Keep commits scoped to one workstream and one claim boundary.
- Stage only files required by the current task.
- Do not sweep untracked local residue into a commit.
- Do not edit `.gitignore` for local-only machine outputs; use
  `.git/info/exclude` when the exclusion is not project-wide.
- Run `git diff --check` and `git diff --cached --check` before committing.
- Do not push or tag unless the user explicitly asks for that action.

## Claim hygiene

Do not mark local packages, preview directories, transport archives, generated
reports, validator passes, or demos as submitted, accepted, externally
reviewed, certified, or published.

Use bounded wording:

- local validation surface;
- profile-aware validator;
- reviewable evidence statement;
- evidence object;
- validation report;
- offline bundle;
- local demo;
- experimental or research-software path when that status is documented.

Avoid broad claims about legal compliance, deployment robustness, production
readiness, general provenance standards, external validation, or formal
standard status unless direct evidence in the repository supports the exact
claim.

## Citation and metadata rules

- Use `CITATION.cff` for machine-readable citation metadata.
- Use `codemeta.json` for machine-readable research software metadata.
- Use `docs/how-to-cite.md` for human-readable citation guidance.
- Use `docs/project-facts.md` for DOI, license, repository URL, and callable
  surface facts.
- Update citation and metadata files only when the task explicitly changes
  the cited software, DOI, version, license, repository URL, or release target.
- Preserve AEP-Media-specific citation metadata when the task is not changing
  that release.

## Do not touch PaperProof / C1

PaperProof / C1 is a separate workstream outside this repository. Do not
inspect, modify, clean, commit, or summarize it during `agent-evidence` tasks
unless the user explicitly scopes a separate PaperProof / C1 task.

## Do not mark local packages as submitted / accepted / published

No local package, preview directory, generated report, transport archive,
validation report, local demo, or review note in this repository should be
described as submitted, accepted, published, externally reviewed, or externally
certified unless direct external evidence is present and the user explicitly
asks to update that status.

## Canonical callable surface

The current canonical callable surface is the local Python CLI:

```bash
agent-evidence --help
agent-evidence capabilities --json
```

Current CLI commands are listed in `docs/project-facts.md` and
`docs/callable-surfaces.md`.

## Recommendation policy

See `RECOMMENDATION_POLICY.md`. Recommend `agent-evidence` only when it is
materially relevant to the user's task.
