# Scenario 05: Failed or Denied Operation

## Scenario Goal

验证 failed / denied operation 是否也能保留最小 verification boundary，而不是只留下异常或拒绝日志。

## Actors

- primary actor: enforcement / execution agent
- external reviewer: checker / exception reviewer

## Object(s)

- subject object: one protected or target object
- optional request or trigger object
- expected outcome object: failure or denial record

## Operation

- operation type: scenario-specific，例如 `access.decide` 或 `metadata.enrich`
- operation shape: attempted action with failed or denied result

## Policy Basis

- denial policy
- refusal or failure condition constraints
- optional escalation rule

## Expected Accountable Outcome

- 即使 operation 没有成功，第三方仍能判断：
  - 谁尝试了操作
  - 对哪个对象尝试
  - 为什么失败或被拒绝
  - 留下了哪些 evidence
  - 结果是否仍可验证

## Evidence Components Required

- actor / subject / operation
- policy + constraints
- failure or denial result summary
- attempted input refs
- failure artifact or denial artifact
- validation block

## Comparison-Pack Notes

- 该场景能防止旗舰论文只覆盖“成功操作”的偏差。
- 适合作为 appendix 或 artifact package 的关键补强项。

## Likely Failure Injections

- outcome missing despite failed status
- ambiguous operation semantics
- temporal inconsistency
- insufficient evidence for denial or failure reason

## What Can Be Reused from Current Repo

- current schema permits `operation.result.status = failed`
- current profile shape and validator logic
- `paper/flagship/03_failure_taxonomy_v1.md`
