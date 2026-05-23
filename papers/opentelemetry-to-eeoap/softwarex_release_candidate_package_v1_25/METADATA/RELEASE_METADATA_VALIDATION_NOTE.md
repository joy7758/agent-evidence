# Release Metadata Validation Note

Purpose: record syntax validation and unresolved fields for the version 1.24
package-local release metadata drafts.

## Draft Paths

- CFF draft:
  `papers/opentelemetry-to-eeoap/softwarex_package_local_release_metadata_v1_24/CITATION_OTEL_EEOAP_RELEASE_DRAFT.cff`
- CodeMeta JSON draft:
  `papers/opentelemetry-to-eeoap/softwarex_package_local_release_metadata_v1_24/codemeta-otel-eeoap-release-draft.json`

## CodeMeta JSON Validation

Command:

```bash
python -m json.tool papers/opentelemetry-to-eeoap/softwarex_package_local_release_metadata_v1_24/codemeta-otel-eeoap-release-draft.json > /tmp/codemeta-otel-eeoap-release-draft.validated.json
```

Result: passed. The JSON parsed successfully.

## CFF YAML Validation

Command:

```bash
python - <<'PY'
from pathlib import Path
try:
    import yaml
except Exception as exc:
    print(f"CFF YAML validation skipped: {exc}")
    raise SystemExit(0)

path = Path("papers/opentelemetry-to-eeoap/softwarex_package_local_release_metadata_v1_24/CITATION_OTEL_EEOAP_RELEASE_DRAFT.cff")
with path.open("r", encoding="utf-8") as f:
    yaml.safe_load(f)
print("CFF YAML validation passed")
PY
```

Result: skipped. Reason: `No module named 'yaml'`.

No dependency was installed for this task.

## Unresolved TODO Fields

- final release version
- final release date
- final public repository or release URL
- final GitHub Issues URL
- final GitHub Release URL
- final Zenodo DOI URL, if DOI is created
- final public archive reference
- final release notes URL or text
- final pushed tag status

## Conclusion

The CodeMeta JSON draft is syntactically checked. The CFF draft remains a
package-local YAML/CFF draft with YAML validation skipped because PyYAML is not
available. These files are not final public release metadata and do not claim a
DOI, GitHub Release, pushed tag, or public archive.
