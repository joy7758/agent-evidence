# 证据缺口清单

## external validity

### already have

- 同一 minimal profile 已在两个 controlled contexts 下通过。
- 当前仓库已有 CLI、tests、demo、release、DOI 的闭环证据。

### partially have

- `valid-retention-review-evidence.json` 已提供 second-context validity evidence。
- `docs/fdo-mapping/` 已说明本研究线与 FDO object-facing shape 的关系。

### missing

- 仓库之外的 independent checker 或外部复核记录。
- 明确来自 STAP / data space 语境的外部 scenario package。

### next evidence to build

- 一个外部来源但受控的 scenario corpus。
- 一次由非当前实现者执行的 checker run 与 failure review 记录。

## multi-scenario coverage

### already have

- metadata enrichment 场景。
- retention review 场景。

### partially have

- 已覆盖单输入单输出与双输入单输出两种 linkage pattern。

### missing

- no-output / deny / destructive update / failed operation 等边界场景。
- policy change、对象版本变化、时间冲突等时序场景。

### next evidence to build

- 至少 3 个受控新场景，每个只扩一类边界压力。
- 一个 scenario matrix，明确哪些边界保持稳定，哪些规则需要场景化增强。

## independent checker

### already have

- 一个 reference validator。
- 机器可读 JSON 报告、summary、error code 已稳定。

### partially have

- 当前 validator 已经以 CLI 形式暴露，不只是库内函数。

### missing

- 第二个独立实现。
- checker 之间的一致性结果。

### next evidence to build

- 一个最小第二 checker，可以是独立脚本、独立语言或规则引擎版本。
- 同一 corpus 下的 pass/fail 与 primary code 对照表。

## comparison strength

### already have

- 已有 logs / provenance / policy 的结构性比较论述。
- retention review 场景下已有同案比较草稿。

### partially have

- 目前比较已经能说明“partial capability holders”这个判断。

### missing

- 更系统的同案对照模板。
- audit trail 作为独立比较对象的清晰位置。

### next evidence to build

- 同一 scenario 的四路比较模板：logs / provenance-only / policy-only / boundary-based statement。
- reviewer-facing 对照表：每种方法能回答什么，不能回答什么。

## failure-model completeness

### already have

- 5 个 invalid examples 已形成 seed failure surface。
- 若干主错误码已经稳定。

### partially have

- duplicate identifier、integrity mismatch 等代码面已经具备，但文稿层尚未整理为 taxonomy。

### missing

- identity、target、outcome、temporal、implementation-coupled 等 failure classes 的直接证据。
- “当前已覆盖”和“下一轮待覆盖”的明确边界图。

### next evidence to build

- 4 个新增 invalid cases，每个只破坏 1 条主规则。
- 一个 failure taxonomy coverage matrix。

## portability claims

### already have

- basic portability evidence：同一 core field model、同一 validator path、第二个 valid context。

### partially have

- 当前 `FDO-based agent systems` framing 已经成立。

### missing

- STAP / data space 语境中的受控实例。
- 跨实现、跨框架、跨对象风格的稳定 pass/fail 证据。

### next evidence to build

- 一个面向 STAP / data space 的 boundary translation note。
- 两个不改变 core boundary、只改变语境和对象类型的通过样例。

## 总结

旗舰论文当前最缺的不是更多文案，而是四类新证据：外部场景、独立 checker、更系统的 failure taxonomy、以及更强的同案比较。这四类补齐后，主张才会从“仓库内方法学成立”进一步上升到“问题定义本身成立”。
