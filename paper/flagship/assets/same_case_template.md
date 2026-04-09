# Same-Case Template

## 固定 comparison case

建议默认使用 `retention review` 作为 fixed case。

### Case Summary

- actor:
  - one review agent
- subject:
  - one dataset package
- operation:
  - one retention review
- policy basis:
  - retention-review policy
- inputs:
  - dataset package
  - review ticket
- output:
  - one retention decision object

## 表达模板

### 1. logs-only

- 应包含：
  - timestamps
  - service or actor name
  - review start/end messages
  - optional file/object paths
- what remains unprovable：
  - 当前执行与哪一版 policy 明确绑定
  - input/output refs 是否闭合
  - decision output 是否形成独立 evidence block
  - 第三方如何独立 validation

### 2. provenance-only

- 应包含：
  - subject, inputs, output 的 lineage links
  - actor 与 operation 的 derivation relation
- what remains unprovable：
  - governing policy 是否是当前执行依据
  - review-report artifact 是否足够
  - checker 应如何给出 pass/fail

### 3. policy-only

- 应包含：
  - retention rules
  - escalation conditions
  - allowed classes
- what remains unprovable：
  - 实际 review 是否发生
  - 作用对象是不是当前 subject
  - 输出 decision 是否由当前 operation 产生

### 4. audit-trail-only

- 应包含：
  - reviewed history
  - action sequence
  - operator/system context
- what remains unprovable：
  - 是否已经形成一个最小、portable、local statement
  - 离开原系统语义后能否被独立检查

### 5. boundary-based accountability statement

- 应包含：
  - actor / subject / operation
  - policy / constraints
  - provenance
  - evidence references and artifacts
  - validation block
- what remains unprovable：
  - 全局 workflow history
  - 更大治理流程
- why this is still enough：
  - 因为本文问题只要求 single-operation accountability boundary，而不是整套 governance replay

## Template Usage

- 所有 comparison 写作都应围绕同一 fixed case。
- 不允许换场景再换结论。
- 每种表示都要回答同一组问题：
  - 谁执行了操作？
  - 对哪个对象执行？
  - operation 语义是否明确？
  - policy 是否与本次执行绑定？
  - 输入输出是否闭合？
  - evidence 是否足以支撑结果？
  - validation path 是否明确？
