# AEP-Media SoftwareX Submission Checklist

## Repository

- [x] Repository URL identified: https://github.com/joy7758/agent-evidence
- [x] Primary Python package identified: `agent_evidence`
- [x] License file present.
- [x] License declared in `pyproject.toml`.
- [ ] Confirm repository is public at submission time.
- [ ] Confirm AEP-Media path is discoverable from the top-level README.

## License

- [x] Apache-2.0 license present.
- [x] Apache-2.0 is OSI-compatible.
- [ ] Confirm all included examples, fixtures, and generated materials are compatible with the repository license.

## Documentation

- [x] Specs present under `spec/`.
- [x] Schemas present under `schema/`.
- [x] Examples present under `examples/media/`.
- [x] Demos present under `demo/`.
- [x] Reports present under `docs/reports/`.
- [ ] Add or update a short README section that points directly to the AEP-Media profile, examples, commands, and evaluation pack.

## Installation and Tests

- [x] Package metadata present in `pyproject.toml`.
- [x] Console script `agent-evidence` declared.
- [x] Prior reports record targeted tests and evaluation runs.
- [ ] Rerun targeted tests before submission and record current output.
- [ ] Rerun full repository tests only if needed for release confidence.

## Evaluation and Reproducibility

- [x] Default evaluation documented: 18 cases, `unexpected=0`.
- [x] Adapter-inclusive evaluation documented: 26 cases, `unexpected=0`.
- [x] Optional-tool reporting evaluation documented: 23 cases, `unexpected=0`.
- [x] Combined adapter and optional-tool evaluation documented from prior release materials: 31 cases, `unexpected=0`.
- [ ] Rerun all evaluation commands for the final SoftwareX release.
- [ ] Archive evaluation outputs in a release package.

## Archive / DOI

- [x] Repository DOI exists in README: `10.5281/zenodo.19334062`.
- [ ] Confirm whether the DOI corresponds to the exact AEP-Media release.
- [ ] Create a tagged release for the SoftwareX submission if needed.
- [ ] Create or update an AEP-Media-specific archive DOI if needed.

## Submission Hygiene

- [x] No local absolute paths should appear in SoftwareX draft files.
- [x] No unrelated paper-workspace content should be copied into the SoftwareX package.
- [x] TSE lifecycle claims removed from Path A framing.
- [x] Legal and forensic claims kept as explicit non-claims.
- [x] AI-assisted writing disclosure included in manuscript draft.
- [ ] Prepare final SoftwareX manuscript in the required journal template.
- [ ] Prepare software metadata and software availability statement for the submission system.

## Current Readiness

Status: NOT READY.

Remaining blockers:

- AEP-Media CLI commands expected by tests and documentation are not currently registered.
- AEP-Media-specific DOI / archive decision.
- Fresh passing test run after the CLI blocker is fixed.
- Final SoftwareX template formatting review by the author.
