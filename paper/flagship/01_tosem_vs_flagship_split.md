# TOSEM 与旗舰论文分工

## 分工总表

| role | core question | contribution type | evidence type | validation level | expected reviewer takeaway | risk | mitigation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TOSEM 现有稿件 | 能否把单 operation accountability statement 做成一个最小可验证 profile，并配上 validator、examples、demo 与 artifact package？ | methodology + validator + artifact | 仓库内 spec、schema、2 valid + 5 invalid、CLI、tests、demo、release、DOI | 仓库内 conformance、diagnostic readability、single-path closure、basic portability evidence | 这是一个实现完整、边界清楚、证据克制的软件工程方法学工件 | 被误读成“只是另一个 profile paper”或“只是实现说明” | 明确把 claim 限定为 smallest verifiable artifact；不夸大 external validity |
| 未来旗舰论文 | 为什么 operation accountability 必须被定义为 machine-actionable object systems 的 first-class verification boundary？这个 boundary 最小该包含什么？缺了会怎样失败？ | problem definition + boundary model + failure taxonomy + external validation agenda | TOSEM 工件作为最小 witness；再加 multi-scenario corpus、independent checker、同案比较、外部复核记录 | 超出仓库内自证，进入 boundary-level reasoning、failure-model completeness、external validation、comparison strength | 这篇论文不是重复实现，而是在定义一个值得独立研究的问题边界 | 变成大而空的治理叙事，或反过来退化成“TOSEM 扩写版” | 始终围绕单 operation、最小 verification boundary、failure taxonomy、external validation，不扩展到 broad governance narrative |

## 分工说明

TOSEM 当前最强的地方是“闭环已经存在”：profile、validator、examples、demo、release 和 DOI 都可核实。它证明当前 research line 不是空想。

旗舰论文最强的地方不应再是“又做了一个 profile”，而应是把这个闭环上移为一个更基础的问题判断：如果系统允许 agent 对机器可操作对象执行动作，那么 operation accountability 就必须被视为一个可以被独立定义、独立检查、独立比较的 verification boundary。

## 决断句

TOSEM proves “it can be built”; flagship proves “it must be defined as a first-class verification problem”.
