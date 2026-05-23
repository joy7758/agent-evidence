# Software Package Gap

This analysis treats the current repository as a possible SoftwareX software
distribution for the OpenTelemetry-to-EEOAP adapter package. It does not modify
repository layout.

## What Is Ready

- Root `README.md` exists and explains `agent-evidence`, EEOAP, AEP-Media, CLI
  examples, installation, validation, and scope boundaries.
- Root `LICENSE` exists and is Apache-2.0.
- `pyproject.toml` defines the Python package, dependencies, optional
  development dependencies, package data, and CLI entry point.
- Source code exists under `agent_evidence/`.
- The OpenTelemetry-to-EEOAP adapter exists at
  `tools/opentelemetry_to_eeoap_adapter.py`.
- Local fixtures exist under `examples/opentelemetry/`.
- Generated EEOAP-compatible statements and adapter reports exist under
  `generated/`.
- Tests exist under `tests/test_opentelemetry_to_eeoap_adapter.py`.
- Scoped adapter tests pass.
- Frozen package material exists under
  `papers/opentelemetry-to-eeoap/frozen_v0_5/`.
- Local immutable tags exist for EEOAP and AEP artifact references:
  `eeoap-v0.1-artifact` and `aep-v0.1-artifact`.

## What Is Weak

- The root README is broad and not focused on the OpenTelemetry-to-EEOAP adapter
  as the SoftwareX software object.
- The adapter is in `tools/`, not an installed package module or CLI subcommand.
- There is no `src/` directory and no `repo/src` release layout.
- Root citation metadata currently describes AEP-Media, not the
  OpenTelemetry-to-EEOAP adapter package.
- The v1.0 manuscript is too long and shaped like a journal method paper.
- The v0.5 frozen package predates the v0.7 second valid trace expansion.
- Local tags are not pushed and are not public artifact identifiers.
- Dirty out-of-scope worktree items create release risk if a release is cut from
  the current workspace without isolation.

## What Blocks SoftwareX Readiness

- No clean release branch/package has been isolated for OpenTelemetry-to-EEOAP.
- No public tag, release, archive, or DOI exists for the OpenTelemetry-to-EEOAP
  package.
- Source layout does not match the explicit `repo/src` expectation in the
  SoftwareX guide.
- `LICENSE.txt` is absent, though `LICENSE` is present.
- OpenTelemetry-to-EEOAP-specific `CITATION.cff` or CodeMeta metadata is absent.
- The support material needs a final package that includes both v0.5 frozen
  material and v0.7 second-trace evidence.
- The repository contains unrelated dirty/untracked files under AEP-Media,
  `pd-oap`, `tmp`, and other paths.

## What Can Be Solved Without Changing Research Claims

- Create a clean release branch.
- Add SoftwareX-facing README material.
- Add or mirror `LICENSE.txt` if required.
- Prepare source-layout strategy without changing adapter behavior.
- Add citation metadata for the OpenTelemetry-to-EEOAP package.
- Cut a release-candidate support package with checksums.
- Rewrite the paper into a shorter SoftwareX article.
- Add data availability, generative AI disclosure, conflict, and funding
  statements.

## What Should Not Be Solved Now

- Do not add LangChain runtime integration.
- Do not add OpenTelemetry Collector integration.
- Do not broaden OpenTelemetry compatibility claims.
- Do not change the EEOAP schema.
- Do not add new fixtures during this route-analysis step.
- Do not push local tags before the release branch is clean.
- Do not create a DOI before the public artifact scope is frozen.
