# Scenario 04: Object Derivation Handoff

## Scenario Goal

验证对象派生并交付到外部空间时，boundary-based statement 是否仍保持最小、可检查、可移植，而不是退化成实现私有 handoff log。

## Actors

- primary actor: derivation or packaging agent
- external reviewer: receiver-side checker

## Object(s)

- source object: one input digital object
- derived object: one transformed or packaged output object
- handoff target: external space, registry placeholder, or data space endpoint

## Operation

- operation type: `object.derive.handoff`
- operation shape: one input, one derived output, one handoff artifact

## Policy Basis

- derivation policy
- packaging / handoff constraints
- allowed metadata or transformation rules

## Expected Accountable Outcome

- 第三方可判断输出对象是否真由当前 subject 派生
- handoff 是否保留最小 evidence continuity
- 输出 locator 是否不依赖实现私有路径

## Evidence Components Required

- actor / subject / operation
- input/output refs
- handoff artifact or receipt artifact
- policy + constraints
- provenance
- validation block

## Comparison-Pack Notes

- 这是最适合测试 portability 与 implementation-coupling 的 scenario。
- 同时也是 later FDO / data space framing 的关键连接点。

## Likely Failure Injections

- missing target binding for derived object
- broken evidence continuity across handoff
- outcome unverifiability
- implementation-coupled locator or artifact

## What Can Be Reused from Current Repo

- `examples/minimal-valid-evidence.json`
- `demo/artifacts/derived-object.json`
- `docs/fdo-mapping/execution-evidence-to-fdo.md`
- `release/minimal-demo.md`
