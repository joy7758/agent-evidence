# 独立 Checker Package 定义

## 目的

旗舰论文如果只依赖当前 reference validator，就很难支撑“这是一条 first-class verification boundary”这一更强主张。原因不是 reference validator 不重要，而是它仍然来自同一仓库、同一 research line、同一规则解释路径。对于 flagship-paper evidence 来说，第二个 checker 的价值在于降低“规则定义者和规则执行者完全重合”的风险，并把验证问题从单一实现提升到至少两个 reasoning paths 之间可对照的问题。

## 为什么 second checker 很关键

- 它让验证结果不再只是一份 reference implementation 的输出。
- 它逼迫边界规则以更显式的方式被重述，而不是隐藏在当前模块实现里。
- 它为 failure taxonomy 提供第二条观察面，帮助区分：
  - 规则本身稳定；
  - 当前实现特有；
  - 仍存在边界歧义。
- 它能为旗舰论文提供更像“evidence-building package”的资产，而不是单一 artifact closure。

## Independence Rule

这里的 “independent” 有一个最小但明确的含义：

- second checker **不得** 直接包装、调用或导入当前 reference validator CLI/module。
- 它 **不得** 以 `agent-evidence validate-profile` 的结果作为自己的判断来源。
- 它 **不得** 通过 `agent_evidence.oap.validate_profile_file`、`build_validation_report` 等函数转手输出结论。

允许的最小复用只有两类：

- 读取同一输入 JSON 格式；
- 在文档中说明它对当前 profile identity 的假设。

如果未来确实要复用 schema 文件，也必须仅作为输入契约说明，而不是把 schema + reference validator 重新包一层。

## Scope of Checks

second checker 的 scope 不追求与 reference validator 完全等价，而追求对 boundary-oriented failure classes 有独立覆盖。v1 至少应检查：

- identity binding presence
- target binding presence
- operation semantics presence
- policy linkage presence
- evidence continuity presence
- validation declaration presence
- outcome presence
- temporal consistency sanity checks
- obvious implementation-coupled fields or over-coupling markers

换句话说，它更像一个 minimal boundary checker，而不是 schema-complete checker。

## Input Assumptions

- 当前输入对象以仓库 central format 为主：
  - `execution-evidence-operation-accountability-profile@0.1`
- 输入应是单个 operation accountability statement JSON。
- v1 不要求支持历史 `Execution Evidence Object` 与 `AEP bundle` 全部变体。
- v1 允许把当前 `examples/minimal-valid-evidence.json` 与 `examples/valid-retention-review-evidence.json` 视为中心语料。

## Expected Outputs

最小输出要求保持简单、可读、可脚本处理：

- 总体结论：`PASS` 或 `FAIL`
- detected issues 列表
- short reason labels

建议输出形态：

```text
FAIL path/to/file.json (3 issue(s))
- [missing_policy_linkage] operation.policy_ref: ...
- [broken_evidence_continuity] operation.output_refs[0]: ...
- [implementation_coupling_marker] evidence.references[1].locator: ...
```

## Limitations

这个 second checker 在旗舰论文里应被如实描述为“minimal and incomplete”：

- 它不是完整 conformance checker。
- 它不保证与 reference validator 在所有边缘 case 上一致。
- 它主要检查 boundary conditions，而不是完整 schema semantics。
- temporal consistency 在 current format 下只能做 sanity checks，不能替代完整时序模型。
- implementation-coupling 检测带有启发式性质，不是形式化证明。

## Minimal Implementation Strategy

最小实现策略应尽量朴素：

1. 使用标准库读取 JSON。
2. 通过手写规则检查最小边界条件。
3. 不导入 reference validator 模块。
4. 优先输出 short reason labels，而不是复杂 validation report。
5. 只支持 central profile format，并在 README 中明确写出这个假设。

## v1 Repo Asset 建议

建议把 second checker 放在：

- `paper/flagship/prototype/independent_checker/`

该目录至少包含：

- `README.md`
- `check_minimal_boundary.py`

这样做的好处是边界清楚：

- 不污染当前主 reference implementation；
- 不与 TOSEM artifact 混淆；
- 方便 later flagship validation package 直接引用。

## 结论

对旗舰论文来说，second checker 不是为了声称“已经有独立实现收敛”，而是为了提供第一步更强证据：这条 verification boundary 已经可以被两条不同的 reasoning paths 检查，而不是只存在于当前 reference validator 的内部逻辑中。
