# Same-Case Comparison Pack

## 目的

旗舰论文需要一个固定 case，把不同表示方式放到同一问题上比较。否则“logs-only / provenance-only / policy-only / audit-trail-only 只能部分覆盖问题”很容易停留在概念判断。

## 固定比较案例

建议使用：

- `retention review` 作为 fixed comparison case

原因：

- 当前 repo 已有 `examples/valid-retention-review-evidence.json`
- 它同时包含：
  - actor
  - subject
  - 双输入引用
  - decision output
  - policy basis
  - review artifact
- 这个结构比 metadata enrichment 更适合同步比较 logs、provenance、policy、audit trail 与 boundary-based statement。

## Case Design

固定 case 只讨论一个问题：

一个 `retention-reviewer` agent 在 `policy:retention-review-v1` 约束下，对 `obj:dataset-package-042` 执行一次 `retention.review` operation，读取 dataset 与 retention ticket，输出 retention decision object。比较重点不是“哪种表示更丰富”，而是“哪种表示能让第三方独立回答 operation accountability 问题”。

## 五种表示方式

### 1. logs-only

- can support：
  - 运行片段
  - 时间戳
  - 部分 actor / process 信息
  - 可能的输入输出路径
- cannot conclude：
  - policy 是否与本次执行明确绑定
  - 输入输出是否局部闭合
  - validation path 是什么
- why insufficient alone：
  - 它记录很多事，但通常不形成一个局部闭合 statement。

### 2. provenance-only

- can support：
  - 对象派生关系
  - actor / object / output 之间的 lineage links
- cannot conclude：
  - governing policy 是否是当前执行的规则依据
  - evidence block 是否足以支持结果
  - external checker 应如何判断 pass/fail
- why insufficient alone：
  - 它擅长回答“从哪里来”，不擅长单独回答“是否已形成最小可验证责任单元”。

### 3. policy-only

- can support：
  - 规则依据
  - 允许条件
  - constraint catalog
- cannot conclude：
  - 实际执行了什么 operation
  - 哪个对象被处理
  - 什么 evidence 支撑当前执行结果
- why insufficient alone：
  - 它说明“应该如何做”，不能单独说明“这次具体做了什么”。

### 4. audit-trail-only

- can support：
  - 更长时间跨度的审计记录
  - 更丰富的事件保留
  - 可能更强的 history reconstruction
- cannot conclude：
  - 是否已经存在一个局部、最小、portable 的 statement
  - 是否可以脱离原实现知识做局部验证
- why insufficient alone：
  - 它常常范围过大、实现耦合过深，容易变成“可回放的历史”，而不是“可独立检查的边界单元”。

### 5. boundary-based accountability statement

- can support：
  - actor / subject / operation / policy / provenance / evidence / validation 的局部绑定
  - input/output closure
  - external checker path
  - stable failure boundary
- cannot conclude：
  - 全局 workflow history
  - 完整组织治理流程
  - 广泛生态互操作已完成
- why it is sufficient for this problem：
  - 它直接面向 single-operation accountability 的最小验证问题，而不是试图替代所有外围系统。

## 可直接进论文的比较表

| representation | 可以支持什么 | 不能单独得出什么结论 | 为什么单独不足 |
| --- | --- | --- | --- |
| logs-only | 事件片段、时间戳、部分执行路径 | policy 绑定、局部闭合、validation path | 记录丰富，但通常不是 statement |
| provenance-only | derivation links、对象关系 | governing policy、evidence sufficiency、checker path | 强 lineage，弱局部验证闭环 |
| policy-only | 规则依据、constraint catalog | concrete operation、执行结果、evidence continuity | 只说明 should，不说明 did |
| audit-trail-only | 审计历史、保留记录 | 最小 portable boundary 是否成立 | 过大且实现耦合，难以局部验证 |
| boundary-based statement | 单 operation 的最小验证闭环 | 全局治理或全 workflow 结论 | 足以回答本文问题，但不替代更大系统 |

## 当前 repo 可复用材料

- `examples/valid-retention-review-evidence.json`
- `paper/tosem_cn/comparative_case_analysis.md`
- `paper/flagship/02_minimal_verification_boundary.md`
- `paper/flagship/03_failure_taxonomy_v1.md`

## 结论

same-case comparison pack 的目标不是证明替代物“没用”，而是证明它们与本文解决的问题不是同一个边界。只要这个边界判断被固定到同一 case 上，旗舰论文的比较部分就会从泛泛论述变成可检查的结构性比较。
