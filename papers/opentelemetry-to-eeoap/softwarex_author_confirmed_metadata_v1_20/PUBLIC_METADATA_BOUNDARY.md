# Public Metadata Boundary

## Allowed Public Metadata

The following fields can be used in later SoftwareX metadata, manuscript,
support-package, CFF, and CodeMeta update drafts:

- Name: `Bin Zhang / 张斌`
- ORCID: `https://orcid.org/0009-0002-8861-1481`
- Affiliation: `Independent Researcher, China`
- Corresponding author email: `joy7759@gmail.com`
- Support contact preference: GitHub Issues
- Funding statement: this research received no specific grant from any funding
  agency in the public, commercial, or not-for-profit sectors.
- Country: China
- License: Apache-2.0
- Keywords: OpenTelemetry; EEOAP; agent telemetry; operation accountability;
  execution evidence; validation; reproducibility

Use GitHub Issues as the preferred support mechanism unless the author later
confirms a dedicated support email.

## Not Allowed In Public Metadata

The following must not be added to public metadata, manuscript files, CFF,
CodeMeta JSON, README, support contact fields, SoftwareX files, or release
artifacts:

- Private phone numbers.
- Home address.
- Unrelated private identifiers.
- Private production telemetry.
- Patient data.
- Human subject data.
- Any personal data not explicitly approved by the author for public release.

## Still TODO

- Final conflict of interest statement.
- Acknowledgements.
- Final support URL after repository/release strategy is fixed.
- Public release URL.
- DOI.
- Final release version.
- Final public artifact availability wording.

## Rule For Uncertain Fields

If a value is uncertain, keep it as TODO. Do not infer affiliation, funding,
conflicts, acknowledgements, or private-contact details from surrounding
repository context.
