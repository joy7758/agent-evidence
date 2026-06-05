# 当前状态

> Current release-prep status for v0.3.1 is tracked in
> `docs/release-readiness.md` and `docs/release-checklist.md`. The historical
> notes below include earlier v0.1/v0.2 readiness context.

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
- M12 AGT-to-EEOAP v0.1 reference adapter：已完成
- M12b AGT docs-only interoperability note：已完成（merged upstream）
- M12c AGT AuditEntry accountability export example：已完成（merged upstream）
- M7 旗舰论文规划包：已完成
- M8 frozen EDC Java spike main-repo entry：已完成

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

## M12 AGT-to-EEOAP v0.1 reference adapter
- 状态：已完成
- 定位结论：
  - 本轮只做 `AGT-to-EEOAP Interoperability Adapter`，作为一个外部、非侵入式 reference integration。
  - AGT 被定位为 upstream runtime governance source；EEOAP v0.1 保持为 external operation-accountability statement format。
  - 本轮不修改 EEOAP v0.1 schema，不修改现有 validator 语义，不引入 AGT package dependency。
- 本轮新增产物：
  - `docs/cookbooks/agt_to_eeoap_v0_1.md`
  - `integrations/agt/README.md`
  - `integrations/agt/convert_agt_evidence_to_eeoap.py`
  - `integrations/agt/fixtures/agt-evidence-minimal.synthetic.json`
  - `integrations/agt/fixtures/eeoap-from-agt.expected.json`
  - `tests/test_agt_adapter.py`
- 本轮边界收敛：
  - `agt-evidence-minimal.synthetic.json` 明确为 synthetic AGT-like runtime evidence，不声明为 AGT 官方 schema。
  - 转换器复用 `agent_evidence.oap.sha256_digest` 与 `with_recomputed_integrity` 计算 `references_digest`、`artifacts_digest`、`statement_digest`。
  - 转换结果只使用 EEOAP v0.1 schema 允许的顶层字段。
  - AGT runtime evidence 和 decision receipt 均进入 `evidence.artifacts[]`，不新增 `agt_*` 顶层字段。
- 验收结果：
  - synthetic AGT-like fixture 能转换为合法 EEOAP v0.1 statement。
  - 转换结果通过 `agent-evidence validate-profile` / `validate_profile_file`。
  - AGT-specific material 只作为 `evidence.artifacts[]` 引用，不进入顶层字段。
  - 现有 profile schema 和 validator 语义保持不变。
- 对外互操作反馈：
  - AGT issue：`https://github.com/microsoft/agent-governance-toolkit/issues/1314`
- 上游合并状态：
  - docs-only interoperability note：`microsoft/agent-governance-toolkit#1319`
  - AuditEntry accountability export example：`microsoft/agent-governance-toolkit#1370`
- 本轮核验：
  - 命令：`python3 integrations/agt/convert_agt_evidence_to_eeoap.py --input integrations/agt/fixtures/agt-evidence-minimal.synthetic.json --output integrations/agt/fixtures/eeoap-from-agt.generated.json`
    - 结果：生成 `integrations/agt/fixtures/eeoap-from-agt.generated.json`
    - 是否通过：通过
  - 命令：`agent-evidence validate-profile integrations/agt/fixtures/eeoap-from-agt.generated.json`
    - 结果：`ok: true`, `issue_count: 0`
    - 是否通过：通过
  - 命令：`python -m pytest tests/test_agt_adapter.py`
    - 结果：`1 passed`
    - 是否通过：通过
  - 命令：`ruff check integrations/agt/convert_agt_evidence_to_eeoap.py tests/test_agt_adapter.py`
    - 结果：`All checks passed!`
    - 是否通过：通过
  - 命令：`python -m pytest`
    - 结果：`67 passed, 1 skipped, 15 warnings`
    - 是否通过：通过；warnings 为既有 Python 3.14 / langchain 兼容性提示

## M12b AGT docs-only interoperability note
- Status: merged upstream
- PR: `microsoft/agent-governance-toolkit#1319`
- Issue: `microsoft/agent-governance-toolkit#1314`
- Scope: documentation-level interoperability note for external operation-accountability profiles
- Boundary: no AGT runtime changes, no replacement of `agt verify --evidence`, no AGT package dependency, no new runtime contract

## M12c AGT AuditEntry accountability export example
- Status: merged upstream
- PR: `microsoft/agent-governance-toolkit#1370`
- Issue: `microsoft/agent-governance-toolkit#1314`
- Scope: real `AuditService` / `AuditEntry` output -> smallest-stable external accountability export shape -> EEOAP mapping example
- Boundary: no AGT runtime changes, no `AuditEntry` / `AuditService` contract changes, no replacement of `agt verify --evidence`, no required dependency on external validator

