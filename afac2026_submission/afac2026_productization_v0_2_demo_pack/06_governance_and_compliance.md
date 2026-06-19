# Governance and Compliance Note

## Human-in-the-Loop

TRPS 默认人机协同。高风险、证据缺失、冲突信号和越权意图场景会触发人工复核、升级或阻断。

## Kill Switch

每个可演示场景都必须记录 kill switch 状态。若 kill switch 缺失，策略闸门只能进入阻断路径。

## Whitelist Actions

v0.2 仅使用白名单动作：`ALLOW`、`WARN`、`REVIEW_REQUIRED`、`ESCALATE`、`BLOCK`、`DEGRADE_TO_SAFE_MODE`、`HUMAN_OVERRIDE`。

## Policy Gate

策略闸门负责检查风险预算、高波动、证据缺失、冲突信号、回执完整性和安全停止要求。gate action 必须能解释触发约束。

## Audit Receipt

receipt 记录 decision id、scenario hash、model version、policy version、triggered constraints、human review status、final action、rationale、limitations 和 reproducibility hash。

## Model and Policy Versioning

每次 demo 输出都绑定模型版本与策略版本，便于追溯同一场景在不同版本下的判断差异。

## Simulated Execution Only

v0.2 只记录离线合成模拟结果。它不创建实际交易，不连接外部执行系统，不进入真实资金链路。

## No Personal Investment Advice

TRPS 的输出是机构治理层的复核对象，不是面向个人的投资建议。

## No Autonomous Live Trading

TRPS 不定位为自主执行系统。任何下游动作都必须由机构已有流程和授权角色负责。

## No Regulatory Certification Claim

TRPS 不把本地验证、demo 或 receipt 描述为监管认可、外部审查或法律合规证明。

## Sensitive Data Minimization

v0.2 使用合成受控数据。未来试点应优先使用脱敏、最小化、可授权、可审计的数据字段。

## Third-Party Model Risk Boundary

如果未来接入第三方模型，TRPS 只把模型输出作为待复核输入之一。模型供应商、提示词、版本、输出摘要和限制都应进入 receipt 或等价审计记录。
