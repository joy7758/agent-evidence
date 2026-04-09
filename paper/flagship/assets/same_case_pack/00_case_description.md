# Fixed Case Description

## Case Name

Retention review for one dataset package.

## Core Facts

- actor:
  - `retention-reviewer`
- subject:
  - `obj:dataset-package-042`
- operation:
  - `retention.review`
- policy basis:
  - `policy:retention-review-v1`
- inputs:
  - `ref:input-dataset`
  - `ref:input-retention-ticket`
- output:
  - `ref:output-retention-decision`

## Accountability Question

第三方是否能仅凭一个局部表示，独立判断：

- 谁执行了 retention review；
- 对哪个对象执行；
- 依据了什么 policy；
- 输入输出是否闭合；
- decision output 是否有足够 evidence；
- validation path 是否明确。

## Why This Case Was Chosen

- 它比 metadata enrichment 更适合比较 decision-style accountability。
- 它已经有 current repo 的 central valid anchor。
- 它能同时暴露 logs、provenance、policy、audit trail 的部分覆盖边界。
