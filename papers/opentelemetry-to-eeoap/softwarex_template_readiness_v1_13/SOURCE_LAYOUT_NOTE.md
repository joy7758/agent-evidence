# Source Layout Note

## Current Paths

- Adapter source: `tools/opentelemetry_to_eeoap_adapter.py`
- Broader package source: `agent_evidence/`
- Scoped tests: `tests/test_opentelemetry_to_eeoap_adapter.py`
- Examples: `examples/opentelemetry/`
- Generated artifacts: `generated/`

## SoftwareX Layout Issue

Earlier SoftwareX route analysis noted a `repo/src` expectation. This
repository does not currently use a `repo/src` layout for the adapter. The
adapter is a tool inside the broader `agent-evidence` repository.

## Why Rewrite Is Deferred

Changing source layout before template conversion would create release churn and
could affect imports, CLI behavior, tests, generated outputs, and package
metadata. The current issue is packaging description, not runtime behavior.

## Honest Article Wording

The article should state that the adapter entry point is under `tools/`, the
broader package source is under `agent_evidence/`, examples are under
`examples/opentelemetry/`, scoped tests are under `tests/`, and generated review
artifacts are under `generated/`.

The lack of `repo/src` should be disclosed as a packaging issue to resolve or
explain before final submission.
