# Privacy and Public Metadata Boundary

## Allowed If Author Confirms

- Name.
- ORCID.
- Affiliation.
- Professional email.
- Project support contact.
- Repository issue tracker or project support URL.

## Not Allowed

- Phone number.
- Home address.
- Unrelated private identifiers.
- Private production telemetry.
- Patient data.
- Human subject data.
- Private operational logs.

## Rules

- Use TODO if uncertain.
- Do not infer affiliation from location.
- Do not scrape personal data from outside sources.
- Do not copy private contact data into public metadata without explicit author
  confirmation.
- Final public metadata must be author-approved.

## Current Boundary Decision

The root repository metadata contains contact and affiliation information for
the AEP-Media release line. Version 1.19 does not treat those fields as final
OpenTelemetry-to-EEOAP metadata. They remain author-confirmation inputs only.
