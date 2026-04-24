# Repository compatibility artifacts

This directory contains derived views for probing existing repository validators.

The NCS pack contract is not changed by these files. The strict NCS validator is
still `paper-ncs-execution-evidence/scripts/validate_ncs_pack.py`.

## Files

- `ncs_bundle_view.json`: canonical JSON copy of the NCS `bundle.json` with no semantic changes.
- `operation_accountability_statement.json`: conservative mapping into the repository's older `execution-evidence-operation-accountability-profile@0.1` statement shape.
- `artifact_index.json`: digest index for the NCS pack and derived compatibility files.

## Compatibility adjustments

The repository schema requires profile name `execution-evidence-operation-accountability-profile`
and version `0.1`, plus single-operation fields such as `statement_id`,
`constraints`, `evidence.references`, `evidence.artifacts` and
`evidence.integrity`. The derived statement therefore maps the NCS FASTQ QC
operation into that older single-operation shape. This is advisory compatibility,
not strict validation of the whole NCS pack.
