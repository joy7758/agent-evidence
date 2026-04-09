# 同案比较：retention review 场景下的四种表达方式

## 1. 场景说明

本文选用当前仓库已存在的 `valid-retention-review-evidence.json` 作为同案比较场景。该场景中，
一个 `retention-reviewer` 智能体在 `policy:retention-review-v1` 约束下，对
`obj:dataset-package-042` 执行一次 `retention.review` operation；它读取两个输入引用
`ref:input-dataset` 与 `ref:input-retention-ticket`，并生成一个输出引用
`ref:output-retention-decision`。这个场景保持了本文当前 scope：单 operation statement、
最小 policy 绑定、最小 provenance 链接、最小 evidence，以及独立 validation 路径。

## 2. 用 ordinary logs 表达会得到什么

如果用 ordinary logs 表达该场景，通常可以记录时间戳、运行消息、函数调用片段、输入文件路径、
输出对象 locator，甚至可以看出某个 agent 曾执行过一次 retention review。它对于调试、追踪
执行顺序、排查运行异常是有价值的。

但 ordinary logs 仍难以独立建立一个稳定的 operation accountability unit。它通常不能保证：
`operation` 被显式建模为问责中心；`policy` 与这次具体执行之间有明确绑定；输入输出对象引用
已经闭合；最小 execution evidence 已被收束为可交换对象；第三方能够沿着固定 validation
path 独立复核。换言之，ordinary logs 能“记事”，却不自动形成一个可外部验证的最小 statement。

## 3. 用 provenance-only 表达会得到什么

如果用 provenance-only 表达该场景，通常可以较好地表达对象之间的来源关系，例如哪个 actor
参与了操作、哪个 subject 被处理、哪些输入对象导出了哪个输出对象。对于回答“这个输出从哪里来”
这样的问题，provenance 结构是有力的。

但 provenance-only 仍不足以独立建立本文要求的 operation accountability。它不必然要求
显式绑定 governing policy，也不必然把最小 execution evidence 收敛为一个可独立交换的
evidence block；更不会天然给出 `validation.method`、`validation.status` 与固定 error code
分类。它能说明“来源链”，却不能单独说明“这次操作在什么 policy 约束下、留下了哪些最小证据、
以及第三方该如何验证”。

## 4. 用 policy-only 表达会得到什么

如果用 policy-only 表达该场景，通常可以清楚说明 retention review 应满足哪些规则，例如只允许
使用批准的 retention class、受限数据集需要升级审查等。对于表达规范要求、控制边界和合规约束，
policy-only 表达是必要的。

但 policy-only 只能说明“应该如何做”，不能独立说明“实际做了什么”。它不能单独建立本次
operation 的 actor、subject、input/output refs、provenance linkage、evidence artifact，
也不能说明第三方验证该 statement 时应检查哪些局部对象与交叉字段关系。因此，policy-only
对于 operation accountability 是部分能力持有者，而不是完整表达。

## 5. 用本文 profile 表达会额外得到什么

本文 profile 的额外价值，不在于替代 logs、provenance 或 policy，而在于把它们在该场景下
最关键的问责要素绑定进同一个最小可验证 statement：`operation` 明确成为问责中心；
`policy` 被显式绑定到本次执行；`provenance` 将 actor、subject 与 input/output refs 串联；
`evidence` 收纳最小 references、artifacts 与 integrity；`validation` 给出第三方验证路径。

因此，在同一个 retention review 场景中，本文 profile 额外提供的是一个可独立交换、可由
validator 复核、并能产生稳定 failure category 的最小责任单元。这个判断是结构性判断，
不是实验性优越结论；它说明本文方法补齐了 operation accountability 所需的最小闭环，而不声称
ordinary logs、provenance-only 或 policy-only 在各自问题面上没有价值。
