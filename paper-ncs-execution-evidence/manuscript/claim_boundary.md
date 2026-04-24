# Claim boundary

## Main claim

A minimal, validator-backed evidence boundary can turn a scientific workflow execution into a portable object that an independent party can verify outside the original runtime.

## What the validator may claim

The validator may claim:

1. required evidence fields are present;
2. canonical serialization was used;
3. input/output digests match declared values;
4. operation, policy, provenance and evidence links are closed;
5. the claimed receipt digest is reproducible;
6. failure cases produce deterministic exit codes;
7. the pack can be verified offline when all referenced artifacts are included.

## What the validator must not claim

The validator must not claim:

1. the scientific conclusion is true;
2. the workflow is statistically valid;
3. the software is secure;
4. the data are ethically or legally usable;
5. the profile is an official FDO standard;
6. the method replaces RO-Crate, Workflow Run RO-Crate, W3C PROV, BioCompute Object or OpenTelemetry;
7. regulatory compliance has been achieved.

## Boundary against related manuscript lines

| Related line | NCS treatment |
|---|---|
| Single-operation accountability profile | foundation only |
| AEP / autonomous-agent evidence | secondary generalization only |
| AI Act compliance evidence | excluded from main claim |
| UDI-DICOM mapping | not used as NCS main workflow |
| AEEP curation profile | not used as main result |

## Safe formulation

The proposed evidence boundary complements existing provenance and workflow packaging systems by adding deterministic validator semantics at the operation-accountability layer.
