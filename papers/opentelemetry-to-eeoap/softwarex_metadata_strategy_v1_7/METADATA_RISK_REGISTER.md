# Metadata Risk Register

| Risk | Severity | Likelihood | Mitigation | Next action |
|---|---|---|---|---|
| Root metadata conflicts with AEP-Media | high | high | Do not edit root metadata until release scope is fixed. | Create OpenTelemetry-to-EEOAP-specific draft metadata under `papers/opentelemetry-to-eeoap/`. |
| Premature root metadata overwrite | high | medium | Keep root `CITATION.cff` and `codemeta.json` unchanged during strategy and draft phases. | Require explicit release-scope decision before root edits. |
| Local tags are not public | high | high | Treat local tags as internal anchors only. | Decide tag push/archive strategy later. |
| No DOI | high | high | Do not invent DOI. | Decide archive strategy after final release payload exists. |
| Release URL not available | high | high | Avoid final citation claims until public release exists. | Prepare placeholder-free metadata only after release candidate tag is fixed. |
| SoftwareX final metadata mismatch | high | medium | Keep article, metadata, release tag, and availability statement aligned. | Build metadata checklist before article compression. |
| Repository contains multiple paper lines | medium | high | Scope OpenTelemetry-to-EEOAP metadata locally. | Avoid broad root claims until repository release policy is settled. |
| Source layout issue | medium | medium | Document current `tools/`, `agent_evidence/`, examples, tests, and generated output layout. | Decide whether to explain layout or prepare a release package later. |
| Generated artifacts included in repo | medium | medium | State which generated files are part of reproducibility evidence. | Include generated statements in artifact availability note. |
| AI-assisted writing disclosure not final | medium | medium | Keep disclosure as a final submission blocker. | Draft venue-specific disclosure before submission. |
