# Submission Checklist

## Paper Files

- `papers/opentelemetry-to-eeoap/paper_v0_3.md`
- `papers/opentelemetry-to-eeoap/claim_boundary.md`
- `papers/opentelemetry-to-eeoap/evaluation_summary.md`
- `papers/opentelemetry-to-eeoap/reviewer_positioning.md`
- `papers/opentelemetry-to-eeoap/reference_todo.md`

## Artifact Files

- `tools/opentelemetry_to_eeoap_adapter.py`
- `tests/test_opentelemetry_to_eeoap_adapter.py`
- `examples/opentelemetry/valid-agent-trace.json`
- `examples/opentelemetry/invalid-missing-agent-span.json`
- `examples/opentelemetry/invalid-unresolved-tool-span.json`
- `examples/opentelemetry/invalid-broken-parent-span.json`
- `examples/opentelemetry/invalid-missing-operation-name.json`
- `generated/valid-agent-trace-eeoap-statement.json`
- `generated/valid-agent-trace-adapter-report.json`
- `docs/opentelemetry-to-eeoap-evaluation.md`
- `docs/opentelemetry-to-eeoap-paper-claim.md`
- `docs/opentelemetry-to-eeoap-reviewer-notes.md`

## Commands to Reproduce

```bash
git checkout opentelemetry-to-eeoap-adapter

.venv/bin/python tools/opentelemetry_to_eeoap_adapter.py \
  examples/opentelemetry/valid-agent-trace.json

.venv/bin/agent-evidence validate-profile \
  generated/valid-agent-trace-eeoap-statement.json

.venv/bin/python -m pytest tests/test_opentelemetry_to_eeoap_adapter.py -q
```

Optional full repository context check:

```bash
.venv/bin/python -m pytest
```

## Tests

- Scoped adapter tests: `pytest tests/test_opentelemetry_to_eeoap_adapter.py -q`
- Expected scoped result: `6 passed`
- Observed v0.3 scoped result: `6 passed in 1.51s`
- Existing evidence closure full pytest result:
  `164 passed, 1 skipped, 15 warnings in 35.38s`
- Existing EEOAP validator result for generated statement:
  `ok=true`, `issue_count=0`

## Known Limitations

- The fixture set is local and intentionally small.
- The adapter does not prove legal accountability.
- The adapter does not reconstruct the full runtime environment.
- The adapter does not claim broad OpenTelemetry implementation compatibility.
- The adapter does not claim cross-framework generality.
- The adapter does not prove agent-output correctness.
- The adapter does not define a new EEOAP profile.
- Full repository Ruff was not rerun for v0.3 because unrelated pre-existing
  lint debt remains in out-of-scope directories such as `pd-oap/` and
  SoftwareX-related paper-support trees.

## Items Still Missing Before External Submission

- Replace citation placeholders with verified bibliographic entries.
- Verify OpenTelemetry GenAI and agent-span documentation against official
  current pages immediately before submission.
- Verify JSON Schema 2020-12, W3C PROV, and ACM artifact badging references
  against official sources.
- Decide target venue and adapt length, formatting, and artifact checklist.
- Add final bibliography in the venue-required format.
- Decide whether to include a public artifact archive or DOI after venue choice.
- Re-run the scoped adapter tests and generated-statement validator check on
  the final submission commit.
- Decide how to disclose repository-wide Ruff debt in the final artifact
  appendix or limitations section.
