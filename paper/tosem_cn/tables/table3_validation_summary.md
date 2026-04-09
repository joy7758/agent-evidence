# 表 3 样例验证摘要

| example file | example role | scenario / failure mode | expected validation result | expected main error code (if invalid) | current evidence source |
| --- | --- | --- | --- | --- | --- |
| `minimal-valid-evidence.json` | valid | metadata enrichment；单输入 / 单输出 | pass | - | both |
| `valid-retention-review-evidence.json` | valid | retention review；双输入 / 单输出决策 | pass | - | both |
| `invalid-missing-required.json` | invalid | 必填字段缺失；移除 `validation.method` | fail | `schema_violation` | test |
| `invalid-unclosed-reference.json` | invalid | output ref 不闭合 | fail | `unresolved_output_ref` | test |
| `invalid-policy-link-broken.json` | invalid | policy / evidence 链接不一致 | fail | `unresolved_evidence_policy_ref` | test |
| `invalid-provenance-output-mismatch.json` | invalid | provenance / output cross-field mismatch | fail | `provenance_output_refs_mismatch` | test |
| `invalid-validation-provenance-link-broken.json` | invalid | validation / provenance 引用闭合失败 | fail | `unresolved_validation_provenance_ref` | test |

Caption draft：表 3 以当前仓库已存在的样例、测试与 CLI 路径为基础，压缩展示“哪些 profile 样例被验证、预期结果为何、失败时主错误码是什么”，用于让 evaluation 中的验证覆盖面更易扫描。
