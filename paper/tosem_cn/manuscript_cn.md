# 面向 FDO 智能体系统操作问责的最小可验证 Profile: 方法、Validator 与工件包

对应分稿：
[标题摘要](./00_title_abstract_keywords.md) |
[提纲](./01_outline.md) |
[引言](./02_introduction.md) |
[问题与目标](./03_problem_and_design_goals.md) |
[最小 Profile](./04_minimal_profile.md) |
[验证模型与 Validator](./05_validation_model_and_validator.md) |
[Artifact Package](./06_artifact_package.md) |
[Evaluation](./07_evaluation.md) |
[Discussion](./08_discussion_limits_threats.md) |
[同案比较](./comparative_case_analysis.md) |
[Related Work Scaffold](./09_related_work_scaffold.md) |
[Conclusion](./10_conclusion.md)

## 图表索引（草案）

- 图 2：最小可验证 profile 结构，突出 operation 是 accountability center
  - 源文件：`./figures/fig2_profile_structure.mmd`
- 图 6：两层 validator workflow
  - 源文件：`./figures/fig6_validator_workflow.mmd`
- 图 7：artifact closure，从 spec 到 release / DOI
  - 源文件：`./figures/fig7_artifact_closure.mmd`
- 表 1：方法类别对比
  - 源文件：`./tables/table1_method_comparison.md`
- 表 2：artifact 状态
  - 源文件：`./tables/table2_artifact_status.md`
- 表 3：样例验证摘要
  - 源文件：`./tables/table3_validation_summary.md`
- 表 4：基础可迁移性迷你矩阵
  - 源文件：`./tables/table4_portability_mini_matrix.md`

## 摘要

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
`10.5281/zenodo.19334062`。与此同时，论文明确标注其范围边界：仅覆盖单 operation
statement，未覆盖复杂多智能体编排、完整密码学信任基础设施、或跨框架大规模经验评估。

关键词：FDO；智能体系统；操作问责；provenance；evidence；validator；artifact

## 1. 引言

AI 智能体系统已经能够持续产生日志、trace 和运行事件，但这些材料通常只服务于调试、
追踪或运维观察。对于面向 FDO 的对象流转场景，真正需要回答的常常是另一组更窄的问题：
谁执行了某个 operation，作用到了哪个对象，受到什么 policy 约束，输入与输出对象如何
被引用，产生了哪些 evidence，以及第三方如何独立复核这一 statement。仅有运行日志，
通常不足以把这些问题压缩为一个可以交换、验证和复现的对象级表述。

当前仓库围绕这个 accountability gap 提供了一个克制的实现路径。它没有扩展成泛化治理
平台，没有新造 registry，也没有试图一次性完成全部 FDO 映射。相反，仓库将问题收缩为
“单 operation accountability statement 的最小可验证闭环”，并据此补齐了 profile、
schema、样例、validator、CLI、demo 与交付文稿。

基于当前工作区能够核实的材料，本文报告三项贡献：第一，提出并实现一个最小可验证 profile，
将操作问责收缩为单 statement 的对象模型；第二，提供一个 profile-aware validator，
在 schema 之外继续检查引用闭合、关联一致性与最小 integrity；第三，将这些内容冻结为
一个可以通过 release 与 DOI 锚定的 artifact package。本文不声称已完成一般意义上的
标准化，也不把当前工作包装为完整治理平台。

## 2. 问题定义与设计目标

本文解决的问题不是“如何完整治理智能体系统”，而是更小、更硬的一个子问题：在一个
FDO-based agent system 中，如何把一次具体 operation 组织成一个最小但可验证的
operation accountability statement，使第三方能够检查 actor、subject、operation、
policy、输入输出引用、evidence 与 validation 路径。

围绕这一问题，本文坚持五个设计目标：最小而非完备、可验证而非仅可描述、复用现有仓库表面、
面向 artifact 复现、以及面向 FDO 语境但不试图一次解决全部映射。由此带来的关键取舍是：
采用 profile 而不是平台、采用 staged validation 而不是一次性展开全部次生错误、采用
单链路 demo 而不是多场景堆叠。

