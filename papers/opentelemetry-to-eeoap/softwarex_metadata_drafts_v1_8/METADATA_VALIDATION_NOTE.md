# Metadata Validation Note

## Draft Paths

- CFF draft:
  `papers/opentelemetry-to-eeoap/softwarex_metadata_drafts_v1_8/CITATION_OTEL_EEOAP.cff`
- CodeMeta JSON draft:
  `papers/opentelemetry-to-eeoap/softwarex_metadata_drafts_v1_8/codemeta-otel-eeoap.json`

## JSON Validation

CodeMeta JSON parsed successfully:

```bash
python -m json.tool papers/opentelemetry-to-eeoap/softwarex_metadata_drafts_v1_8/codemeta-otel-eeoap.json > /tmp/codemeta-otel-eeoap.validated.json
```

## CFF YAML Validation

PyYAML was not available in the active Python environment, so YAML parsing was
skipped:

```text
YAML validation skipped: No module named 'yaml'
```

The CFF file is intentionally simple YAML, but it remains a local draft until a
full CFF/schema check is run before release.

## Known TODO Fields

- Release version.
- Release date.
- Public repository release URL.
- Project or release URL.
- DOI or archive identifier.
- Final public affiliation and contact metadata.
- Final operating system support statement.
- Final issue tracker URL.
- Final artifact availability statement.
- Final data availability statement.
- Final venue-specific declarations.

## Conclusion

These local metadata drafts are strategy and preparation material only. They are
not final release metadata and do not claim a public release, DOI, pushed tag,
or GitHub Release. CodeMeta JSON syntax is valid; CFF YAML syntax still needs a
parser-backed check when PyYAML or another YAML validator is available.
