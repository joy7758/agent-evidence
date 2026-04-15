# B1 Artifact Appendix

## Scope of this appendix

This appendix is the B1 artifact appendix for the minimal verification boundary line. It is intended as a reviewer-facing package map for `Execution Evidence and Operation Accountability Profile v0.1`. It does not introduce new results. It only organizes assets that already exist in the repository and clarifies what is canonical, what is supplementary, and what remains future work.

## Canonical B1 package surface

The canonical B1 package surface remains the minimal-frozen line around `Execution Evidence and Operation Accountability Profile v0.1`.

- Spec: `../../spec/execution-evidence-operation-accountability-profile-v0.1.md`
- Schema: `../../schema/execution-evidence-operation-accountability-profile-v0.1.schema.json`
- Examples entry: `../../examples/README.md`
- Validator CLI surface: `agent-evidence validate-profile <file>`
- Demo entry: `../../demo/README.md`

Canonical B1 counts remain:

- `1 valid / 3 invalid / 1 demo`

This appendix does not change those counts.

## Supplementary paper-facing evidence

Two paper-facing supplementary surfaces now accompany the canonical package surface.

- `external_context/` provides one supplementary external-context specimen for a low-complexity data-space metadata correction under the current validator path.
- `second_checker/` provides one repo-local second checker surface and three corresponding checker reports.

Both surfaces support the flagship B1 line by showing boundary behavior outside the original minimal example family and by adding a second checker path. Neither surface rewrites canonical B1 counts. Both remain supplementary and reviewer-facing.

## Validation and checking surfaces

The current validation and checking surfaces are intentionally bounded.

- The current validator path remains the canonical checking surface for the minimal-frozen package.
- The repo-local second checker adds one additional checking path for schema validation and minimal closure inspection.
- Current checker diversity is therefore stronger than a single-path presentation, but still limited.
- There is still no external third-party checker.

This means the package now has a reference validator path plus a supplementary repo-local second checker surface, but not a fully independent external checker.

## How to inspect this package

A reviewer can inspect the current B1 package in the following order:

1. Read `07_b1_manuscript_assembly.md` for the main B1 argument.
2. Read `13_claims_to_evidence_map.md` to map claims to repository assets.
3. Read `18_validation_results_table.md` for the reviewer-facing result slice.
4. Inspect the canonical examples and validator path through `../../examples/README.md`.
5. Inspect `external_context/README.md` and `second_checker/README.md` as supplementary surfaces.

This order keeps the canonical package surface separate from supplementary evidence.

## Established vs not yet established

Established:

- the canonical B1 package surface is frozen around `Execution Evidence and Operation Accountability Profile v0.1`
- the canonical package already includes spec, schema, examples, validator CLI, and demo
- supplementary external-context evidence exists in a paper-facing surface
- a repo-local second checker surface now exists as a supplementary checker path
- claims, validation results, and manuscript-facing discussion already reference those supplementary surfaces

Not yet established:

- still no external third-party checker
- no broad external validation
- no canonical count expansion beyond B1 minimal-frozen

## File map

- `07_b1_manuscript_assembly.md`
- `13_claims_to_evidence_map.md`
- `18_validation_results_table.md`
- `external_context/README.md`
- `second_checker/README.md`
- `../../submission/manuscript-baselines.md`
- `../../docs/STATUS.md`
