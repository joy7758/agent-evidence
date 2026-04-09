# Corpus Manifest

## 说明

这份 manifest 用于组织 flagship validation corpus，不等于实验结果汇总。它只说明当前 repo 中有哪些 scenario assets、它们想覆盖什么 failure surface、以及它们在 checker/comparison 包中的状态。

## Scenario Manifest

| scenario_id | title | intended evidence type | failure coverage | checker coverage | comparison coverage | status |
| --- | --- | --- | --- | --- | --- | --- |
| S01 | metadata enrichment | valid baseline statement + invalid anchor family | identity / target / policy / evidence | reference + independent checker | partial | existing |
| S02 | retention review | valid decision-style statement + fixed same-case anchor | policy / evidence / outcome / temporal | reference + independent checker | strong | existing |
| S03 | access decision | decision corpus specimen | policy / operation semantics / outcome | reference + independent checker | strong | existing |
| S04 | object derivation handoff | derivation + handoff specimen | target / evidence / outcome / coupling | reference + independent checker | strong | existing |
| S05 | failed or denied operation | failed/denied specimen | outcome / semantics / temporal / evidence | reference + independent checker | medium | existing |
| B06 | missing identity binding | direct boundary stress specimen | identity binding | reference + independent checker | none | existing |
| B07 | temporal inconsistency | direct boundary stress specimen | temporal consistency | reference + independent checker | none | existing |
| B08 | implementation-coupled evidence | direct boundary stress specimen | implementation coupling | reference + independent checker | none | existing |
| B09 | missing target binding | direct boundary stress specimen | target binding | reference + independent checker | none | existing |
| B10 | ambiguous operation semantics | direct boundary stress specimen | operation semantics | reference + independent checker | none | existing |
| B11 | outcome unverifiability | direct boundary stress specimen anchored in S04 | outcome accountability | reference + independent checker | none | existing |

## 读法

- `S01` 到 `S05` 是 central scenarios。
- `B06` 到 `B10` 是 cross-scenario boundary stress materials。
- `B11` 虽然是 direct failure specimen，但它故意绑定在 `object derivation handoff` 上，因为 outcome unverifiability 在该场景下最清楚。

## 状态定义

- `existing`：当前 repo 已有可直接复用或已直接创建的 specimen
- `partial`：已有结构性材料，但仍缺 central specimen 或 direct invalid
- `missing`：目前只有计划，没有中心 specimen
