# 旗舰论文总定位

## 一句话 thesis

在 FDO / STAP / data space 这一类 machine-actionable object systems 中，operation accountability 应被定义为一次具体 operation statement 的最小验证边界，而不是散落在 logs、policy、provenance 与 audit trail 里的事后描述。

## 固定英文主张

Operation accountability is not a logging detail but a first-class verification boundary for machine-actionable object systems.

## 直白解释

如果 agent 已经可以直接对对象执行机器可操作的动作，那么外部复核者真正需要的，不只是“系统记了什么日志”，而是“能不能拿到一个小而完整的 statement，独立判断这次操作是否可验证”。这个 statement 至少要能回答：

- 谁执行了操作；
- 对哪个对象执行；
- 执行的 operation 是什么；
- 依据了什么 policy 与 constraints；
- 输入输出引用是否闭合；
- 留下了什么 evidence；
- 第三方如何 validation。

如果这些条件必须依赖原运行时、内部数据库或实现细节才能拼出来，那么系统只是可执行，不是外部可验证。

## 为什么 TOSEM 论文不等于旗舰论文

TOSEM 当前最适合承担的是一个 methodology + validator + artifact paper 的角色。它回答的是一个较小的问题：最小 profile、profile-aware validator、样例集、demo 和 artifact package 能不能被明确规定、实现、测试并冻结为可复现工件。

旗舰论文要回答的是更上位的问题：为什么在 machine-actionable object systems 中，operation accountability 必须被定义为一个 first-class verification problem；这个问题的最小验证边界是什么；如果边界缺失会出现哪些稳定 failure classes；要把这个问题做成有说服力的研究结论，还需要哪些 external validation。

因此，TOSEM 是最小实现、stake-in-the-ground、smallest verifiable artifact。旗舰论文则应该是 problem-defining paper。

## 研究问题

1. 在 FDO-based agent systems 及其相邻的 STAP / data space 语境中，一次 operation accountability statement 的最小 verification boundary 到底是什么？
2. 为什么 logs、provenance、policy、audit trail 都重要，但都不足以单独构成这个 boundary？
3. 当这个 boundary 缺失、断裂或被实现细节绑死时，会出现哪些可归纳、可检查、可复现的 failure classes？
4. 要把“operation accountability 是一等验证问题”从仓库内方法学主张推进为旗舰论文结论，还需要哪些 external validation、independent checker 与 multi-scenario evidence？

## 主要贡献

1. 把 operation accountability 从“日志细节”上移为“verification boundary”问题，并给出清晰的问题定义。
2. 给出一个最小边界模型，解释为什么 `operation / policy / provenance / evidence / validation` 必须被绑定为同一个外部可检查单元。
3. 基于当前 invalid cases 与 validator error surface，整理出一个可继续扩展的 failure taxonomy v1。
4. 明确 TOSEM 与旗舰论文的分工，并给出面向 external validity、independent checker、comparison strength 与 portability 的执行路线。

## 术语约束

- 仓库当前的主术语仍然是：`operation accountability statement`、`minimal verifiable profile`、`profile-aware validator`、`policy / provenance / evidence / validation`。
- 旗舰论文中的 `machine-actionable object systems` 是总括性 framing，用来容纳 FDO / STAP / data space 语境，不替换仓库当前 `FDO-based agent systems` 的用法。
- 本轮不进入 broad digital persona narrative，也不扩展成泛化治理平台。
