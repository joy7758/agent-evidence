# Final Q&A Defense: 50 Questions

## Q1. 你们是不是做自动交易？

- 30 秒版本：不是。TRPS 是交易前风险治理和审计留痕平台。
- 90 秒版本：TRPS 位于下游执行系统之前，输出复核、升级、阻断、安全降级和 audit receipt。它不负责自主执行。
- 证据路径：`01_final_submission_overview.md`, `05_governance_note_final.md`
- 禁止踩线提醒：不要把 TRPS 说成自动执行系统。

## Q2. 有没有真实收益？

- 30 秒版本：v0.3 不讲真实收益，讲治理闭环。
- 90 秒版本：当前证据来自合成受控场景，指标是危险动作拦截、复核触发、凭证完整和约束违规，不是收益。
- 证据路径：`07_pitch_script_8min.md`, `outputs/validation_report.json`
- 禁止踩线提醒：不要承诺收益。

## Q3. 数据从哪里来？

- 30 秒版本：当前使用合成受控场景和本地 receipt/metrics。
- 90 秒版本：试点阶段可使用授权、脱敏、最小化的控制信号，先做回放和旁路记录。
- 证据路径：`03_project_solution_final.md`, `04_business_plan_final.md`
- 禁止踩线提醒：不要虚构真实客户数据。

## Q4. 没有客户怎么参赛？

- 30 秒版本：初创组可以用产品 Demo、商业路径和试点诉求参赛。
- 90 秒版本：v0.3 已有可运行离线 Demo、门户文案、商业计划、治理说明和最终 ZIP。下一步是寻求试点合作。
- 证据路径：`02_portal_copybook_final.md`, `04_business_plan_final.md`
- 禁止踩线提醒：不要写已有客户落地。

## Q5. 如何落地？

- 30 秒版本：从合成评估、控制信号回放、shadow mode 到人机协同试点。
- 90 秒版本：先不接真实资金链路，只在旁路记录判断和 receipt，稳定后再进入受控流程。
- 证据路径：`04_business_plan_final.md`
- 禁止踩线提醒：不要说直接上线真实交易。

## Q6. 监管风险怎么处理？

- 30 秒版本：TRPS 不替代合规体系，只提供治理和审计材料。
- 90 秒版本：系统保留人工复核、kill switch、版本记录、白名单动作和 receipt，供机构内部审查。
- 证据路径：`05_governance_note_final.md`
- 禁止踩线提醒：不要暗示监管认可。

## Q7. 为什么不是普通风控系统？

- 30 秒版本：普通风控偏规则执行，TRPS 关注 AI 决策前的结构化治理。
- 90 秒版本：TRPS 把 belief state、risk distribution、policy gate、human review 和 receipt 合成一条链。
- 证据路径：`03_project_solution_final.md`
- 禁止踩线提醒：不要贬低现有机构系统。

## Q8. 为什么不是普通 LLM 助手？

- 30 秒版本：LLM 助手输出文本，TRPS 输出可审计决策对象。
- 90 秒版本：TRPS 记录触发约束、人工复核、版本、限制和哈希，适合机构治理。
- 证据路径：`14_claim_evidence_map_final.md`
- 禁止踩线提醒：不要说 LLM 本身能负责。

## Q9. 为什么不是论文项目？

- 30 秒版本：v0.3 是产品包，有 Demo、门户文案、商业计划和 ZIP。
- 90 秒版本：论文侧重理论表达，TRPS 当前交付面向评委、门户和试点沟通。
- 证据路径：`15_file_manifest_final.md`
- 禁止踩线提醒：不要把本包说成论文已投稿。

## Q10. 为什么选择初创组？

- 30 秒版本：TRPS 的重点是可演示产品闭环、商业化叙事和治理落地。
- 90 秒版本：它不是单题挑战算法，而是面向机构流程的产品化系统。
- 证据路径：`01_final_submission_overview.md`
- 禁止踩线提醒：不要说挑战组不适合所有金融 AI。

## Q11. 如何做 POC？

- 30 秒版本：定义机构场景、配置策略、运行 receipt、人工复核结果。
- 90 秒版本：POC 用 10-20 个风险场景开始，不碰真实资金链路。
- 证据路径：`04_business_plan_final.md`
- 禁止踩线提醒：不要跳过授权和隔离。

## Q12. 如何收费？

