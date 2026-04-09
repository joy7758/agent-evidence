# Validation Plan v1

## 定位

这份 validation plan 面向旗舰论文，而不是当前 TOSEM line。TOSEM 已经证明 `minimal verifiable profile + profile-aware validator + examples + demo` 可以被实现。旗舰论文的验证任务更高一层：证明 operation accountability 作为一条 minimal verification boundary 是可定义、可比较、可失败、可外部复核的研究问题。

## 1. Validation Goals

旗舰论文的验证不追求大规模 benchmark，而追求五个更贴近问题定义的目标：

1. 证明这条 boundary 在多个受控场景下都能成立，而不只服务于单一 demo。
2. 证明 failure taxonomy 不是事后拼出来的错误列表，而是能被稳定触发和检测的 failure classes。
3. 证明验证结论不依赖单一 reference implementation，至少存在一个 independent checker 路径。
4. 证明 logs-only、provenance-only、policy-only、audit-trail-only 都只能部分覆盖问题，不能替代 boundary-based statement。
5. 证明 minimality 与 verifiability 之间存在可观察、可讨论的张力，而不是任意字段取舍。

## 2. Multi-Scenario Coverage

### 目标

验证同一 minimal verification boundary 是否能跨多个对象操作语境保持稳定，而不被单一场景绑死。

### 最小场景组

| scenario class | example intent | boundary stress |
| --- | --- | --- |
| metadata enrichment | 对单对象做受 policy 约束的内容增强 | 基础通过路径，单输入单输出 |
| retention review | 对对象做保留/处置判断 | 双输入单输出，decision-style operation |
| access decision | 对对象或对象集合做允许/拒绝决定 | no-output 或 decision output 边界 |
| object derivation handoff | 生成派生对象并交付到外部空间 | output verifiability 与 portability |
| failed or denied operation | 操作未成功完成，但仍需可验证 | result/status 与 evidence sufficiency |

### 成功标准

- 每个场景都复用同一核心边界：`operation / policy / provenance / evidence / validation`。
- 场景差异主要体现在对象类型、input/output pattern、policy shape，而不改变主边界定义。
- 至少一个场景明确位于 STAP 或 data space 语境，而不是只停留在 repo 内 demo 风格。

## 3. Failure Taxonomy Coverage

### 目标

把 failure taxonomy 从概念表升级为受控验证面。

### v1 覆盖类目

| class | target evidence |
| --- | --- |
| missing identity binding | actor 缺失或 actor/provenance 断裂的 invalid case |
| missing target binding | subject 缺失或 operation/subject 断裂的 invalid case |
| ambiguous operation semantics | operation verb 过泛、结果语义不足的 borderline case |
| broken policy linkage | policy ref 或 constraint ref 断裂的 invalid case |
| broken evidence continuity | ref closure / role mismatch / digest mismatch |
| outcome unverifiability | 声称成功但输出证据不足 |
| temporal inconsistency | statement 时间锚点与 policy / input / output 时序冲突 |
| implementation-coupled evidence | evidence 只能依赖原实现解释 |

### 成功标准

- 每一类至少有 1 个单点破坏样例。
- checker 对每类失败给出稳定 primary code 或稳定 failure label。
- 论文明确区分：哪些类已直接覆盖，哪些类仍属部分覆盖。

## 4. Independent Checker Plan

### 目标

降低“同一团队定义规则、同一仓库实现验证器”的闭环风险。

### 最小实施方案

1. 保留当前 `profile-aware validator` 作为 reference checker。
2. 新增一个 second checker，要求：
   - 不复用同一实现逻辑文件；
   - 可用独立脚本、独立规则层，或独立语言实现；
   - 只复现 boundary rules，不扩展额外平台逻辑。
3. 对同一 corpus 做 pass/fail 对照与主要 failure label 对照。

### 成功标准

- 两个 checker 对 valid/invalid corpus 的主结论一致。
- 差异项必须可解释，并归类为规则歧义、实现缺陷或 taxonomy 未冻结。
- 论文如实说明“independent checker”不等于“广泛社区实现收敛”。

## 5. Comparison Plan

### 目标

把“partial rather than sufficient”从概念判断变成结构性比较结果。

### 比较对象

- logs-only
- provenance-only
- policy-only
- audit-trail-only
- boundary-based statement

### 比较方法

对同一固定场景，逐项检查以下问题能否被独立回答：

| question | logs-only | provenance-only | policy-only | audit-trail-only | boundary-based statement |
| --- | --- | --- | --- | --- | --- |
| 谁执行了操作 | 可能部分 | 可能部分 | 否 | 可能部分 | 是 |
| 对哪个对象执行 | 可能部分 | 是 | 否 | 可能部分 | 是 |
| operation 语义是否明确 | 可能部分 | 部分 | 否 | 部分 | 是 |
| policy 依据是否与本次执行绑定 | 弱 | 弱 | 是 | 部分 | 是 |
| 输入输出引用是否局部闭合 | 弱 | 部分 | 否 | 部分 | 是 |
| evidence 是否连续可复核 | 弱 | 弱 | 否 | 部分 | 是 |
| validation path 是否明确 | 否 | 否 | 否 | 弱 | 是 |

### 成功标准

- 结论不是“替代物无价值”，而是“替代物不能单独完成问题”。
- 至少一个同案比较来自真实 scenario，而不是纯抽象表格。

## 6. Minimality vs Verifiability Analysis

### 目标

证明这不是随意加字段，而是一个可分析的边界张力。

### 分析方法

- 做减法：移除 actor、policy、provenance、evidence、validation、temporal anchor 中任一关键部分，观察 statement 在何处失去可验证性。
- 做加法：引入完整 logs、全链 provenance graph、组织流程字段、实现私有 telemetry，观察 statement 在何处失去最小性、 portability 或 local inspectability。

### 预期结果

- 太小：退化成描述性 statement。
- 太大：退化成 runtime replay、审计包或治理系统切片。
- 合理边界：第三方可仅凭 statement 做出局部验证判断。

## 7. Threats to Validity

| threat | meaning | mitigation |
| --- | --- | --- |
| 单仓库偏差 | 规则定义和 reference checker 来自同一 research line | 增加 second checker 与外部 scenario |
| 场景偏窄 | 通过样例仍可能过度贴合当前对象类型 | 引入 decision、failed、handoff 等不同场景 |
| 比较偏概念化 | 与 logs / provenance / policy / audit trail 的比较可能停留在文字层 | 使用同案比较模板和 reviewer-facing matrix |
| taxonomy 未冻结 | 失败类目可能随新场景继续变化 | 明确写为 v1，并区分 covered vs missing |
| portability 过度解读 | 多场景通过不等于 broad cross-framework validation | 在论文中显式限制 claim |

## 8. 最低可交付验证包

旗舰论文的最小验证包至少应包含：

- 1 份 multi-scenario matrix
- 1 组 failure taxonomy coverage matrix
- 1 个 independent checker 对照结果
- 1 份同案比较表
- 1 段 minimality vs verifiability 分析
- 1 节 threats to validity

## 结论

旗舰论文的 validation plan 不应再围绕“这个 profile 能不能跑通”展开，而应围绕“这条 verification boundary 是否跨场景成立、是否可稳定失败、是否可被独立检查、以及为什么替代物只能部分覆盖问题”展开。只有这样，validation 才真正服务于 problem-defining paper，而不是重复 TOSEM 的 artifact closure。
