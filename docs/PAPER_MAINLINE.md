# Paper Mainline

This document states the current paper-facing mainline for `agent-evidence`.

## Mainline

The current mainline is:

`operation accountability statement -> Execution Evidence and Operation Accountability Profile v0.1 -> profile-aware validator -> controlled examples -> metadata-enrichment demo -> review package`

The mainline exists to make a small execution-evidence claim independently
checkable. It should make the paper-facing core smaller and easier to review,
not broader.

## Allowed Work

Allowed changes for this mainline:

- clarify the `Execution Evidence and Operation Accountability Profile v0.1`
  boundary
- keep the validator path stable and documented
- maintain `agent-evidence validate-profile`
- maintain the paper-minimal examples
- maintain the metadata-enrichment demo
- maintain a clean rerun script
- maintain a review package that includes the profile, schema, examples,
  validator entrypoint, demo, rerun result, and claim boundary
- improve paper-facing terminology without changing validator behavior

## Deferred Work

Deferred work for this mainline:

- AEP-Media
- AI Act
- Sovereign-pFDO
- new runtime integration
- Automaton expansion
- LangChain expansion
- OpenAI Agents expansion
- broad governance-platform framing
- full-repository restructuring
- production deployment packaging

These materials may remain in the repository as historical or adjacent research
surfaces. They should not be presented as part of the current paper-minimal
claim.

## Active Boundary

The active boundary is artifact-bounded:

- 1 valid example
- 3 controlled invalid examples
- 1 metadata-enrichment demo
- 1 profile-aware validator path
- 1 reproducible rerun surface

The paper-facing path does not depend on full repository test success,
framework-specific integration tests, AEP-Media tests, or external services.

## Stop Conditions

Stop and re-check the boundary before doing any of the following:

- adding a new claim family
- adding a new runtime integration to the paper path
- adding a new venue-specific submission package
- presenting adjacent materials as paper-minimal evidence
- changing validator behavior instead of documenting the current behavior
- claiming production readiness, compliance approval, legal non-repudiation, or
  official FDO adoption

## Current First Rerun

Use:

```bash
bash scripts/reproduce_paper_minimal.sh
```

The script writes machine-readable rerun evidence under:

```text
artifacts/paper-minimal-rerun/
```
