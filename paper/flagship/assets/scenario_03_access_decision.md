# Scenario 03: Access Decision

## Scenario Goal

验证 allow/deny 类操作是否也应进入同一 accountability boundary，而不是被简化成 policy check log 或 access-control side effect。

## Actors

- primary actor: access decision agent or policy enforcement agent
- external reviewer: checker / data access reviewer

## Object(s)

- subject object: one protected dataset or record set
- optional requester object: ticket / request object
- expected outcome object: access decision statement or decision token

## Operation

- operation type: `access.decide`
- operation shape: one or two inputs, one allow/deny style output

## Policy Basis

- access policy version
- clearance or consent constraints
- requester eligibility constraints

## Expected Accountable Outcome

- 第三方能够判断这次 allow/deny 决策是否绑定了明确 policy
- decision result 是否有足够 evidence 支撑
- 即使没有内容派生，也仍能形成 operation accountability statement

## Evidence Components Required

- actor / subject / operation
- request input ref
- decision output ref or decision artifact
- policy + constraints
- provenance closure
- validation block

## Comparison-Pack Notes

- 比 retention review 更贴近 access-governed data space 语境。
- 适合 later flagship validation，但当前 repo 还没有现成 specimen。

## Likely Failure Injections

- ambiguous operation semantics
- missing policy linkage
- outcome unverifiability
- temporal inconsistency around decision time
- private access-engine locator leakage

## What Can Be Reused from Current Repo

- current OAP field model and schema
- retention review 的 decision-style pattern
- `paper/flagship/11_multiscenario_corpus_v1.md`
