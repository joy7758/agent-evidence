# AFAC2026 TRPS 路演 Markdown

## Page 1. 标题与一句话定位 / Positioning

主信息：TRPS：面向金融机构交易前风险治理的可审计智能决策与模拟执行平台。

讲稿提示：我们不是做自动交易，而是做交易前风险决策的治理层，把高风险动作变成可复核、可解释、可留痕的对象。

## Page 2. 行业痛点 / Pain Point

主信息：金融机构正在使用 AI 辅助策略、投顾和运营判断，但高风险建议在动作发生前缺少统一的复核和审计对象。

讲稿提示：真正的问题不是模型能不能给建议，而是机构能不能在建议进入业务动作前看清风险、责任和证据。

## Page 3. 目标客户与流程位置 / Customers and Workflow

主信息：目标客户包括券商资管、财富管理平台、银行投顾中台、风控与合规团队。TRPS 位于下游执行系统之前。

讲稿提示：TRPS 是 pre-action governance layer，帮助机构先复核，再决定是否继续流转。

## Page 4. TRPS 闭环架构 / Closed Loop

主信息：`input -> belief_state -> risk_distribution -> policy_gate -> action -> human_review -> simulated_execution -> receipt`

讲稿提示：每一步都能被机器读取，也能被评委或业务负责人复核。

## Page 5. 核心技术创新 / Core Innovation

主信息：TRPS 把 AI 建议、风险结构、策略约束、人工复核和审计回执合并为同一个可追溯对象。

讲稿提示：我们的核心不是收益预测，而是把“为什么放行、警告、升级或阻断”变成证据链。

## Page 6. Demo 场景 / Demo Scenarios

主信息：v0.2 demo 覆盖正常市场、市场冲击、误导性输入三类场景。

讲稿提示：这三类场景对应机构评审最关心的低风险、压力风险和越权风险。

## Page 7. Demo 结果 / Demo Results

主信息：场景 A 输出 `WARN`，场景 B 输出 `ESCALATE`，场景 C 输出 `BLOCK`。

讲稿提示：系统没有把高风险场景放行，而是触发复核、升级或阻断，并保留 receipt。

## Page 8. 量化指标 / Metrics

主信息：3 个场景、1 次危险动作拦截、2 次强制人工复核、100% 审计凭证完整率、0 次策略约束违规。

讲稿提示：这些指标让评委能看到系统的治理价值，而不是听抽象概念。

## Page 9. 替代方案对比 / Alternative Comparison

主信息：普通风控系统偏规则，普通 LLM 助手偏对话，普通 BI 看板偏展示。TRPS 专注决策前治理和 receipt。

讲稿提示：TRPS 的差异是把 AI 输出变成机构可复核的责任对象。

## Page 10. 商业模式 / Business Model

主信息：POC 试点、私有化部署、模块授权、年度维护与合规报告服务。

讲稿提示：买方愿意为降低越权动作、缩短复核时间和提高审计完整率付费。

## Page 11. 合规治理 / Governance

主信息：human-in-the-loop、kill switch、白名单动作、policy gate、audit receipt、模型/策略版本记录和数据最小化。

讲稿提示：我们主动把边界说清楚：v0.2 是合成受控 demo，不是外部批准或真实业务上线。

## Page 12. 里程碑与合作诉求 / Milestones and Ask

主信息：v0.1 完成可运行内核，v0.2 完成评委可看产品包，v0.3 将整理最终报名包、8 分钟路演稿和门户逐项填写版本。

讲稿提示：我们希望获得试点场景、业务反馈和评审建议，用合成与旁路方式逐步验证治理价值。
