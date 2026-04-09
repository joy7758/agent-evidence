# 问题陈述草稿

在 FDO、STAP、data space 这一类 machine-actionable object systems 中，系统能力的重心正在发生变化。对象不再只是被存储、传输和检索，它们越来越多地成为可被机器直接处理、派生、审核、批准、拒绝、转换和发布的操作对象。与此同时，围绕 AI agent 的工程实践已经可以稳定产生日志、trace、runtime events、policy records、provenance fragments 和各类 audit trail。表面上看，这些材料似乎已经足以描述“发生了什么”。但一旦问题被收紧到一次具体 operation，情况就不再简单。外部复核者真正需要回答的，往往不是系统是否留下了大量记录，而是：谁对哪个对象执行了什么操作，这个操作受什么 policy 和 constraints 约束，输入输出引用是否闭合，产生了哪些 evidence，以及第三方如何在脱离原运行时的情况下判断这次操作是否可验证。

这正是 operation accountability 的问题所在。它不是泛化的“治理叙事”，也不是笼统的“可观测性增强”。它关注的是一个更小、更硬的对象级问题：一次 operation accountability statement 能否被定义为局部闭合、可交换、可检查的验证单元。如果答案是否定的，那么系统虽然可以执行动作，却无法为这些动作提供清晰的外部复核边界。对 machine-actionable object systems 来说，这不是边角问题。只要系统允许 agent 直接对对象做出会影响派生关系、状态判断、发布决定或访问结果的动作，那么“这次操作到底能否被独立验证”就会成为一个一等问题。没有这条边界，所谓 accountability 只能停留在分散记录的事后拼接，而不是可被稳定检查的 engineering object。

当前实践之所以容易低估这个问题，一个重要原因在于 operation accountability 仍然处于 under-specified 状态。很多系统默认认为，logs、provenance、policy 和 audit trail 的叠加大致可以覆盖问责需求，但这种假设很少把“最小验证边界”明确提出来。日志通常擅长记录事件片段、时间戳、调用路径和调试上下文；provenance 擅长表达对象如何派生、如何关联；policy 擅长表达规则依据和允许条件；audit trail 擅长保留更长时间跨度的审计记录。这些材料都重要，但它们回答的问题并不相同。更关键的是，它们常常分布在不同系统表面、由不同实现逻辑塑形，并不天然形成一个对单次 operation 可直接检查的 statement。也就是说，现有系统往往有“记录能力”，却没有把“单次操作可验证性”抽象为一个明确、最小且稳定的对象。

这类 under-specification 会带来三个后果。第一，责任边界模糊。系统可能能证明“某些事件发生过”，却无法局部回答“谁在何种约束下对哪个对象做了这次操作”。第二，验证边界漂移。为了复核一项操作，检查者不得不回到原运行时、内部数据库、框架私有事件模型或组织流程文档中重新拼装事实，这意味着 statement 本身并不构成验证单元。第三，失败模型不可读。因为系统没有把 operation accountability 作为一个独立问题定义出来，失败往往被埋在零散异常、平台私有字段或实现耦合的诊断路径里，而不能被整理为稳定的 failure classes。对于 journal 级 problem-defining paper 来说，这正说明问题还没有被充分命名。

更深一层看，这种 under-specification 还会遮蔽一个常被忽略的层次差异。logs、policy、provenance、audit trail 往往分别属于不同的工程层面：有的是 runtime observability 层，有的是 rule-expression 层，有的是 lineage-expression 层，有的是 compliance retention 层。它们当然可以相互补充，但“可以相互补充”并不等于“已经共同构成了最小验证边界”。如果论文不把这一点说清楚，读者就会误以为 operation accountability 只是把若干现有记录拼在一起的集成问题，而不是一个需要独立定义边界条件、失败条件和验证条件的问题。本文恰恰要反过来主张：在这些材料之上，仍然存在一个更小、更明确、也更值得单独研究的问题单元。

从这个角度看，现有 artifact 之所以只部分覆盖问题，不是因为它们无用，而是因为它们的边界与本文要定义的问题边界并不相同。ordinary logs 可以告诉我们系统曾执行某些步骤，也可能记录某个 actor 或服务在某一时刻产生了某段输出，但它们通常不会确保 `operation` 是责任中心，也不会确保 `policy`、`provenance`、`evidence` 和 `validation` 以局部闭合方式绑定在一起。provenance-oriented artifacts 可以很好地说明对象之间的来源关系，却未必显式携带 governing policy，也未必给出 external checker 应如何判断 pass/fail。policy artifacts 则更接近“应该怎样做”的规范表达，而不是“这次具体做了什么、留下了什么可复核证据、第三方如何验证”的执行 statement。audit trail 虽然看起来更接近 accountability，但它常常范围过大、实现耦合过深、粒度不稳，最后仍然需要依赖原系统知识来解释。

