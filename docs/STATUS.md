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
- M8 可选 trust binding 扩展：已完成
- M9 EDC augmentation 边界与最小接入文档：已完成
- M7 旗舰论文规划包：已完成

## 当前落地产物
- profile 规范：`spec/execution-evidence-operation-accountability-profile-v0.1.md`
- schema：`schema/execution-evidence-operation-accountability-profile-v0.1.schema.json`
- 样例：`examples/minimal-valid-evidence.json` 及 3 个 invalid 样例
- validator：`agent_evidence/oap.py` 与 CLI 命令 `agent-evidence validate-profile <file>`
- demo：`demo/run_operation_accountability_demo.py`
- 文稿：`docs/research-brief-zh.md`、`docs/abstract-en.md`
- 可选 trust-binding 扩展：`validation.trust_bindings[]`、对应样例与说明文档

## 已验证结果
- `./.venv/bin/ruff check agent_evidence/oap.py agent_evidence/cli/main.py demo/run_operation_accountability_demo.py tests/test_operation_accountability_profile.py` 通过
- `./.venv/bin/python -m pytest tests/test_operation_accountability_profile.py tests/test_aep_profile.py tests/test_cli.py` 通过
- `python3 demo/run_operation_accountability_demo.py` 通过
- `validate-profile` 对 valid 样例返回 `ok: true`
- `validate-profile` 对 invalid 样例返回 `ok: false` 且带明确 error code
- `validate-profile` 对 trust-binding valid 样例返回 `ok: true`
- `validate-profile` 对 trust-binding invalid 样例返回 `ok: false` 且主错误码为 `trust_binding_target_digest_mismatch`

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

## M9 EDC augmentation 边界与最小接入文档
- 状态：已完成
- 定位结论：
  - EDC 不是本仓库的新研究主线，不是替代品，也不是竞争关系。
  - 在 dataspace / policy-governed data exchange 场景中，EDC 被定位为 `agent-evidence` 的 execution-evidence augmentation layer。
  - EDC 负责 catalog、contract、transfer governance；`agent-evidence` 负责把执行过程打包成可独立验证的 evidence。
- 本轮新增产物：
  - `docs/edc/EDC_AUGMENTATION_BOUNDARY.md`
  - `docs/edc/edc_minimal_evidence_profile_draft.md`
  - `docs/edc/edc_demo_minimal_path.md`
  - `README.md` 中新增最小导航入口 `EDC / Dataspace augmentation`
  - `plans/implementation-plan.md` 同步新增 EDC augmentation 文档里程碑
- 本轮边界收敛：
  - 只做最小接入 demo 路径、最小 profile 草案、最小独立验证说明
  - 首个推荐接入面是 control-plane event extension，不先改 persistence，也不先碰 data plane
  - 不扩张成完整 EDC 平台、connector 产品、dataspace 全栈、通用 usage control 系统
- 官方依据：
  - EDC Control Plane 文档明确控制面负责 catalog、contract agreement、transfer governance，且 transfer 不直接发送数据
  - EDC Extensions 文档明确运行时扩展入口为 `ServiceExtension`
  - EDC Service Layers 文档明确 `EventRouter`、in-process events、callbacks 是官方事件接入面
  - DSP 官方规范明确范围是 publish data、negotiate agreements、access data
- 本轮核验：
  - `git diff --check`：通过
  - 文档引用来源：仅使用 EDC / DSP 官方公开文档链接
  - 本轮未改动 Python 代码、schema、examples、tests，因此未额外运行代码路径测试

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

## M8 可选 trust binding 扩展
- 状态：已完成
- 本轮新增或更新：
  - spec：为 `validation.trust_bindings[]` 增加可选外部验证挂接位
  - schema：新增 trust binding 结构定义
  - validator：新增本地 target closure 与 digest 一致性校验
  - examples：新增 `valid-trust-binding-evidence.json` 与 `invalid-trust-binding-digest-mismatch.json`
  - demo：最小 demo 增加 1 个 trust binding 占位示例
  - docs：README、中文 README、cookbook、demo 说明补齐“trust binding 不是本地签名系统”边界
- 本轮边界结论：
  - trust binding 是可选 external verification hook，不是 mandatory signing system
  - 当前 validator 只验证本地 target / digest 一致性，不验证外部透明日志、registry 或第三方信任服务
  - `export` / `verify-export` 继续以本仓库内建 manifest signing 为主，不依赖 trust binding
- 本轮核验：
  - 命令：`./.venv/bin/python -m pytest tests/test_operation_accountability_profile.py`
    - 结果：`10 passed, 1 warning in 0.61s`
    - 是否通过：通过
  - 命令：`./.venv/bin/agent-evidence validate-profile examples/valid-trust-binding-evidence.json`
    - 结果：`ok: true`
    - 是否通过：通过
  - 命令：`./.venv/bin/agent-evidence validate-profile examples/invalid-trust-binding-digest-mismatch.json`
    - 结果：`ok: false`，primary error code `trust_binding_target_digest_mismatch`
    - 是否通过：通过
  - 命令：`python3 demo/run_operation_accountability_demo.py`
    - 结果：demo 闭环执行完成，末尾输出 `PASS execution-evidence-operation-accountability-profile@0.1 ...`
    - 是否通过：通过

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
  - DataCite API 可见 Zenodo DOI `10.5281/zenodo.19334062`
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
