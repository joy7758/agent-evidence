# 当前状态

## 仓库现状摘要
- 已有资产：`spec/`、`schema/`、`examples/`、`scripts/`、`tests/`、`submission/`、`agent_evidence/cli`。
- 已有实现：`execution-evidence-object` 原型、`agent_evidence.aep` bundle 校验链、若干导出和验证命令。
- 缺失资产：面向 operation accountability 的最小 profile、与该 profile 对应的样例集、专用验证入口、闭环 demo、面向当前主题的简明文稿。
- 可直接复用部分：现有 Python 技术栈、`click` CLI、`jsonschema`、测试框架、`spec/schema/examples` 提案层、`scripts` 演示层。
- 最小新增实现路径：在现有目录中新增 profile 规范与 schema，扩充 `examples/`，在现有 Python 包和 CLI 中增加校验器，再补一个单链路 `demo/` 目录和两份文稿。
- 当前建议技术栈：Python 3.11 + `jsonschema` + 现有 `click` CLI + `pytest`。

## 里程碑状态
- M1 仓库扫描与计划：已完成
- M2 最小 profile 与 schema：已完成
- M3 样例集：已完成
- M4 validator 与 CLI：已完成
- M5 demo 与文稿：已完成

## 当前落地产物
- profile 规范：`spec/execution-evidence-operation-accountability-profile-v0.1.md`
- schema：`schema/execution-evidence-operation-accountability-profile-v0.1.schema.json`
- 样例：`examples/minimal-valid-evidence.json` 及 3 个 invalid 样例
- validator：`agent_evidence/oap.py` 与 CLI 命令 `agent-evidence validate-profile <file>`
- demo：`demo/run_operation_accountability_demo.py`
- 文稿：`docs/research-brief-zh.md`、`docs/abstract-en.md`

## 已验证结果
- `./.venv/bin/ruff check agent_evidence/oap.py agent_evidence/cli/main.py demo/run_operation_accountability_demo.py tests/test_operation_accountability_profile.py` 通过
- `./.venv/bin/python -m pytest tests/test_operation_accountability_profile.py tests/test_aep_profile.py tests/test_cli.py` 通过
- `python3 demo/run_operation_accountability_demo.py` 通过
- `validate-profile` 对 valid 样例返回 `ok: true`
- `validate-profile` 对 invalid 样例返回 `ok: false` 且带明确 error code

## 术语与命名统一结果
- profile 正式名称统一为 `Execution Evidence and Operation Accountability Profile v0.1`
- profile 标识字符串统一为 `execution-evidence-operation-accountability-profile@0.1`
- profile 载荷统一称为 `operation accountability statement`
- validator 输出统一称为 `validation report`
- CLI 入口统一为 `agent-evidence validate-profile <file>`
- 历史仓库中的 `Execution Evidence Object` 与 `Agent Evidence Profile` 保留为既有表面，不作为本轮 v0.1 最小路径命名

## Known environment note
- 现有 `.venv` 使用 Python 3.14。
- broader test runs 和已安装 CLI 在该环境下会出现一条来自 `langchain_core` 的 warning。
- 这条 warning 不影响本轮 minimal profile / validator / demo 的执行结果。

## 当前执行原则
- 不平行新建第二套工程。
- 优先沿用现有 Python 包、CLI、tests、docs 结构。
- 先交付最小闭环，再考虑更广映射。

## 本轮最小验证记录
- 命令：`./.venv/bin/ruff check agent_evidence/oap.py agent_evidence/cli/main.py demo/run_operation_accountability_demo.py tests/test_operation_accountability_profile.py`
  - 结果：`All checks passed!`
  - 是否通过：通过
- 命令：`./.venv/bin/python -m pytest tests/test_operation_accountability_profile.py tests/test_aep_profile.py tests/test_cli.py`
  - 结果：`18 passed, 1 warning in 1.16s`
  - 是否通过：通过
- 命令：`./.venv/bin/agent-evidence validate-profile examples/minimal-valid-evidence.json`
  - 结果：`ok: true`, `issue_count: 0`
  - 是否通过：通过
- 命令：`./.venv/bin/agent-evidence validate-profile examples/invalid-missing-required.json`
  - 结果：`ok: false`, primary error code `schema_violation`
  - 是否通过：通过
- 命令：`./.venv/bin/agent-evidence validate-profile examples/invalid-unclosed-reference.json`
  - 结果：`ok: false`, primary error code `unresolved_output_ref`
  - 是否通过：通过
- 命令：`./.venv/bin/agent-evidence validate-profile examples/invalid-policy-link-broken.json`
  - 结果：`ok: false`, primary error code `unresolved_evidence_policy_ref`
  - 是否通过：通过
- 命令：`python3 demo/run_operation_accountability_demo.py`
  - 结果：demo 闭环执行完成，末尾输出 `PASS execution-evidence-operation-accountability-profile@0.1 ...`
  - 是否通过：通过

## 本轮仍残留的问题
- `.venv` 的 Python 3.14 环境会带出一条 `langchain_core` warning。
- 仓库内仍保留历史 `Execution Evidence Object` / `Agent Evidence Profile` 资料；本轮没有重写这些既有表面，只通过 README 和状态文档把 v0.1 最小路径与其分开说明。

## 第三轮发布前复验
- 命令：`./.venv/bin/ruff check agent_evidence/oap.py agent_evidence/cli/main.py demo/run_operation_accountability_demo.py tests/test_operation_accountability_profile.py`
  - 结果：`All checks passed!`
  - 是否通过：通过
- 命令：`./.venv/bin/python -m pytest tests/test_operation_accountability_profile.py tests/test_aep_profile.py tests/test_cli.py`
  - 结果：`18 passed, 1 warning in 1.16s`
  - 是否通过：通过
- 命令：`./.venv/bin/agent-evidence validate-profile examples/minimal-valid-evidence.json`
  - 结果：`ok: true`, `issue_count: 0`
  - 是否通过：通过
- 命令：`./.venv/bin/agent-evidence validate-profile examples/invalid-missing-required.json`
  - 结果：`ok: false`, primary error code `schema_violation`
  - 是否通过：通过
- 命令：`./.venv/bin/agent-evidence validate-profile examples/invalid-unclosed-reference.json`
  - 结果：`ok: false`, primary error code `unresolved_output_ref`
  - 是否通过：通过
- 命令：`./.venv/bin/agent-evidence validate-profile examples/invalid-policy-link-broken.json`
  - 结果：`ok: false`, primary error code `unresolved_evidence_policy_ref`
  - 是否通过：通过
- 命令：`python3 demo/run_operation_accountability_demo.py`
  - 结果：demo 闭环执行完成，末尾输出 `PASS execution-evidence-operation-accountability-profile@0.1 ...`
  - 是否通过：通过
- 仍残留的问题：
  - `.venv` 的 Python 3.14 环境 warning 仍存在，但不影响本轮交付判断
