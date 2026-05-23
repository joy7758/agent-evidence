# Remaining Blockers

| Blocker | Severity | Status after v1.11 | Action required |
|---|---|---|---|
| Public release strategy | blocker | Not decided. | Decide main repo release, focused subpackage release, or supplemental package release. |
| Root metadata mismatch | blocker | Root `CITATION.cff` and `codemeta.json` still describe AEP-Media. | Decide whether/when to adjust root or release metadata. |
| Local metadata drafts not final | important | v1.8 drafts exist only locally. | Convert to final release metadata after release scope. |
| CFF YAML validation skipped | important | PyYAML unavailable in v1.8. | Run parser-backed CFF/YAML validation before release. |
| Tags not pushed | blocker | Local EEOAP/AEP tags only; no package release tag. | Push only after release strategy. |
| DOI not created | blocker | No DOI for this package. | Create only after release payload is frozen, if DOI route is chosen. |
| GitHub Release not created | blocker | No GitHub Release for this package. | Create only after release candidate passes checks. |
| SoftwareX official template not applied | important | Draft remains Markdown. | Apply template after blocker plan. |
| Metadata table TODOs | important | TODOs remain. | Fill after release metadata decisions. |
| No `repo/src` layout | important | Adapter remains under `tools/`. | Decide whether to explain, package, or restructure later. |
| v0.5 frozen package predates v0.7 second trace | important | Frozen package does not include second-trace expansion. | Refresh final support package before release. |
| Final references | blocker | EEOAP/AEP artifact references unresolved. | Replace with stable public identifiers. |
| Declarations final wording | important | Draft declarations only. | Adapt to target venue policy. |
| Final clean-clone check | important | Existing clean-clone evidence predates final release package. | Rerun after release candidate is frozen. |
