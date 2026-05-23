# SoftwareX Metadata Update Plan

Purpose: plan later metadata updates using the version 1.20 confirmed public
metadata. This file does not edit any target metadata or manuscript file.

| Target field | Current v1.20 value | Target file to update later | Update timing | Still TODO? | Notes |
|---|---|---|---|---:|---|
| Manuscript author name | Bin Zhang / 张斌 | `papers/opentelemetry-to-eeoap/softwarex_template_file_conversion_v1_17/MANUSCRIPT/softwarex_template_file_draft_v1_17.md`; future official SoftwareX LaTeX template file | Version 1.21 metadata update draft | no | Keep English name for citation systems and include Chinese name only if the venue accepts it. |
| ORCID | `https://orcid.org/0009-0002-8861-1481` | v1.17 manuscript draft; future CFF metadata draft; future CodeMeta JSON draft | Version 1.21 metadata update draft | no | Already present in local metadata drafts. |
| Affiliation | Independent Researcher, China | v1.17 manuscript draft; future official SoftwareX LaTeX template file; future CFF and CodeMeta drafts | Version 1.21 metadata update draft | no | Replace affiliation TODO in manuscript/template drafts. |
| Corresponding author email | `joy7759@gmail.com` | v1.17 manuscript draft; future official SoftwareX LaTeX template file; future CFF and CodeMeta drafts | Version 1.21 metadata update draft | no | Use only as corresponding author email. Do not use a private phone number. |
| Support contact | GitHub Issues | v1.17 manuscript metadata table; future support package metadata; future official SoftwareX LaTeX template file | Version 1.21 metadata update draft, then final release metadata pass | partially | Final public issue URL depends on release/repository strategy. |
| Funding statement | This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors. | v1.17 manuscript declaration section; future official SoftwareX LaTeX template file; future declaration drafts | Version 1.21 metadata update draft | no | Replace funding TODO with confirmed statement. |
| Conflict of interest statement | TODO: author confirmation required | v1.17 manuscript declaration section; future official SoftwareX LaTeX template file; future declaration drafts | Wait for author confirmation | yes | Do not finalize from earlier draft without explicit author approval. |
| Acknowledgements | TODO: author confirmation required | v1.17 manuscript or final template if acknowledgements are needed | Wait for author confirmation | yes | Omit or fill only after author decision. |
| Public release URL | TODO | future release-candidate support package; future CFF metadata draft; future CodeMeta JSON draft; references | After release strategy and public release action | yes | Do not invent GitHub Release URL. |
| DOI | TODO | future CFF metadata draft; future CodeMeta JSON draft; manuscript metadata table; references | After DOI/archive action, if selected | yes | Do not invent DOI. |
| Software version | TODO; existing internal placeholder `otel-eeoap-adapter-v0.1.0-rc` | future release-candidate support package; future CFF metadata draft; future CodeMeta JSON draft | After release naming decision | yes | Keep placeholder until release version is approved. |
| License | Apache-2.0 | v1.17 manuscript metadata table; future support package; future CFF and CodeMeta drafts | Version 1.21 metadata update draft | no | Root `LICENSE` remains unchanged. |
| Keywords | OpenTelemetry; EEOAP; agent telemetry; operation accountability; execution evidence; validation; reproducibility | v1.17 manuscript draft; future CFF and CodeMeta drafts | Version 1.21 metadata update draft | no | Reconfirm during final template pass. |
| Local metadata drafts | Existing v1.8 drafts | `papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_15/METADATA/`; future release-candidate support package | After v1.21 template metadata draft and release metadata strategy | partially | Existing v1.15 package is not edited in v1.20. |
| Root `CITATION.cff` | Describes AEP-Media | root `CITATION.cff` only if a focused release branch decision authorizes it | Later release metadata stage only | yes | Do not overwrite blindly. |
| Root `codemeta.json` | Describes AEP-Media | root `codemeta.json` only if a focused release branch decision authorizes it | Later release metadata stage only | yes | Package-local metadata remains safer until route is decided. |

## Later Target Files

- `papers/opentelemetry-to-eeoap/softwarex_template_file_conversion_v1_17/MANUSCRIPT/softwarex_template_file_draft_v1_17.md`
- `papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_15/METADATA/`
- Future release-candidate support package.
- Future CFF metadata draft.
- Future CodeMeta JSON draft.
- Future official SoftwareX LaTeX template file.
- Root `CITATION.cff` only if a focused release branch decision is made later.
- Root `codemeta.json` only if a focused release branch decision is made later.
