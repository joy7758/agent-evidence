# 表 2 Artifact 状态

| 工件项 | 当前状态 | 依据 | 备注 |
| --- | --- | --- | --- |
| profile spec | 已存在 | `spec/execution-evidence-operation-accountability-profile-v0.1.md` | OAP v0.1 的规范文本 |
| JSON Schema | 已存在 | `schema/execution-evidence-operation-accountability-profile-v0.1.schema.json` | 与 profile 同名同版本 |
| valid examples | 已存在，2 个 | `examples/minimal-valid-evidence.json`、`examples/valid-retention-review-evidence.json` | 第二个 valid 提供 second-context validity evidence，但不构成广泛 portability claim |
| invalid examples | 已存在，5 个 | `examples/invalid-missing-required.json`、`examples/invalid-unclosed-reference.json`、`examples/invalid-policy-link-broken.json`、`examples/invalid-provenance-output-mismatch.json`、`examples/invalid-validation-provenance-link-broken.json` | 每个样例只故意破坏 1 条主规则；边界覆盖已增强，但不代表穷尽 |
| reference validator | 已存在 | `agent_evidence/oap.py` | 仓库内 reference implementation，执行 staged validation |
| CLI | 已存在 | `agent_evidence/cli/main.py`、`pyproject.toml` | 暴露 `agent-evidence validate-profile` |
| tests | 已存在 | `tests/test_operation_accountability_profile.py`、`tests/test_cli.py` | 当前工作区复验通过 |
| single-chain demo | 已存在 | `demo/run_operation_accountability_demo.py` | 生成 `minimal-profile-evidence.json` 与 `validation-report.json` |
| GitHub Release v0.2.0 | 已核实 | 本地 `git tag`、`git show v0.2.0`、GitHub Release API | release 版本是 `v0.2.0`，其中冻结 OAP package `v0.1` |
| Zenodo DOI | 已核实，但仓库文案未全同步 | DataCite API：`10.5281/zenodo.19334062` | 仓库部分旧文档仍出现 `10.5281/zenodo.19055948` |

Caption draft：表 2 汇总当前仓库可直接支撑的 artifact 组成与状态，其中 invalid-example 覆盖已扩展到 5 个反例，但仍应视为受控边界覆盖而非穷尽覆盖。
