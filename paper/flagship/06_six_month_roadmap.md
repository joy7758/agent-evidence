# 六个月执行路线

## 月度计划

| month | deliverables | success criteria |
| --- | --- | --- |
| Month 1 | 冻结旗舰论文主张、术语表、boundary 叙事；完成 master positioning、TOSEM split、minimal verification boundary、failure taxonomy v1 | 所有核心句子稳定；不会再把旗舰论文写回“另一个 profile paper” |
| Month 2 | 扩 failure corpus；把 current invalid cases 补成更完整 taxonomy seed；新增 identity / outcome / temporal / implementation-coupled 四类草案样例 | 每个新增 invalid 只打破 1 条主规则；主错误码可读；coverage matrix 可生成 |
| Month 3 | 做 independent checker 最小原型；整理同一 corpus 下 reference validator 与 second checker 的一致性结果 | 两个 checker 对核心样例的 pass/fail 一致；差异项可解释，而不是隐性漂移 |
| Month 4 | 增补 multi-scenario coverage；至少补两个不改变 core boundary 的新场景，其中一个面向 STAP 或 data space 语境 | 新场景复用同一 minimal boundary；不需要重写核心问题定义 |
| Month 5 | 强化 comparison strength；完成 logs / provenance / policy / audit trail 的同案比较模板与 reviewer-facing matrix；补一轮外部复核 | 比较结论变得更具体；至少形成一份外部 reviewer 或 collaborator 的 boundary review 记录 |
| Month 6 | 写完整旗舰稿；完成 figures、tables、appendix、evidence gap closure note；形成投稿前 freeze 版本 | 主文、附录、artifact witness、roadmap 与 claim 完整对齐；所有不能声称的点写明白 |

## 当前主线

- 把 operation accountability 明确定义为 verification boundary。
- 用 failure taxonomy 说明为什么这不是“换个 JSON 字段名”的问题。
- 用 TOSEM 工件证明这条主线已有最小 witness。
- 用 external validation agenda 说明旗舰论文真正还要补什么。

## 长期方向

- 从最小 verification boundary 走向更稳定的 community profile。
- 逐步形成 cross-framework conformance profile。
- 增加 persistent identifier binding 与 registry-facing packaging。
- 让 FDO / STAP / data space 语境下的对象操作具备更清楚的 external validation path。

## Deferred Items

- broad digital persona 叙事
- 泛化 agent governance platform
- 全量跨风味 FDO 映射
- 复杂多智能体编排
- 完整密码学信任基础设施
- 大规模性能或产业部署主张

## 执行原则

- 每个月只补“会增强主张”的证据，不补旁枝。
- 不为了追求宏大叙事而扩大边界。
- 只要某项工作不能直接增强 boundary、taxonomy 或 external validation，就先 defer。
