# Policy-Only Representation

## Sample Representation

```text
policy: retention-review-v1
- only approved retention classes may be assigned
- restricted datasets require review escalation before finalization
- retention review must emit a final decision record
```

## What It Supports

- 可以明确规则依据
- 可以明确 review 的允许条件和约束条件
- 可以说明 decision record 是应有结果

## What It Cannot Conclude Alone

- actor 是否实际执行了本次 review
- subject 是否就是当前 dataset package
- 双输入是否真的被使用
- decision output 是否真的被发出
- 第三方如何验证这次执行结果

## Why It Is Insufficient Alone

它说明 should，不说明 did，也不形成局部 execution evidence。
