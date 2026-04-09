# Scenario 01: Metadata Enrichment

## Scenario Goal

验证一个最小、稳定、可通过的 baseline：agent 在明确 metadata policy 约束下，对单个对象执行一次 enrichment operation，并输出一个可独立检查的 accountability statement。

## Actors

- primary actor: `metadata-enricher`
- external reviewer: independent checker / paper reviewer

## Object(s)

- subject object: one client note object
- input object: original note
- output object: derived note with approved metadata

## Operation

- operation type: `metadata.enrich`
- operation shape: one input, one output

## Policy Basis

- approved metadata fields only
- note body remains unchanged

## Expected Accountable Outcome

- 输出一个 derived object
- statement 中能明确绑定 actor、subject、operation、policy、provenance、evidence、validation
- 第三方可在脱离原 runtime 的情况下判断该 operation statement 是否可验证

## Evidence Components Required

- `actor`
- `subject`
- `operation`
- `policy` + `constraints`
- `provenance`
- `evidence.references` with input/output roles
- `evidence.artifacts` with one operation log
- `validation`
- stable `timestamp`

## Comparison-Pack Notes

- 适合做 baseline comparison，但不是最强 same-case comparison case。
- 可用于展示 logs-only 和 boundary-based statement 之间的差别。

## Likely Failure Injections

- actor/provenance binding broken
- missing subject digest or locator
- stale policy link
- unclosed output ref
- implementation-coupled locator

## What Can Be Reused from Current Repo

- `examples/minimal-valid-evidence.json`
- `demo/scenario.md`
- `demo/run_operation_accountability_demo.py`
- `demo/artifacts/minimal-profile-evidence.json`
- `demo/artifacts/validation-report.json`
