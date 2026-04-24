# Scientific workflow evidence pack

This is the main reviewer-facing scientific workflow pack.

This is currently an executable smoke pack. It uses a deterministic local FASTQ
fixture to wire the bundle, receipt, summary and failure-injection validation
surface. The local FASTQ fixture is not the final public Nature Computational
Science dataset.

## Required files

- `manifest.json`
- `bundle.json`
- `receipt.json`
- `summary.json`
- `expected_digest.txt`
- `inputs/`
- `outputs/`
- `failures/`

## Verification command

```bash
python paper-ncs-execution-evidence/scripts/build_scientific_workflow_pack.py \
  --pack paper-ncs-execution-evidence/paper_packs/scientific_workflow \
  --force
```

```bash
bash paper-ncs-execution-evidence/scripts/ncs_verify_pack.sh \
  paper-ncs-execution-evidence/paper_packs/scientific_workflow
```

```bash
bash paper-ncs-execution-evidence/scripts/run_scientific_workflow_validation_matrix.sh
```

Expected valid-pack outcome: exit code `0`.

## Expected failure cases

| Failure directory | Expected exit code |
|---|---:|
| `failures/tampered_input` | 2 |
| `failures/tampered_output` | 2 |
| `failures/missing_policy` | 5 |
| `failures/broken_evidence_link` | 11 |
| `failures/version_mismatch` | 4 |
| `failures/temporal_inconsistency` | 6 |
| `failures/outcome_unverifiable` | 7 |

## Suggested workflow options

- small FASTQ QC workflow
- small read classification workflow
- toy-but-real variant-calling workflow
- small RNA-seq QC workflow

## Exclusion

Do not use UDI-DICOM medical-device imaging as the main NCS scientific workflow.
