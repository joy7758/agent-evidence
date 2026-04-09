# 最小验证边界

## 边界定义

这里的 minimal verification boundary，指的是：第三方在不依赖原运行时内部状态的前提下，对一次 operation accountability statement 做出 `verifiable / not verifiable` 判断所必需的最小组成集合。

这条边界的目标不是复刻整个 runtime，也不是替代完整治理体系。它只负责把“一次操作是否可被外部复核”这件事压缩成一个局部、可交换、可检查的判断单元。

## 为什么这不只是 logs / provenance / policy / audit trail

- logs 能记运行片段，但通常不能形成一个局部闭合、面向外部 checker 的 statement。
- provenance 能说明对象从哪里来、怎么派生，但不自动给出 governing policy 与 validation path。
- policy 能说明“应该如何做”，但不能单独说明“这次具体做了什么”。
- audit trail 可能很丰富，但常常实现耦合、范围过大、粒度不稳，不天然等于一个最小可验证单元。

因此，真正的问题不是“这些材料是否有价值”，而是“它们能否被绑定成一个最小外部可检查边界”。

## Boundary Components

| component | minimal role in the boundary | what breaks if removed | what goes wrong if over-expanded |
| --- | --- | --- | --- |
| actor identity binding | 说明谁执行了这次 operation | 无法归责；第三方无法判断执行主体是否明确 | 一旦扩成完整组织身份图谱，边界会从单 operation 漂移到全局身份治理 |
| subject / target binding | 说明操作作用于哪个对象 | 无法判断操作对象；policy、provenance、evidence 都失去落点 | 一旦扩成完整对象图与 registry，同一 statement 会变成对象管理平台切片 |
| operation semantics | 说明执行了什么 operation、结果如何 | 只能知道“发生过事件”，不能判断具体责任语义 | 一旦扩成完整 workflow DSL，会把单 operation boundary 膨胀成编排系统 |
| policy / constraints binding | 说明这次执行依据了什么规则 | 只能看到发生了什么，看不到为什么这样做是被允许或约束的 | 一旦吸收全部治理规则和组织流程，statement 会失去最小性 |
| provenance closure | 把 actor、subject、operation 与 input/output refs 串成局部闭环 | 无法判断输入输出是否与当前 operation 对齐 | 一旦扩成全链路 lineage graph，局部检查会变成重建整个历史 |
| evidence continuity | 给出支撑 statement 的 references、artifacts 与 integrity material | 结果无法复核；对象和输出只能停留在口头宣称 | 一旦把所有 runtime telemetry 都装进来，evidence 会变成不可移植的大包 |
| validation declaration | 说明第三方如何检查、检查到什么状态 | statement 只能被描述，不能被验证 | 一旦把完整审计流程、审批流程都塞进来，边界会从 verification drift 到 governance workflow |
| temporal anchor | 说明 statement 处于哪个时间点 | policy 生效时点、对象版本、结果先后无法判断 | 一旦要求完整事件时间线，边界会退化成 trace replay |

## 中心张力：minimality vs verifiability

这条边界的难点不在于“多放点字段”，而在于同时守住两个条件：

- 太小：如果把 policy、provenance、evidence 或 validation 中任意一个拿掉，statement 会退回成描述性对象，而不是可验证对象。
- 太大：如果把完整 logs、全量 lineage、registry、组织流程、密码学基础设施都装进来，statement 会失去稳定边界，也失去可复用性。

因此，最小验证边界的判据应该是：

第三方是否已经可以仅凭这个 statement，对一次 operation 做出局部而明确的验证判断；如果还不行，边界太小；如果必须重建整个 runtime，边界太大。

## 对旗舰论文的意义

TOSEM 工件已经证明这条边界“可以被实现为最小 profile + validator + demo”。旗舰论文要进一步证明的是：这条边界不是实现便利，而是 machine-actionable object systems 中必须被明确提出的研究问题。
