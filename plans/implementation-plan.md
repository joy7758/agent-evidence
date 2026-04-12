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

## M8 可选 trust binding 扩展
- 输入：
  - 当前 OAP v0.1 spec/schema/validator/examples/demo
  - README 与 cookbook 中现有签名、离线验证、detached anchor 说明
- 输出：
  - `validation.trust_bindings[]` 可选字段
  - 对应 schema 与 validator 校验
  - 1 个 valid trust-binding 样例与 1 个 single-failure invalid 样例
  - README / cookbook / demo / STATUS 中的边界澄清
- 验收条件：
  - trust binding 明确是可选外部验证挂接点，不是强制签名系统
  - 支持多个机制标签，不内置绑定任何单一信任系统
  - validator 只检查本地目标引用与 digest 一致性，不伪装成外部系统验证器
  - 最小 demo 与既有 local signing / verify-export 路径保持不变

## M9 EDC augmentation 边界、最小 profile 草案与最小 demo 路径
- 输入：
  - 官方 EDC 文档中的 control plane、extensions、events / callbacks 材料
  - 官方 DSP 规范中的 protocol scope 材料
  - 当前仓库已有 `spec/`、`schema/`、`examples/`、`demo/`、`docs/` 结构
- 输出：
  - `docs/edc/EDC_AUGMENTATION_BOUNDARY.md`
  - `docs/edc/edc_minimal_evidence_profile_draft.md`
  - `docs/edc/edc_demo_minimal_path.md`
  - `README.md` 最小导航入口
  - `docs/STATUS.md` 里程碑记录
- 验收条件：
  - 明确 EDC 是 `agent-evidence` 的 execution-evidence augmentation layer，而不是新主线
  - 明确 EDC 与 `agent-evidence` 的职责边界：前者负责 exchange / contract / transfer governance，后者负责执行证据
  - 最小 profile 草案只保留独立验证所需字段，不带 secrets、privateProperties、内部实现细节
  - 最小 demo 路径清楚描述 asset -> policy / contract definition -> contract agreement -> transfer process -> evidence bundle -> independent verify
  - 明确首个推荐接入面是 control-plane event extension / exporter，而不是 persistence 或 data plane
  - 仅引用官方 EDC / DSP 公开材料，不基于二手解读
