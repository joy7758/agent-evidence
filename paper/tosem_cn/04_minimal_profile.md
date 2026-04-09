# 最小 Profile

## 1. Profile 标识与范围

当前仓库定义的 profile 名称为
`execution-evidence-operation-accountability-profile`，版本为 `0.1`。它描述的是
一个 single operation accountability statement，而不是一组操作、一个 workflow
图，或一个治理 registry。

其顶层必需部分包括：

- `profile`
- `statement_id`
- `timestamp`
- `actor`
- `subject`
- `operation`
- `policy`
- `constraints`
- `provenance`
- `evidence`
- `validation`

其中，本文持续采用的核心结构是：
`operation / policy / provenance / evidence / validation`。
`actor` 与 `subject` 提供 statement 的执行主体和作用对象，`constraints` 用于承接
policy 的具体规则集合。

## 2. 最小对象模型

### `operation`

记录一次具体操作的身份、类型、输入输出引用、结果状态与摘要。它回答“做了什么”。

### `policy`

记录 governing policy 的身份、名称以及它所引用的 constraint 集。它回答“受什么规则约束”。

### `provenance`

把 actor、subject、operation 与输入输出引用串起来。它回答“这些元素之间如何形成可追溯
链接”。

### `evidence`

收纳 references、artifacts 与 integrity digest。它回答“留下了哪些可复核材料”。

### `validation`

记录验证对象、验证方法、验证状态和 validator 标识。它回答“第三方如何检查该 statement”。

## 3. 关键字段关系

仓库规范中明确给出最小链接规则。论文可直接沿用以下规则：

- `operation.subject_ref` 必须等于 `subject.id`
- `operation.policy_ref` 必须等于 `policy.id`
- `policy.constraint_refs[]` 必须解析到 `constraints[].id`
- `operation.input_refs[]` 与 `operation.output_refs[]` 必须解析到
  `evidence.references[].ref_id`
- `provenance` 中的 `actor_ref`、`operation_ref`、`subject_ref` 必须分别对应
  `actor.id`、`operation.id`、`subject.id`
- `provenance.input_refs` 与 `provenance.output_refs` 必须和 `operation` 中的同名字段一致
- `evidence` 中的 `subject_ref`、`operation_ref`、`policy_ref` 必须分别与主体 statement 一致
- `validation` 中的 `evidence_ref`、`provenance_ref`、`policy_ref` 必须解析到本地对象

## 4. 合规条件

仓库当前要求一个 statement 合规，至少应满足：

1. `profile.name` 为固定值
2. `profile.version` 为 `0.1`
3. JSON 实例通过 schema
4. 本地引用全部闭合
5. input refs 指向 `role=input`
6. output refs 指向 `role=output`
7. policy / provenance / evidence 链接一致
8. `references_digest` 可重算
9. `artifacts_digest` 可重算
10. `statement_digest` 可重算

## 5. 样例集如何支撑该 profile

当前仓库样例集正好对应这组设计：

- `minimal-valid-evidence.json`
  - 用于说明 profile 的正常闭环形态。
- `invalid-missing-required.json`
  - 故意删去 `validation.method`，对应“必填字段缺失”。
- `invalid-unclosed-reference.json`
  - 故意让 output ref 不可解析，对应“引用闭合失败”。
- `invalid-policy-link-broken.json`
  - 故意让 `evidence.policy_ref` 与 `policy.id` 不一致，对应“policy/evidence 关联不一致”。

这组样例的价值在于，它们不是泛化测试集，而是最小规则面的精确切口。每个 invalid 只破坏
1 条主规则，使 validator 的输出能和 profile 设计目标一一对应。

## 6. 为什么这是“最小 profile”

该 profile 的“最小”体现在三个层面：

- 最小问题面：只覆盖单 operation statement
- 最小字段面：只保留支撑问责闭环的必要字段
- 最小验证面：只要求能完成第三方最基础的独立检查

它不提供更大的编排语义，也不预设跨组织的全局注册机制。这种收缩不是能力不足，而是
方法学选择：先把最小单元做成可验证对象，再讨论更大的生态层。

## 投稿前待补

- 表 1：顶层字段、是否必填、作用说明
- 若需要 appendix，可补一份压缩后的最小 JSON 示例