- 30 秒版本：POC fixed fee、私有化部署、模块授权、年度维护和治理报告服务。
- 90 秒版本：费用对应机构降低风险和提高审计效率的价值。
- 证据路径：`04_business_plan_final.md`
- 禁止踩线提醒：不要承诺投资回报。

## Q13. 如何私有化部署？

- 30 秒版本：部署在机构内网、合规沙箱或隔离试点环境。
- 90 秒版本：早期只接授权控制信号和内部复核流程，不接外部执行系统。
- 证据路径：`04_business_plan_final.md`
- 禁止踩线提醒：不要承诺即插即用生产系统。

## Q14. 如何扩展到银行？

- 30 秒版本：先从投顾中台和风控复核流程开始。
- 90 秒版本：银行场景需要更强的权限、数据、审计和人工复核适配，TRPS 可作为治理层。
- 证据路径：`02_portal_copybook_final.md`
- 禁止踩线提醒：不要说已有银行批准。

## Q15. 如何扩展到券商？

- 30 秒版本：从资管和投顾输出复核开始。
- 90 秒版本：券商可用 TRPS 记录策略建议、风险预算、复核状态和 receipt。
- 证据路径：`04_business_plan_final.md`
- 禁止踩线提醒：不要写已接券商接口。

## Q16. 如何扩展到资管？

- 30 秒版本：用控制信号回放和 shadow mode 检验风险治理一致性。
- 90 秒版本：资管流程强调授权、风险预算和复核留痕，TRPS 正好补齐动作前治理。
- 证据路径：`03_project_solution_final.md`
- 禁止踩线提醒：不要声称真实投资效果。

## Q17. 如何避免幻觉？

- 30 秒版本：不直接相信模型输出，先结构化再过策略闸门。
- 90 秒版本：缺证据、冲突信号和越权意图会触发阻断或复核。
- 证据路径：`05_governance_note_final.md`
- 禁止踩线提醒：不要说完全消除幻觉。

## Q18. 如何处理错判？

- 30 秒版本：通过 incident review protocol 回看 receipt 和版本。
- 90 秒版本：系统保留场景、策略、模型版本、复核状态和限制，便于复盘。
- 证据路径：`05_governance_note_final.md`, `13_risk_register.md`
- 禁止踩线提醒：不要说系统不会错。

## Q19. 谁承担责任？

- 30 秒版本：机构授权人员承担业务动作责任，TRPS 提供治理材料。
- 90 秒版本：TRPS 默认 human-in-the-loop，不替代人工责任。
- 证据路径：`05_governance_note_final.md`
- 禁止踩线提醒：不要把责任转给模型。

## Q20. receipt 的价值是什么？

- 30 秒版本：它让每次判断可复核、可留存、可追溯。
- 90 秒版本：receipt 绑定场景、约束、人工复核、最终动作、限制和哈希。
- 证据路径：`v0_1_outputs/demo_receipts.json`, `14_claim_evidence_map_final.md`
- 禁止踩线提醒：不要说 receipt 是收益引擎。

## Q21. human review 在哪里？

- 30 秒版本：在 gate decision 之后、下游动作之前。
- 90 秒版本：高风险路径必须由风险经理、控制负责人或授权角色复核。
- 证据路径：`06_demo_guide_final.md`, `05_governance_note_final.md`
- 禁止踩线提醒：不要跳过人工复核。

## Q22. kill switch 怎么触发？

- 30 秒版本：当高风险路径缺少安全停止能力时进入阻断。
- 90 秒版本：kill switch 是硬边界，确保异常状态不能继续流转。
- 证据路径：`05_governance_note_final.md`
- 禁止踩线提醒：不要把它说成可选装饰。

## Q23. 没有真实交易是不是价值不够？

- 30 秒版本：早期价值是降低动作前治理风险，不是执行交易。
- 90 秒版本：金融机构更需要先证明边界、复核和审计链，再谈试点扩展。
- 证据路径：`04_business_plan_final.md`
- 禁止踩线提醒：不要为了显得强而接真实链路。

## Q24. synthetic evaluation 的边界是什么？

- 30 秒版本：它证明闭环可演示，不证明真实世界效果。
- 90 秒版本：合成受控评估适合早期验证逻辑、流程和回执结构。
- 证据路径：`06_demo_guide_final.md`
- 禁止踩线提醒：不要把合成结果说成外部验证。

