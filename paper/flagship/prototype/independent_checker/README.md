# Independent Checker Prototype

## Purpose

这个目录包含一个 genuinely separate 的最小 checker 原型，用于旗舰论文的 evidence-building package。它的目标不是替代当前 reference validator，而是提供第二条独立的 reasoning path，用来检查 minimal verification boundary。

## Independence

本 checker 满足以下最小独立性约束：

- 不导入 `agent_evidence.oap`
- 不调用 `agent-evidence validate-profile`
- 不包装当前 reference validator 的 JSON 输出

它只读取相同的 central input format，并用标准库手写一组 boundary-oriented checks。

## Supported Input

- 当前只支持 central format：
  - `execution-evidence-operation-accountability-profile@0.1`
- 当前最适合的输入文件：
  - `examples/minimal-valid-evidence.json`
  - `examples/valid-retention-review-evidence.json`
  - 现有 `examples/invalid-*.json`

## What It Checks

- profile identity presence
- identity binding presence
- target binding presence
- operation semantics presence
- policy linkage presence
- evidence continuity presence
- validation declaration presence
- outcome presence and minimal outcome distinguishability
- timestamp sanity checks
- obvious implementation-coupling markers

## What It Does Not Try to Do

- 它不是完整 schema validator
- 它不重建 reference validator 的 staged logic
- 它不保证与 reference validator 对所有 edge cases 完全一致
- 它只做 minimal boundary checks

## Usage

```bash
python3 paper/flagship/prototype/independent_checker/check_minimal_boundary.py \
  examples/minimal-valid-evidence.json
```

也可以一次检查多个文件：

```bash
python3 paper/flagship/prototype/independent_checker/check_minimal_boundary.py \
  examples/minimal-valid-evidence.json \
  examples/invalid-unclosed-reference.json
```

## Output

输出保持简单：

- `PASS` / `FAIL`
- issue count
- short reason labels
- path + message

## Limitations

- temporal consistency 目前只是 sanity checks
- implementation coupling 检测是启发式
- `outcome_unverifiable` 目前只覆盖一个非常窄的 case：
  - `succeeded` statement 的所有 output refs 都没有引入可区分的 outcome object

## Why This Still Matters

即使这个 checker 仍然是 minimal and incomplete，它也已经完成一件关键事情：把 operation accountability 的一部分判断，从单一 reference validator 内部逻辑，推进成可以被另一套独立代码直接检查的 boundary evidence。
