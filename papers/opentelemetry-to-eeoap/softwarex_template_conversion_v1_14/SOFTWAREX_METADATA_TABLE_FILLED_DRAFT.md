# SoftwareX Metadata Table Filled Draft

## Metadata Table

| Field | Value |
|---|---|
| Current software version | TODO: assign release version before external submission. Draft label: `otel-eeoap-adapter-v0.1.0-rc`. |
| Permanent link to reproducible capsule | TODO: create public release, archive, DOI, or immutable public commit reference before formal submission. |
| Legal software license | Apache-2.0 via root `LICENSE`. TODO: confirm whether final SoftwareX package needs `LICENSE.txt`. |
| Code repository | TODO: set public release URL. Current readiness work is local to the release-candidate branch. |
| Software code languages, tools, and services used | Python; JSON fixtures; local `agent-evidence` CLI validator path; no external OpenTelemetry service. |
| Compilation requirements, operating environments, and dependencies | Python 3.11+; `click`, `jsonschema`, `pydantic`; `pytest` for scoped tests. TODO: confirm final operating-system statement. |
| If available, link to developer documentation/manual | Local docs under `papers/opentelemetry-to-eeoap/`; TODO: add public link after release. |
| Support email for questions | TODO: confirm public support contact before submission. |

## Field Sources

- Draft title and description: `softwarex_template_readiness_v1_13/`.
- Author and ORCID: `softwarex_metadata_drafts_v1_8/CITATION_OTEL_EEOAP.cff`.
- License: root `LICENSE` and `pyproject.toml`.
- Runtime and dependencies: `pyproject.toml`.
- Source path: `tools/opentelemetry_to_eeoap_adapter.py`.
- Tests path: `tests/test_opentelemetry_to_eeoap_adapter.py`.
- Examples path: `examples/opentelemetry/`.
- Generated artifacts path: `generated/`.

## TODO Fields

- Final release version.
- Permanent release/archive/DOI link.
- Public repository or release URL.
- Final documentation/manual URL.
- Public support email.
- Final operating system wording.
- Whether `LICENSE.txt` is required in addition to root `LICENSE`.

## Before Formal Submission

Replace all TODO fields with final public release metadata. Do not invent DOI,
release URL, pushed tag URL, or public archive reference.
