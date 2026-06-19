# Demo Guide Final

## 如何打开离线 Demo

打开：

`afac2026_submission/afac2026_productization_v0_2_demo_pack/demo/index.html`

该 Demo 只使用 synthetic controlled scenarios，可离线查看。

## 5 分钟评审演示路线

1. 0:00-0:30 讲项目定位：TRPS 是交易前风险治理和审计留痕平台。
2. 0:30-1:10 展示指标面板：3 个场景、1 次危险动作拦截、2 次强制人工复核、0 次策略约束违规。
3. 1:10-2:00 点击正常市场场景，说明低风险也保留 warning 和 receipt。
4. 2:00-3:00 点击市场冲击场景，说明高波动触发 escalation。
5. 3:00-4:20 点击误导性输入场景，重点展示 triggered constraints、BLOCK、human review 和 receipt。
6. 4:20-5:00 回到底部边界声明，强调 Demo 不连接真实交易链路。

## 3 分钟快速演示路线

1. 0:00-0:30 打开 Demo 并读一句话定位。
2. 0:30-1:40 直接点击误导性输入场景。
3. 1:40-2:30 展示 risk distribution、triggered constraints、gate decision、receipt。
4. 2:30-3:00 展示指标和边界声明。

## 三个场景如何讲

- 正常市场：系统不是为了阻断一切，而是把低风险建议变成可复核对象。
- 市场冲击：高波动和风险预算压力触发升级，而不是直接进入下游动作。
- 误导性输入：系统识别证据缺失和越权意图，挡住危险动作并生成 receipt。

## 每个场景要强调的点

- belief state：系统先把输入结构化。
- risk distribution：风险不是一个黑箱分数，而是分维度解释。
- triggered constraints：哪些规则被触发要可见。
- gate decision：系统输出复核、升级、阻断或安全降级。
- receipt：每次判断都有可保留的问责凭证。

## 看到哪些指标说明系统有效

- 危险动作拦截次数大于 0。
- 强制人工复核触发次数大于 0。
- 策略约束违规次数为 0。
- 审计凭证完整率为 100%。
- 审计链路关联率为 100%。

## 现场不能打开 HTML 的兜底方式

1. 打开 `07_metrics_translation.md` 说明指标。
2. 打开 `v0.1 outputs/demo_receipts.json` 展示 receipt。
3. 打开 `v0.2 demo/assets/trps_demo_data.json` 展示场景数据。
4. 打开 `08_demo_script_3min.md` 直接按脚本口播。

## 边界

Demo 只使用 synthetic controlled scenarios。它展示治理闭环，不展示真实资金动作。
