# AGENTS.md

你在当前仓库中的首要任务，是复用现有资产，补齐一个“最小可验证闭环”。

## 仓库级目标
围绕以下五部分推进：
- operation
- policy
- provenance
- evidence
- validation

本轮只交付四类东西：
1. minimal profile
2. profile-aware validator
3. 单链路 demo
4. 对外文稿骨架

## 目录策略
先复用现有目录，不要平行新建第二套体系。

优先级：
- 已有 `spec/` 就扩 `spec/`
- 已有 `schema/` 就补 `schema/`
- 已有 `examples/` 就补 `examples/`
- 已有 `verify/` 或现有 CLI / scripts / tests，就沿用
- 已有 `demo/` 就在原 demo 位置补闭环
- 已有 `submission/` 或文稿目录，就优先放文稿骨架

只有确实缺失时才新增目录。

## 禁止事项
- 不要扩展成泛化 agent governance 平台
- 不要新造大而全 registry
- 不要试图一次解决全量跨风味 FDO 映射
- 不要追求完整密码学基础设施
- 不要做复杂多智能体编排
- 不要用宏大叙事替代可运行产物

## 产出标准
必须形成：
- 1 个 valid 样例
- 3 个 invalid 样例，且每个 invalid 只故意打破 1 条主规则
- validator 至少检查：
  - 结构完整性
  - 必填字段
  - 引用闭合
  - policy / provenance / evidence 关联一致性
- validator 输出：
  - 机器可读 JSON
  - 人可读失败摘要
  - 明确 error code
- demo 必须闭环：
  对象载入或创建
  → profile 检查
  → operation 调用
  → evidence 生成
  → validator 验证
  → 输出验证结果

## 执行方式
- 先扫描仓库
- 先写 `docs/STATUS.md`
- 再写 `plans/implementation-plan.md`
- 然后按最小增量补齐 profile / examples / validator / demo / 文稿骨架
- 每完成一个 milestone，更新 `docs/STATUS.md`
- 优先最小、最稳、最容易测试的方案
