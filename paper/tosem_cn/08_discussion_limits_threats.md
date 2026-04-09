# 讨论、局限与威胁

## 1. 为什么要刻意收缩

本文最大的设计选择不是“做了很多”，而是“明确不做很多”。当前仓库把问题收缩为一个
single operation accountability statement，并围绕它提供最小 profile、validator
和 artifact。这样做的收益是边界清楚、验证清楚、复现清楚；代价则是覆盖范围明显受限。

对于 TOSEM 读者，这种收缩应该被理解为方法学立场，而不是暂时性缺陷：如果最小闭环都还
没有被做成稳定工件，那么更大规模的架构叙事往往难以检验。

## 2. 主要局限

### L1. 只覆盖单 operation statement

当前 profile 不覆盖多步骤 workflow，也不覆盖复杂多智能体协调。

### L2. 只提供最小 integrity 面

当前 integrity 只重算 `references_digest`、`artifacts_digest` 和 `statement_digest`。
这足以支撑最小闭环，但不足以构成完整信任基础设施。

### L3. 只提供单链路 demo

当前 demo 采用 metadata enrichment 场景。它适合说明问题，但不能代表所有 FDO-based
agent systems。

### L4. 相关工作与经验评估尚未完成

当前仓库足以支撑 artifact-oriented 论文草稿，但还不足以支撑完整 comparative study。

## 3. 有效性威胁

### T1. Construct validity

本文把“操作问责”具体化为 profile 中的一组字段与规则关系。这个构造本身是方法学选择。
如果读者希望讨论的是组织治理、合规审计全链路、或非抵赖性，那么本文定义过窄。

### T2. Internal validity

当前样例、validator 和 demo 来自同一仓库实现。尽管这保证了最小闭环一致，但也意味着
“规则设计者”和“规则实现者”尚未分离。

### T3. External validity

当前仍只有一个核心 demo 场景，但样例集已经补到第二个 valid context。这个变化增强了
basic portability evidence，却还不足以把结论外推到更广的操作类型或运行框架。
表 4 把这种“能支持什么、仍不能支持什么”的边界直接写成了迷你矩阵，因此 external validity
的口径现在更容易保持克制，也更不容易被误读成 broad portability claim。

### T4. Release packaging validity

当前外部 release 与 DOI 已存在，但仓库内部仍有旧 DOI 文本残留。这不会推翻工件存在性，
但会影响 artifact 叙述的一致性。

## 4. 这项工作的正确扩展方向

如果要继续扩展，正确顺序应当是：

1. 增补更多受控场景样例
2. 保持 profile 不膨胀的前提下补更多 validator 测试
3. 明确与现有 AEP bundle / 历史 Execution Evidence Object 表面的桥接关系
4. 在真正需要时再讨论更大范围的 FDO 映射与生态集成

不建议的扩展方向是：立即把当前工作包装成全栈治理平台或宏大标准化方案。

## 投稿前待补

- threat-to-validity 表格化版本
- 是否需要在 discussion 中单列“ethics / compliance”说明；当前证据不足，不建议扩写
