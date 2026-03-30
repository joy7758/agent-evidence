# Release Readiness Check

## 1. 当前发布对象是什么

- 冻结后的 `Execution Evidence and Operation Accountability Profile v0.1`
  handoff 包。

## 2. 发布范围是什么

- profile spec
- JSON Schema
- profile-aware validator 与 CLI 入口
- 1 个 valid + 3 个 invalid 样例
- 单链路 demo
- brief / abstract / status / acceptance / handoff 文档

## 3. 不包含什么

- 泛化治理平台
- registry 扩展
- 多智能体编排
- 全量 FDO 映射
- 完整密码学基础设施
- 对历史 `Execution Evidence Object` / `Agent Evidence Profile` 路线的重写

## 4. 阻塞项是否为 0

- blocking：0

## 5. 非阻塞项有哪些

- `.venv` 的 Python 3.14 环境在 broader test runs 和已安装 CLI 下会出现一条
  `langchain_core` warning。
- 仓库中仍保留历史 `Execution Evidence Object` / `Agent Evidence Profile`
  资料，但已与本轮 v0.1 主路径分开说明。

## 6. 结论：是否建议现在提交

- 建议现在提交。
- 原因：blocking 为 0，最小验证已通过，handoff 材料已齐，剩余问题均为可交代的
  non-blocking 项。

## Latest validation

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
