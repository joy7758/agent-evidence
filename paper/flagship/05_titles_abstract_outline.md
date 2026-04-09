# 标题、摘要骨架与提纲

## Candidate Titles

1. **Operation Accountability as a First-Class Verification Boundary for Machine-Actionable Object Systems**
2. **Defining the Minimal Verification Boundary for Operation Accountability in FDO-Based Agent Systems**
3. **From Execution Evidence to Verification Boundary: Operation Accountability across FDO, STAP, and Data Space Contexts**

## 推荐标题

推荐使用标题 1。

理由很简单：

- 它直接把论文主张固定在 `first-class verification boundary` 上，而不是滑回 implementation naming。
- 它保留了固定英文 thesis sentence 的核心力度。
- 它允许正文再用 FDO-based agent systems 与 STAP / data space context 收紧语境，而不把标题绑死在当前仓库实现表面。

如果目标 venue 更偏好窄标题，再退到标题 2。

## 当前主稿基线

当前 manuscript-core drafting 应以下列文件为主基线，而不是继续直接扩写本文件中的 skeleton：

- `paper/flagship/29_abstract_integrated.md`
- `paper/flagship/25_introduction_integrated.md`
- `paper/flagship/26_problem_boundary_failure_core.md`
- `paper/flagship/21_validation_section_integrated.md`
- `paper/flagship/27_conclusion_integrated.md`
- `paper/flagship/28_full_manuscript_spine.md`

## Abstract Skeleton (English)

Machine-actionable object systems in FDO-based agent systems and adjacent STAP and data space settings increasingly allow agents to act directly on digital objects, yet current execution records do not define what must be externally verifiable for one concrete operation.

This paper frames that gap as an operation-accountability problem: a single operation should be representable as a bounded statement that binds actor identity, target object, operation semantics, policy basis, provenance closure, evidence continuity, and a validation path.

We argue that logs, provenance, policy expressions, and audit trails remain important but partial surfaces; none of them alone defines the minimal verification boundary required for independent checking.

We then define that boundary, derive a failure taxonomy covering identity, target, policy, evidence, outcome, temporal, and implementation-coupling failures, and bound the current validation claim to a five-scenario corpus, a fixed same-case comparison, and a two-checker comparison over a frozen 19-file corpus.

The current TOSEM artifact line is used as the smallest working witness rather than the final claim: it shows that a minimal profile-aware validator, controlled example corpus, and closed demo can be built.

The flagship contribution is therefore not another profile proposal, but a problem definition and verification framing for operation accountability, together with an evidence-bounded validation package that exposes where existing validation surfaces still stop.

说明：

- 上述 abstract skeleton 仍保留为作者比较稿。
- 当前更接近 manuscript 使用状态的 abstract 版本，见 `paper/flagship/29_abstract_integrated.md`。

## 中文白话摘要

这篇旗舰论文不应该再讲“我们做了一个 profile 和 validator”，而应该讲清楚：只要 agent 已经能对机器可操作对象执行动作，operation accountability 就不是日志里的附带细节，而是一条必须被单独定义的 first-class verification boundary。logs、provenance、policy、audit trail 都重要，但它们通常分散在不同表面，不能直接组成一个可外部复核的最小 statement。论文的任务，是先定义这条最小边界，再说明边界缺失时会出现哪些稳定 failure classes，再用当前 frozen validation package 给出 evidence-bounded 的验证支撑。当前 TOSEM 工件在这里的作用，是证明这条边界不是空想，而是已经有一个 smallest working witness。

## 旗舰论文提纲

1. **Introduction**
   - 提出主张：operation accountability 是 verification boundary，不是 logging detail。
2. **Context and Problem Scope**
   - 交代 FDO / STAP / data space 语境。
   - 明确只讨论 single-operation accountability。
3. **Why Existing Surfaces Are Not Enough**
   - 分析 logs、provenance、policy、audit trail 的边界。
4. **Minimal Verification Boundary**
   - 给出边界定义、组成部分与最小性判据。
5. **Failure Taxonomy**
   - 给出 v1 taxonomy，并说明为什么 failure classes 是问题定义的一部分。
6. **Current TOSEM Artifact as Smallest Working Witness**
   - 说明当前仓库证明了什么，没证明什么。
7. **Validation**
   - multi-scenario corpus、same-case comparison、two-checker comparison、current evidence boundary。
8. **Related Work**
   - 把 profile、conformance、validation、provenance、audit trail 放回方法边界里比较。
9. **Discussion and Limits**
   - 明确不扩展成 broad governance platform，并收紧 external validity claim。
10. **Conclusion**
   - 重申这是 first-class verification boundary，而不是 another profile paper。

当前 section spine 以 `paper/flagship/28_full_manuscript_spine.md` 为准。

## 写作提醒

- 标题、摘要、引言都要先讲 problem definition，再讲 artifact witness。
- TOSEM 的 profile / validator / demo 只能作为证据，不应重新成为旗舰稿的主角。
- validation 的表述必须以 frozen run archive、same-case pack 与 two-checker comparison 为边界。
- 绝不把 portability、external validity、independent implementation 说过头。
- `first-class verification boundary` 是主文稳定 thesis；`first-class verification problem` 只能在解释问题上移时有限使用，不应替代 thesis。
