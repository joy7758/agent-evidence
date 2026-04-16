# Repo Map Audit

Scope: `agent-evidence` only.

Method: filesystem scan, `README.md`, `pyproject.toml`, `.github/workflows/`, `docs/lineage.md`, and current directory contents. This audit classifies the repository into canonical core, active product surface, and history/frozen material. It does not propose cross-repo changes.

Current working assumption: the current primary implementation line is the `Execution Evidence and Operation Accountability Profile v0.1` path, while older `Execution Evidence Object` and legacy AEP surfaces remain in-repo for lineage and reproducibility.

## 1. Current top-level directory map

Operational directories such as `.git/`, `.venv/`, `.pytest_cache/`, and `.ruff_cache/` are excluded from the product map below.

| Path | Current role | Dominant class | Audit note |
| --- | --- | --- | --- |
| `.github/` | CI and repo automation | Active support surface | Mixed current CI and legacy prototype checks coexist here. |
| `agent_evidence/` | Installable Python package, CLI, validator, storage, library integrations | Canonical core | This is the main code surface. |
| `demo/` | Runnable single-path demo and generated artifacts | Active product surface | Fits the current minimal closed-loop story. |
| `docs/` | Product docs, status docs, lineage docs, EDC notes, outreach notes | Active product surface, mixed | Keep active, but treat some subtrees as frozen/reference only. |
| `examples/` | Valid/invalid evidence statements and runnable examples | Active product surface | Part of the current verification entry path. |
| `integrations/` | Framework-specific exporter demos | Active product surface | Useful developer surface, but should stay narrow. |
| `paper/` | Manuscript workspaces and flagship planning | Historical / paper / lineage | Important provenance, not primary product entry. |
| `plans/` | Implementation planning | Active support surface | Current execution-control surface for Phase A work. |
| `poster/` | Poster text and visual assets | Historical / outreach | Not part of the active product surface. |
| `proposal/` | Early proposal material | Historical / lineage | Background only. |
| `release/` | Release notes, outward positioning, frozen `v0.1-live-chain` package | Historical / frozen | Includes retained frozen package material. |
| `research/` | Research support notes and release materials | Historical / support | Supporting material, not a first-time developer path. |
| `roadmap/` | Roadmap and standardization notes | Historical / planning | Useful background, but not active product surface. |
| `schema/` | Canonical JSON schemas | Canonical core | Normative contract layer. |
| `scripts/` | Gates, verification helpers, historical prototype scripts | Mixed support surface | Highest confusion directory because current and legacy scripts share one path. |
| `speaking/` | Talk scripts and demo speaking notes | Historical / outreach | Not part of the product entry. |
| `spec/` | Canonical profile/spec documents | Canonical core | Holds both current and historical normative text. |
| `submission/` | Submission and handoff package materials | Historical / paper / release | Important for provenance, not for install/run entry. |
| `tests/` | Automated verification and regression tests | Canonical core | Protects current package behavior. |

## 2. Canonical core directories

The canonical core is the smallest set of directories that define what `agent-evidence` is as a package and what its current contract means.

- `agent_evidence/`
  - Main installable implementation surface.
  - Includes the CLI, validator, storage, bundle verification path, and library-side integrations.
- `spec/`
  - Normative profile/spec layer.
  - Current primary spec is `execution-evidence-operation-accountability-profile-v0.1.md`.
- `schema/`
  - Normative schema layer.
  - Current primary schema is `execution-evidence-operation-accountability-profile-v0.1.schema.json`.
- `tests/`
  - Regression guardrail for the canonical package.

Important note: these directories also contain retained historical files, especially `Execution Evidence Object` assets in `spec/` and `schema/`. They remain canonical for lineage, but they are not the current primary surface.

## 3. Active product surface directories

These directories are the ones a first-time developer or platform engineer should encounter after the canonical core.

- `demo/`
  - Current single-path demo and artifact output surface.
- `examples/`
  - Current valid/invalid examples and profile-facing specimen surface.
- `integrations/`
  - Runnable framework exporter demos.
  - Current priority should remain narrow: LangChain / LangGraph first, OpenAI-compatible second.
- `docs/`
  - Active only in a selective sense.
  - Current primary docs appear to be `docs/STATUS.md`, `docs/ACCEPTANCE-CHECKLIST.md`, `docs/high-risk-scenario-entry.md`, and `docs/cookbooks/`.
- `plans/`
  - Active coordination surface during the current tightening phase.
- `.github/`
  - Active support surface because CI and repo gates shape what is treated as live.

Important note: `docs/` is not a uniformly active product directory. It currently mixes active product docs with lineage and frozen-reference subtrees.