本文明确不做泛化 agent governance 平台、不做大而全 registry、不做全量跨风味 FDO
映射、不做完整密码学信任基础设施，也不做复杂多智能体编排。成功标准也因此被压缩为：
2 个 valid 样例、5 个单点破坏 invalid 样例、可执行 validator、闭环 demo、以及可发布
工件包。

表 1 汇总了本文与 ordinary logs、provenance-only、policy-only、audit trails 之间的
问题面差异。这里的对比是方法边界对比，而不是文献效果排名；它的作用是说明本文为什么坚持把
operation、policy、provenance、evidence 和 validation 固定进同一个最小 profile。
为避免表 1 悬空，本文另用 `retention review` 场景补了一段同案比较，见
`comparative_case_analysis.md`。

## 3. 最小 Profile

当前仓库定义的 profile 名称为
`execution-evidence-operation-accountability-profile`，版本为 `0.1`。其顶层必需部分包括
`profile`、`statement_id`、`timestamp`、`actor`、`subject`、`operation`、
`policy`、`constraints`、`provenance`、`evidence` 和 `validation`。本文持续采用的
核心结构是 `operation / policy / provenance / evidence / validation`；`actor`、
`subject` 和 `constraints` 用于补齐最小上下文。

在对象模型上，`operation` 记录具体动作与结果，`policy` 记录 governing policy 及其
constraint refs，`provenance` 串联 actor、subject、operation 与 I/O refs，
`evidence` 收纳 references、artifacts 与 integrity digest，`validation` 则标识第三方
验证路径。规范同时要求一组明确的链接规则，例如 `operation.subject_ref` 必须等于
`subject.id`，`policy.constraint_refs[]` 必须解析到 `constraints[].id`，
`operation.input_refs[]` 与 `operation.output_refs[]` 必须解析到
`evidence.references[].ref_id`，以及 `validation` 中各类 ref 必须落到本地对象。

样例集进一步把这些规则具体化。当前仓库提供 2 个 valid 样例和 5 个 invalid 样例：
一个 valid 对应 metadata enrichment 场景，另一个 valid 对应 retention review 场景，
并展示第二种 input linkage 形态。5 个 invalid 分别覆盖：缺失 `validation.method`、
output ref 不闭合、`evidence.policy_ref` 与 `policy.id` 不一致、`provenance.output_refs`
与 `operation.output_refs` 不一致、以及
`validation.provenance_ref` 不可解析。每个 invalid 样例只打破 1 条主规则，因此既服务于
profile 设计，也直接服务于 validator 的可解释失败输出。与最初的最小路径相比，这组样例
增强了 failure-boundary coverage；第二个 valid 样例则提供了 basic portability evidence，
但这并不等于 broad cross-framework validation。

图 2 给出该最小 profile 的结构关系：`operation` 位于 accountability center，周围由
`policy`、`provenance`、`evidence` 和 `validation` 构成最小可验证闭环。

## 4. 验证模型与 Validator

validator 已落地在 `agent_evidence/oap.py` 与 `agent_evidence/cli/main.py` 中，并通过
`agent-evidence validate-profile <file>` 暴露为 CLI。其验证流程采用四阶段设计：

1. `schema`：检查结构完整性、字段形状与必填字段。
2. `references`：检查本地引用闭合与标识符重复。
3. `consistency`：检查 policy / provenance / evidence 的语义一致性。
4. `integrity`：重算 `references_digest`、`artifacts_digest`、`statement_digest`。

该 validator 的输出是一个 validation report，包含 `ok`、`profile`、`source`、
`issue_count`、`stages` 和 `summary`。当验证成功时，`summary` 只输出一行 `PASS ...`；
失败时则输出一行 `FAIL ...` 和逐条错误摘要。当前仓库已通过样例与测试展示若干主错误码，
如 `schema_violation`、`unresolved_output_ref`、`unresolved_evidence_policy_ref`。

之所以称其为 “profile-aware”，不是因为它仅仅读取了一个 schema 文件，而是因为它显式
执行了该 profile 的固定身份检查、引用规则检查、一致性规则检查与 digest 重算逻辑。

图 6 将 validator 的执行过程收束为两层：先做 structural conformance，再做
accountability conformance，最后落到 error classification 与主错误码输出。