## Q25. 你们现在缺什么？

- 30 秒版本：缺真实机构试点场景、人工复核角色表和授权控制信号。
- 90 秒版本：我们希望从 shadow mode 与 human-in-the-loop pilot 开始合作。
- 证据路径：`13_risk_register.md`, `12_manual_submission_steps.md`
- 禁止踩线提醒：不要虚构缺口已解决。

## Q26. 现场 Demo 打不开怎么办？

- 30 秒版本：用 Markdown 和 JSON 兜底。
- 90 秒版本：打开 demo data、receipt、metrics 和 3 分钟脚本即可说明闭环。
- 证据路径：`06_demo_guide_final.md`
- 禁止踩线提醒：不要现场临时改代码。

## Q27. 为什么需要策略闸门？

- 30 秒版本：策略闸门把机构边界变成可检查条件。
- 90 秒版本：它能处理风险预算、高波动、缺证据、冲突信号和安全停止。
- 证据路径：`03_project_solution_final.md`
- 禁止踩线提醒：不要把模型输出当规则。

## Q28. 你们的指标说明什么？

- 30 秒版本：说明 Demo 能覆盖风险、拦截危险动作、触发复核并保持凭证完整。
- 90 秒版本：指标服务治理解释，不服务收益叙事。
- 证据路径：`outputs/final_submission_readiness_score.json`
- 禁止踩线提醒：不要说指标代表真实收益。

## Q29. 如果客户已有风控系统怎么办？

- 30 秒版本：TRPS 可作为前置治理和 receipt 层补充。
- 90 秒版本：它不替换核心风控，而是给 AI 决策提供复核和留痕对象。
- 证据路径：`03_project_solution_final.md`
- 禁止踩线提醒：不要说替代银行系统。

## Q30. 如何处理模型版本变化？

- 30 秒版本：receipt 记录 model version。
- 90 秒版本：不同版本下同一场景的判断可以回放和比较。
- 证据路径：`05_governance_note_final.md`
- 禁止踩线提醒：不要忽略版本漂移。

## Q31. 如何处理策略版本变化？

- 30 秒版本：receipt 记录 policy version。
- 90 秒版本：策略变动可追溯到当时生效的约束。
- 证据路径：`05_governance_note_final.md`
- 禁止踩线提醒：不要把策略当隐含常量。

## Q32. 如何保护敏感数据？

- 30 秒版本：数据最小化、脱敏、授权和隔离。
- 90 秒版本：v0.3 不含真实客户数据，试点也应只收集必要字段。
- 证据路径：`05_governance_note_final.md`
- 禁止踩线提醒：不要上传未授权数据。

## Q33. 第三方模型风险怎么处理？

- 30 秒版本：第三方模型输出只是待复核输入。
- 90 秒版本：TRPS 不把供应商输出等同于机构授权。
- 证据路径：`05_governance_note_final.md`
- 禁止踩线提醒：不要替供应商背书。

## Q34. 为什么要有 final ZIP？

- 30 秒版本：方便报名上传和评审复核。
- 90 秒版本：ZIP 包含文档、Demo、manifest、验证报告和 readiness score。
- 证据路径：`outputs/TRPS_AFAC2026_FINAL_SUBMISSION_PACK.zip`
- 禁止踩线提醒：不要把 ZIP 说成已提交。

## Q35. 是否需要 PPTX？

- 30 秒版本：如果工具可用会生成，否则用 Markdown fallback。
- 90 秒版本：当前环境缺少 python-pptx，已记录 fallback，可人工转 PPT。
- 证据路径：`outputs/pptx_generation_skipped.md`
- 禁止踩线提醒：不要覆盖旧 PPTX。

## Q36. 报名门户怎么填？

- 30 秒版本：复制 `02_portal_copybook_final.md` 对应字段。
- 90 秒版本：先选初创组，再填团队信息、项目摘要、创新、场景、商业价值和附件说明。
- 证据路径：`12_manual_submission_steps.md`
- 禁止踩线提醒：不要勾选不实认证或客户项。

## Q37. 你们的合作诉求是什么？

- 30 秒版本：寻找试点合作。
- 90 秒版本：先做合成评估、控制信号回放、shadow mode，再做人机协同试点。
- 证据路径：`02_portal_copybook_final.md`
- 禁止踩线提醒：不要说已有融资或客户。

## Q38. 如何控制项目风险？

