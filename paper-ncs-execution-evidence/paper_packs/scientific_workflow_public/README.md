# Public scientific workflow evidence pack

This is the manuscript-facing public scientific workflow pack.

## Dataset

- DOI: `10.5281/zenodo.826906`
- Record: `https://zenodo.org/records/826906`
- Source: Galaxy Training Network small RNA-seq tutorial dataset
- Biological context: downsampled Drosophila small RNA-seq FASTQ files
- GEO accession noted by source: `GSE82128`

No biological discovery is claimed. The experiment tests portable,
validator-backed execution evidence over a public scientific workflow.

## Build

```bash
python paper-ncs-execution-evidence/scripts/build_public_scientific_workflow_pack.py \
  --pack paper-ncs-execution-evidence/paper_packs/scientific_workflow_public \
  --force
```

## Verify

```bash
bash paper-ncs-execution-evidence/scripts/ncs_verify_pack.sh \
  paper-ncs-execution-evidence/paper_packs/scientific_workflow_public
```

## Matrix

```bash
bash paper-ncs-execution-evidence/scripts/run_public_scientific_workflow_validation_matrix.sh
```

## Independent checker agreement

```bash
bash paper-ncs-execution-evidence/scripts/run_independent_checker_agreement.sh \
  paper-ncs-execution-evidence/paper_packs/scientific_workflow_public
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
