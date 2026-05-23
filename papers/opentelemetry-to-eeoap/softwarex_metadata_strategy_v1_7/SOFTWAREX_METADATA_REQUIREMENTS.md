# SoftwareX Metadata Requirements

| Metadata requirement | Planned source | Current status | Action needed | Risk |
|---|---|---|---|---|
| Software title | Future `CITATION_OTEL_EEOAP.cff`; `SOFTWARE_METADATA.md` | missing for OpenTelemetry-to-EEOAP | Draft a bounded title naming the adapter package. | Medium: title may overstate scope. |
| Version | Future metadata draft and release strategy | missing | Choose a provisional version or release-candidate label. | Medium: no public release tag yet. |
| Authors | Future metadata draft | partial | Reuse verified authorship only after final approval. | Low to medium: avoid private/unwanted fields. |
| ORCID | Future metadata draft | partial | Use only if intended for public release. | Low. |
| Repository URL | Future metadata draft | partial | Use repository URL only when public release strategy is fixed. | Medium: release URL not available yet. |
| Release tag | Future release strategy | missing | Create only after metadata and release scope are fixed. | High: premature tag can misidentify object. |
| License | Root `LICENSE`; future metadata draft | ready | Reference repository Apache-2.0 license. | Low. |
| Keywords | Future metadata draft | missing | Draft OpenTelemetry-to-EEOAP-specific keywords. | Low. |
| Programming language | `pyproject.toml`; future metadata draft | ready | Record Python. | Low. |
| Dependencies | `pyproject.toml`; future metadata draft | ready at package level | Identify adapter-relevant runtime/dev dependencies. | Medium: dev dependencies exceed minimal adapter needs. |
| Operating system | Future metadata draft | missing | Mark tested local environment conservatively. | Medium: avoid broad OS compatibility claim. |
| Documentation | `papers/opentelemetry-to-eeoap/`; future `SOFTWARE_METADATA.md` | partial | Point to adapter docs, frozen package, SoftwareX route docs. | Low. |
| Tests | `tests/test_opentelemetry_to_eeoap_adapter.py` | ready | Record scoped adapter test command and latest result. | Low. |
| Examples | `examples/opentelemetry/` | ready | Record two valid and four invalid fixtures. | Low. |
| Citation | Future `CITATION_OTEL_EEOAP.cff` | missing | Create local draft before root metadata decisions. | High if root AEP-Media citation is reused. |
| Related artifacts: EEOAP and AEP | Local tags and future availability note | partial | Record local tags, push/archive only after release decision. | Medium to high: local tags are not public. |
| Artifact availability statement | Future `ARTIFACT_AVAILABILITY.md` | partial | Draft current availability and final release requirements. | High before submission. |
| Data availability statement | Future SoftwareX article/declarations | missing | State local fixtures/generated outputs and public release status. | Medium. |
| Generative AI disclosure | Future SoftwareX declarations | missing | Draft venue-specific disclosure later. | Medium. |
| Conflict of interest | Future SoftwareX declarations | missing | Draft final statement before submission. | Low. |
| Funding | Future SoftwareX declarations | missing | Draft final statement before submission. | Low. |
