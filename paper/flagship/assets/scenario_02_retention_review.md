# Scenario 02: Retention Review

## Scenario Goal

验证 decision-style operation 是否也能被压缩成同一 minimal verification boundary，而不是只适用于 enrichment 类派生操作。

## Actors

- primary actor: `retention-reviewer`
- external reviewer: checker / policy reviewer

## Object(s)

- subject object: one dataset package
- input objects:
  - dataset package
  - retention ticket
- output object: retention decision object

## Operation

- operation type: `retention.review`
- operation shape: two inputs, one decision output

## Policy Basis

- retention catalog constraint
- restricted-escalation constraint

## Expected Accountable Outcome

- statement 能说明这次 review 在什么 policy basis 下完成
- 输入 dataset 与 ticket 是否都被纳入 evidence continuity
- decision output 是否可被独立复核

## Evidence Components Required

- actor / subject / operation
- dual input refs
- one decision output ref
- review-report artifact
- policy + constraints
- provenance closure
- validation block

## Comparison-Pack Notes

- 这是当前最适合做 fixed same-case comparison 的场景。
- 能同时暴露 logs-only、policy-only、provenance-only、audit-trail-only 的不足。

## Likely Failure Injections

- broken policy linkage
- broken input/output closure
- outcome present but evidence insufficient
- temporal mismatch between review decision and policy basis
- implementation-coupled review artifact

## What Can Be Reused from Current Repo

- `examples/valid-retention-review-evidence.json`
- `paper/tosem_cn/comparative_case_analysis.md`
- `paper/flagship/12_same_case_comparison_pack.md`
