# Package-Local Metadata Files Plan

| Target file | Purpose | Current source | Fields to update | Requires release URL? | Requires DOI? | Can be drafted before release? |
|---|---|---|---|---:|---:|---:|
| `papers/opentelemetry-to-eeoap/CITATION_OTEL_EEOAP.cff` | Package-local CFF metadata for OpenTelemetry-to-EEOAP | v1.8 `CITATION_OTEL_EEOAP.cff` | author affiliation, email if appropriate, version, release date, repository URL, release URL, DOI if created, keywords | yes | only if DOI route selected | yes, with TODO values |
| `papers/opentelemetry-to-eeoap/codemeta-otel-eeoap.json` | Package-local CodeMeta JSON | v1.8 `codemeta-otel-eeoap.json` | author affiliation, issue tracker, repository URL, version, dates, related links, DOI identifier if created | yes | only if DOI route selected | yes, with TODO values |
| `papers/opentelemetry-to-eeoap/SOFTWARE_METADATA.md` | Human-readable software metadata | v1.8 `SOFTWARE_METADATA.md` and v1.20 confirmed metadata | final version, support URL, release URL, release tag, DOI status, declarations | yes | only if DOI route selected | yes |
| `papers/opentelemetry-to-eeoap/ARTIFACT_AVAILABILITY.md` | Public artifact availability statement | v1.8 artifact availability draft and v1.15 support package status | release URL, tag, DOI, support package path, checksum status | yes | only if DOI route selected | yes, with TODO values |
| Support package `METADATA/` copies | Submission support metadata snapshot | v1.15 support package `METADATA/` | copy final package-local metadata after updates | yes | only if DOI route selected | no; update after source metadata drafts |
| SoftwareX template metadata table | Manuscript metadata table | v1.22 declaration-finalized manuscript | version, permanent link, repository, support issue URL, release URL, DOI | yes | only if DOI route selected | yes, with TODO values |
| Final references file | Reference source for manuscript and template | v1.17 references and v1.22 TODO list | release URL, tag, DOI/archive, exact artifact references | yes | only if DOI route selected | partial only |

## Notes

- Version 1.23 does not create or update these target files.
- Version 1.24 should create package-local release metadata drafts using the
  confirmed author metadata and provisional tag naming.
