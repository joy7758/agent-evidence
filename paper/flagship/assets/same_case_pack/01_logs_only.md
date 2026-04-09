# Logs-Only Representation

## Sample Representation

```text
2026-03-31T00:00:00Z INFO retention-reviewer review.start dataset=obj:dataset-package-042
2026-03-31T00:00:01Z INFO retention-reviewer input.loaded ref=ref:input-dataset locator=urn:demo:dataset-package-042
2026-03-31T00:00:01Z INFO retention-reviewer input.loaded ref=ref:input-retention-ticket locator=urn:demo:retention-ticket-042
2026-03-31T00:00:03Z INFO retention-reviewer rule.applied retention-policy=v1
2026-03-31T00:00:04Z INFO retention-reviewer output.emitted ref=ref:output-retention-decision locator=urn:demo:retention-decision-042
2026-03-31T00:00:04Z INFO retention-reviewer review.complete status=succeeded
```

## What It Supports

- 可以看出 review 确实发生过
- 可以看出 actor、subject、输入输出 locator 的部分信息
- 可以看出完成状态

## What It Cannot Conclude Alone

- `policy:retention-review-v1` 是否与当前执行稳定绑定
- 双输入与 decision output 是否构成局部闭合 statement
- supporting evidence block 是什么
- 第三方该用什么 validation path 判断可验证性

## Why It Is Insufficient Alone

它说明了一串事件，但没有形成一个单 operation accountability statement。
