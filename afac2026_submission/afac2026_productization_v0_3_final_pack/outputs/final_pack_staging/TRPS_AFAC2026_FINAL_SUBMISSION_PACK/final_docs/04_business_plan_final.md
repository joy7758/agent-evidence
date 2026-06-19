# Business Plan Final

## 客户是谁

目标客户包括券商资管、财富管理平台、银行投顾中台、风控团队和合规团队。

## 谁付款

实际付款方通常是风险治理负责人、合规负责人、投顾运营负责人、资管信息化负责人或创新业务负责人。

## 为什么付款

机构愿意为减少越权动作、减少人工复核重复劳动、提高审计完整率、缩短事故复盘时间、降低 AI 使用组织风险而付款。

## 从哪里部署

优先部署在机构内网、合规沙箱或隔离试点环境。早期不要求接入真实交易链路，可以从授权的控制信号和合成场景开始。

## POC 怎么做

POC 阶段定义 10-20 个风险场景，配置机构策略边界，运行 policy gate 和 audit receipt，人工复核 Demo 输出，并形成试点评估报告。

## 怎么避免一开始就碰真实交易

POC 使用 synthetic controlled evaluation 和 historical control-signal replay，不调用外部执行系统，不进入资金链路，不生成实际订单。

## 怎么从 synthetic demo 进入 shadow mode

先把合成场景扩展成机构控制信号模板，再在真实业务旁路记录风险判断和 receipt。shadow mode 只观察和记录，不影响业务动作。

## 怎么进入 human-in-the-loop pilot

当 shadow mode 结果稳定后，选择低风险、可控、人工复核充分的流程进入 pilot。TRPS 只提供治理对象，由授权人员决定是否进入下一步。

## 怎么进入 controlled rollout

pilot 通过后，按机构内控流程扩大范围：先单团队、后单产品线、再多业务线；每一步都保留版本记录、复核记录和回滚策略。

## 收费模式

- `POC fixed fee`
- `private deployment`
- `annual maintenance`
- `governance report service`
- `module licensing`

## ROI 逻辑

- 减少越权动作。
- 减少人工复核重复劳动。
- 提高审计完整率。
- 缩短事故复盘时间。
- 降低 AI 使用的组织风险。
