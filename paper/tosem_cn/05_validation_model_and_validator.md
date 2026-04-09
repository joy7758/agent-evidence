# 验证模型与 Validator

## 1. 设计原则

当前仓库中的 validator 不是一个抽象概念，而是已经落地在
`agent_evidence/oap.py` 与 `agent_evidence/cli/main.py` 中的具体实现。它服务于一个
非常明确的目标：把最小 profile 变成“能被独立执行验证”的 artifact，而不仅是文档中
的对象模型。

## 2. 四阶段验证模型

validator 采用 staged validation，按以下顺序执行：

### Stage 1. Schema

使用 JSON Schema 检查结构完整性、字段形状和必填字段。这一阶段的主错误码示例是
`schema_violation`。

### Stage 2. References

在 schema 通过后，检查本地引用是否闭合、标识符是否重复、以及各类 ref 是否能解析到
本地对象。这一阶段覆盖：

- subject ref
- policy ref
- constraint refs
- input refs
- output refs
- provenance / evidence / validation 中的本地 ref

这一阶段的主错误码示例包括：

- `unresolved_input_ref`
- `unresolved_output_ref`
- `unresolved_evidence_policy_ref`
- `duplicate_reference_id`

### Stage 3. Consistency

在引用闭合的前提下，检查 policy / provenance / evidence 的关联一致性，以及输入输出
role 是否正确。当前实现还检查：

- `provenance.input_refs` 是否与 `operation.input_refs` 一致
- `provenance.output_refs` 是否与 `operation.output_refs` 一致
- `operation`、`evidence`、`validation` 是否携带同一 `policy_ref`
- 至少有一个 input ref 指向 `subject`

### Stage 4. Integrity

在前三阶段无误时，重算：

- `references_digest`
- `artifacts_digest`
- `statement_digest`

并与 `evidence.integrity` 中记录的值比较。这一阶段保证 statement 不只是“结构上看起来
合理”，还必须在最小证据面上保持可重算一致性。

## 3. 输出模型

validator 输出一个 validation report，其中包含：

- `ok`
- `profile`
- `source`
- `issue_count`
- `stages`
- `summary`

这组输出正好对应仓库级要求：

- 机器可读 JSON
- 人类可读失败摘要
- 明确 error code

其中 `summary` 由 `render_summary_lines()` 生成。成功时为一行 `PASS ...`；失败时为一行
`FAIL ...` 加若干逐条错误摘要。

## 4. CLI 表面

validator 已经接入 CLI，入口命令为：

```bash
agent-evidence validate-profile <file>
```

该命令读取 JSON profile，输出 validation report；如果 `ok=false`，则以非零状态退出。
因此它既可用于人工检查，也可直接嵌入脚本或 CI。

`pyproject.toml` 进一步把 `agent-evidence` 暴露为 console script，说明这不是仓库内部
脚本，而是已经被整理为对外可调用的命令表面。

## 5. 测试与样例如何支撑 validator

当前可直接锚定的测试与样例包括：

- `tests/test_operation_accountability_profile.py`
  - 覆盖 valid 样例通过
  - 覆盖 5 个 invalid 样例失败
  - 覆盖 CLI 命令输出可解析 JSON
- `examples/README.md`
  - 明确说明每个 invalid 样例只打破 1 条主规则

在仓库当前实现中，可以直接对应到以下错误示例：

- `schema_violation`
- `unresolved_output_ref`
- `unresolved_evidence_policy_ref`
- `provenance_output_refs_mismatch`
- `unresolved_validation_provenance_ref`

这组反例覆盖面已经比最初的最小路径更厚，但它仍然只是受控边界覆盖，而不是穷尽 failure
taxonomy。

## 6. 为什么说它是“profile-aware”

这里的 “profile-aware” 不只是“知道有个 schema 文件”。它具体表现为：

- 固定校验 `profile.name` 与 `profile.version`
- 理解 `operation / policy / provenance / evidence / validation` 的内部语义关系
- 按该 profile 的引用和一致性规则执行业务校验
- 重算该 profile 约定的三类 digest

换言之，validator 是 profile 的执行语义，而不是 profile 旁边的一个泛用 JSON linter。

## 投稿前待补

- 表 2：各阶段输入、检查点、主错误码、失败示例
- 如需补充算法框，可将 digest 重算逻辑写成伪代码
