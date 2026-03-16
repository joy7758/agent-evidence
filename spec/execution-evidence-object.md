# Execution Evidence Object

**English**  Execution Evidence Object
**IPA**  /ɪɡˈzekjuːʃən ˈevɪdəns ˈɑːbdʒekt/
**中文发音**  伊格泽丘申 埃维登斯 奥布杰克特。
**中文**  执行证据对象。

## Key Message / 核心说明

**English**  Execution Evidence Object is a portable and verifiable object for AI runtime evidence.
**IPA**  /ɪɡˈzekjuːʃən ˈevɪdəns ˈɑːbdʒekt ɪz ə ˈpɔːrtəbəl ənd ˈverɪfaɪəbəl ˈɑːbdʒekt fɔːr eɪ aɪ ˈrʌnˌtaɪm ˈevɪdəns/
**中文发音**  伊格泽丘申 埃维登斯 奥布杰克特 依兹 额 波特伯 安德 维瑞法耶伯 奥布杰克特 佛 诶艾 软泰姆 埃维登斯。
**中文**  执行证据对象是一种面向 AI 运行时证据的可移植、可验证对象。

## Purpose / 目的
- **EN**: Turn runtime activity into a bounded object that can be exported, checked, and reused.
- **中文**：把运行时活动压缩成一个有边界的对象，便于导出、校验和复用。

## Object Identity / 对象身份
- **EN**: The core identity fields are `object_type`, `agent_framework`, `run_id`, and `timestamp`.
- **中文**：核心身份字段是 `object_type`、`agent_framework`、`run_id` 和 `timestamp`。

## Evidence Structure / 证据结构
- **EN**: The object includes `steps`, `context`, and `hashes`.
- **中文**：对象包含 `steps`、`context` 和 `hashes`。

## Integrity Verification / 完整性验证
- **EN**: Integrity is checked through `action_hash`, `trace_hash`, and `proof_hash`.
- **中文**：完整性通过 `action_hash`、`trace_hash` 和 `proof_hash` 来验证。

## Runtime Export / 运行时导出
- **EN**: The object is a post-run artifact, not a replacement for full observability.
- **中文**：这个对象是运行结束后的构件，不是完整可观测系统的替代品。

## FDO Compatibility / FDO 兼容性
- **EN**: The object can be discussed in FDO-facing terms through identity, metadata, integrity, and provenance.
- **中文**：这个对象可以通过身份、元数据、完整性和来源信息，用 FDO 面向的方式来讨论。