## 5. Artifact Package

当前 artifact package 已由仓库中的方法、样例、验证器、测试、demo 和交付文档共同构成。

### 研究工件索引（草案）

- profile spec：`spec/execution-evidence-operation-accountability-profile-v0.1.md`
- JSON Schema：`schema/execution-evidence-operation-accountability-profile-v0.1.schema.json`
- valid / invalid examples：`examples/`
- reference validator：`agent_evidence/oap.py`
- CLI：`agent_evidence/cli/main.py`
- tests：`tests/test_operation_accountability_profile.py`、`tests/test_cli.py`
- demo：`demo/run_operation_accountability_demo.py`
- release / archive 锚点：GitHub Release `v0.2.0`、Zenodo DOI `10.5281/zenodo.19334062`
核心入口包括：

- `spec/execution-evidence-operation-accountability-profile-v0.1.md`
- `schema/execution-evidence-operation-accountability-profile-v0.1.schema.json`
- `examples/` 中的 2 个 valid 与 5 个 invalid 样例
- `agent_evidence/oap.py` 与 `agent_evidence/cli/main.py`
- `tests/test_operation_accountability_profile.py`
- `demo/run_operation_accountability_demo.py`
- `submission/package-manifest.md` 与 `submission/release-readiness-check.md`

从 artifact reviewer 的角度，最小复现路径是先运行 `agent-evidence validate-profile`
检查样例，再运行 `python3 demo/run_operation_accountability_demo.py`，最后检查
`demo/artifacts/` 里的 evidence 与 validation report。

图 7 将这一闭环进一步组织为 artifact closure：从 profile spec、JSON Schema、
valid/invalid examples、reference validator、CLI、tests、demo 一直收束到
release / DOI。

表 2 汇总当前仓库中每一项核心 artifact 的状态，并区分“仓库内已存在”和“通过外部元数据已核实”
这两类证据来源。

发布与归档层面，当前工作区已经可核实本地 tag `v0.2.0`，`git show v0.2.0` 显示该 tag
冻结了 OAP v0.1 package。进一步通过 GitHub Release API 与 DataCite API，可以核实公开
release `Agent Evidence v0.2.0` 以及 Zenodo DOI `10.5281/zenodo.19334062`。需要如实
说明的是，仓库内部仍保留历史 specimen 轨道的旧 DOI `10.5281/zenodo.19055948` 文案；
当前 package 与历史 specimen 已在公开文档中按双轨口径分开说明。

## 6. Evaluation

本文不虚构仓库之外的实验数据，因此 evaluation 仅报告当前仓库可直接支撑的内容。首先，
样例层已经形成一组最小但闭合的规则验证面：2 个 valid 与 5 个单点破坏 invalid。其次，
`tests/test_operation_accountability_profile.py` 直接覆盖 valid/invalid 样例与 CLI
输出。当前工作区复验命令：

```bash
./.venv/bin/python -m pytest \
  tests/test_operation_accountability_profile.py \
  tests/test_aep_profile.py \
  tests/test_cli.py
```

返回 21 项测试通过，并带 1 条已知 non-blocking warning。该 warning 与 Python 3.14
环境下的 `langchain_core` 有关，仓库现有状态文档已将其说明为不影响当前 minimal path。
表 3 将当前样例层验证面压缩成一张 reviewer 友好的摘要表，直接标出 valid / invalid、
场景 / 失败模式、预期结果与主错误码。

再次，demo 闭环验证命令：

```bash
python3 demo/run_operation_accountability_demo.py
```

会按“对象载入/创建 -> profile 预检查 -> operation 调用 -> evidence 生成 ->
validator 验证 -> 输出结果”六个步骤运行，并最终生成 `minimal-profile-evidence.json`
和 `validation-report.json`。发布层面，`v0.2.0` release 与 DOI 进一步说明该工件已经
进入可发布、可引用、可归档状态。

第二个 valid 样例把“通过边界”扩展到第二语境，因此能支撑 basic portability evidence；
但当前仓库不能直接支撑的主张仍包括：跨框架广泛通用性已被系统验证、与其他方案的对照实验、
用户研究、以及大规模性能评测。本文不会把这些写成既成结果。

