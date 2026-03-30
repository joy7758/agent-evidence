# ACCEPTANCE CHECKLIST

## 1. Profile 文档是否边界清楚，字段、关系、合规/失败条件完整

- 状态：PASS
- 证据文件：
  - `spec/execution-evidence-operation-accountability-profile-v0.1.md`
  - `schema/execution-evidence-operation-accountability-profile-v0.1.schema.json`
- 还差什么：
  - 无阻塞缺口。
- 你准备怎么补：
  - 当前不再扩 scope，后续只在同一 profile 名称下做窄增量修订。

## 2. Schema、examples、validator 三者是否严格一致

- 状态：PASS
- 证据文件：
  - `schema/execution-evidence-operation-accountability-profile-v0.1.schema.json`
  - `examples/minimal-valid-evidence.json`
  - `examples/invalid-missing-required.json`
  - `examples/invalid-unclosed-reference.json`
  - `examples/invalid-policy-link-broken.json`
  - `agent_evidence/oap.py`
  - `tests/test_operation_accountability_profile.py`
- 还差什么：
  - 无阻塞缺口。
- 你准备怎么补：
  - 后续如果字段有变更，继续以 schema 为锚点，同步更新样例与 validator 测试。

## 3. 1 个 valid + 3 个 invalid 是否都能稳定给出预期结果，且每个 invalid 只打破 1 条主规则

- 状态：PASS
- 证据文件：
  - `examples/README.md`
  - `demo/expected-output.md`
  - `tests/test_operation_accountability_profile.py`
- 还差什么：
  - 无阻塞缺口。
- 你准备怎么补：
  - 维持 staged validation 输出，继续保证 invalid 样例只命中 1 个主错误码。

## 4. Demo 是否形成单链路闭环，且 README/scenario/脚本三者叙述一致

- 状态：PASS
- 证据文件：
  - `demo/README.md`
  - `demo/scenario.md`
  - `demo/run_operation_accountability_demo.py`
  - `demo/expected-output.md`
- 还差什么：
  - 无阻塞缺口。
- 你准备怎么补：
  - 当前只保留单链路 metadata enrichment 场景，不另开第二条主线。

## 5. 中文 brief 与英文 abstract 是否与 spec/validator/demo 保持同一术语，不漂移

- 状态：PASS
- 证据文件：
  - `docs/research-brief-zh.md`
  - `docs/abstract-en.md`
  - `README.md`
  - `docs/STATUS.md`
- 还差什么：
  - 历史仓库中仍保留旧的 `Execution Evidence Object` 和 `Agent Evidence Profile` 表述，但已与本轮 v0.1 最小路径分开说明，不构成本轮阻塞。
- 你准备怎么补：
  - 后续继续把 v0.1 最小路径限定为 `Execution Evidence and Operation Accountability Profile v0.1`、operation accountability statement、validation report 这组术语。
