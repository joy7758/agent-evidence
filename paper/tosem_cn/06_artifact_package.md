# Artifact Package

## 1. Artifact 的组成

当前仓库已经具备一篇 methodology + validator + artifact paper 所需的最小工件表面。
按仓库现状，可将 artifact package 组织为以下部分：

- 方法与规范
  - `spec/execution-evidence-operation-accountability-profile-v0.1.md`
  - `schema/execution-evidence-operation-accountability-profile-v0.1.schema.json`
- 样例
  - `examples/minimal-valid-evidence.json`
  - `examples/valid-retention-review-evidence.json`
  - `examples/invalid-missing-required.json`
  - `examples/invalid-unclosed-reference.json`
  - `examples/invalid-policy-link-broken.json`
  - `examples/invalid-provenance-output-mismatch.json`
  - `examples/invalid-validation-provenance-link-broken.json`
- 验证器
  - `agent_evidence/oap.py`
  - `agent_evidence/cli/main.py`
- 测试
  - `tests/test_operation_accountability_profile.py`
  - `tests/test_cli.py`
- Demo
  - `demo/README.md`
  - `demo/scenario.md`
  - `demo/run_operation_accountability_demo.py`
  - `demo/expected-output.md`
- 交付文档
  - `submission/package-manifest.md`
  - `submission/release-readiness-check.md`
  - `submission/final-handoff.md`

## 2. 可复现的最小路径

从 artifact reviewer 的角度，当前最小复现实线路径已经清楚：

1. 运行 `agent-evidence validate-profile` 检查 2 个 valid 与 5 个 invalid 样例。
2. 运行 `python3 demo/run_operation_accountability_demo.py`。
3. 检查 `demo/artifacts/` 目录下生成的 evidence 与 validation report。

这一路径对应的产出是清晰且可核对的：样例是否通过、错误码是否正确、demo 是否以一条
`PASS execution-evidence-operation-accountability-profile@0.1 ...` 收束。

新增的第二个 valid 样例没有引入新理论或新校验阶段。它只是把同一最小 profile 放到第二种
对象/operation 语境中，并使用不同的 input linkage 形态，因此可以作为 basic portability
evidence，而不能被表述为广泛跨框架验证。

## 3. Release 与归档锚点

当前工作区之外但可核实的发布锚点包括：

- Git 仓库本地 tag：`v0.2.0`
- `git show v0.2.0` 可见该 tag 冻结了 OAP v0.1 package
- GitHub Release API 可见公开 release `Agent Evidence v0.2.0`
- DataCite API 可见 Zenodo DOI `10.5281/zenodo.19334062`

这说明本文并非只对应一份本地草稿仓库，而是已经存在一个可以被第三方引用的发布与归档表面。

## 4. 当前需要如实说明的文档不一致

当前 current-package 文档已经按双轨口径完成同步：

- `README.md`
- `README.zh-CN.md`
- `submission/artifact-availability.md`

它们现在明确区分：

- 当前 OAP package：GitHub Release `v0.2.0`，Zenodo DOI `10.5281/zenodo.19334062`
- 历史 specimen track：`v0.1-live-chain`，旧 DOI `10.5281/zenodo.19055948`

仍保留旧 DOI 的 `release/v0.1-live-chain/RELEASE_NOTE.md` 属于历史 specimen 资料，而不是
当前 package 的 artifact availability 文本。

## 5. 本文如何使用 artifact package

对于 TOSEM 版本，artifact 章节建议只承担三件事：

- 给出工件组成与入口
- 给出最小复现步骤
- 给出 release / DOI 锚点与当前文档同步状态

不要在这一章扩展成生态介绍，也不要把历史 `Execution Evidence Object` 或 `Agent
Evidence Profile` 的所有遗留表面都展开介绍。本文只需要围绕当前 OAP v0.1 package。

## 投稿前待补

- 统一仓库内 DOI 文本
- 增补一个 artifact appendix 草稿
- 若 TOSEM 要求单独 artifact availability statement，可由本章抽出独立版本
