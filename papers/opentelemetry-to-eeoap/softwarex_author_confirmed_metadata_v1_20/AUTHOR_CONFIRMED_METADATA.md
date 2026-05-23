# Author-Confirmed Metadata

Purpose: record author-confirmed public metadata for later SoftwareX metadata,
template, support-package, CFF, and CodeMeta updates. This file does not execute
those updates.

| Field | Confirmed value | Public use allowed? | Target use | Notes |
|---|---|---:|---|---|
| Author name | Bin Zhang / 张斌 | yes | Manuscript author line; future CFF and CodeMeta drafts | Author-provided spelling. |
| ORCID | `https://orcid.org/0009-0002-8861-1481` | yes | Manuscript author information; future CFF and CodeMeta drafts | Already present in earlier metadata drafts and reconfirmed here. |
| Affiliation | Independent Researcher, China | yes | Manuscript affiliation; future CFF and CodeMeta drafts | Author states no institutional affiliation. |
| Corresponding author email | `joy7759@gmail.com` | yes | Corresponding author contact field | Author-provided for this route; final venue form should still be checked before submission. |
| Support contact | GitHub Issues | yes | Software support route; developer documentation/manual support field | Preferred over publishing a private phone number or unmanaged personal contact route. |
| Funding statement | This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors. | yes | Funding declaration | Author-confirmed no-funding statement. |
| Conflict of interest statement | TODO: author confirmation required | TODO | Declaration of competing interest | Do not use the earlier draft as final until the author confirms it. |
| Acknowledgements | TODO: author confirmation required | TODO | Acknowledgements section, if any | Do not invent acknowledgements. |
| Phone number | Excluded from public metadata; value intentionally not recorded | no | None | Do not include in manuscript, CFF, CodeMeta JSON, README, SoftwareX files, support fields, or public artifacts. |
| Country | China | yes | Affiliation/country context where needed | Use only as part of public affiliation or venue-required author metadata. |
| License | Apache-2.0 | yes | Software metadata table; future release metadata | Confirmed by root `LICENSE` and existing metadata drafts. |
| Keywords | OpenTelemetry; EEOAP; agent telemetry; operation accountability; execution evidence; validation; reproducibility | yes | Manuscript keywords; future metadata drafts | Same keyword set used in the version 1.19 collection. |

## Resolved From Version 1.19

- Affiliation can move from TODO to `Independent Researcher, China`.
- Corresponding author email can move from TODO to `joy7759@gmail.com`.
- Support contact strategy can move from TODO to `GitHub Issues`.
- Funding statement can move from TODO to the confirmed no-specific-grant
  statement above.
- ORCID remains confirmed.

## Still Unresolved

- Conflict of interest statement.
- Acknowledgements.
- Final public release URL.
- DOI.
- Final release version.
- Final support URL or issue-tracker URL after release strategy is fixed.
