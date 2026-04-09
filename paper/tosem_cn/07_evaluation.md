# Evaluation

## 1. 评估原则

本文不虚构仓库之外的实验数据，也不把尚未完成的比较评估写成既成事实。因此，本章只报告
当前工作区和现有发布材料能够直接支撑的 evaluation evidence。它更接近
“conformance + reproducibility + artifact sanity check”，而不是大规模经验评估。

## 2. 规范、样例与规则面的对应性

当前仓库已经形成一组最小但闭合的规则验证面：

- 2 个 valid 样例
- 5 个 invalid 样例

并且 `examples/README.md` 明确说明：

- `minimal-valid-evidence.json` 对应 metadata enrichment 场景
- `valid-retention-review-evidence.json` 对应 retention review 场景，并展示第二种 input linkage 形态
- `invalid-missing-required.json` 对应必填字段缺失
- `invalid-unclosed-reference.json` 对应引用闭合失败
- `invalid-policy-link-broken.json` 对应 policy/evidence 链接不一致
- `invalid-provenance-output-mismatch.json` 对应 provenance/output cross-field mismatch
- `invalid-validation-provenance-link-broken.json` 对应 validation/provenance 引用闭合失败

这使得最小 profile 的主规则面能够以“正例 + 单点破坏反例”的方式被直接测试。
与最初的最小路径相比，这一反例集增强了 failure-boundary coverage，但它仍不代表穷尽覆盖。
第二个 valid 样例则把“通过边界”从单一场景扩展到第二语境，因此只足以支撑 basic portability
evidence 或 second-context validity evidence，而不足以支撑 broad cross-framework validation。
表 3 对这些样例的角色、场景 / 失败模式、预期结果与主错误码做了压缩汇总，使“当前到底验证了什么”
更容易被 reviewer 直接扫描。

## 3. Validator 层验证

`tests/test_operation_accountability_profile.py` 直接覆盖：

- valid 样例通过
- 5 个 invalid 样例失败
- CLI 命令输出 JSON

在当前工作区复验中，以下测试命令通过：

```bash
./.venv/bin/python -m pytest \
  tests/test_operation_accountability_profile.py \
  tests/test_aep_profile.py \
  tests/test_cli.py
```

当前复验结果为：

- 21 项测试通过
- 1 条 non-blocking warning

表 3 也把当前样例层的验证入口压缩成一张更易读的摘要表：两个 valid 样例的预期结果都是
pass，五个 invalid 样例都对应一个当前已落地的主错误码。

warning 来自 Python 3.14 环境下的 `langchain_core`，仓库 `docs/STATUS.md` 与
`submission/release-readiness-check.md` 都已将其标记为不影响当前 minimal profile /
validator / demo 路径的已知环境项。

## 4. Demo 闭环验证

当前工作区复验中，以下命令通过：

```bash
python3 demo/run_operation_accountability_demo.py
```

其输出按六个步骤展开：

1. object load or creation
2. profile precheck
3. operation call
4. evidence generation
5. validator verification
6. output verification result

最终输出一条 `PASS execution-evidence-operation-accountability-profile@0.1 ...`，并在
`demo/artifacts/` 下写出 `minimal-profile-evidence.json` 与 `validation-report.json`。
这说明本文主张的“最小可验证闭环”在仓库中已经不是纸面流程，而是可运行流程。

## 5. 发布层验证

仓库当前还能提供发布级证据：

- 本地 `git tag` 中存在 `v0.2.0`
- `git show v0.2.0` 显示该 tag 冻结了 OAP v0.1 package
- GitHub Release API 返回公开 release `Agent Evidence v0.2.0`
- DataCite API 返回 DOI `10.5281/zenodo.19334062`

这部分证据不直接说明“方法学优于其他方案”，但它说明工件已经进入可发布、可引用、可归档
的状态。

## 6. 同案比较的结构性观察

为避免让表 1 停留在纯概念层，本文另外整理了一个同案比较说明：
`paper/tosem_cn/comparative_case_analysis.md`。该说明固定使用当前仓库已经存在的
`valid-retention-review-evidence.json` 场景，并把 ordinary logs、provenance-only、
policy-only 与本文 profile 放在同一 operation accountability 问题上比较。

这个比较的价值是结构性而不是实验性的。它更具体地说明：ordinary logs 能记事，但难以独立
形成可验证问责单元；provenance-only 能表达来源链，但不必然绑定 policy、minimal evidence
与 validation path；policy-only 能表达规则依据，但不能单独说明实际执行、对象引用闭合与
验证状态。本文 profile 的额外增量，是把这些要素在同一个最小 statement 中绑定起来。

这仍不是对照实验，也不构成性能或效果优越性的实证结论；它只是为表 1 与 related work
中的方法边界判断提供一个仓库内、场景固定的落点。

## 7. 基础可迁移性的小矩阵

表 4 将当前仓库对 portability 的证据压缩为五个维度：context diversity、input/output
linkage pattern diversity、same validator path reuse、same core field model reuse、
以及 current external-validity limit。它把“第二个 valid 样例增强了 portability evidence”
这句话拆成更可检查的最小判断。

这个矩阵目前只支持一个克制结论：同一 minimal verifiable profile 已经在第二个不同语境下
通过同一路径验证，因此 basic portability evidence 已经存在。它同时明确写出当前不能支持的
结论，包括 broad cross-framework validation、复杂 workflow 外推、以及独立实现收敛。

## 8. 当前不能声称的评估结果

基于当前仓库，本文不能声称以下结果，因为缺乏直接证据：

- 跨框架广泛通用性已经被系统验证
- 与其他 provenance / logging / governance 方案做过对照实验
- 用户研究或审稿人可用性研究已经完成
- 在大规模对象图或多智能体编排下的性能与可扩展性已被评估

这些都必须留在“投稿前待补”或未来工作中。

## 投稿前待补

- 如果投稿需要更强 evaluation 章节，可补一组严格受控的 ablation：
  - 不同 invalid 样例对应的错误码稳定性
  - CLI 与 API 路径的一致性
- 如需进一步增强 reviewer 友好性，可在表 3 与表 4 之外补一页 appendix 级命令摘录，
  但不应虚构新的实验结果。
