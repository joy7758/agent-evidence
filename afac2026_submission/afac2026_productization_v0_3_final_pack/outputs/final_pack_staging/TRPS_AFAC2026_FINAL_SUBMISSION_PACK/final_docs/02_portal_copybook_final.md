# AFAC2026 Portal Copybook Final

## 1. 项目名称，中文

TRPS：面向金融机构交易前风险治理的可审计智能决策与模拟执行平台

## 2. 项目名称，英文

TRPS: An Auditable Intelligent Decision and Simulated Execution Platform for Pre-Trade Risk Governance in Financial Institutions

## 3. 一句话简介，中文，80 字以内

TRPS 将交易前高风险决策转化为策略闸门、人工复核和审计回执，帮助金融机构先治理再动作。

## 4. One-Sentence Summary, English, within 160 characters

TRPS turns pre-trade risk decisions into policy gates, human review states, and audit receipts before downstream action.

## 5. 项目摘要，中文，500 字以内

TRPS 面向金融机构交易前风险治理场景，提供可审计智能决策与模拟执行平台。系统把场景输入转化为 belief state、risk distribution、policy gate、human review、simulated execution 和 audit receipt，使高风险建议在进入下游动作前被结构化复核。当前包包含可运行离线 Demo、合成受控评估、三类风险场景、完整 receipt、门户文案、路演稿和最终 ZIP。本项目不使用真实客户数据，不连接真实交易系统，不生成真实订单，不提供个人投资建议，目标是从 shadow mode 与 human-in-the-loop pilot 开始寻求试点合作。

## 6. Project Abstract, English, within 1000 characters

TRPS is a pre-trade risk-governance platform for financial institutions. It turns scenario inputs into belief states, risk distributions, policy gates, human review states, simulated execution outcomes, and audit receipts. The current pack includes an offline demo, synthetic controlled scenarios, complete receipts, portal copy, pitch scripts, and a final local ZIP package. TRPS does not use real customer data, connect to external execution systems, generate actual transactions, or provide personal investment advice. The project seeks pilot collaboration through shadow mode and human-in-the-loop workflows before any institution-specific rollout.

## 7. 技术创新，中文，500 字以内

TRPS 的创新点是把 AI 金融建议从“文本输出”转成“交易前治理对象”。系统将输入意图、证据完整性、市场压力、流动性压力和操作风险结构化，再由策略闸门选择警告、复核、升级、阻断或安全降级。每次决策都会生成 audit receipt，记录模型版本、策略版本、场景哈希、触发约束、人工复核状态、最终动作、限制说明和可复现哈希。它强调责任链和审计链，而不是收益预测。

## 8. 应用场景，中文，500 字以内

TRPS 可用于券商资管、财富管理平台、银行投顾中台、风控与合规团队的交易前复核流程。典型场景包括：市场冲击下的风险预算复核、AI 生成建议的策略闸门、证据缺失时的阻断、冲突信号下的安全降级、人工复核前的责任记录、以及事后审计材料生成。当前 demo 覆盖正常市场、市场冲击和误导性输入三类合成受控场景。

## 9. 商业价值，中文，500 字以内

TRPS 帮助机构降低越权动作风险、减少人工复核重复劳动、提高审计凭证完整率、缩短事故复盘时间，并降低组织使用 AI 的治理风险。商业路径可从 POC fixed fee 开始，进入私有化部署、模块授权、年度维护和治理报告服务。试点路径建议先做 synthetic controlled evaluation，再做 historical control-signal replay、shadow mode、human-in-the-loop pilot 和 controlled rollout。

## 10. 合规治理，中文，300 字以内

TRPS 默认 human-in-the-loop，保留白名单动作、禁止动作、kill switch、策略版本、模型版本、audit receipt、证据最小化和敏感数据最小化。当前包只做合成受控评估和模拟执行，不提供个人投资建议，不连接真实交易链路，也不声称监管认可。

## 11. 关键词，中文

交易前风险治理；可审计智能决策；审计回执；人工复核；策略闸门；合成受控评估；金融机构 AI 治理；TRPS

## 12. Keywords, English

pre-trade risk governance; auditable intelligent decision; audit receipt; human-in-the-loop; policy gate; synthetic controlled evaluation; financial AI governance; TRPS

## 13. 团队简介草稿，中文，300 字以内

团队当前聚焦 AI 决策证据、责任链、金融风险治理和可复核 Demo 工程化。项目已有本地可运行内核、离线可视化 Demo、合成受控评估和完整提交材料包。团队正在寻求金融机构、投顾中台、资管风控或合规团队的试点合作，以旁路和人机协同方式验证治理价值。

## 14. 参赛优势，中文，300 字以内

TRPS 不是泛化聊天助手，也不是收益叙事项目，而是围绕金融机构“动作前治理”构建产品闭环。它具备离线 Demo、三类风险场景、策略闸门、人工复核、audit receipt、指标面板和最终报名 ZIP，评委可以直接看到从输入到问责凭证的完整链路。

## 15. 项目阶段，中文，100 字以内

本地最终报名准备阶段：已完成 v0.1 内核、v0.2 可视化材料、v0.3 最终报名包，正在寻求试点合作。

## 16. 可量化指标，中文，300 字以内

当前合成受控 Demo 覆盖 3 个风险场景，危险动作拦截 1 次，强制人工复核触发 2 次，审计凭证完整率 100%，策略约束违规次数 0，审计链路关联率 100%，本地平均决策耗时 29ms。以上指标用于展示治理闭环，不用于真实业务吞吐或收益承诺。

## 17. 融资/合作诉求，中文，200 字以内

寻求金融机构、投顾中台、资管风控、合规团队和技术合作伙伴开展 POC。合作方式建议从 synthetic controlled evaluation、control-signal replay、shadow mode 和 human-in-the-loop pilot 开始。

## 18. 附件说明，中文，200 字以内

附件建议上传 `TRPS_AFAC2026_FINAL_SUBMISSION_PACK.zip`。其中包含项目方案、商业计划、治理说明、路演稿、Demo 说明、Q&A、claim-evidence map、离线 Demo、验证报告、manifest 和 readiness score。
