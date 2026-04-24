# NCS execution-evidence manuscript workspace

This directory is the isolated Nature Computational Science paper workspace.

## Target

Nature Computational Science.

## Manuscript type

Article / Resource dual track until the Week 4 decision gate.

## Core claim

We present a validator-backed execution-evidence boundary for independently verifiable scientific workflows.

## Directory rule

All assets for this manuscript live under `paper-ncs-execution-evidence/`.

Existing `paper-*` directories are older or adjacent manuscript lines and must not be edited by this scaffold.

## Scientific priority

The scientific workflow is the main experiment.

The manuscript-facing main experiment is now
`paper-ncs-execution-evidence/paper_packs/scientific_workflow_public/`, built
from the public Drosophila small RNA-seq dataset `10.5281/zenodo.826906`.

The earlier `paper_packs/scientific_workflow/` smoke pack remains a regression
fixture for validator and failure-matrix development.

The agent/tool-use workflow is a secondary generalization experiment only.

## Not the main claim

This manuscript does not claim:

- official FDO standard status;
- AI Act compliance;
- replacement of RO-Crate, Workflow Run RO-Crate, W3C PROV, BioCompute Object or OpenTelemetry;
- UDI-DICOM mapping as the main scientific workflow;
- agent evidence as the primary result.
