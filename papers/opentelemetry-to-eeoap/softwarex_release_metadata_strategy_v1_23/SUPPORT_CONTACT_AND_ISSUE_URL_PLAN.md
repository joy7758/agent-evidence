# Support Contact And Issue URL Plan

## Current Support Contact Strategy

The author-confirmed support contact strategy is GitHub Issues.

## Current Issue URL Status

The final issue URL is TODO until the public repository or release URL is
finalized.

## Options

### Repository Issue Tracker URL

Use the public repository issue tracker as the support route.

Advantages:

- Standard for open-source software.
- Public, auditable, and tied to the repository.
- Avoids exposing private phone numbers or home addresses.

Risks:

- Requires the public repository/release route to be final.
- If the repository has multiple project lines, issue labels/templates may be
  needed for scope clarity.

### Release-Specific Issue Template

Create or reference an issue template dedicated to the OpenTelemetry-to-EEOAP
SoftwareX package.

Advantages:

- Helps route support questions.
- Reduces ambiguity in a multi-line repository.

Risks:

- Requires repository configuration changes later.
- Should not be done before release scope is decided.

### Dedicated Support Email

Use a dedicated project support email.

Advantages:

- Fits SoftwareX table wording if an email is strictly required.

Risks:

- Requires creating and maintaining the address.
- Less transparent than public issue tracking.

## Privacy Note

No phone number and no home address should be used for support metadata.

## Recommendation

Use the repository issue tracker URL after the public release route is fixed.
If the venue requires an email-only field, make a separate author-approved
decision later. Do not introduce a private contact route in this plan.

## Fields To Update Later

- CodeMeta `issueTracker`.
- CFF or human-readable metadata support/contact note if used.
- SoftwareX metadata table support contact field.
- Artifact availability and documentation/manual support note.
