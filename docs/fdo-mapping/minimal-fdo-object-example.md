# Minimal FDO-style Object Example

**English**  Minimal FDO-style Object Example
**IPA**  /ˈmɪnɪməl ˌef diː ˈoʊ staɪl ˈɑːbdʒekt ɪɡˈzæmpəl/
**中文发音**  米尼默尔 艾弗迪欧 斯泰尔 奥布杰克特 伊格赞普尔。
**中文**  最小 FDO 风格对象示例。

## Key Message / 核心说明

**English**  The FDO-style example keeps the verified evidence payload inside a wrapper with identity, integrity, and provenance.
**IPA**  /ðə ˌef diː ˈoʊ staɪl ɪɡˈzæmpəl kiːps ðə ˈverɪfaɪd ˈevɪdəns ˈpeɪloʊd ɪnˈsaɪd ə ˈræpər wɪð aɪˈdentəti ɪnˈteɡrəti ənd ˈprɑːvənəns/
**中文发音**  德 艾弗迪欧 斯泰尔 伊格赞普尔 凯普斯 德 维瑞法艾德 埃维登斯 佩楼德 因赛德 额 瑞泼 维兹 艾丹提提 因泰格若提 安德 普若文嫩斯。
**中文**  这个 FDO 风格示例把已验证的证据载荷放进一个带身份、完整性和来源信息的外壳里。

## What Comes from the Evidence Object / 哪些部分来自证据对象
- **EN**: The embedded payload contributes steps, context, framework, hashes, and timestamp.
- **中文**：内嵌载荷提供步骤、上下文、框架、哈希和时间戳。

## What Represents FDO-style Identity / 哪些部分代表 FDO 风格身份
- **EN**: `object_id`, `object_type`, `pid_placeholder`, and `metadata` are the outer identity layer.
- **中文**：`object_id`、`object_type`、`pid_placeholder` 和 `metadata` 是外层身份层。

## What Represents Integrity and Provenance / 哪些部分代表完整性和来源
- **EN**: `integrity.*` carries hash material, and `provenance.*` carries runtime origin.
- **中文**：`integrity.*` 承载哈希材料，`provenance.*` 承载运行来源。
