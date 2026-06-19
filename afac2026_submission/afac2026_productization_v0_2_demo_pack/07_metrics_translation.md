# Metrics Translation for Judges

## Metric Mapping

| Technical Metric | Judge-Facing Business Meaning | v0.1 Value |
| --- | --- | --- |
| `scenario_count` | 覆盖的风险场景数量 | `3` |
| `blocked_unsafe_action_count` | 危险动作拦截次数 | `1` |
| `mandatory_review_count` | 强制人工复核触发次数 | `2` |
| `receipt_completeness_rate` | 审计凭证完整率 | `1.0` |
| `policy_violation_count` | 策略约束违规次数 | `0` |
| `audit_trace_linkage_rate` | 审计链路关联率 | `1.0` |
| `average_decision_latency_ms` | 单次决策耗时 | `29` |

## Judge Interpretation

- 3 个场景表示 demo 覆盖正常、冲击和误导输入三类风险。
- 1 次危险动作拦截表示系统能在高危输入下停止继续流转。
- 2 次强制人工复核表示系统没有把高风险场景伪装成低风险。
- 100% 审计凭证完整率表示每个 demo 决策都有可复核 receipt。
- 0 次策略约束违规表示 selected gate action 覆盖了触发约束。
- 100% 审计链路关联率表示 scenario、decision、policy 和 receipt 能互相定位。
- 29ms 是本地合成 demo 的运行耗时，不用于真实业务吞吐承诺。

## Readiness Score Output

The generated readiness score lives at:

- `outputs/submission_readiness_score.json`
- `outputs/submission_readiness_score.md`
