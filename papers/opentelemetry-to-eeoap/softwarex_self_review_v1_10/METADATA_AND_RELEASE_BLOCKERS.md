# Metadata and Release Blockers

| Blocker | Current status | Severity | Needed before template conversion? | Needed before formal submission? | Recommended action |
|---|---|---|---|---|---|
| Root `CITATION.cff` mismatch | Describes AEP-Media, not OpenTelemetry-to-EEOAP. | blocker | no | yes | Do not edit yet; decide release scope first. |
| Root `codemeta.json` mismatch | Describes AEP-Media, not OpenTelemetry-to-EEOAP. | blocker | no | yes | Do not edit yet; decide release scope first. |
| Local metadata drafts only | v1.8 drafts exist under paper directory. | important | no | yes | Convert to final release metadata later. |
| CFF YAML not validated | PyYAML missing in v1.8. | important | no | yes | Run parser-backed CFF/YAML validation before release. |
| No pushed tags | EEOAP/AEP tags are local only; no OpenTelemetry-to-EEOAP release tag. | blocker | no | yes | Decide and push only after release strategy. |
| No DOI | No DOI for this package. | blocker | no | yes if DOI route chosen | Create only after public release payload is frozen. |
| No GitHub Release | No public release for this package. | blocker | no | yes | Create only after clean release candidate is ready. |
| No final release tag | Package-specific tag not created. | blocker | no | yes | Define tag after metadata and release scope. |
| Source layout issue | Adapter is under `tools/`, not `repo/src`. | important | maybe | yes or editorial clarification | Decide whether to explain, package, or restructure later. |
| SoftwareX metadata table TODOs | Present in v1.9. | important | yes | yes | Resolve or clearly mark before template conversion. |
| Final references | EEOAP/AEP public references unresolved. | blocker | no | yes | Replace local placeholders with stable references. |
| Declarations | Draft only. | important | yes | yes | Adapt to venue policy. |
| Data availability | Draft only. | important | yes | yes | Update after release/archive decision. |
| Artifact availability | Draft only. | blocker | yes | yes | Align with actual public release state. |
