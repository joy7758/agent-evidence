# 问题定义与设计目标

## 1. 问题定义

本文要解决的问题不是“如何完整治理智能体系统”，而是更小、更硬的一个子问题：

在一个 FDO-based agent system 中，如何把一次具体 operation 组织成一个最小但可验证的
operation accountability statement，使第三方能够检查：

- actor 是谁；
- subject 是哪个对象；
- operation 是什么；
- policy 与 constraint 是什么；
- 输入输出引用是否闭合；
- evidence 是否足以支撑该 statement；
- validation 路径是否明确。

这一定义故意把问题限定在一次操作、一个 subject、一个 statement 的粒度上。原因是：
如果连这个最小单元都无法稳定描述和验证，那么更大的编排层、治理层或生态层讨论会很容易
漂浮成叙事，而不是可运行产物。

## 2. 设计目标

### G1. 最小而非完备

profile 只保留能够支撑最小问责闭环的字段。仓库规范明确列出必填字段，并将 optional
字段收缩到最少，避免 profile 过早膨胀。

### G2. 可验证而非仅可描述

本文不满足于“有 JSON 结构”。profile 必须能被 validator 检查。当前仓库至少检查：

- 结构完整性
- 必填字段
- 引用闭合
- policy / provenance / evidence 关联一致性
- 最小 integrity digest 重算

### G3. 复用现有仓库表面

实现不平行新建第二套系统，而是直接沿用现有 `spec/`、`schema/`、`examples/`、
`agent_evidence/`、`tests/`、`demo/`、`submission/` 等目录。这一点与仓库级 AGENTS
要求一致，也保证本工作本身就是对既有仓库的最小增量扩展。

### G4. 面向 artifact 复现

本文不仅要有方法学叙述，还要有可运行工件。因而仓库必须同时存在：

- spec 与 schema
- valid / invalid 样例
- validator 与 CLI
- tests
- 单链路 demo
- release / handoff 文档

### G5. 面向 FDO 语境，但不试图一次解决全部映射

本文采用 FDO-based agent systems 作为问题语境，强调对象、引用、证据、验证路径的
可交换性与可复核性，但不在本轮中构造全量跨风味 FDO registry 或全生态映射。

## 3. 关键设计取舍

### T1. 用 profile，而不是泛化平台

profile 的好处是边界清楚、验证面明确、容易冻结为 artifact。代价是覆盖面窄，只能先解决
单一 statement 的操作问责问题。

### T2. 用 staged validation，而不是一次性报告所有次生错误

当前 validator 的策略是先 schema，再 references，再 consistency，最后 integrity。
这种 staged 方式有利于稳定输出主失败面，代价是某些次生错误不会在同一轮报告中全部展开。

### T3. 用单链路 demo，而不是多场景堆叠

仓库当前采用 metadata enrichment 作为唯一闭环场景。这样做的好处是最稳、最容易测试、
最容易给出 expected output；代价是外部效度有限。

## 4. 非目标

本文明确不做：

- 泛化 agent governance 平台
- 大而全 registry
- 全量跨风味 FDO 映射
- 完整密码学信任基础设施
- 复杂多智能体编排
- 与本文主论点无关的 broad survey

## 5. 成功标准

一个最小方案被视为成功，至少应同时满足以下条件：

- 有 2 个 valid 样例与 5 个 invalid 样例
- 每个 invalid 只故意破坏 1 条主规则
- validator 输出 JSON、摘要与 error code
- demo 闭环从对象载入到验证结果输出完整跑通
- 工件能被 release 和 DOI 锚定

## 投稿前待补

- 是否把“research questions”显式写入该章；当前可不写
- 是否加入 formal requirements notation；如加入，必须保持最小化
