# Reviewer Notes

## Why This Is Not Duplicate Work with the Earlier EEOAP Paper

- The earlier EEOAP work defines and validates the operation accountability
  statement profile.
- This work assumes that profile exists and asks how external agent telemetry
  can enter it.
- The contribution is not another definition of EEOAP. It is a concrete
  adapter path from OpenTelemetry-style agent spans to an existing EEOAP
  statement.
- The evaluation centers on mapping success and mapping failure diagnostics,
  not on re-arguing the profile itself.

## Why This Is Not Duplicate Work with AEP

- AEP is a broader evidence-object and artifact line in this repository.
- This adapter targets the EEOAP v0.1 operation accountability statement and
  the existing EEOAP validator path.
- The input is OpenTelemetry-style GenAI telemetry, not a new AEP profile,
  bundle, release, or media evidence object.
- The contribution should be reviewed as a telemetry ingestion and mapping
  artifact, not as an AEP replacement or extension claim.

## Why This Is Not a New Profile Paper

- No new profile is introduced.
- The EEOAP schema is not changed.
- The adapter does not rename or fork EEOAP.
- The generated output is validated by the existing
  `agent-evidence validate-profile` command.
- The paper claim is about bounded transformation into an existing evidence
  object shape.

## Why the Contribution Is Adapter, Mapping, and Evaluation

- Adapter: the implementation reads one local OpenTelemetry-style trace JSON and
  emits one EEOAP-compatible operation accountability statement.
- Mapping: the work specifies where trace ids, span ids, agent attributes,
  operation names, parent links, tool spans, timestamps, and error types land in
  the EEOAP statement or adapter report.
- Evaluation: the artifact includes one valid trace, four invalid traces,
  generated outputs, adapter diagnostics, validator results, and pytest
  evidence.
- The strongest claim is that a narrow telemetry-to-evidence bridge can be made
  validator-checkable without changing EEOAP.

## Ruff Disclosure

Full-repository `ruff check .` is currently blocked by unrelated pre-existing
lint debt in out-of-scope directories such as `pd-oap/` and other generated or
paper-support trees.

This should be disclosed directly:

- the full-repository ruff issue predates and sits outside the adapter commit;
- the adapter files passed scoped ruff checks during implementation;
- the staged adapter commit passed pre-commit `ruff check` and `ruff format`;
- full pytest passed with `164 passed, 1 skipped, 15 warnings`;
- the ruff debt should not be presented as part of the adapter evaluation
  failure surface.

The honest paper wording is: full-repository lint is not currently a clean
artifact-wide signal because of pre-existing out-of-scope repository debt, so
the adapter evaluation relies on scoped lint/pre-commit evidence plus the full
pytest result.
