# Governance Note Final

## Default Human-in-the-Loop

TRPS 默认 human-in-the-loop。高波动、证据缺失、冲突信号或越权意图不会被静默放行，而会进入人工复核、升级、阻断或安全降级。

## White-Listed Actions

白名单动作包括：`ALLOW`、`WARN`、`REVIEW_REQUIRED`、`ESCALATE`、`BLOCK`、`DEGRADE_TO_SAFE_MODE`、`HUMAN_OVERRIDE`。

## Forbidden Actions

禁止动作包括：绕过人工复核、缺证据继续流转、把模型输出当作授权结果、把合成 Demo 当作真实业务证明、把 simulated execution 当作真实执行。

## Kill Switch

每个高风险路径都必须能触发安全停止。若 kill switch 不可用，系统进入阻断路径。

## Policy Versioning

每次决策绑定 policy version，用于解释当时生效的约束与边界。

## Model Versioning

每次决策绑定 model version，用于追踪模型或规则变化对判断结果的影响。

## Audit Receipt

audit receipt 记录场景、风险、约束、人工复核、最终动作、限制说明和可复现哈希。receipt 是问责机制，不是收益引擎。

## Evidence Minimization

只记录复核必需的证据摘要、引用和状态，避免把不必要的数据塞进审计材料。

## Sensitive Data Minimization

v0.3 使用合成受控材料。未来试点必须采用授权、脱敏、最小字段、可审计的数据处理方式。

## Third-Party Model Boundary

第三方模型输出只能作为待复核输入之一，不能替代机构策略、授权角色或人工责任。

## Non-Investment-Advice Statement

TRPS 输出是机构治理材料，不是个人投资建议。

## No Live Trading Statement

TRPS 当前包不连接真实交易链路，不生成真实订单，不进入资金系统。

## No Regulatory Certification Statement

TRPS 不把本地验证、Demo、receipt 或 ZIP 包描述为监管认可、外部批准或法律合规证明。

## Escalation Protocol

高风险预算超限、高波动、冲突信号和缺证据场景必须升级到风险经理、控制负责人或指定复核角色。

## Override Protocol

人工 override 必须记录角色、理由、约束、时间和可复核证据。硬阻断场景不能用普通 override 绕过。

## Incident Review Protocol

若发现错判或争议，必须回看 scenario、policy version、model version、receipt、human review state 和 limitations，形成复盘记录。
