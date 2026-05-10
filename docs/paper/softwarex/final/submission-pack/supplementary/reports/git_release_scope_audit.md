# AEP-Media Git Release Scope Audit

Date: 2026-05-10

## Intended Release Scope

The proposed `aep-media-v0.1.0` release should include the repository snapshot containing:

- AEP-Media source modules under `agent_evidence/`
- adapter modules under `agent_evidence/adapters/`
- AEP-Media CLI registrations in `agent_evidence/cli/main.py`
- AEP-Media specs under `spec/`
- AEP-Media schemas under `schema/`
- examples and fixtures under `examples/media/`
- media demos under `demo/`
- AEP-Media tests under `tests/`
- AEP-Media reports under `docs/reports/`
- SoftwareX materials under `docs/paper/softwarex/`
- `README.md`
- `LICENSE`
- `CITATION.cff`
- `.zenodo.json`
- `codemeta.json`
- `docs/how-to-cite.md`
- `pyproject.toml`

## Explicitly Excluded

Do not include unrelated or local-only material in release staging:

- virtual environments;
- bytecode caches;
- local temporary outputs;
- old journal staging packs;
- unrelated paper workspaces;
- unrelated archive-only full staging packs.

## Working Tree Note

The repository currently contains a broad dirty/untracked working tree from prior AEP-Media missions. If release publication is later requested, do not blindly stage all files. Stage only the intended AEP-Media/SoftwareX/readiness files and verify exclusions before tagging.

## Related Untracked Directory

An unrelated untracked paper-workspace directory is visible in `git status`. It is explicitly excluded from AEP-Media release staging and must not be staged, copied into release candidate archives, or referenced as part of the SoftwareX package.

## Release Safety Result

Release publication status: blocked by publish guard.

Release candidate preparation status: allowed.
