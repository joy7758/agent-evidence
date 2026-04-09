# Checker Comparison Note

## 目的

这份 note 用于给 reviewer-facing validation section 提供一个诚实的对照面：当前 reference validator 与独立 checker 在同一 corpus 上到底对齐到什么程度，哪里对齐，哪里不对齐，以及这些差异对旗舰论文意味着什么。

## Corpus Covered

本次对照覆盖 19 个文件：

- 2 个现有 valid anchors
  - `examples/minimal-valid-evidence.json`
  - `examples/valid-retention-review-evidence.json`
- 5 个现有 invalid anchors
  - `examples/invalid-missing-required.json`
  - `examples/invalid-unclosed-reference.json`
  - `examples/invalid-policy-link-broken.json`
  - `examples/invalid-provenance-output-mismatch.json`
  - `examples/invalid-validation-provenance-link-broken.json`
- 6 个 scenario specimens
  - `scenario_03_access_decision_valid.json`
  - `scenario_03_access_decision_invalid_missing_policy_linkage.json`
  - `scenario_04_object_derivation_handoff_valid.json`
  - `scenario_04_object_derivation_handoff_invalid_broken_evidence_continuity.json`
  - `scenario_05_failed_or_denied_operation_valid.json`
  - `scenario_05_failed_or_denied_operation_invalid_missing_outcome.json`
- 6 个 direct failure specimens
  - `scenario_06_missing_identity_binding_invalid.json`
  - `scenario_07_temporal_inconsistency_invalid.json`
  - `scenario_08_implementation_coupled_evidence_invalid.json`
  - `scenario_09_missing_target_binding_invalid.json`
  - `scenario_10_ambiguous_operation_semantics_invalid.json`
  - `scenario_11_outcome_unverifiability_invalid.json`

补充说明：

- `paper/flagship/assets/same_case_pack/05_boundary_based_accountability.json` 已单独检查，两个 checker 都通过。
- 它没有放进主 comparison corpus，因为它与 `examples/valid-retention-review-evidence.json` 属于同一底层 case 的 OAP-style 重表达。

## Checker Invocation

### Reference validator

- canonical entry point：
  - `agent-evidence validate-profile <file>`
- 本次 automation 实际调用：
  - `agent_evidence.oap.validate_profile_file(...)`

说明：

- automation 直接调用库函数，是为了方便冻结 primary issue codes。
- 它与当前 repo 的 canonical CLI 指向同一 reference implementation。

### Independent checker

- entry point：
  - `python3 paper/flagship/prototype/independent_checker/check_minimal_boundary.py <file>`

### Comparison helper

- automation script：
  - `python3 paper/flagship/prototype/independent_checker/compare_checkers.py`

## Pass/Fail Comparison Table

| file | reference | reference labels | independent | independent labels |
| --- | --- | --- | --- | --- |
| `examples/minimal-valid-evidence.json` | PASS | - | PASS | - |
| `examples/valid-retention-review-evidence.json` | PASS | - | PASS | - |
| `examples/invalid-missing-required.json` | FAIL | schema_violation | FAIL | missing_validation_declaration |
| `examples/invalid-unclosed-reference.json` | FAIL | unresolved_output_ref | FAIL | broken_evidence_continuity |
| `examples/invalid-policy-link-broken.json` | FAIL | unresolved_evidence_policy_ref | FAIL | broken_policy_linkage |
| `examples/invalid-provenance-output-mismatch.json` | FAIL | provenance_output_refs_mismatch | FAIL | broken_evidence_continuity |
| `examples/invalid-validation-provenance-link-broken.json` | FAIL | unresolved_validation_provenance_ref | FAIL | broken_evidence_continuity |
| `paper/flagship/assets/specimens/scenario_03_access_decision_valid.json` | PASS | - | PASS | - |
| `paper/flagship/assets/specimens/scenario_03_access_decision_invalid_missing_policy_linkage.json` | FAIL | unresolved_policy_ref | FAIL | broken_policy_linkage |
| `paper/flagship/assets/specimens/scenario_04_object_derivation_handoff_valid.json` | PASS | - | PASS | - |
| `paper/flagship/assets/specimens/scenario_04_object_derivation_handoff_invalid_broken_evidence_continuity.json` | FAIL | unresolved_output_ref | FAIL | broken_evidence_continuity |
| `paper/flagship/assets/specimens/scenario_05_failed_or_denied_operation_valid.json` | PASS | - | PASS | - |
| `paper/flagship/assets/specimens/scenario_05_failed_or_denied_operation_invalid_missing_outcome.json` | FAIL | schema_violation | FAIL | missing_outcome_presence |
| `paper/flagship/assets/specimens/scenario_06_missing_identity_binding_invalid.json` | FAIL | unresolved_actor_ref | FAIL | broken_identity_binding |
| `paper/flagship/assets/specimens/scenario_07_temporal_inconsistency_invalid.json` | PASS | - | FAIL | temporal_inconsistency |
| `paper/flagship/assets/specimens/scenario_08_implementation_coupled_evidence_invalid.json` | PASS | - | FAIL | implementation_coupling_marker |
| `paper/flagship/assets/specimens/scenario_09_missing_target_binding_invalid.json` | FAIL | unresolved_subject_ref | FAIL | broken_target_binding |
| `paper/flagship/assets/specimens/scenario_10_ambiguous_operation_semantics_invalid.json` | PASS | - | FAIL | ambiguous_operation_semantics |
| `paper/flagship/assets/specimens/scenario_11_outcome_unverifiability_invalid.json` | PASS | - | FAIL | outcome_unverifiable |

