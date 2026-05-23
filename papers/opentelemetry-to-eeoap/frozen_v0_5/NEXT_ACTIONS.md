# Next Actions

## A. Internal Archive Path

Priority: first.

- Keep `frozen_v0_5/` as the internal frozen paper package.
- Review package contents manually for internal consistency.
- Decide whether to create a local zip package after this commit.
- If packaging as a release candidate, rerun:
  `pytest tests/test_opentelemetry_to_eeoap_adapter.py -q`.
- Consider recording the final v0.5 commit hash in a follow-up archive note.
- Keep the package local until references and archive metadata are verified.

## B. External Submission Path

Priority: second.

- Choose a target venue only after internal review.
- Convert `paper_v0_4.md` or a later paper file to the target format.
- Replace citation placeholders with verified official references.
- Verify OpenTelemetry, JSON Schema, W3C PROV, ACM artifact guidance, EEOAP,
  and AEP citation metadata.
- Prepare an artifact appendix if required by the venue.
- Decide whether to archive through GitHub release, Zenodo DOI, or another
  repository after venue requirements are known.

## C. Deferred Engineering Path

Priority: last.

- Do not add a second runtime fixture until the frozen package has been
  reviewed.
- Defer LangChain, CrewAI, AutoGen, and OpenTelemetry Collector integration.
- Defer adapter feature expansion.
- Defer EEOAP schema changes.
- Defer full-repository lint cleanup unless it becomes a separate repository
  hygiene task.
