# Claims to Evidence Map

## 说明

这张表的目的，是把 flagship-paper claims 从“说法”压到“具体 repo asset”。它不报告已完成实验，只报告：

- 当前 repo 已支持什么；
- 还缺什么；
- 下一步该补什么 artifact。

## 映射表

| claim | why it matters | what current repo already supports | what is still missing | exact next artifact to build | needed for |
| --- | --- | --- | --- | --- | --- |
| operation accountability is a first-class verification boundary | 这是旗舰论文总主张 | `paper/flagship/00_master_positioning.md`、`02_minimal_verification_boundary.md`、当前 OAP spec/validator/demo、`21_validation_section_integrated.md` | 仍缺 repo 外或第三方语境下的外部支撑 | external scenario package + third-party checker note | main paper |
| existing artifacts only partially cover the problem | 用来区分 logs/provenance/policy/audit trail 与本文问题边界 | `12_same_case_comparison_pack.md`、`assets/same_case_pack/`、`22_appendix_validation_integrated.md` | 仍缺第二个 fixed case 与 camera-ready comparison table 定稿 | second comparison case or paper-table polish | main paper |
| the minimal boundary is stable across more than one scenario | 防止边界被单一 demo 绑死 | 当前已有 5 个 scenario families，且 `15_validation_appendix_index.md` 已把它们压成 reviewer-facing corpus index | 仍缺 repo 外场景与更多 object-operation diversity | additional external-context specimens | main paper |
| failure taxonomy is a structural part of the problem | 证明 failure classes 不是实现附录 | `03_failure_taxonomy_v1.md`、`assets/specimens/README.md`、6 个 direct failure specimens、19-file checker comparison 与 run archive | 仍缺 taxonomy freeze 之外的外部复核 | external scenario + appendix-ready taxonomy table | main paper |
| the boundary can be checked by more than one reasoning path | 降低单实现闭环风险 | reference validator、independent checker prototype、`14_checker_comparison_note.md`、19-file pass/fail comparison、run archive、`assets/run_archive/json/` | 仍缺更强独立性与第三方实现 | third-party or different-language checker | main paper / artifact package |
| direct failure coverage now includes all 8 v1 failure classes | 让 validation section 可以从 planning prose 升级到 executed evidence | `scenario_06` 到 `scenario_11`、existing policy/evidence invalid anchors、`18_validation_results_table.md`、`assets/run_archive/json/comparison_matrix.json` | 仍缺更多 than-one specimen family per class | second specimen per boundary class | appendix / artifact package |
| outcome accountability includes failed, denied, and unverifiable outcomes | 防止只覆盖成功故事 | `scenario_05_*`、`scenario_11_outcome_unverifiability_invalid.json`、run archive 中的真实 checker outputs | 仍缺更多 than-one denial/failure pattern 与 repo 外样例 | second failed/denied family + external outcome case | appendix / artifact package |
| flagship validation should not repeat TOSEM artifact closure | 保持两篇论文分工清楚 | `01_tosem_vs_flagship_split.md`、`09_validation_plan_v1.md`、`21_validation_section_integrated.md`、`22_appendix_validation_integrated.md` | 仍缺与最终全文的最后一轮 stitching | manuscript integration pass | main paper |

## 结论

这张 map 当前已经能把 validation claim 与 concrete asset 对齐到 reviewer-facing 程度。最重要的变化是：

- v1 failure taxonomy 的 8 个主类现在都已有 repo 内 executed specimen；
- 19-file checker comparison 已经能支撑正文里的 agreement/divergence 讨论；
- same-case pack、run archive、integrated validation text 与 appendix text 已经开始形成同一套证据链。

下一步最该补的，不是再写 planning prose，而是：

- external-context evidence
- third-party checker
- introduction / discussion / conclusion 的连续 manuscript assembly
