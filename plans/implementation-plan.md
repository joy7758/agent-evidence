# implementation plan

## M1 仓库扫描与计划
- 输入：现有 `spec/`、`schema/`、`examples/`、`scripts/`、`tests/`、CLI 结构。
- 输出：`docs/STATUS.md`、`plans/implementation-plan.md`。
- 验收条件：明确已有资产、缺失资产、最小新增路径、建议技术栈。

## M2 最小 profile 与 schema
- 输入：现有 `execution-evidence-object` 原型、FDO 映射文档、当前主题边界。
- 输出：新增最小 profile 规范文档和 JSON Schema。
- 验收条件：字段能回答谁执行、对什么对象执行、执行了什么 operation、受何 policy 约束、输入输出如何引用、结果是什么、完整性材料是什么、第三方如何验证。

## M3 样例集
- 输入：M2 产出的规范与 schema。
- 输出：1 个 valid 样例、3 个 invalid 样例、`examples/README.md`。
- 验收条件：每个 invalid 样例只破坏 1 条主规则，README 清楚解释通过或失败原因。

## M4 validator 与 CLI
- 输入：M2 schema、M3 样例、现有 Python 包和 CLI。
- 输出：可复用的 profile 校验模块、CLI 命令、测试。
- 验收条件：至少覆盖结构完整性、必填字段、引用闭合、policy/provenance/evidence 关联一致性；输出 JSON 结果、人类可读摘要、明确 error code。

## M5 demo 与文稿
- 输入：M2-M4 产物。
- 输出：单链路 `demo/` 闭环、`docs/research-brief-zh.md`、`docs/abstract-en.md`。
- 验收条件：demo 可运行并打印验证结果；文稿聚焦 minimal profile / validator / demo / accountability gap，不扩展成宏大平台叙事。
