# 表 1 方法类别对比

说明：本表按本文的问题定义做概念性对比，用于说明“最小可验证 operation accountability profile”补齐了哪些要素；它不是系统文献评测结论。表中判断已尽量与 `retention review` 同案比较保持一致，正式 related work 引文投稿前待补。

| 方法类别 | explicit operation representation | explicit policy binding | object context/provenance linkage | minimal execution evidence | external validation path | stable failure categories | portable standalone profile |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Ordinary logs | 可记录事件，但通常不形成显式问责单元 | 通常弱或外置 | 弱，常为上下文片段 | 否，常为分散日志 | 通常无独立路径 | 通常无固定主类别 | 否 |
| Provenance-only approaches | 可有，但通常不以 operation 为问责中心 | 通常弱或外置 | 是 | 可有，但未必收敛为最小执行证据 | 通常不固定 | 通常不固定 | 通常否 |
| Policy-only approaches | 通常否 | 是 | 弱，常缺对象级执行链接 | 否 | 常依赖外部实现 | 通常不固定 | 否 |
| Audit trails | 可有 | 可有 | 可有 | 可有，但未必为最小可移植对象 | 可有，但常依赖系统实现 | 可有，但未必稳定 | 通常否 |
| Our method | 是，且以 operation 为中心 | 是，且绑定到本次执行 | 是 | 是，收敛为最小 evidence block | 是 | 是 | 是 |

Caption draft：表 1 从本文的问题视角比较不同方法类别，并以 `retention review` 同案比较为落点，强调本文方法把 operation、policy、provenance、evidence 和 validation 收束为一个可独立交换和验证的最小 profile。
