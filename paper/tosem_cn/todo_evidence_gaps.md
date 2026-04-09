# 投稿前待补的证据缺口

## 已解决的证据缺口

当前仓库已经补齐了本文最核心的最小证据面，因此论文不再是“概念提案”，而是一个可运行、
可测试、可归档的 methodology + validator + artifact 草稿。已解决的部分包括：

- 最小 profile 已有规范与 JSON Schema，可以明确表达单 operation accountability statement。
- validator 已有 reference implementation、CLI 入口和测试，可输出 machine-readable JSON、
  人类可读摘要与明确 error code。
- 样例集已具备 2 个 valid 与 5 个 invalid，且每个 invalid 只故意破坏 1 条主规则。
- 单链路 demo 已闭环，能从对象载入一路走到 validation report 输出。
- 当前论文工作区已补齐主稿、图表源、对比表、artifact 表与 DOI/version 审计说明。
- 当前 package 的 GitHub Release `v0.2.0` 与 Zenodo DOI `10.5281/zenodo.19334062`
  已被核实，可作为当前投稿版本的 release / archive 锚点。

## 部分解决但仍偏弱的缺口

这些部分已经有初步支撑，但对于更强的 TOSEM 投稿仍偏弱：

- invalid-example 覆盖面仍然偏窄。
  当前 5 个 invalid 已覆盖必填字段、引用闭合、policy link、不一致的 provenance/output
  绑定，以及 validation/provenance 引用闭合；但还没有覆盖更细的责任点失败，例如
  input/output role mismatch、digest mismatch、duplicate identifier 等。
- cross-implementation portability 仍然偏弱，但已不再只有旁证。
  当前 OAP 主路径除了 demo、CLI 和 examples 之外，已经有第二个 valid context，说明同一
  最小 profile 在第二种对象/operation 语境下仍可稳定通过；不过这还只是 basic portability
  evidence，而不是广泛的跨框架验证。
- 与 ordinary logs / provenance-only / policy-only 的比较，当前主要是概念对比。
  表 1 已经建立了问题框架，但还没有一个足够短、足够具体的同案对照分析。
- evaluation 已经有 conformance 和 reproducibility 证据，但还不够厚。
  当前最强证据来自样例、tests、demo 和 release/DOI；还缺一个更凝练的命令-结果矩阵，
  把这些已存在证据更集中地组织出来。

## 冲击更强 TOSEM 投稿前仍缺的证据

如果目标是把当前稿件从“可提交”推向“更有说服力”，仍缺的不是更长正文，而是更厚一点但仍然
受控的实证层：

- 更广的 invalid-example 覆盖。
  需要在不扩大 profile 范围的前提下，再补 2 到 3 个只破坏单条主规则的 invalid 样例，
  让 validator 的 failure taxonomy 更稳。
- 更厚一点的 portability 组织。
  当前已经有第二个 valid context，但仍缺一个更清楚的 portability mini-matrix，把
  profile-stable 字段与 implementation-specific 字段分开呈现。
- 更锋利的 comparative case analysis。
  需要基于同一个 metadata enrichment 小场景，明确指出 ordinary logs、
  provenance-only、policy-only 与本文方法分别能回答和不能回答的问题。
- 更厚但不虚构的 evaluation 组织。
  需要把现有 tests、CLI 输出、demo 结果和 release/archive 信息整理成更像论文评估材料
  的表格或附录，而不是继续停留在分散文档中。

## 最低成本下一步动作

1. 新增 2 个 invalid 样例并补测试。
   建议优先补 `input/output role mismatch` 和 `integrity digest mismatch`，因为它们直接扩展
   validator 的主失败类别，而且只需要沿用现有 schema、examples 和 test 结构。
2. 新增一个 portability mini-matrix。
   只基于当前两个 valid 样例、demo 产物和现有字段结构，整理哪些字段是 profile-stable，
   哪些字段属于 implementation-specific，把 second-context validity evidence 组织得更清楚。
3. 在主稿中补一个同案比较小节。
   直接围绕当前 metadata enrichment 场景，用半页文字把 ordinary logs、
   provenance-only、policy-only 与本文方法放到同一问责问题上比较。
4. 新增一个 evaluation 命令-结果汇总表。
   只复用现有 `pytest`、CLI 和 demo 输出，把已存在的验证证据收束成论文可直接引用的表格。
5. 在主稿 discussion 中补一个更明确的边界句。
   直接写清楚：第二个 valid 只增强 basic portability evidence，不代表 broad
   cross-framework validation，避免审稿时被误读为过度主张。
