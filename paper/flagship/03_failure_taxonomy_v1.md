# Failure Taxonomy v1

## 说明

这个 taxonomy 把当前仓库 invalid cases 和 validator error surface 视为 seed set，而不是完整覆盖。目标不是一次枚举所有故障，而是把 operation accountability boundary 的主要失败类型从“几个例子”提升成“可讨论、可扩展、可检测的 failure classes”。

## v1 类别表

| failure class | definition | why it matters | minimal example pattern | what a validator/checker should detect |
| --- | --- | --- | --- | --- |
| missing identity binding | 执行主体不存在、不可解析，或与 provenance 绑定断裂 | 无法回答“谁执行了这次操作” | `actor.id` 缺失；或 `provenance.actor_ref` 不等于 `actor.id` | 必填 actor 字段；actor/provenance 引用闭合；主体类型是否可识别 |
| missing target binding | subject 不存在、不可解析，或 operation 没有稳定指向对象 | 无法回答“对哪个对象执行了操作” | `subject.digest` 缺失；或 `operation.subject_ref` 不等于 `subject.id` | 必填 subject 字段；operation/subject 闭合；target 是否具有最小可定位性 |
| ambiguous operation semantics | operation 存在，但语义过于模糊，第三方无法判断实际执行了什么 | 无法比较 policy、结果与 evidence 是否匹配 | `operation.type = "process"`；`result.summary = "done"`；没有最小语义约束 | 检测空洞或过泛的 operation verb；必要时要求场景化 operation vocabulary 或最小结果约束 |
| broken policy linkage | policy 存在，但与 operation、evidence、validation 的绑定不一致，或 constraint 引用不闭合 | 无法判断这次执行是否受明确规则约束 | `evidence.policy_ref != policy.id`；或 `policy.constraint_refs` 指向不存在约束 | 检测 policy ref 一致性；constraint 引用闭合；policy 版本是否明确 |
| broken evidence continuity | input/output refs、artifacts 或 integrity material 断裂，导致 statement 不能被连续复核 | 无法证明输入、输出和证据确实支撑当前 statement | `operation.output_refs` 指向不存在 `ref_id`；或 `references_digest` 重算失败 | 检测 refs 闭合；role 匹配；digest 重算；evidence 与 operation/provenance 一致性 |
| outcome unverifiability | statement 声称某个结果已经发生，但输出对象或结果证据不足以支持该结论 | 只能看到“声称成功”，不能检查“结果是否可复核” | `operation.result.status = "succeeded"`，但没有稳定 `output_refs`，或 output 没有 digest / locator | 检测 result 与 output sufficiency 的最小匹配关系；针对不同 operation class 建立结果约束 |
| temporal inconsistency | statement 的时间锚点与 policy、生效版本、输入输出先后关系冲突 | 即使字段齐全，也无法判断时序是否成立 | `timestamp` 早于输入对象版本，或晚于输出证据生成时间且无解释 | 检测最小时间顺序约束；缺失时间锚点时给出明确不可验证结论 |
| implementation-coupled evidence | evidence 只能在原实现内部解释，离开运行时就失去可读性或可验证性 | 破坏 portability 与 external validation，statement 退回实现私有日志 | `locator` 只有本机临时路径；`artifact.type` 只有框架私有 event dump；没有稳定解释层 | 检测本地私有 locator、未说明的 artifact 类型、无法脱离原 runtime 解释的证据结构 |

## 这 8 类之间的关系

- `missing identity binding`、`missing target binding`、`ambiguous operation semantics` 解决的是“statement 是否成立为一个责任单元”。
- `broken policy linkage`、`broken evidence continuity`、`temporal inconsistency` 解决的是“这个责任单元是否真的闭合”。
- `outcome unverifiability`、`implementation-coupled evidence` 解决的是“这个责任单元是否能被外部世界复核”。

## 与当前仓库的关系

当前仓库已经直接触发并稳定报告了其中一部分失败面，例如：

- required field completeness 失败
- reference closure 失败
- policy linkage 失败
- provenance / operation cross-field mismatch
- validation / provenance closure 失败
- integrity mismatch 与 duplicate identifier 代码面已经存在

但旗舰论文不应把这件事写成“taxonomy 已经完成”。更准确的说法是：当前仓库已经提供了一个足够清晰的 seed set，使 failure taxonomy 可以从工程错误码上升为研究问题的一部分。

## 下一步最值得先补的 failure evidence

1. missing identity binding
2. outcome unverifiability
3. temporal inconsistency
4. implementation-coupled evidence

这四类一旦补齐，旗舰论文对“为什么这是 verification boundary，而不只是 profile 边角”会更有说服力。
