# 8 分钟路演逐字稿

## Slide 1. 标题与一句话定位

Screen content: TRPS：面向金融机构交易前风险治理的可审计智能决策与模拟执行平台。

Speaker script: 各位评委好，TRPS 不是自动交易机器人，而是金融机构交易前风险治理和审计留痕平台。我们关注的是动作发生前，机构如何把 AI 建议、风险、策略边界、人工复核和审计凭证放到同一条可复核链路里。

Time budget: 0:00-0:40

## Slide 2. 行业痛点

Screen content: AI 能生成建议，但机构需要责任、边界和证据。

Speaker script: 金融机构已经开始使用 AI 辅助投顾、资管和运营判断。问题不在于模型能不能生成建议，而在于高风险建议进入下游动作前，机构能不能知道风险从哪里来、规则是否触发、谁复核、凭证是否完整。

Time budget: 0:40-1:15

## Slide 3. 目标客户与流程位置

Screen content: 券商资管、财富管理平台、银行投顾中台、风控与合规团队。

Speaker script: TRPS 的位置在下游执行系统之前。它服务的是风险治理、合规、投顾中台和资管运营团队，帮助这些团队把复杂建议转成可检查的治理对象。

Time budget: 1:15-1:50

## Slide 4. 闭环架构

Screen content: scenario input -> belief state -> risk distribution -> policy gate -> human review -> simulated execution -> audit receipt

Speaker script: 这是 TRPS 的核心闭环。我们先把输入场景结构化，再拆成风险分布，通过策略闸门触发人工复核、升级、阻断或安全降级，最后生成 audit receipt。

Time budget: 1:50-2:30

## Slide 5. 核心技术创新

Screen content: 把 AI 建议转成可审计决策对象。

Speaker script: TRPS 的创新不是收益预测，而是将 AI 建议前置到治理层。每个 receipt 绑定场景、策略版本、触发约束、人工复核状态、最终动作、限制说明和可复现哈希。

Time budget: 2:30-3:10

## Slide 6. Demo 场景

Screen content: 正常市场、市场冲击、误导性输入。

Speaker script: 当前 demo 有三类合成受控场景。正常市场展示低风险也能留痕；市场冲击展示高波动升级；误导性输入展示证据缺失和越权意图会被挡住。

Time budget: 3:10-3:50

## Slide 7. Demo 结果

Screen content: WARN、ESCALATE、BLOCK。

Speaker script: 场景 A 输出 warning，场景 B 输出 escalation，场景 C 输出 block。重点是系统没有把高风险场景当成普通建议继续流转，而是留下可复核的审计凭证。

Time budget: 3:50-4:30

## Slide 8. 量化指标

Screen content: 3 个场景、1 次危险动作拦截、2 次强制人工复核、0 次策略约束违规。

Speaker script: 这些指标对应评委能理解的业务价值：覆盖场景数量、危险动作拦截、人工复核触发、凭证完整率和约束违规次数。我们的 readiness score 是 95.17。

Time budget: 4:30-5:10

## Slide 9. 替代方案对比

Screen content: 普通风控、普通 LLM、普通 BI 看板都不等同于 TRPS。

Speaker script: 普通风控偏规则执行，普通 LLM 偏文本生成，普通 BI 看板偏展示。TRPS 的定位是动作前治理和 audit receipt，让模型输出进入机构责任链。

Time budget: 5:10-5:45

## Slide 10. 商业模式

Screen content: POC fixed fee、private deployment、module licensing、annual maintenance、governance report service。

Speaker script: 商业化可以从 POC 固定费用开始，之后进入私有化部署、模块授权和年度治理报告服务。买方的核心收益是减少越权动作、减少重复复核和提高审计完整率。

Time budget: 5:45-6:30

## Slide 11. 合规治理

Screen content: human-in-the-loop、kill switch、white-listed actions、policy versioning、audit receipt。

Speaker script: 我们主动把边界说清楚。TRPS 不提供个人投资建议，不连接真实交易链路，不把本地验证描述为外部批准。它默认人机协同和安全停止。

Time budget: 6:30-7:15

## Slide 12. 里程碑与合作诉求

Screen content: v0.1 内核、v0.2 Demo 包、v0.3 最终报名包；寻求试点合作。

Speaker script: 最后 30 秒，我们现在寻求试点合作，在不接真实交易、不做自动执行的前提下，从 shadow mode 和 human-in-the-loop pilot 开始验证。我们希望和金融机构一起，把 AI 决策从“能生成建议”推进到“能被治理和审计”。

Time budget: 7:15-8:00