## 投稿状态同步
- `Execution Evidence as a Verifiable Workflow Object: A Minimal Profile and Validator for Operation Accountability` — venue `The Journal of Systems & Software`；manuscript ID `JSSOFTWARE-S-26-00981`；当前状态 `rejected`；备注：已拒稿，不再作为在审稿件统计
- `A Minimal Verifiable Profile and Validator Path for Single-Operation Accountability in FDO and Data-Space Settings` — venue `SIDS 2026 (IEEE MDM 2026 workshop)`；当前状态 `withdrawn`；备注：已撤回，不再作为在审稿件统计

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

## M6 TOSEM 中文论文工作区
- 状态：已完成
- 产出目录：`paper/tosem_cn/`
- 产出文件：
  - `00_title_abstract_keywords.md`
  - `01_outline.md`
  - `02_introduction.md`
  - `03_problem_and_design_goals.md`
  - `04_minimal_profile.md`
  - `05_validation_model_and_validator.md`
  - `06_artifact_package.md`
  - `07_evaluation.md`
  - `08_discussion_limits_threats.md`
  - `09_related_work_scaffold.md`
  - `10_conclusion.md`
  - `manuscript_cn.md`
  - `todo_evidence_gaps.md`
- 写作锚点：
  - profile spec：`spec/execution-evidence-operation-accountability-profile-v0.1.md`
  - JSON Schema：`schema/execution-evidence-operation-accountability-profile-v0.1.schema.json`
  - examples：`examples/README.md` 与 1 个 valid / 3 个 invalid 样例
  - validator：`agent_evidence/oap.py`
  - CLI：`agent_evidence/cli/main.py`
  - tests：`tests/test_operation_accountability_profile.py`
  - demo：`demo/README.md`、`demo/scenario.md`、`demo/run_operation_accountability_demo.py`
- 本轮额外核验：
  - 本地 `git tag` 可见 `v0.2.0`
  - `git show v0.2.0` 可见该 tag 冻结了 OAP v0.1 package
  - GitHub Release API 可见公开 release `Agent Evidence v0.2.0`
  - DataCite API 可见当时的 Zenodo v0.2.0 version DOI；当前项目主 DOI 见
    `docs/release-readiness.md`
- 投稿前待补：
  - 若后续继续扩大 release / DOI 同步面，需要逐项判断其他历史 specimen 材料是否保留旧 DOI `10.5281/zenodo.19055948`
  - related work 正式引文
  - 面向论文正文的图表、表格与 artifact appendix 组织

## M7 旗舰论文规划包
- 状态：已完成
- 产出目录：`paper/flagship/`
- 产出文件：
  - `00_master_positioning.md`
  - `01_tosem_vs_flagship_split.md`
  - `02_minimal_verification_boundary.md`
  - `03_failure_taxonomy_v1.md`
  - `04_evidence_gap_checklist.md`
  - `05_titles_abstract_outline.md`
  - `06_six_month_roadmap.md`
  - `WORKLOG.md`
- 本轮定位结论：
  - TOSEM 稿件继续作为当前 research line 的最小实现、stake-in-the-ground 与 smallest verifiable artifact
  - 旗舰论文不再重复“能否实现 profile / validator / artifact package”，而是上移为“为何 operation accountability 必须被定义为 first-class verification boundary”
- 本轮术语策略：
  - 继续复用仓库当前主术语：`operation accountability statement`、`minimal verifiable profile`、`profile-aware validator`、`policy / provenance / evidence / validation`
  - `machine-actionable object systems` 仅作为旗舰论文的总括性 framing，不替代仓库当前 `FDO-based agent systems` 表述
  - `STAP / data space` 在本轮规划中只作为后续 external validation 目标语境，不写成当前仓库已完成证据
- 本轮仍待后续补强的旗舰证据：
  - 独立 checker
  - 更完整 failure taxonomy 覆盖
  - 多场景外部有效性
  - 更强的 logs / provenance / policy / audit trail 同案比较

## M8 frozen EDC Java spike main-repo entry
- 状态：已完成
- 定位结论：
  - 这轮不是功能开发，也不是把整条 Java spike 并入主仓。
  - 目标只是给已经冻结的 EDC Java spike 增加一个主仓可见、可稳定引用的入口。
- 本轮新增或更新：
  - `docs/edc-java-spike/README.md`
  - `README.md`
  - `docs/STATUS.md`
  - `plans/implementation-plan.md`
- 本轮收敛结果：
  - 主仓现在能稳定指向 tag `edc-java-spike-freeze-v0.1` 下的 freeze package
  - 入口页明确说明了这条 spike 验证了什么、为什么先停在 freeze package、以及为什么不直接 merge 整条 Java / Gradle spike
  - 本轮没有复制 `spikes/edc-java-extension/`，没有合并 Java 代码，也没有引入新的 runtime 能力
- 本轮核验：
  - `git diff --check`：待提交前复验
  - 本轮仅入口整理与文档更新，未改动 Python 主包或运行时代码，因此未额外重跑测试
