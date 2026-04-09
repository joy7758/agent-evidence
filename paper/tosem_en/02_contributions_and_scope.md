# Contributions and Scope

## Contributions

1. We define a minimal verifiable profile for single-operation accountability in FDO-based agent systems, centered on `operation`, `policy`, `provenance`, `evidence`, and `validation`.
2. We provide a profile-aware validation approach that extends structural schema checking with reference closure, cross-field consistency, and explicit error reporting.
3. We ground the method with a boundary-oriented example suite consisting of two valid examples and five invalid examples, making both passing and failing conditions inspectable.
4. We package the method as a reproducible artifact package comprising the profile specification, JSON Schema, examples, validator, CLI, tests, demo, GitHub Release `v0.2.0`, and Zenodo DOI `10.5281/zenodo.19334062`.

## What This Paper Does Not Claim

- It does not claim broad cross-framework validation.
- It does not claim industrial-scale deployment.
- It does not claim a complete governance platform or a universal FDO standard.
- It does not claim full support for complex multi-agent workflows or a complete cryptographic trust infrastructure.

## Why the Scope Is Deliberately Minimal

The paper deliberately narrows the problem to a single operation accountability statement because that is the smallest unit that can still be specified, validated, tested, demonstrated, released, and archived as a coherent software artifact. Expanding the scope too early would blur the method boundary and weaken the evidence. The current contribution is therefore not breadth, but closure: a minimal profile, a validator that enforces its rules, and an artifact package that makes the method inspectable and reproducible.
