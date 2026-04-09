# 引言

## 1. 问题背景

AI 智能体系统已经能够持续产生日志、trace 和运行事件，但这些材料通常只服务于调试、
追踪或运维观察。对于面向 FDO 的对象流转场景，真正需要回答的常常是另一组更窄的问题：
谁执行了某个 operation，作用到了哪个对象，受到什么 policy 约束，输入与输出对象如何
被引用，产生了哪些 evidence，以及第三方如何独立复核这一 statement。仅有运行日志，
通常不足以把这些问题压缩为一个可以交换、验证和复现的对象级表述。

当前仓库围绕这个 accountability gap 提供了一个非常克制的回答。它没有扩展成泛化治理
平台，没有新造 registry，也没有试图一次性完成全部 FDO 映射。相反，仓库将问题收缩为
“单 operation accountability statement 的最小可验证闭环”，并据此补齐了 profile、
schema、样例、validator、CLI、demo 与交付文稿。

## 2. 本文切入点

本文聚焦 `Execution Evidence and Operation Accountability Profile v0.1`。该 profile
在仓库中已经有明确规范、JSON Schema 与对应实现。它围绕
`operation / policy / provenance / evidence / validation` 五个核心部分组织最小
statement，同时保留 `actor`、`subject`、`constraints` 和 `timestamp` 等必要上下文。
与“记录所有可能元数据”的思路不同，这一设计明确把目标限定为：支持第三方对一次具体
操作进行独立复核，而不是为未来所有治理需求预留无上限扩展面。

仓库实现对应的 validator 已集成到现有 Python 包与 CLI 中。校验逻辑并非只做 JSON
Schema 过检，而是采用分阶段策略，进一步检查内部引用闭合、policy/provenance/evidence
一致性，以及最小 integrity digest 的重算结果。与之配套，仓库还提供 2 个 valid 样例、
5 个各自只破坏 1 条主规则的 invalid 样例，以及一条可运行的 metadata enrichment
单链路 demo。

## 3. 仓库已支撑的贡献

基于当前工作区可以直接核实的材料，本文拟报告三项贡献：

1. 一个最小方法学单元。仓库中的 profile 规范和 schema 把“操作问责”压缩为一个单操作、
   单 statement、可验证的最小对象模型。
2. 一个 profile-aware validator。仓库中的 `agent_evidence/oap.py` 和
   `agent_evidence/cli/main.py` 给出机器可读 JSON、人类可读摘要和明确 error code 的
   校验入口。
3. 一个可复现实物包。仓库中的样例、测试、demo、release handoff 文档，以及对外归档的
   GitHub Release `v0.2.0` 与 Zenodo DOI `10.5281/zenodo.19334062`，共同构成本文的
   artifact surface。

## 4. 本文不做什么

本文不声称：

- 当前 profile 已经是通用 FDO 标准；
- 当前 validator 已经覆盖复杂多智能体编排；
- 当前工件已经提供完整密码学信任基础设施或非抵赖性；
- 当前仓库已经完成跨框架的大规模经验评估。

这些都不属于本文的目标。本文只论证：在 FDO-based agent systems 的语境下，是否能够用
一个最小 profile、一个 profile-aware validator 和一个可复现实物包，把操作问责问题
从概念讨论推进到可运行、可检查、可归档的层面。

## 5. 证据锚点

本文叙述将以以下仓库事实为主锚点：

- 规范：`spec/execution-evidence-operation-accountability-profile-v0.1.md`
- Schema：`schema/execution-evidence-operation-accountability-profile-v0.1.schema.json`
- 样例：2 个 valid 样例与 5 个 invalid 样例
- Validator：`agent_evidence/oap.py`
- CLI：`agent_evidence/cli/main.py`
- 测试：`tests/test_operation_accountability_profile.py`
- Demo：`demo/run_operation_accountability_demo.py`
- 发布与归档：GitHub Release `v0.2.0`，Zenodo DOI `10.5281/zenodo.19334062`

## 投稿前待补

- related work 的正式引文
- TOSEM 引言中是否需要补一个更短的 motivating example
- 如果投稿版本要求英文引言草稿，需另补英文平行稿
