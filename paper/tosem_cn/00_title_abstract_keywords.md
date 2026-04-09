# 标题、摘要与关键词

## 暂定标题

面向 FDO 智能体系统操作问责的最小可验证 Profile:
方法、Validator 与工件包

## 英文标题占位

投稿前待补：
Minimal Verifiable Profile for Operation Accountability in FDO-Based Agent Systems:
Methodology, Validator, and Artifact Package

## 中文摘要

面向 FDO 的智能体系统不仅需要记录运行轨迹，还需要回答一个更窄但更关键的问题：某个
actor 在什么 policy 约束下，对哪个 subject 执行了什么 operation，留下了哪些
evidence，以及第三方如何独立验证该 statement。当前仓库围绕这一 accountability gap，
提供了一个刻意收缩的问题定义与实现闭环，而不是一个泛化的治理平台。本文以仓库中已落地
的 `Execution Evidence and Operation Accountability Profile v0.1` 为核心，提出一个
面向单操作 statement 的最小可验证 profile，并给出与其配套的 profile-aware validator
与可复现实物包。

该 profile 以 `operation / policy / provenance / evidence / validation` 为核心结构，
并在最小上下文中保留 `actor`、`subject`、`constraints`、`profile` 和 `timestamp`
等必要字段。仓库当前实现同时提供：一份 profile 规范、一份 JSON Schema、2 个 valid
样例、5 个各自只破坏 1 条主规则的 invalid 样例、集成到现有 Python/CLI 表面的
validator、以及一条从对象载入、profile 预检查、operation 执行、evidence 生成到
validator 验证的单链路 demo。validator 采用 staged validation，至少覆盖结构完整性、
必填字段、引用闭合、以及 policy / provenance / evidence 关联一致性，并补充最小
integrity digest 重算。其输出同时包含机器可读 JSON、人类可读摘要与明确 error code。

本文的贡献不是宣称标准已经被外部采纳，也不是构建一个大而全的 FDO 映射与治理框架；
本文的贡献是把“操作问责”压缩为一个可运行、可测试、可发布、可归档的最小方法学单元。
当前仓库已经形成 GitHub Release `v0.2.0`，并存在对应的 Zenodo 归档 DOI
`10.5281/zenodo.19334062`。与此同时，论文仍将明确标注当前范围边界：仅覆盖单 operation
statement，未覆盖复杂多智能体编排、完整密码学信任基础设施、或跨框架大规模经验评估。

## 中文关键词

- FDO
- 智能体系统
- 操作问责
- provenance
- evidence
- validator
- JSON Schema
- artifact paper

## 投稿前待补

- TOSEM 最终标题长度与副标题风格
- 英文摘要与关键词
- 图 1、表 1 在摘要中的引用是否需要前置