因此，本文要指出的不是“已有 artifacts 不重要”，而是“它们对 operation accountability 的覆盖是 partial rather than sufficient”。只要一个外部检查者仍然需要跨越多个表面、借助原实现语义、临时补足缺失链接，才能判断一次操作是否可验证，那么 operation accountability 就尚未被明确建模。问题的核心不在于材料数量不够，而在于缺少一个最小而明确的 verification boundary。这个 boundary 必须足够小，才能保持 portability 和 local inspectability；也必须足够完整，才能让第三方不依赖原运行时就做出 `verifiable / not verifiable` 判断。换句话说，问题不应再被表述为“如何积累更多 traces”，而应被表述为“什么是一次 operation accountability statement 必须携带的最小验证条件”。

一旦问题被这样重写，failure taxonomy 的地位也会发生变化。在较弱的工程叙事中，失败通常只是 validator 的输出副产品，或只是若干 invalid examples 的展示材料。但如果 operation accountability 本身是一条 verification boundary，那么 failure classes 就不再只是实现细节，而是问题定义的一部分。missing identity binding、missing target binding、broken policy linkage、broken evidence continuity、outcome unverifiability、temporal inconsistency、implementation-coupled evidence，这些都不是“随便列出来的错误名”。它们对应的是边界为什么会失效、第三方为何会失去判断能力、以及 statement 在什么条件下仍然不能成立为验证单元。也正因为如此，旗舰论文不能停留在“哪些样例目前会 fail”，而要进一步说明“哪些 failure classes 对这个问题是结构性的”。

这也解释了为什么当前 research line 中的 TOSEM artifact 只是最小见证，而不是最终答案。现有仓库已经证明：一个 `minimal verifiable profile`、一个 `profile-aware validator`、一组 valid/invalid examples 和一条单链路 demo 是可以被规定、实现、测试并归档的。这个结果很重要，因为它把 operation accountability 从松散叙述压缩成了 smallest verifiable artifact。但这还没有完成旗舰论文的工作。旗舰论文需要更进一步：它必须说明为什么这里的核心创新不只是又一个 profile，而是对问题边界的重新定义；为什么 `operation / policy / provenance / evidence / validation` 的绑定不是实现偏好，而是 minimal verification boundary 的必要条件；为什么 failure taxonomy、independent checker、multi-scenario coverage 和 external validation 应当被视为同一个研究问题的组成部分。

一旦这样表述，问题的结构就会变得清楚。本文并不试图解决 general AI governance，也不试图推出一个完整 registry、一个全量 FDO mapping，或一个大而全的密码学信任基础设施。本文只处理一次具体 operation 的 accountability 条件。但这个“只”并不意味着问题小到不值得单独研究。恰恰相反，正因为大量系统已经可以让 agent 对对象执行可产生实际后果的机器动作，这个最小问题才变得基础。如果连单次 operation 的责任边界都无法稳定定义、无法稳定检测、无法稳定失败，那么更高层的 orchestration、policy automation 或 ecosystem integration 都会缺少坚实的验证地基。

这也是为什么 external validation 在这里不是锦上添花，而是问题完成度的一部分。一个仓库内自洽的 profile、validator 和 demo，足以证明问题可以被实现，但还不足以证明这条边界具有更广的解释力。要把 operation accountability 从“一个做得不错的 artifact line”推进为“一个必须被认真定义的 journal problem”，还需要 multi-scenario coverage、independent checker、以及更强的 comparison strength。换句话说，旗舰论文并不是在否定当前 TOSEM line 的价值，而是在重新界定它的位置：它提供 smallest working witness；而问题本身还要求更强的外部证据来说明，这条 verification boundary 不是某个仓库偶然选出来的实现习惯。

因此，本文的出发点不是提出另一个实现表面，而是提出一个更清晰的问题定义：在 machine-actionable object systems 中，operation accountability 应被视为一条独立、最小且可外部检查的 verification boundary。现有 logs、provenance、policy 和 audit trail 都能提供必要材料，但都不足以单独构成这一边界。只有当 actor identity、target binding、operation semantics、policy linkage、provenance closure、evidence continuity、validation declaration 以及最小 temporal anchor 被绑定为同一个局部 statement 时，第三方才真正拥有对一次 operation 做出独立验证判断的基础。

本文的核心主张因此可以明确写成一句话：Operation accountability is not a logging detail but a first-class verification boundary for machine-actionable object systems.