为补足比较论证的落点，本文还固定使用 `valid-retention-review-evidence.json` 做一个小型
同案比较：ordinary logs、provenance-only 与 policy-only 在该场景下都能覆盖部分能力，
但只有本文 profile 把 operation、policy、provenance、evidence 与 validation 绑定成
一个可独立验证的最小责任单元。这个比较是结构性的 qualitative case analysis，而不是
实验性优越结论。

表 4 则把当前 portability 证据压缩为一个小矩阵，明确区分“现在能支持的 basic portability
evidence”和“仍不能支持的 broad cross-framework validation”。

## 7. 讨论、局限与威胁

本文最大的设计选择不是“做了很多”，而是“明确不做很多”。当前 profile 只覆盖单
operation statement，只提供最小 integrity 面，只给出一个 metadata enrichment demo，
且相关工作与 comparative evaluation 尚未完成。这些都限制了外部效度，但同时也是当前
工作能够保持清晰边界和稳定 artifact 的原因。

有效性威胁主要体现在四处。构造效度上，本文把“操作问责”具体化为一组字段与规则；
若读者讨论的是组织治理或非抵赖性，本文定义会显得过窄。内部效度上，样例、validator
与 demo 来自同一仓库实现。外部效度上，目前只有一个核心 demo 场景。发布包装效度上，
仓库内部尚有旧 DOI 文本残留，需要与外部归档同步。

正确的后续扩展顺序应是：先增补受控样例，再补 validator 测试，再明确与历史 AEP /
Execution Evidence Object 表面的桥接关系，最后才讨论更大范围的 FDO 映射与生态层。

## 8. Related Work

本稿当前只保留 related work 的紧凑骨架，正式引文投稿前待补。建议收束为五个方面：

- FDO 与对象级可验证性
- provenance 与执行证据建模
- runtime tracing / observability 与 accountability 的差异
- conformance profile 与 validator
- reproducible artifact 与 software archive

related work 的最终目的不是做 broad survey，而是给出一个非常具体的定位：现有工作分别
覆盖对象、provenance、tracing、validation 或 artifact 的某些侧面；本文的增量在于，
把这些需求压缩为一个面向单 operation accountability statement 的最小可验证 profile，
并给出与之同仓冻结的 validator 与 artifact package。为避免这一判断停留在抽象层，
本文将 `retention review` 场景的同案比较作为表 1 和 related work 之间的桥接材料。

## 9. 投稿前待补强项

当前稿件的主干已经稳定，投稿前最值得补强的不是更长的叙述，而是更厚一点的证据层。具体说，
优先级最高的补强面有四个：

- 如需进一步增强 failure-boundary 说服力，可再补少量只打破单条主规则的 invalid 样例，
  但不应把样例集扩展成新的研究方向。
- 如需进一步增强 portability 说服力，可再补一个受控的第三语境 valid 样例，
  但当前稿件已经具备 basic portability evidence。
- 将现有 comparative case analysis、表 3 与表 4 进一步压缩到投稿版长度，但不新增未验证结论。
- 如果需要更强 appendix，可补一页命令摘录或验证报告摘录，但不虚构新的实验结果。

这些补强都应当继续沿用当前 mainline，不应把工作扩展成 broad FDO survey、泛化治理平台
或新的研究方向。

## 10. 结论

本文围绕一个非常克制的目标展开：不是为 FDO-based agent systems 构造一个通用治理平台，
而是补齐一个最小可验证单元，用于表达和验证一次具体 operation 的 accountability
statement。当前仓库已经给出这一目标所需的最小闭环：profile、schema、样例、
profile-aware validator、CLI、单链路 demo，以及 release / handoff / archive 表面。

从方法学上看，本文主张对于 FDO 场景，最先需要稳定下来的不是宏大的治理叙事，而是一个
可以回答“谁、对什么对象、在什么 policy 下、做了什么、留下了什么 evidence、如何被验证”
的最小对象。从工程上看，validator 与 demo 使这一对象从规范层落到可执行验证和 artifact
审查路径。投稿前仍需补齐的内容主要集中在 related work 引文、artifact 章节与仓库 DOI
文本同步、以及超出当前仓库证据面的 comparative evaluation。
