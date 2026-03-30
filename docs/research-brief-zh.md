# 研究简报

## 问题

现有 AI 运行日志有助于调试，但它们通常不能直接回答一个更关键的问题：某个 agent
究竟在什么约束下，对哪个对象执行了什么操作，并留下了哪些可复核的证据。对于
FDO 相关场景，这个 accountability gap 会直接影响对象派生、责任归属和第三方复核。

## 本轮贡献

本轮不做泛化治理平台，只补一个最小闭环：

- 一个最小 `Execution Evidence and Operation Accountability Profile v0.1`
- 一个 profile-aware validator
- 一条单链路 demo
- 两类文稿骨架

这个 profile 只围绕五个部分展开：`operation`、`policy`、`provenance`、`evidence`
和 `validation`。字段被压缩到最小，但仍然能够回答谁执行、对什么对象执行、受什么
约束、输入输出如何引用、结果是什么、第三方如何验证。

## 产物

- `spec/execution-evidence-operation-accountability-profile-v0.1.md`
- `schema/execution-evidence-operation-accountability-profile-v0.1.schema.json`
- `examples/minimal-valid-evidence.json` 及 3 个 invalid 样例
- `agent-evidence validate-profile <file>`
- `demo/run_operation_accountability_demo.py`
- `demo/artifacts/validation-report.json`

## 可验证性

validator 至少做四件事：

- 结构完整性检查
- 必填字段检查
- 引用闭合检查
- policy / provenance / evidence 关联一致性检查

同时还会重算最小完整性 digest，避免 profile 只是“结构对了”但证据材料已经漂移。
validator 的输出以 validation report 为主，同时带 machine-readable JSON、
error code 和简短摘要。

## 下一步

下一步不应立刻扩成大而全体系，而应先做三件小事：

- 增补更多受控场景样例
- 明确与现有 AEP bundle 的桥接方式
- 在不增加结构复杂度的前提下，补更稳定的第三方验证约定
