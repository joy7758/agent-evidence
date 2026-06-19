# AFAC 初创组项目方案

## 1. 项目背景

金融机构正在把 AI 能力引入投顾、资管、运营和风控流程，但高风险决策在动作发生前往往缺少统一、可复核、可留痕的治理对象。TRPS 面向这一空白，把交易前决策请求转化为结构化风险判断、策略闸门、人工复核状态和审计回执。

## 2. 金融机构痛点

- AI 生成建议容易和业务动作混在一起，责任边界不清。
- 高波动或证据缺失场景下，人工复核需要临时收集材料。
- 风控规则、合规边界和模型输出常分散在不同系统中。
- 事后审计只能看到结果，难复盘当时为什么放行、警告、升级或阻断。

## 3. TRPS 解决方案

TRPS 是一个 decision-support / governance layer。它接收合成或机构内部可控的场景输入，形成 belief state 和 risk distribution，再通过 constrained policy 选择 gate action，最后生成包含证据、策略、复核和限制说明的 receipt。

## 4. 产品闭环

`scenario input -> belief_state -> risk_distribution -> policy_gate -> action -> human_review -> simulated_execution -> receipt -> metrics`

v0.2 的静态 demo 让评委看到三类场景如何进入同一条闭环，并看到危险动作如何被拦截或升级复核。

## 5. 技术架构

- 数据层：合成受控场景、v0.1 decision/receipt 输出、指标 JSON。
- 风险结构层：belief state、risk distribution、triggered constraints。
- 策略闸门层：白名单动作、约束检查、安全降级、阻断。
- 人工复核层：角色、状态、复核范围和责任记录。
- 回执层：receipt id、policy version、scenario hash、final action、rationale。
- 展示层：离线 HTML/CSS/JS demo 和提交材料 Markdown。

## 6. 核心创新

TRPS 把“AI 建议是否应该继续流转”从口头判断变成可复核对象。它不以收益叙事为中心，而以风险治理、证据完整性、人工责任和可复现回执为中心。

## 7. Demo 场景

- 场景 A：正常市场低风险策略建议，输出 `WARN`。
- 场景 B：市场冲击、高波动、风险预算超限，输出 `ESCALATE`。
- 场景 C：误导性输入、证据缺失、越权意图，输出 `BLOCK`。

## 8. 量化指标

v0.1 已产生 3 个场景、1 次危险动作拦截、2 次强制人工复核、100% 审计凭证完整率、0 次策略约束违规、100% 审计链路关联率和 29ms 平均本地决策耗时。

## 9. 可落地路径

1. 合成受控评估：用可公开解释的场景验证闭环。
2. 历史控制信号回放：使用已脱敏、已授权的控制信号检验一致性。
3. Shadow mode：在真实业务旁路记录，不影响实际动作。
4. Human-in-the-loop pilot：接入人工复核工作流。
5. Controlled rollout：按机构内部审批节奏逐步扩大。

## 10. 风险与边界

本项目不声称真实市场盈利，不声称自动交易上线，不声称监管认可，不声称银行已批准，不声称超过真实银行系统。当前 v0.2 是本地合成受控演示材料包。

## 11. 后续试点计划

下一阶段可以补齐 8 分钟路演稿、门户逐项填写版、最终报名包、人工复核流程图和机构试点假设表。任何进入真实业务环境的动作都必须另设人工审批、数据授权、系统隔离和风险评估。
