# Related Work Scaffold

## 使用说明

本文件只搭 related work 骨架，不预填未核实的引文。所有小节都必须在投稿前补正式参考文献。
本文的 related work 应保持紧凑，只服务于“为什么需要一个最小可验证 profile + validator
+ artifact package”，不扩展成 broad survey。

## 1. FDO 与对象级可验证性

建议比较点：

- FDO 语境下为什么需要对象级身份、引用和验证路径
- 本文工作如何只取“对象化问责 statement”的最小切面

投稿前待补：

- FDO 核心参考文献
- 本文与 FDO 既有概念之间的最小对应关系

## 2. Provenance 与执行证据建模

建议比较点：

- provenance 模型通常关心哪些链接关系
- 本文为什么把 provenance 与 policy / evidence / validation 一起固定进最小 statement

投稿前待补：

- provenance 经典文献
- 与本文字段关系最接近的先行工作

## 3. Runtime tracing、observability 与 accountability 的差异

建议比较点：

- tracing/logging 能回答什么
- operation accountability statement 额外要求回答什么
- 为什么“可观察”不自动等于“可复核”

投稿前待补：

- tracing / observability 代表性引用
- 若引用 agent observability 近作，需使用正式论文或官方技术报告

## 4. Conformance profile 与 validator

建议比较点：

- 为什么 profile 比一般 schema 更强调语义边界
- 为什么 validator 需要做 schema 之外的引用与一致性检查

投稿前待补：

- conformance profile / schema validation 相关引用
- profile-aware validation 的对照对象

## 5. Reproducible artifact 与软件归档

建议比较点：

- 为什么 methodology 论文需要 artifact package
- GitHub Release + DOI 归档对复现和引用的意义

投稿前待补：

- artifact evaluation / software citation 相关引用
- TOSEM 或 ACM 语境下可接受的 artifact 叙述方式

## 6. 建议收束句

related work 最后应收束到一个非常具体的判断：

现有工作分别覆盖对象、provenance、tracing、validation 或 software artifact 的某些侧面；
本文的增量在于，把这些需求压缩为一个面向单 operation accountability statement 的最小
可验证 profile，并给出与之同仓冻结的 validator 与 artifact package。

为了避免这一判断停留在抽象层，可把 `paper/tosem_cn/comparative_case_analysis.md` 作为
桥接材料：在同一个 `retention review` 场景中，依次说明 ordinary logs、
provenance-only、policy-only 与本文 profile 各自能表达什么、仍缺什么。这样 related work
讨论就能从“类别区分”落到“同案下的结构差异”，同时仍保持 methodology + validator +
artifact 的主线，不扩展成 broad survey。
