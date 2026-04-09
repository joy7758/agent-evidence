# 论文提纲

## 定位

- 主目标期刊：TOSEM
- 论文类型：methodology + validator + artifact
- 主论点：面向 FDO 智能体系统操作问责的最小可验证 profile
- 主结构：`operation / policy / provenance / evidence / validation`

## 建议章节

1. 标题、摘要、关键词
   - 对应文件：`00_title_abstract_keywords.md`
   - 目标：用最短篇幅讲清楚问题、方法、validator 和 artifact。
2. 引言
   - 对应文件：`02_introduction.md`
   - 目标：界定 accountability gap，说明为什么本文只做最小闭环。
3. 问题定义与设计目标
   - 对应文件：`03_problem_and_design_goals.md`
   - 目标：给出本文要回答的问题、设计原则与明确非目标。
4. 最小 profile
   - 对应文件：`04_minimal_profile.md`
   - 目标：解释 object model、字段边界、主规则与样例集。
5. 验证模型与 validator
   - 对应文件：`05_validation_model_and_validator.md`
   - 目标：说明 schema + references + consistency + integrity 四阶段校验与 CLI 输出。
6. Artifact package
   - 对应文件：`06_artifact_package.md`
   - 目标：描述 spec、schema、examples、validator、CLI、tests、demo、release 与 DOI。
7. Evaluation
   - 对应文件：`07_evaluation.md`
   - 目标：只报告当前仓库能支撑的验证证据，不虚构额外实验。
8. Discussion / Limits / Threats
   - 对应文件：`08_discussion_limits_threats.md`
   - 目标：压实适用范围，避免滑向泛化治理叙事。
9. Related Work Scaffold
   - 对应文件：`09_related_work_scaffold.md`
   - 目标：搭骨架，不提前填入未核实的引文。
10. Conclusion
   - 对应文件：`10_conclusion.md`
   - 目标：收束到 minimal profile、validator 与 artifact 的三件事。

## 主叙事链

1. 运行日志不等于可复核的操作问责 statement。
2. 对 FDO 场景，最先缺的不是大平台，而是一个最小可验证单元。
3. 本文提出并实现一个单 operation statement 的最小 profile。
4. 该 profile 通过 profile-aware validator 形成可测的规则闭环。
5. 该方法以 artifact package 的形式冻结为可复现仓库与归档对象。

## 建议图表

- 图 1：单链路 demo 闭环
  - 对象载入/创建 -> profile 预检查 -> operation 调用 -> evidence 生成 -> validator 验证 -> 输出结果
  - 投稿前待补：正式制图
- 表 1：最小 profile 的顶层字段与职责
- 表 2：valid / invalid 样例与对应主失败规则
- 表 3：validator 阶段、输入、输出与 error code 类型

## 明确不展开的内容

- 不写成 FDO 全景综述
- 不写成 AI governance 大论文
- 不主张一次解决跨框架全量映射
- 不把当前工作包装成非抵赖或完整信任基础设施

## 投稿前待补

- TOSEM 版式对应的章节名与页数预算
- 图表编号、caption 和交叉引用
- 是否需要加入研究问题编号 RQ1/RQ2；当前不建议强行实验化
