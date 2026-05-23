# Root Layout Decision

## Current Source Layout

The OpenTelemetry-to-EEOAP adapter is located at:

- `tools/opentelemetry_to_eeoap_adapter.py`

Related package and validation code is part of the broader `agent-evidence`
repository. The repository uses a Python package layout centered on
`agent_evidence/`, with metadata in `pyproject.toml`.

There is no root `src/` directory and no `repo/src` layout.

## SoftwareX Expectation

The SoftwareX route analysis recorded an expectation that public software
packages include README material, license material, source code, support
material, and a clear public software version. The v1.4 analysis also noted a
`repo/src` source-layout issue.

## Risks of a Layout Rewrite

- It would change release surface late in the route.
- It could affect package imports, CLI behavior, tests, and generated outputs.
- It could create unnecessary churn unrelated to the adapter evidence story.
- It may require broad repository changes outside the isolated paper package.

## Is a Rewrite Necessary Before Template Conversion?

No. Template conversion should not require a source-layout rewrite. The article
can state that the adapter source is located under `tools/` inside the
`agent-evidence` repository and that the broader package uses `agent_evidence/`
as its Python package directory.

## Possible Narrative Explanation

The OpenTelemetry-to-EEOAP adapter is distributed as part of the
`agent-evidence` repository. The adapter entry point is
`tools/opentelemetry_to_eeoap_adapter.py`; examples are under
`examples/opentelemetry/`; scoped tests are under
`tests/test_opentelemetry_to_eeoap_adapter.py`; generated review artifacts are
under `generated/`.

## Recommendation

Do not rewrite source layout before template conversion unless SoftwareX
explicitly requires it. Treat the lack of `repo/src` as a release-readiness
issue to explain in the draft and revisit only if needed.