- 30 秒版本：风险登记表列出边界、试点、现场和工作树风险。
- 90 秒版本：每个风险都有 mitigation、owner 和 status。
- 证据路径：`13_risk_register.md`
- 禁止踩线提醒：不要淡化未解决风险。

## Q39. ZIP 里有没有旧大文件？

- 30 秒版本：validator 检查不包含旧 ZIP 和旧 PPTX。
- 90 秒版本：staging 明确排除旧包、大文件、环境目录和 secrets。
- 证据路径：`outputs/validation_report.json`
- 禁止踩线提醒：不要手动塞旧文件。

## Q40. 是否能直接上传？

- 30 秒版本：可作为本地上传候选，但仍需人工确认门户规则。
- 90 秒版本：最终提交前要检查字段长度、团队信息、附件限制和官方入口。
- 证据路径：`11_final_submission_checklist.md`
- 禁止踩线提醒：不要说已经上传。

## Q41. 为什么强调 audit receipt？

- 30 秒版本：因为金融机构需要动作前和事后的责任链。
- 90 秒版本：receipt 让 AI 决策进入可追溯治理流程。
- 证据路径：`14_claim_evidence_map_final.md`
- 禁止踩线提醒：不要说 receipt 具有法律终局效力。

## Q42. 可以接入现有审批流吗？

- 30 秒版本：可以作为前置治理对象接入。
- 90 秒版本：接入前需要映射机构角色、策略和审计模板。
- 证据路径：`04_business_plan_final.md`
- 禁止踩线提醒：不要承诺无改造接入。

## Q43. 你们如何处理越权输入？

- 30 秒版本：缺证据或越权意图触发阻断。
- 90 秒版本：最强 Demo 场景就是误导性输入与证据缺失，结果为 BLOCK。
- 证据路径：`08_demo_script_3min.md`
- 禁止踩线提醒：不要说系统会按用户要求继续。

## Q44. 如果评委要求现场试一个新场景？

- 30 秒版本：可以解释 v0.3 是固定合成 Demo，新增场景需离线配置后验证。
- 90 秒版本：为了可审计和可复现，不建议现场临时接入未经验证输入。
- 证据路径：`06_demo_guide_final.md`
- 禁止踩线提醒：不要即兴承诺动态生产能力。

## Q45. 你们和审计系统是什么关系？

- 30 秒版本：TRPS 生成可供审计系统使用的结构化材料。
- 90 秒版本：它不是完整审计平台，而是动作前 governance object 和 receipt 层。
- 证据路径：`01_final_submission_overview.md`
- 禁止踩线提醒：不要说替代审计系统。

## Q46. 是否有开源或可复现材料？

- 30 秒版本：本地材料包括脚本、JSON、HTML 和验证报告。
- 90 秒版本：评委可检查 final manifest 和 ZIP sha256。
- 证据路径：`15_file_manifest_final.md`, `outputs/final_pack_manifest.json`
- 禁止踩线提醒：不要公开未授权材料。

## Q47. 报名截止风险怎么处理？

- 30 秒版本：提前完成 ZIP、字段和人工 checklist。
- 90 秒版本：风险登记表已把截止时间列为人工确认项。
- 证据路径：`13_risk_register.md`
- 禁止踩线提醒：不要临近截止才检查入口。

## Q48. 未 push 会不会有备份风险？

- 30 秒版本：有，本轮按指令不 push，但风险已记录。
- 90 秒版本：提交后本地有 commit 和 ZIP；如后续授权，可再做远程备份。
- 证据路径：`13_risk_register.md`
- 禁止踩线提醒：不要擅自 push。

## Q49. AGENTS.md 和 README 为什么不提交？

- 30 秒版本：它们是本轮前旧改动，指令要求不 stage。
- 90 秒版本：本轮只提交 v0.3 final pack，保持提交范围干净。
- 证据路径：`outputs/validation_report.json`
- 禁止踩线提醒：不要混入旧 worktree drift。

## Q50. 最后一句怎么收束？

- 30 秒版本：TRPS 让金融机构在动作前看清风险、规则、责任和凭证。
- 90 秒版本：我们寻求试点合作，在不接真实交易和不做自动执行的前提下，从 shadow mode 与 human-in-the-loop pilot 开始验证。
- 证据路径：`07_pitch_script_8min.md`
- 禁止踩线提醒：不要把试点说成外部通过。
