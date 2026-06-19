# 3 分钟 Demo 讲稿

## 0:00-0:20 打开 Demo

打开 `afac2026_submission/afac2026_productization_v0_2_demo_pack/demo/index.html`。说明：这是离线 Demo，只使用 synthetic controlled scenarios。

## 0:20-0:40 选择最强场景

点击“误导性输入 + 证据缺失 + 越权交易意图”。说明：这个场景模拟高风险输入要求绕过复核，但我们不会执行交易。

## 0:40-1:05 输入场景

指出输入里包含缺失证据、冲突信号和越权意图。讲法：系统先把输入转成 belief state，而不是直接接受输入指令。

## 1:05-1:30 Risk Distribution

展示 risk distribution。说明：市场、流动性、证据、意图和操作风险都被拆开看，证据风险和意图风险最高。

## 1:30-1:55 Triggered Constraints

展示 triggered constraints。说明：缺证据、越权意图、冲突信号和审计回执要求共同触发策略闸门。

## 1:55-2:15 Gate Decision

展示 gate decision 为 `BLOCK`。若现场版本显示安全降级，也说明它是 `DEGRADE_TO_SAFE_MODE`，不是执行交易。

## 2:15-2:35 Human Review

展示 human review status。说明：高风险路径必须进入人工复核，授权角色负责下一步判断。

## 2:35-2:50 Receipt

展示 receipt id 和 rationale。说明：receipt 记录了为什么挡住危险动作，而不是只给一个黑箱答案。

## 2:50-3:00 Metrics

回到指标面板：危险动作拦截 1 次，强制人工复核 2 次，策略约束违规 0 次，审计凭证完整率 100%。结论：系统挡住了危险动作，而不是执行交易。
