# Public Docs Sync Review

## 安全已更新

- `README.md`
  - 已将仓库顶层 DOI badge 对齐到当前 package 对应的 `10.5281/zenodo.19334062`。
  - 已在 `Current v0.1 package` 段落中明确：
    - repository release 是 `v0.2.0`
    - current package DOI 是 `10.5281/zenodo.19334062`
    - package version inside that release 仍为 `v0.1`
  - 已把旧 specimen DOI 的语义改写为“historical specimen DOI”，避免继续把它表述成当前最新工件。
- `README.zh-CN.md`
  - 已将顶层 DOI badge 对齐到 `10.5281/zenodo.19334062`。
  - 已新增“当前 OAP v0.1 package”段落，明确当前论文工件路径、release `v0.2.0` 与 DOI。
  - 已把 `v0.1-live-chain` 路径改写为历史样品轨道，保留其旧 DOI。
- `submission/artifact-availability.md`
  - 文件意图明确，是当前论文的 artifact availability 说明。
  - 已对齐为当前 OAP v0.1 package、repository release `v0.2.0`、Zenodo DOI `10.5281/zenodo.19334062`。

## 有意保留为历史资料

- `release/v0.1-live-chain/RELEASE_NOTE.md`
  - 文件标题、内容和目录位置都明确表明它描述的是历史 `v0.1-live-chain` specimen。
  - 其中的 DOI `10.5281/zenodo.19055948` 与该历史 specimen 语义一致，因此本轮保持不动。

## 需人工判断

- 本轮检查的 4 个目标文件中，当前无新增“必须人工判断后才能动”的项目。
- 但如果后续要继续统一仓库更广范围的 release / DOI 口径，仍应对 `release/` 目录下其他历史资料做逐项人工复核，而不是批量替换。

## 判断依据

- 当前 package 的锚点来自：
  - 本地 `git tag` 中的 `v0.2.0`
  - `git show v0.2.0`
  - GitHub Release API
  - DataCite API 中的 `10.5281/zenodo.19334062`
- 历史 specimen 的判断依据来自：
  - 文件路径显式位于 `release/v0.1-live-chain/`
  - 标题和正文都在描述 `AEP v0.1 Live-Chain Specimen`
  - 该材料与当前 OAP v0.1 paper package 不是同一发布表面
