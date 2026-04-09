# Front Package

## Preferred Title

A Minimal Verifiable Profile for Operation Accountability in FDO-Based Agent Systems

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

## Four Contributions

1. We define a minimal verifiable profile for single-operation accountability in FDO-based agent systems, centered on `operation`, `policy`, `provenance`, `evidence`, and `validation`.
2. We provide a profile-aware validation approach that extends structural schema checking with reference closure, cross-field consistency, and explicit error reporting.
3. We ground the method with a boundary-oriented example suite consisting of two valid examples and five invalid examples, making both passing and failing conditions inspectable.
4. We package the method as a reproducible artifact package comprising the profile specification, JSON Schema, examples, validator, CLI, tests, demo, GitHub Release `v0.2.0`, and Zenodo DOI `10.5281/zenodo.19334062`.

## Scope Boundary Note

This paper does not claim a general governance platform, a universal FDO standard, industrial-scale deployment, or broad cross-framework validation. Its scope is deliberately minimal: one profile model, one validator path, one artifact package, two valid contexts, and five invalid boundary cases.

## Intro Opening Paragraph

Software systems built around AI agents are increasingly able to emit logs, traces, and runtime events at high volume. Those materials are useful for debugging, observability, and post hoc inspection. In FDO-based agent systems, however, a narrower and harder question often remains unresolved: for one concrete operation, which operation was performed on which digital object context, under which policy constraints, through which input and output references, with what evidence, and through what validation path? In other words, it is not enough to know that an execution happened. A third party may need a compact statement that can be packaged, checked, and archived as an accountability unit for a single operation.
