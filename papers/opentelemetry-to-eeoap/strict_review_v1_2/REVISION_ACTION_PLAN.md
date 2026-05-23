# Revision Action Plan

## Must fix before any formal submission

- Create stable public identifiers for EEOAP-Artifact and AEP-Artifact, or
  remove/replace unstable references.
- Finalize references and remove submission-stage TODOs.
- Prepare a final artifact availability statement.
- Decide route before formatting.
- Prepare venue-specific conflict and AI-assisted writing disclosure.

## Should fix before journal submission

- Add one real framework-derived fixture if pursuing JSS/IST.
- Add a comparison baseline showing telemetry-only versus EEOAP validation.
- Formalize the failure taxonomy.
- Add a concise algorithm or method summary.
- Re-run clean-clone verification for the final package.
- Strengthen related work around provenance, observability, and artifact
  evaluation.

## Optional / defer

- OpenTelemetry Collector integration.
- Third synthetic valid trace.
- Broad cross-framework evaluation.
- User or reviewer study.
- Full-repository Ruff cleanup outside the adapter scope.

## One-week revision plan

Day 1: Decide route: SoftwareX/artifact by default, JSS/IST only if willing to
add a real runtime fixture.

Day 2: Create stable artifact identifiers or an immutable local tag plan for
EEOAP/AEP references.

Day 3: Draft a SoftwareX-oriented version or, if continuing JSS/IST, design one
LangChain-derived fixture without changing the EEOAP schema.

Day 4: Finalize references, artifact availability wording, and disclosure
notes.

Day 5: Re-run scoped tests, validator checks, clean-clone verification, and
prepare a route-specific review package.
