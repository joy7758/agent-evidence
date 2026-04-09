# 引言骨架

## 用途

这份 skeleton 面向旗舰论文引言，不面向 TOSEM 的 methodology + validator + artifact paper。引言要先定义问题，再引入最小验证边界，最后再把 TOSEM artifact 作为 smallest working witness 放进来。

## 段落级结构

### Paragraph 1: Problem surface

- 目标：从 machine-actionable object systems 的现实变化切入。
- 核心内容：
  - FDO / STAP / data space 语境下，agent 已经不只是产生日志，而是在对对象执行可产生后果的操作。
  - 问题不再是“系统有没有记录”，而是“对一次具体 operation，外部第三方到底能验证什么”。
- 结尾句功能：
  - 收束到 single-operation accountability。

### Paragraph 2: Sharp problem statement

- 目标：把 operation accountability 直接定义为论文问题。
- 核心内容：
  - 一次 operation accountability statement 至少要回答 actor、subject、operation、policy、input/output refs、evidence、validation path。
  - 如果这些条件不能在一个局部 statement 中成立，就不能算 external verifiability。
- 结尾句功能：
  - 引出“under-specified”判断。

### Paragraph 3: Why the problem is under-specified

- 目标：说明为什么这个问题长期没有被独立定义。
- 核心内容：
  - 当前实践常把 logs、provenance、policy、audit trail 混在一起讨论。
  - 这些材料都重要，但很少被组织成“最小验证边界”。
  - 结果是系统有记录面，却没有清晰 verification boundary。
- 结尾句功能：
  - 过渡到 existing artifacts only partially cover the problem。

### Paragraph 4: Limits of logs and traces

- 目标：先处理最常见的替代物。
- 核心内容：
  - ordinary logs / traces 适合 observability 和 debugging。
  - 它们通常分散、实现耦合、弱 policy binding、弱 local closure。
  - 它们可以说明发生了很多事情，但不等于一个可被独立检查的 accountability statement。
- 结尾句功能：
  - 明确“not enough”但不贬低其价值。

### Paragraph 5: Limits of provenance, policy, and audit trail

- 目标：把其余 partial surfaces 一次收拢。
- 核心内容：
  - provenance 强在 derivation links，不自动给出 governing policy 与 validation declaration。
  - policy 强在 rule basis，不自动说明 concrete executed operation。
  - audit trail 强在保留记录，但常常过大、过深、过度实现耦合。
  - 共同问题：都只部分覆盖 operation accountability。
- 结尾句功能：
  - 引出核心 tension。

### Paragraph 6: Central tension

- 目标：提出全文的核心 tension。
- 核心内容：
  - 太小，statement 无法验证。
  - 太大，statement 退化成 trace replay、治理平台切片或实现私有审计包。
  - 因此真正的问题是 minimality vs verifiability。
- 结尾句功能：
  - 引出本文 approach。

### Paragraph 7: Approach overview

- 目标：用一句话说明本文怎么回答这个 tension。
- 核心内容：
  - 本文提出把 operation accountability 定义为 minimal verification boundary。
  - 该边界围绕 `operation / policy / provenance / evidence / validation`，并要求 actor、subject、constraints、temporal anchor 等最小支撑条件。
  - 本文同时把 stable failure classes 视为问题定义的一部分，而非实现附录。
- 结尾句功能：
  - 引出 TOSEM artifact 的角色。

### Paragraph 8: Role of the current TOSEM artifact line

- 目标：防止引言滑回 TOSEM 论文。
- 核心内容：
  - 当前仓库和 TOSEM artifact line 的作用，是提供 smallest working witness。
  - 它说明 minimal verifiable profile、profile-aware validator、examples、demo 可以被实现。
  - 但这不是本文最终 claim；本文的 claim 是问题定义和 verification framing。
- 结尾句功能：
  - 引出旗舰论文贡献。

### Paragraph 9: Contributions

- 目标：给出旗舰论文版本的贡献列表。
- 核心内容：
  - 定义 operation accountability 的最小 verification boundary。
  - 解释为什么 existing artifacts only partially cover the problem。
  - 提出 failure taxonomy v1。
  - 给出 external validation agenda，包括 independent checker、multi-scenario coverage、comparison strength、portability claims。
- 结尾句功能：
  - 转入 implication。

### Paragraph 10: Implication and scope discipline

- 目标：讲清楚这篇 paper 的意义和边界。
- 核心内容：
  - implication：把 accountability 从 logging detail 上移为 first-class verification problem。
  - scope：不进入 digital persona narrative，不扩展成 broad governance platform，不声称现已完成普遍标准化。
  - 强调本文只处理单 operation 的 verification boundary，但这是更大系统可信性的基础层。
- 结尾句功能：
  - 用固定英文 claim 收尾，或作为 paragraph closing sentence。

## 建议的引言收尾句

- 中文：
  - 因而，本文主张的并不是再增加一种描述执行的 artifact，而是把 operation accountability 明确提升为 machine-actionable object systems 中一条不可省略的最小验证边界。
- English:
  - Operation accountability is not a logging detail but a first-class verification boundary for machine-actionable object systems.

## 写作提醒

- Paragraph 1-3 先定义问题，不要先讲仓库。
- Paragraph 4-6 讲 partial coverage 和 central tension，不要写成 related work survey。
- Paragraph 7-8 才引入当前 artifact line，而且必须明确其 witness 角色。
- Paragraph 9-10 再给贡献与 implication，避免重新落回 TOSEM 的 artifact-package framing。
