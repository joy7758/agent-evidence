# Risk Register

| risk | impact | mitigation | owner | status |
| --- | --- | --- | --- | --- |
| 无真实客户证据 | 评委可能质疑落地性 | 明确寻求试点合作，用 POC 路径回答 | founder | open |
| 无真实金融机构试点 | 商业证明不足 | 从 shadow mode 和 human-in-the-loop pilot 开始 | founder | open |
| synthetic demo 边界 | 被误解为真实业务证明 | 所有材料写明合成受控评估 | owner | controlled |
| 被误解为自动交易 | 高风险定位偏差 | 开场、治理说明、Q&A 反复澄清 | presenter | controlled |
| Python 3.14/Pydantic warning | 评审可能看到 warning | validation report 记录为 non-blocking warning | engineer | monitored |
| 旧工作树脏文件 | 误提交无关材料 | 只 stage v0.3 目录，提交前查 staged list | engineer | controlled |
| 未 push 备份风险 | 本地 commit 丢失风险 | 按指令不 push；后续授权后可备份 | owner | accepted |
| 报名截止时间风险 | 错过官方窗口 | 人工提交前再次检查官方页面和时间 | owner | open |
| 现场 demo 打不开风险 | 影响评审展示 | 准备 Markdown/JSON 兜底和录屏 | presenter | mitigated |
| 门户字段长度变化 | 文案复制失败 | 手工压缩 copybook 字段 | owner | open |
| 附件大小限制 | ZIP 无法上传 | 拆分材料或只上传核心 PDF/Markdown | owner | open |
| 团队信息不完整 | 无法提交 | 人工补齐成员和联系方式 | owner | open |
