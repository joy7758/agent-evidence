# Software Metadata Table TODO Plan

| Metadata field | Current value | TODO reason | Required before template conversion? | Required before formal submission? | Final source |
|---|---|---|---|---|---|
| Current software version | Draft label `otel-eeoap-adapter-v0.1.0-rc` | Final release version not assigned. | no | yes | Final release tag or release metadata |
| Permanent link to reproducible capsule | TODO | Public release/archive/DOI not created. | no | yes | GitHub Release, DOI archive, or immutable public commit |
| Legal software license | Apache-2.0 via root `LICENSE` | Need confirm whether `LICENSE.txt` copy is required. | no | yes | Root `LICENSE` or final release package |
| Code repository | TODO public URL | Current work is local release-candidate branch. | no | yes | Public repository/release URL |
| Software code languages, tools, and services used | Python; JSON; local CLI validator | Stable enough for draft. | yes | yes | `pyproject.toml`, adapter docs, tests |
| Compilation requirements, operating environments, and dependencies | Python 3.11+; `click`, `jsonschema`, `pydantic`; `pytest` | Final OS wording not confirmed. | no | yes | `pyproject.toml`, final release README |
| Developer documentation/manual | Local docs under `papers/opentelemetry-to-eeoap/` | Public doc URL missing. | no | yes | Final public documentation path |
| Support email | TODO | Public support contact not confirmed. | no | yes | Final submission metadata |
| Release tag | TODO | OpenTelemetry-to-EEOAP package tag not created or pushed. | no | yes | Final local/public tag decision |
| DOI | TODO | DOI not created and may not be chosen. | no | yes if archive route is chosen | Zenodo or equivalent archive metadata |
| Local metadata drafts | `softwarex_metadata_drafts_v1_8/` | Draft only, not final release metadata. | yes as draft support | yes as final metadata | Final CFF/CodeMeta files |
| Related EEOAP artifact | Local tag `eeoap-v0.1-artifact`, not pushed | Public reference missing. | no | yes | Pushed tag, release, DOI, or immutable commit |
| Related AEP artifact | Local tag `aep-v0.1-artifact`, not pushed | Public reference missing. | no | yes | Pushed tag, release, DOI, or immutable commit |

## Template-Conversion Rule

During official template conversion, keep unresolved public-release fields as
explicit TODOs. Do not invent version numbers, DOI values, release URLs, pushed
tag URLs, or public archive links.
