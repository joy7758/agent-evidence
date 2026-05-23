# Claim Evidence Audit

| Claim | Evidence cited or available | Support level | Reviewer risk | Required fix |
|---|---|---|---|---|
| Telemetry is not automatically portable operation evidence. | v1.0 problem section and comparison table. | bounded | Conceptual claim may need stronger support from related work. | Add tighter references or framing in final paper. |
| Adapter transforms OpenTelemetry-style traces to EEOAP-compatible statements. | Adapter code, two valid fixtures, generated statements, tests. | strong | Only local OpenTelemetry-style fixtures are covered. | Keep "OpenTelemetry-style" wording. |
| Adapter preserves trace/span provenance. | Generated statements, adapter reports, tests checking span artifacts. | strong | Provenance semantics are local, not a full PROV mapping. | Avoid claiming general provenance compliance. |
| Adapter resolves tool spans. | Tests for direct-child and workflow-child tool spans. | strong | Only two ancestry patterns are tested. | Add more patterns if journal route continues. |
| Adapter checks parent-child relationships. | Broken-parent invalid fixture and tests. | strong | The check is structural, not semantic. | Phrase as structural parent-link validation. |
| Adapter is more than field copying. | Method section, tests, diagnostics, validator routing. | bounded | Skeptical reviewers may still see it as a converter. | Add baseline comparison and algorithmic summary. |
| Two valid traces pass. | v0.7 command log, v1.0 evaluation, scoped tests. | strong | The number remains small. | Do not inflate beyond controlled contexts. |
| Four invalid traces expose diagnostics. | Invalid fixtures and tests. | strong | Diagnostics are selected by authors; not exhaustive. | Present as bounded diagnostic surface. |
| Existing EEOAP validator accepts generated statements. | Validator results `ok=true`, `issue_count=0`. | strong | Depends on existing EEOAP validator credibility. | Cite or archive EEOAP validator artifact. |
| No EEOAP schema change required. | Commit history and v1.0 statements. | strong | Reviewer may ask if schema was simply flexible enough. | Explain schema-safe mapping locations. |
| Clean-clone verification supports reproducibility. | v0.5 clean-clone note and checksums. | bounded | It predates v1.0/v1.1 packet and is not a final package verification. | Re-run clean-clone verification before final submission. |
| This is software engineering research. | Method framing and validator-aware transformation. | weak | Current evidence may be seen as tool engineering, not research. | Add real runtime fixture or stronger method comparison for JSS/IST. |
| Journal route is plausible. | v0.9 route assessment and v1.0 manuscript. | weak | Plausible does not mean ready; JSS/IST bar is higher. | Treat journal route as conditional on revision. |
| Broad OpenTelemetry compatibility is not claimed. | Abstract, threats, conclusion, v0.9 citation audit. | strong | Title may still imply broad compatibility. | Keep non-claim explicit and possibly adjust title for final route. |
