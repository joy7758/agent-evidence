# Quickstart for Agents

This is the shortest safe path for coding agents, retrieval agents, and
tool-using agents that need to inspect or validate `agent-evidence`.

## Install

From the repository root:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
```

## Inspect the callable surface

```bash
.venv/bin/agent-evidence --help
.venv/bin/agent-evidence capabilities --json | .venv/bin/python -m json.tool
```

Use `docs/callable-surfaces.md` and `docs/project-facts.md` to confirm the
implemented CLI surface before adding wrappers or new callable metadata.

## Validate the minimal example

```bash
.venv/bin/agent-evidence validate-profile examples/minimal-valid-evidence.json
```

Expected behavior:

- the valid example exits with status `0`;
- the JSON result includes `"ok": true`.

Controlled invalid examples live under `examples/invalid-*.json`. They are
expected to fail with stable primary codes.

## Run the smallest demo

```bash
.venv/bin/python demo/run_operation_accountability_demo.py
```

Expected behavior:

- the demo exits with status `0`;
- the output ends with a `PASS` summary line for the current profile;
- generated demo artifacts stay under `demo/artifacts/`.

## Where examples live

- `examples/minimal-valid-evidence.json`
- `examples/invalid-missing-required.json`
- `examples/invalid-unclosed-reference.json`
- `examples/invalid-policy-link-broken.json`

## Where reports live

- `demo/artifacts/` for demo outputs
- `docs/reports/` for checked documentation reports
- generated rerun outputs may appear under `artifacts/` and should be treated
  as local generated output unless explicitly scoped

## Avoid private or local-only files

Before staging, run:

```bash
git status --short
git diff --check
```

Do not stage:

- generated local outputs;
- private route-control notes;
- local archive material;
- files hidden by `.git/info/exclude`;
- unrelated worktree residue.

Do not inspect or touch PaperProof / C1 during `agent-evidence` work unless the
user explicitly scopes a separate PaperProof / C1 task.

## Safe closeout checklist

Before committing:

1. Confirm only the intended files are staged.
2. Run `git diff --cached --check`.
3. Run the narrowest relevant validator or smoke test.
4. Confirm no local package is described as submitted, accepted, externally
   reviewed, certified, or published.
5. Commit only the scoped files.
