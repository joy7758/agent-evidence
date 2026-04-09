# Multi-Scenario Corpus v1

## 目的

这份 corpus 不是一组已完成实验结果，而是一组可复用、可扩展、可被 checker 和 comparison pack 共用的 validation corpus 计划。它的作用是把旗舰论文的验证从单一 demo 推向多场景 boundary evidence。

## 场景列表

### Scenario 01: metadata enrichment

- 为什么重要：
  - 这是当前 repo 最稳定的基础通过场景。
- 它测试的 accountability question：
  - 一个 agent 是否能在明确 policy 约束下，对单对象做一次可验证的 enrichment operation。
- 必需 evidence components：
  - actor / subject / operation
  - policy / constraints
  - 单输入单输出 references
  - execution-log artifact
  - validation block
- 可能触发的 failure classes：
  - missing identity binding
  - missing target binding
  - broken policy linkage
  - broken evidence continuity
  - implementation-coupled evidence
- 当前 repo 是否已有部分材料：
  - 有，且最完整。可直接复用 `examples/minimal-valid-evidence.json`、`demo/` 和 `demo/artifacts/`。

### Scenario 02: retention review

- 为什么重要：
  - 它比 metadata enrichment 更接近 decision-style object operation。
- 它测试的 accountability question：
  - 一个 review operation 是否能把 policy basis、双输入引用和 decision output 绑定成同一个可验证 statement。
- 必需 evidence components：
  - actor / subject / operation
  - 双输入 references
  - decision output reference
  - review-report artifact
  - validation block
- 可能触发的 failure classes：
  - broken policy linkage
  - broken evidence continuity
  - outcome unverifiability
  - temporal inconsistency
- 当前 repo 是否已有部分材料：
  - 有。可直接复用 `examples/valid-retention-review-evidence.json` 和 `paper/tosem_cn/comparative_case_analysis.md`。

### Scenario 03: access decision

- 为什么重要：
  - access decision 能测试允许/拒绝类操作是否也属于同一 accountability boundary。
- 它测试的 accountability question：
  - 对对象或对象集合做 access allow/deny 时，系统能否给出可独立复核的 decision statement。
- 必需 evidence components：
  - actor / subject 或 subject-set
  - operation type 与 decision result
  - governing access policy
  - 至少一个 input reference
  - decision artifact 或 decision output reference
  - validation block
- 可能触发的 failure classes：
  - ambiguous operation semantics
  - broken policy linkage
  - outcome unverifiability
  - temporal inconsistency
- 当前 repo 是否已有部分材料：
  - 现已具备中心 specimen：
    - `paper/flagship/assets/specimens/scenario_03_access_decision_valid.json`
    - `paper/flagship/assets/specimens/scenario_03_access_decision_invalid_missing_policy_linkage.json`

### Scenario 04: object derivation handoff

- 为什么重要：
  - 该场景把“生成输出”推进到“生成并交付到外部空间”，更贴近 data space / FDO handoff 语境。
- 它测试的 accountability question：
  - 当系统派生对象并交付出去时，输出对象是否仍保留最小可验证边界，而不是退化成实现私有产物。
- 必需 evidence components：
  - source subject
  - derivation operation
  - output object reference
  - handoff artifact 或 external locator
  - policy / provenance / validation
- 可能触发的 failure classes：
  - broken evidence continuity
  - outcome unverifiability
  - implementation-coupled evidence
  - missing target binding
- 当前 repo 是否已有部分材料：
  - 现已具备中心 specimen，并继续复用：
    - `paper/flagship/assets/specimens/scenario_04_object_derivation_handoff_valid.json`
    - `paper/flagship/assets/specimens/scenario_04_object_derivation_handoff_invalid_broken_evidence_continuity.json`
    - `demo/artifacts/derived-object.json`
    - `docs/fdo-mapping/` 相关 framing

### Scenario 05: failed or denied operation

- 为什么重要：
  - 如果失败或拒绝类操作不能进入 accountability boundary，那么验证边界只覆盖“成功故事”。
- 它测试的 accountability question：
  - 当操作失败或被拒绝时，系统能否仍然输出可复核的 statement，而不仅是异常日志。
- 必需 evidence components：
  - actor / subject / operation
  - failure or denial result
  - policy basis
  - evidence of attempted action
  - validation block
- 可能触发的 failure classes：
  - outcome unverifiability
  - ambiguous operation semantics
  - broken evidence continuity
  - temporal inconsistency
- 当前 repo 是否已有部分材料：
  - 现已具备中心 specimen：
    - `paper/flagship/assets/specimens/scenario_05_failed_or_denied_operation_valid.json`
    - `paper/flagship/assets/specimens/scenario_05_failed_or_denied_operation_invalid_missing_outcome.json`

## Coverage Matrix

说明：

- `P` = primary coverage
- `S` = secondary / likely coverage
- `C` = checker candidate
- `X` = suitable for same-case comparison use

| scenario | ID | TGT | OPR | POL | EVD | OUT | TIME | COUP | checker use | comparison use | current status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| metadata enrichment | P | P | S | P | P | S | S | P | C | S | existing |
| retention review | S | P | P | P | P | P | S | S | C | X | existing |
| access decision | S | S | P | P | S | P | P | S | C | X | existing |
| object derivation handoff | S | P | S | S | P | P | S | P | C | X | existing |
| failed or denied operation | S | S | P | P | S | P | P | S | C | X | existing |

## Boundary Stress Materials

除 5 个 scenario 之外，当前 repo 还新增了 6 个 direct failure specimens：

- cross-scenario boundary stress：
  - `scenario_06_missing_identity_binding_invalid.json`
  - `scenario_07_temporal_inconsistency_invalid.json`
  - `scenario_08_implementation_coupled_evidence_invalid.json`
  - `scenario_09_missing_target_binding_invalid.json`
  - `scenario_10_ambiguous_operation_semantics_invalid.json`
- scenario-tied boundary stress：
  - `scenario_11_outcome_unverifiability_invalid.json`

它们的用途不是扩展 scenario diversity，而是把 v1 failure taxonomy 中此前偏弱的 failure classes 压成可运行输入。

## 使用原则

- 这组 corpus 用于三类事情：
  - checker corpus
  - failure taxonomy corpus
  - same-case comparison corpus
- 不是每个 scenario 都要一步到位变成完整实验。
- 第一阶段优先把：
  - metadata enrichment
  - retention review
  - access decision
  - failed or denied operation
 变成最小可验证语料。

## 结论

旗舰论文的 corpus 重点不是“场景越多越好”，而是“这条 minimal verification boundary 是否在不同 object-operation settings 下保持稳定，同时能暴露不同 failure classes”。这就是 Multi-Scenario Corpus v1 的作用。