## 4. Historical / paper / lineage / frozen asset directories

These directories matter for provenance, publications, prior framing, and outward communication, but they should not read as the active implementation line.

- `paper/`
  - Manuscript workspaces, flagship planning, and submission assembly.
- `poster/`
  - Poster and figure production assets.
- `proposal/`
  - Early proposal framing.
- `release/`
  - Historical release-facing material, including frozen `v0.1-live-chain`.
- `research/`
  - Research support material.
- `roadmap/`
  - Standardization and future planning notes.
- `speaking/`
  - Talk scripts and presentation aids.
- `submission/`
  - Submission and handoff pack material.

Frozen or lineage-heavy subtrees inside otherwise active directories:

- `docs/architecture/`
  - Historical `Execution Evidence Object` framing.
- `docs/edc/`
  - Frozen asset/reference surface, not an active code line.
- `docs/fdo-mapping/`
  - Supporting lineage/reference material.
- `docs/outreach/`
  - Outward positioning rather than product entry.
- `release/v0.1-live-chain/`
  - Frozen legacy AEP package surface.

Mixed historical files inside otherwise canonical or active paths:

- `spec/execution-evidence-object.md`
- `schema/execution-evidence-object.schema.json`
- `examples/evidence-object-openai-run.json`
- `scripts/verify_evidence_object.py`
- `scripts/demo_execution_evidence_object.py`

## 5. Keep / weaken / move / archive recommendations

### Keep

- Keep `agent_evidence/`, `spec/`, `schema/`, and `tests/` as the canonical core.
- Keep `examples/`, `demo/`, `integrations/`, and selected `docs/` pages as the active developer surface.
- Keep `plans/` during Phase A because the repo is still tightening its primary entry path.
- Keep historical and paper material in-repo for provenance; this repo clearly serves both product and manuscript evidence functions.

### Weaken

- Weaken `paper/`, `poster/`, `proposal/`, `release/`, `research/`, `roadmap/`, `speaking/`, and `submission/` from any primary install/run navigation.
- Weaken `docs/edc/` to explicit frozen-reference status.
- Weaken `docs/architecture/`, `docs/fdo-mapping/`, and `docs/outreach/` from the primary product path.
- Weaken legacy prototype commands and wording that still make `Execution Evidence Object` or older AEP surfaces look co-equal with the current v0.1 path.
- Weaken legacy-only repo gates if they remain visible as if they define the active product contract.

### Move

- Do not do broad directory moves in Phase A.
- The first future move candidate is inside `scripts/`: separate current support scripts from legacy prototype scripts behind a clear legacy boundary.
- The second future move candidate is not a filesystem move first; it is a navigation move: route all historical prototype references through `docs/lineage.md` instead of the top-level entry path.

### Archive

- Treat `proposal/`, `poster/`, `speaking/`, and completed submission/release packs as archived-from-entry-surface material.
- Archive here means “kept for provenance, but not presented as active product surface,” not “delete” and not “move out of this repository now.”

## 6. Minimal move plan with lowest-risk sequencing

1. Freeze the classification first.
   - Use this audit as the repo boundary note.
   - Do not move directories yet.

2. Tighten navigation before paths.
   - Rewrite the top-level README to point only to the active product path.
   - Keep historical and frozen links, but put them behind explicit labels such as lineage, frozen asset, or background.

3. Keep mixed directories stable during Phase A.
   - `docs/` and `scripts/` are mixed, but moving them now creates avoidable churn.
   - Use labeling first, not path reshaping first.

4. After README and quickstart are stable, do only surgical cleanup if still needed.
   - Separate legacy prototype scripts from current support scripts.
   - Optionally isolate frozen package/release material behind one clearer archive convention.

5. Defer any large top-level consolidation until after the Phase A gate.
   - The current problem is entry confusion, not lack of storage hierarchy.
   - Large moves would break links and distract from the current developer-product tightening work.

## 7. Risks if no changes are made

- First-time developers will continue to see multiple competing narratives at once: package, prototype, paper, roadmap, release, and outreach.
- Historical `Execution Evidence Object` and legacy AEP surfaces will keep reading as if they are equal to the current `v0.1` package line.
- `docs/edc/` and related frozen material can be misread as active implementation commitments.
- Mixed support surfaces such as `scripts/` and `.github/workflows/` will keep blurring which checks define the current canonical contract.
- Future README and quickstart work will have to fight the repo shape every time, instead of benefiting from a stable active/frozen boundary.

Bottom line: the repository does not need a large restructuring first. It needs a clear active/frozen boundary, narrowed primary navigation, and only then selective cleanup of mixed directories.
