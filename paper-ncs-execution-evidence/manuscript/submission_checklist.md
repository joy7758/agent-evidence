# Submission checklist

## Manuscript package

- [ ] main manuscript
- [ ] abstract route selected
- [ ] methods complete
- [ ] related manuscript disclosure updated

## Figures

- [ ] Fig. 1 problem and method boundary
- [ ] Fig. 2 evidence object model
- [ ] Fig. 3 scientific workflow main experiment
- [ ] Fig. 4 failure injection matrix
- [ ] Fig. 5 baseline comparison
- [ ] Fig. 6 reproducibility and independent checking

## Artifacts

- [ ] scientific workflow pack
- [ ] agent/tool-use workflow pack
- [ ] failure cases
- [ ] independent checker
- [ ] container and environment records

## Conflict-control

- [ ] no official FDO standard claim
- [ ] no AI Act main framing
- [ ] no UDI-DICOM main experiment
- [ ] no agent-first framing
- [ ] overlap disclosure finalized

## Final gate

```bash
python paper-ncs-execution-evidence/scripts/build_public_scientific_workflow_pack.py \
  --pack paper-ncs-execution-evidence/paper_packs/scientific_workflow_public \
  --force

bash paper-ncs-execution-evidence/scripts/ncs_verify_pack.sh \
  paper-ncs-execution-evidence/paper_packs/scientific_workflow_public

bash paper-ncs-execution-evidence/scripts/run_public_scientific_workflow_validation_matrix.sh

bash paper-ncs-execution-evidence/scripts/run_independent_checker_agreement.sh \
  paper-ncs-execution-evidence/paper_packs/scientific_workflow_public

bash paper-ncs-execution-evidence/scripts/run_cross_environment_verification.sh \
  paper-ncs-execution-evidence/paper_packs/scientific_workflow_public
```
