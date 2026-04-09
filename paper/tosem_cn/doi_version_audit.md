# DOI / Version Consistency Audit

## 审计范围

本次审计在仓库根目录检索以下字符串：

- `10.5281/zenodo.19055948`
- `10.5281/zenodo.19334062`
- `v0.1.0`
- `v0.2.0`

审计时间：当前工作区回合内
审计目的：区分旧 DOI、已核实的新 DOI，以及 release/version 文字是否与当前 OAP v0.1 package + repository release v0.2.0 的定位一致。

## 检索结果摘要

- `10.5281/zenodo.19055948`
  - 命中旧 DOI 文案与旧 release surface。
- `10.5281/zenodo.19334062`
  - 命中新论文工作区与 `docs/STATUS.md` 中的已核实新 DOI 说明。
- `v0.1.0`
  - 本轮检索未命中。
- `v0.2.0`
  - 命中新论文工作区、`docs/STATUS.md`，以及本轮已核实的 release 表述。

## 仍提及旧 DOI 的文件

### 以历史 specimen 语义保留旧 DOI

- `README.md`
- `README.zh-CN.md`
- `release/v0.1-live-chain/RELEASE_NOTE.md`

### 在审计或问题说明中提及旧 DOI

- `docs/STATUS.md`
- `paper/tosem_cn/06_artifact_package.md`
- `paper/tosem_cn/manuscript_cn.md`
- `paper/tosem_cn/tables/table2_artifact_status.md`
- `paper/tosem_cn/todo_evidence_gaps.md`
- `paper/tosem_cn/doi_version_audit.md`

## 提及新 DOI 的文件

- `docs/STATUS.md`
- `paper/tosem_cn/00_title_abstract_keywords.md`
- `paper/tosem_cn/02_introduction.md`
- `paper/tosem_cn/06_artifact_package.md`
- `paper/tosem_cn/07_evaluation.md`
- `paper/tosem_cn/10_conclusion.md`
- `paper/tosem_cn/manuscript_cn.md`
- `paper/tosem_cn/todo_evidence_gaps.md`
- `paper/tosem_cn/tables/table2_artifact_status.md`
- `paper/tosem_cn/doi_version_audit.md`

## Release / Version 文字存在歧义或需统一说明的文件

### 已在本轮可安全同步的文件

- `README.md`
  - 已区分 current OAP package 与 historical specimen track。
- `README.zh-CN.md`
  - 已新增当前 OAP package 段落，并把旧 DOI 明确为历史样品 DOI。
- `submission/artifact-availability.md`
  - 已对齐到 current OAP package / release `v0.2.0` / DOI `10.5281/zenodo.19334062`。
- `docs/STATUS.md`
  - 已改为更明确地指出旧 DOI 命中位置与 `v0.2.0` / OAP `v0.1` 的关系。
- `plans/implementation-plan.md`
  - 已补充 M6 输出包含 figures、tables 与 DOI/version audit。
- `paper/tosem_cn/06_artifact_package.md`
  - 已补充更完整的旧 DOI 文件范围，并明确新 DOI 通过外部元数据核实。
- `paper/tosem_cn/manuscript_cn.md`
  - 已补充图表占位，并把 release / DOI 叙述与审计结果对齐。
- `paper/tosem_cn/todo_evidence_gaps.md`
  - 已把旧 DOI 命中面更新为更完整列表。

### 需人工判断

- 当前本轮目标文件中无新增必须人工判断后才能修改的 current-package 文档。
- `release/v0.1-live-chain/RELEASE_NOTE.md`
  - 已判断为历史 specimen 资料，因此保留旧 DOI，不作为 current-package 文档处理。

## 本轮已做的安全修正

- 在 `paper/tosem_cn/` 内新增 figures、tables 与审计文件。
- 在 `paper/tosem_cn/`、`docs/STATUS.md`、`plans/implementation-plan.md` 内把 release / DOI 叙述与当前核验结果对齐。
- 已安全修改 `README.md`、`README.zh-CN.md`、`submission/artifact-availability.md`。
- 保留 `release/v0.1-live-chain/RELEASE_NOTE.md` 作为历史 specimen 文档，不做自动替换。

## 当前结论

- 新 DOI `10.5281/zenodo.19334062` 已通过外部元数据核实，可用于 TOSEM 中文论文工作区。
- 仓库内仍有若干旧 DOI `10.5281/zenodo.19055948` 文案，且部分文件是否应更新取决于其是否在描述历史 specimen。
- 因此，面向论文稿的安全策略应是：
  - 在 `paper/tosem_cn/` 中使用已核实的新 DOI；
  - 把旧 DOI 保留为审计问题说明；
  - 把 current-package 文档与 historical specimen 文档明确分流，不做跨语义替换。
