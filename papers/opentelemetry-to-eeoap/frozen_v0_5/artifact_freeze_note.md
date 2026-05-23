# Artifact Freeze Note

## Scope

This note freezes the current OpenTelemetry-to-EEOAP adapter paper package as a
local submission-prep artifact. It does not publish a DOI, choose a venue, add
runtime features, or expand the evaluation beyond the committed fixtures.

## Branch and Commits

- Branch: `opentelemetry-to-eeoap-adapter`
- Adapter prototype commit:
  `c5df6ce235b7194cafe35945e4b60bd5963c8b94`
- Paper evidence closure commit:
  `ff8c794b1444527e40b587aef41597bd919b157b`
- Paper v0.1 commit:
  `c4a7d5667cca9717ed6516589472b116ae997889`
- Paper v0.2 commit:
  `07d31cd4fc2758d1c901ba1c5b69339803ae434c`
- Paper v0.3 commit:
  `af28ea5a0c9cc161c0f5488ee8661a9fe5ac89a4`
- Current v0.4 commit placeholder:
  `to be filled after commit`

## Reproduction Command

Scoped adapter test command:

```bash
.venv/bin/python -m pytest tests/test_opentelemetry_to_eeoap_adapter.py -q
```

Scoped adapter test result from v0.3:

```text
6 passed in 1.51s
```

Existing evidence closure full pytest result:

```text
164 passed, 1 skipped, 15 warnings in 35.38s
```

## Freeze Assertions

- Runtime code did not change after the adapter prototype commit
  `c5df6ce235b7194cafe35945e4b60bd5963c8b94`.
- The EEOAP schema did not change.
- No adapter features were added for v0.4.
- The current paper package is a citation-cleanup and artifact-freeze draft.
- The generated valid statement remains:
  `generated/valid-agent-trace-eeoap-statement.json`.
- The generated adapter report remains:
  `generated/valid-agent-trace-adapter-report.json`.

## Out of Scope

The following worktree areas are unrelated to this paper freeze and are not
part of the OpenTelemetry-to-EEOAP adapter package:

- SoftwareX paper files and submission-pack material.
- `pd-oap/` and `pd-oap.zip`.
- `tmp/`.
- Other pre-existing untracked or modified paper-support files outside
  `papers/opentelemetry-to-eeoap/`.

Full repository Ruff is not used as a clean v0.4 signal because unrelated
pre-existing lint debt remains in out-of-scope directories. This is repository
hygiene debt, not an adapter failure.

## Preserved Non-Claims

- No legal accountability proof.
- No full runtime reconstruction.
- No general OpenTelemetry implementation compatibility claim.
- No cross-framework generality claim.
- No agent-output correctness claim.
- No new profile claim.
