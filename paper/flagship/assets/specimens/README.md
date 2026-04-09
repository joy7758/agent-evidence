# Validation Specimens

## 用途

这些文件是 flagship validation package 的 central specimens。它们服务于三类工作：

- multi-scenario corpus
- direct failure coverage
- checker comparison 与 reviewer-facing appendix

这些 specimen **不是** benchmark claims，也**不是**经验评估结果。它们只是把当前 repo 已经形成的 OAP v0.1 line 压成一组可以重复检查的 validation assets。

## 文件列表

| file | scenario or anchor | role | intended failure class | coverage mode |
| --- | --- | --- | --- | --- |
| `scenario_03_access_decision_valid.json` | access decision | valid central specimen | n/a | scenario-tied |
| `scenario_03_access_decision_invalid_missing_policy_linkage.json` | access decision | invalid single-rule specimen | missing/broken policy linkage | scenario-tied |
| `scenario_04_object_derivation_handoff_valid.json` | object derivation handoff | valid central specimen | n/a | scenario-tied |
| `scenario_04_object_derivation_handoff_invalid_broken_evidence_continuity.json` | object derivation handoff | invalid single-rule specimen | broken evidence continuity | scenario-tied |
| `scenario_05_failed_or_denied_operation_valid.json` | failed or denied operation | valid central specimen | n/a | scenario-tied |
| `scenario_05_failed_or_denied_operation_invalid_missing_outcome.json` | failed or denied operation | invalid single-rule specimen | missing outcome | scenario-tied |
| `scenario_06_missing_identity_binding_invalid.json` | boundary stress | invalid direct failure specimen | missing/broken identity binding | cross-scenario |
| `scenario_07_temporal_inconsistency_invalid.json` | boundary stress | invalid direct failure specimen | temporal inconsistency | cross-scenario |
| `scenario_08_implementation_coupled_evidence_invalid.json` | boundary stress | invalid direct failure specimen | implementation-coupled evidence | cross-scenario |
| `scenario_09_missing_target_binding_invalid.json` | boundary stress | invalid direct failure specimen | missing/broken target binding | cross-scenario |
| `scenario_10_ambiguous_operation_semantics_invalid.json` | boundary stress | invalid direct failure specimen | ambiguous operation semantics | cross-scenario |
| `scenario_11_outcome_unverifiability_invalid.json` | object derivation handoff anchor | invalid direct failure specimen | outcome unverifiability | scenario-tied stress |

## 结构锚点

这些 specimen 明确复用了当前 repo 的 central OAP v0.1 结构与术语，主要锚点包括：

- `spec/execution-evidence-operation-accountability-profile-v0.1.md`
- `schema/execution-evidence-operation-accountability-profile-v0.1.schema.json`
- `examples/minimal-valid-evidence.json`
- `examples/valid-retention-review-evidence.json`
- `agent_evidence/oap.py`

## 设计约束

- 所有 specimen 都保持 current OAP v0.1 shape。
- 所有新增 invalid specimen 都只故意打破 1 条主规则。
- `scenario_06` 到 `scenario_10` 用于直打 cross-scenario failure classes，不对应新增业务故事。
- `scenario_11` 仍然复用 `object derivation handoff` 这个 central scenario，因为 outcome unverifiability 在“宣称派生产物已发出”的情形下最容易被 reviewer 直观看懂。
- 这些文件不会覆盖现有 released examples，只是旗舰 validation corpus 的补充层。

## 当前覆盖读法

当前 specimen set 已经把 v1 failure taxonomy 的 8 个主类全部压到了 repo 内可运行资产上：

- identity binding
- target binding
- operation semantics
- policy linkage
- evidence continuity
- outcome accountability / outcome unverifiability
- temporal consistency
- implementation-coupling

这不等于 taxonomy 已经冻结，只等于当前旗舰 validation package 已经不再停留在 planning prose。
