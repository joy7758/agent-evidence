# 表 4 基础可迁移性迷你矩阵

| 维度 | evidence now available | what this supports | what it still does not support |
| --- | --- | --- | --- |
| context diversity | `minimal-valid-evidence.json` 对应 metadata enrichment；`valid-retention-review-evidence.json` 对应 retention review | 同一最小 profile 在第二个不同语境中也能成立，支持 basic portability evidence | 不支持 broad cross-framework validation，也不支持广泛操作类型外推 |
| input/output linkage pattern diversity | 一个 valid 为单输入 / 单输出；另一个 valid 为双输入 / 单输出 | 支持最小 profile 已覆盖不止一种 I/O linkage pattern | 不支持复杂对象图、多步骤 workflow 或多智能体编排 |
| same validator path reuse | 两个 valid 都走同一 profile name/version 与同一 validator 路径 | 支持同一验证路径可复用于第二语境 | 不支持独立实现之间的一致性结论 |
| same core field model reuse | 两个 valid 都复用 `operation / policy / provenance / evidence / validation` 核心结构 | 支持最小字段模型在第二语境下保持稳定 | 不支持证明该字段模型已覆盖所有 FDO-based agent system 需求 |
| current external-validity limit | 当前仍是 2 个 valid 样例、1 个核心 demo、单仓实现 | 支持克制地陈述“已有第二语境有效性证据” | 不支持跨运行框架、跨实现、跨生态的大范围泛化主张 |

Caption draft：表 4 将当前仓库对 portability 的可支撑结论压缩为一个小矩阵：它足以支撑 basic portability evidence，但不足以支撑 broad cross-framework validation。
