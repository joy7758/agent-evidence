# Conformance Profile Draft

**English**  Conformance Profile Draft
**IPA**  /kənˈfɔːrməns ˈproʊfaɪl dræft/
**中文发音**  康福门斯 普若法艾尔 抓夫特。
**中文**  符合性 profile 草案。

## Key Message / 核心说明

**English**  This draft defines what a minimally conforming Execution Evidence Object should include.
**IPA**  /ðɪs dræft dɪˈfaɪnz wʌt ə ˈmɪnɪməli kənˈfɔːrmɪŋ ɪɡˈzekjuːʃən ˈevɪdəns ˈɑːbdʒekt ʃʊd ɪnˈkluːd/
**中文发音**  迪斯 抓夫特 迪凡兹 沃特 额 米尼默利 康福明 伊格泽丘申 埃维登斯 奥布杰克特 休德 因克路德。
**中文**  这份草案定义了一个最小符合性的执行证据对象应该包含什么。

## Required Fields / 必填字段
- **EN**: `object_type`, `agent_framework`, `run_id`, `steps`, `hashes`, `context`, `timestamp`.
- **中文**：`object_type`、`agent_framework`、`run_id`、`steps`、`hashes`、`context`、`timestamp`。

## Optional Fields / 可选字段
- **EN**: Extra step summaries, extra metadata, policy references, or wrapper-level identity.
- **中文**：额外步骤摘要、额外元数据、策略引用或外层身份字段。

## Integrity Requirements / 完整性要求
- **EN**: The object must pass schema validation and hash recomputation.
- **中文**：对象必须通过 schema 验证和哈希重算。

## Provenance Requirements / 来源要求
- **EN**: Runtime source and run identity must be explicit.
- **中文**：运行来源和 run identity 必须清晰可见。

## Portability Requirements / 可移植性要求
- **EN**: Different frameworks should emit the same core fields and support shared verification.
- **中文**：不同框架应当导出同一组核心字段，并支持共享验证。
