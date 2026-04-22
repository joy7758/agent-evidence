# implementation plan

## M1 仓库扫描与计划
- 输入：现有 `spec/`、`schema/`、`examples/`、`scripts/`、`tests/`、CLI 结构。
- 输出：`docs/STATUS.md`、`plans/implementation-plan.md`。
- 验收条件：明确已有资产、缺失资产、最小新增路径、建议技术栈。

## M2 最小 profile 与 schema
- 输入：现有 `execution-evidence-object` 原型、FDO 映射文档、当前主题边界。
- 输出：新增最小 profile 规范文档和 JSON Schema。
- 验收条件：字段能回答谁执行、对什么对象执行、执行了什么 operation、受何 policy 约束、输入输出如何引用、结果是什么、完整性材料是什么、第三方如何验证。

## M3 样例集
- 输入：M2 产出的规范与 schema。
- 输出：1 个 valid 样例、3 个 invalid 样例、`examples/README.md`。
- 验收条件：每个 invalid 样例只破坏 1 条主规则，README 清楚解释通过或失败原因。

## M4 validator 与 CLI
- 输入：M2 schema、M3 样例、现有 Python 包和 CLI。
- 输出：可复用的 profile 校验模块、CLI 命令、测试。
- 验收条件：至少覆盖结构完整性、必填字段、引用闭合、policy/provenance/evidence 关联一致性；输出 JSON 结果、人类可读摘要、明确 error code。

## M5 demo 与文稿
- 输入：M2-M4 产物。
- 输出：单链路 `demo/` 闭环、`docs/research-brief-zh.md`、`docs/abstract-en.md`。
- 验收条件：demo 可运行并打印验证结果；文稿聚焦 minimal profile / validator / demo / accountability gap，不扩展成宏大平台叙事。

## M6 TOSEM 中文论文工作区
- 输入：M2-M5 产物、`submission/` handoff 文档、release / DOI 元数据。
- 输出：`paper/tosem_cn/` 章节化中文草稿、拼接稿、证据缺口清单、figures / tables、DOI/version audit。
- 验收条件：
  - 统一定位为 TOSEM methodology + validator + artifact paper
  - 统一主论点为 “a minimal verifiable profile for operation accountability in FDO-based agent systems”
  - 所有章节只复用已核实仓库事实，未支撑处显式标为 `TODO` 或“投稿前待补”
  - 图表与表格只使用当前仓库可核实内容，不虚构额外评估结果
  - DOI / version 审计只在低风险路径内做安全措辞同步
  - 不扩展成泛化 FDO survey 或 AI governance 综述

## M7 旗舰论文规划包
- 输入：
  - `paper/tosem_cn/` 与 `paper/tosem_en/` 当前主线
  - `spec/`、`schema/`、`examples/`、`agent_evidence/oap.py`、`demo/`
  - `docs/fdo-mapping/`、`roadmap/`、`submission/` 中已存在的定位材料
- 输出：
  - `paper/flagship/00_master_positioning.md`
  - `paper/flagship/01_tosem_vs_flagship_split.md`
  - `paper/flagship/02_minimal_verification_boundary.md`
  - `paper/flagship/03_failure_taxonomy_v1.md`
  - `paper/flagship/04_evidence_gap_checklist.md`
  - `paper/flagship/05_titles_abstract_outline.md`
  - `paper/flagship/06_six_month_roadmap.md`
  - `paper/flagship/WORKLOG.md`
- 验收条件：
  - 明确区分 TOSEM 与旗舰论文分工，不把 TOSEM 重写成旗舰稿
  - 旗舰论文主线转为 problem-defining paper，而非另一个 profile paper
  - 明确提出 minimal verification boundary、failure taxonomy、external validation agenda
  - 保持 Chinese-first、plain language、结构紧凑
  - 不修改现有 `paper/submission_tosem/`、blind package 或 review artifacts

## M8 frozen EDC Java spike main-repo entry
- 输入：
  - 已冻结的 EDC Java spike tag：`edc-java-spike-freeze-v0.1`
  - 当前主仓 README、`docs/STATUS.md` 与本计划文件
  - freeze package 中的 summary / validated surfaces / handoff / runbook 文档
- 输出：
  - `docs/edc-java-spike/README.md`
  - `README.md` 中的最小入口导航
  - `docs/STATUS.md` 的入口整理里程碑
  - 如有必要，本计划中的对应里程碑
- 验收条件：
  - 主仓新增一个克制的 EDC Java spike 入口页
  - 所有 freeze package 链接都使用基于 tag `edc-java-spike-freeze-v0.1` 的稳定 GitHub 链接
  - 明确说明当前应引用 freeze package，而不是把整条 Java spike 直接并入 `main`
  - 不复制 `spikes/edc-java-extension/`，不合并 Java 代码，不新增运行时功能
  - `git diff --check` 通过

## M12 AGT-to-EEOAP v0.1 reference adapter
- 输入：
  - 当前 canonical package：`Execution Evidence and Operation Accountability Profile v0.1`
  - 现有 `agent_evidence/oap.py` digest / validation helpers
  - 现有 `schema/`、`integrations/`、`docs/cookbooks/`、`tests/` 结构
  - 一个明确标注为 synthetic 的 AGT-like runtime evidence fixture
- 输出：
  - `docs/cookbooks/agt_to_eeoap_v0_1.md`
  - `integrations/agt/README.md`
  - `integrations/agt/convert_agt_evidence_to_eeoap.py`
  - `integrations/agt/fixtures/agt-evidence-minimal.synthetic.json`
  - `integrations/agt/fixtures/eeoap-from-agt.expected.json`
  - `tests/test_agt_adapter.py`
- 验收条件：
  - 转换器读取 synthetic AGT-like evidence，并输出合法 EEOAP v0.1 statement
  - 输出 statement 通过现有 `validate_profile_file` 和 CLI `agent-evidence validate-profile`
  - AGT-specific runtime material 被保留为 `evidence.artifacts[]` 中的 artifact 引用，不新增顶层字段
  - 不修改 EEOAP v0.1 schema、不修改 validator 语义、不引入 AGT package dependency
  - 文档明确 non-goals：不改 AGT runtime、不改 AGT policy engine、不新增 EEOAP 字段、不替代 `agt verify --evidence`