## Major Agreement Points

- 在 19-file corpus 中，15 个文件保持 `PASS / FAIL` 对齐。
- 2 个现有 valid anchors 与 3 个新增 valid specimens 都被两个 checker 接受。
- 5 个现有 invalid anchors 与 5 个 direct/scenario invalid specimens 都被两个 checker 一致拒绝。
- `scenario_06` 与 `scenario_09` 说明 identity binding 和 target binding 目前已经能被两条 checker path 同时接住。

## Major Divergence Points

### 1. temporal inconsistency 是真实 pass/fail divergence

- `scenario_07_temporal_inconsistency_invalid.json`
- reference validator：`PASS`
- independent checker：`FAIL` with `temporal_inconsistency`

这说明 current reference validator 仍然没有 temporal sanity rule surface。

### 2. implementation-coupled evidence 是真实 pass/fail divergence

- `scenario_08_implementation_coupled_evidence_invalid.json`
- reference validator：`PASS`
- independent checker：`FAIL` with `implementation_coupling_marker`

这说明 current reference validator 仍然没有 portability-oriented coupling rule surface。

### 3. ambiguous operation semantics 是真实 pass/fail divergence

- `scenario_10_ambiguous_operation_semantics_invalid.json`
- reference validator：`PASS`
- independent checker：`FAIL` with `ambiguous_operation_semantics`

这说明“结构完整”不等于“operation semantics 已达到 boundary-level clarity”。

### 4. outcome unverifiability 是真实 pass/fail divergence

- `scenario_11_outcome_unverifiability_invalid.json`
- reference validator：`PASS`
- independent checker：`FAIL` with `outcome_unverifiable`

这说明“有 output ref”也不自动等于“outcome 可验证”。在当前 specimen 中，成功声明虽然存在，但 output 并没有引入可区分的 outcome object。

### 5. issue label abstraction level 仍然不同

- reference validator 倾向给出 staged implementation-facing code：
  - `schema_violation`
  - `unresolved_output_ref`
  - `unresolved_subject_ref`
- independent checker 倾向给出 boundary-facing taxonomy label：
  - `missing_outcome_presence`
  - `broken_evidence_continuity`
  - `broken_target_binding`

这不是 pass/fail divergence，但它意味着两者仍处在不同解释层次。

## What These Divergences Mean for the Flagship Paper

- 当前 repo 已经不只是有一个 second checker，而是已经出现 4 类真实、可重复的 pass/fail divergence。
- 这对旗舰论文有两层意义：
  - 第一，它说明 current reference validator 的 coverage boundary 到哪里为止，现在已经可见。
  - 第二，它说明 operation accountability 若被当作 verification boundary，就不能只读成 schema + ref closure。

同时也必须克制表述：

- 这些结果不证明 independent checker 一定更正确。
- 它们只证明：在当前 repo 资产上，已经存在一批 boundary classes，reference validator 还未直接覆盖，而 second checker 已把它们当作 failure surfaces。

## What the New Direct Failures Add

- `scenario_09` 让 missing target binding 从 planning taxonomy 变成 executed specimen。
- `scenario_10` 第一次把 ambiguous operation semantics 变成真实 checker divergence。
- `scenario_11` 第一次把 stronger outcome unverifiability 变成真实 checker divergence。

因此，这一轮最大的增量不是“又多了 3 个 invalid 文件”，而是：

- v1 failure taxonomy 的 8 个主类现在都已有 repo 内 executed specimen；
- checker comparison 已经从 2 类 divergence 扩展到 4 类 divergence；
- reviewer 可以直接看到 current validation surface 的边界在哪里停下。

## What Still Remains Before a Reviewer-Ready Validation Section

1. 还缺 repo 外场景或第三方 checker 证据
2. 还缺更强的 raw stage-level archival，而不只是当前 pass/fail + label freeze
3. 还缺与最终主文全稿完全整合后的 manuscript stitching

## Bottom Line

这份 comparison note 现在足以支持一个克制但明确的结论：在当前 19-file flagship corpus 上，两个 checker 在大多数文件上的通过/失败结论一致，但 temporal inconsistency、implementation-coupled evidence、ambiguous operation semantics 与 outcome unverifiability 已经暴露出 4 类真实的 pass/fail divergence。这使当前 validation package 从“planning-oriented evidence backlog”推进到了“可以进入正文和 appendix 的 reviewer-facing comparison asset”。
