# Commercial Delivery Surface

Status: internal hardening only.

This file defines the narrow delivery surface used for Stage 1 clean-clone
hardening checks. It does not mark `agent-evidence` as commercial-ready,
production-ready, externally validated, certified, standardized, legally
compliant, submitted, accepted, or published.

## Purpose

The delivery surface gives coding agents and reviewers a machine-checkable
boundary for the files that may be treated as the minimal EEOAP evidence-gate
implementation during internal hardening.

The machine-readable source is:

- `packaging/commercial-delivery-surface.json`

The local checker is:

- `scripts/check_delivery_surface.py`

## Included Surface

The included surface is limited to:

- package metadata and source code needed to install and run the validator;
- agent-readable entry points such as `AGENTS.md` and `llms.txt`;
- EEOAP protocol metadata and protocol documentation;
- minimal examples and the operation-accountability demo path;
- EEOAP evidence-gate workflow, PR template, and repo-local skill material;
- Stage 1 support documentation for error codes, troubleshooting, and support
  boundaries;
- Stage 1 workflow permission, advisory/enforce mode, and workflow-hardening
  summary documentation;
- validation support files used by package-level checker, validator, and
  negative-control tests;
- focused tests for the citation checker, CLI, delivery-surface checker, and
  release metadata consistency.
- release metadata files read by the focused metadata consistency test.

## Stage 1 Support Documents

The Stage 1 support documents are part of the delivery surface because they
define how a user or coding agent should interpret local failures without
expanding the project scope:

- `docs/ERROR_CODES.md`
- `docs/TROUBLESHOOTING.md`
- `docs/SUPPORT_BOUNDARY.md`

These files do not add protocol clauses, change validator behavior, or claim
commercial readiness. They only make the existing internal hardening surface
easier to inspect and support.

## Validation Support Files

The delivery surface includes validation support files needed for package-level
checks:

- workflow permission review documentation;
- advisory/enforce mode documentation;
- Stage 1 workflow hardening summary documentation;
- validator schema files;
- invalid examples used as negative controls;
- exact spec files required by the protocol citation checker.
- release metadata consistency tests required by RC package validation.
- release metadata inputs read by the metadata consistency test, including
  citation metadata, generated agent metadata, project facts, release notes,
  release readiness notes, and release checklist documentation.

These files are included only so an unpacked package can run the existing local
checkers, validator, and focused tests. Paper, submission, manuscript, media,
route, and portal-upload materials remain excluded.

Including validation support files does not make the project commercial-ready or
production-ready. It also does not create external validation, certification,
standardization, legal compliance, publication, tag, release, or package
publication.

## Excluded Surface

The delivery surface excludes paper, submission, manuscript, media, route,
generated package, build, archive, document-export, and generated artifact
paths.

Examples of excluded paths include:

- `paper/`
- `papers/`
- `submission/`
- `submissions/`
- `manuscript/`
- `manuscripts/`
- `media/`
- `route/`
- `routes/`
- `artifacts/`
- `dist/`
- `build/`
- `*.docx`
- `*.pdf`
- `*.zip`

These files may remain in the repository for research-history or governance
reasons, but they are not part of the commercial delivery surface.

## Non-Claims

This delivery-surface definition does not claim:

- commercial readiness;
- production readiness;
- external validation;
- certification;
- standardization;
- legal compliance;
- submission, acceptance, or publication.

It is only an internal hardening boundary for clean-clone checks and future
review of what should be packaged as the minimal EEOAP evidence-gate surface.
