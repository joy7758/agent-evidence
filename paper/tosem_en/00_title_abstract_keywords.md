# Title, Abstract, and Keywords

## Preferred Title

A Minimal Verifiable Profile for Operation Accountability in FDO-Based Agent Systems

## Alternative Titles

1. A Minimal Verifiable Profile for Operation Accountability in FDO-Based Agent Systems: Validator and Artifact Package
2. Operation Accountability in FDO-Based Agent Systems: A Minimal Verifiable Profile

## Abstract

FDO-based agent systems require more than execution traces when a single operation must be checked outside the original runtime context. They need a compact accountability statement that can specify which operation was performed on which digital object context, under which policy basis, with which input and output references, what evidence was produced, and how the statement can be independently validated. This paper presents a minimal verifiable profile for that purpose and grounds it in the current `agent-evidence` repository. The profile is intentionally narrow: it centers operation accountability and binds `operation`, `policy`, `provenance`, `evidence`, and `validation` into one portable, externally checkable statement while keeping only the supporting context needed for independent review. The repository provides a profile specification, a JSON Schema, two valid examples, five invalid examples, a profile-aware validator, a CLI entry point, tests, and a runnable single-path demo. The validator goes beyond structural schema checks to cover reference closure, cross-field consistency, and minimal integrity checks, and it produces machine-readable JSON reports, human-readable summaries, and explicit error codes. The current artifact package is anchored by GitHub Release `v0.2.0` and Zenodo DOI `10.5281/zenodo.19334062`. The paper does not claim broad cross-framework validation or industrial-scale deployment. Its claim is narrower: in the current repository context, operation accountability can be packaged as a minimal, testable, reproducible, and archivable engineering unit.

## Keywords

- FDO-based agent systems
- operation accountability
- provenance
- execution evidence
- profile-aware validation
- JSON Schema
- software artifact
