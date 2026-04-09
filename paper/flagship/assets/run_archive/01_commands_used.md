# Commands Used

以下命令都在 repo 根目录实际执行过。

## 1. Sanity Compile

```bash
python3 -m py_compile \
  paper/flagship/prototype/independent_checker/check_minimal_boundary.py \
  paper/flagship/prototype/independent_checker/compare_checkers.py
```

## 2. Independent Checker on the New Direct Failure Specimens

```bash
python3 paper/flagship/prototype/independent_checker/check_minimal_boundary.py \
  paper/flagship/assets/specimens/scenario_09_missing_target_binding_invalid.json \
  paper/flagship/assets/specimens/scenario_10_ambiguous_operation_semantics_invalid.json \
  paper/flagship/assets/specimens/scenario_11_outcome_unverifiability_invalid.json
```

## 3. Reference Validator on the Same 3 Files

本轮 automation 实际调用的是 reference validator 的库入口：

```bash
python3 - <<'PY'
from pathlib import Path
from agent_evidence.oap import validate_profile_file
paths = [
  'paper/flagship/assets/specimens/scenario_09_missing_target_binding_invalid.json',
  'paper/flagship/assets/specimens/scenario_10_ambiguous_operation_semantics_invalid.json',
  'paper/flagship/assets/specimens/scenario_11_outcome_unverifiability_invalid.json',
]
for raw in paths:
    report = validate_profile_file(Path(raw))
    codes = []
    for stage in report['stages']:
        for issue in stage['issues']:
            if issue['code'] not in codes:
                codes.append(issue['code'])
    print(raw, 'PASS' if report['ok'] else 'FAIL', ','.join(codes) if codes else '-')
PY
```

说明：

- canonical CLI 仍然是 `agent-evidence validate-profile <file>`
- 这里用库入口，是为了直接冻结 pass/fail + primary issue code 摘要

## 4. Refreshed Broader Corpus Comparison

```bash
python3 paper/flagship/prototype/independent_checker/compare_checkers.py
```

说明：

- compare helper 当前覆盖 19-file corpus
- 该运行会再次比较现有 anchors、scenario specimens、以及全部 direct failure specimens

## 5. Machine-Readable Freeze Basis

本轮 `json/` 目录没有引入新的 validation run。三份 JSON 文件都只从当前已冻结的 matrix 与 specimen table 投影而来：

- `paper/flagship/assets/run_archive/04_pass_fail_matrix.md`
- `paper/flagship/assets/specimens/README.md`

也就是说，machine-readable outputs 是现有结果的结构化冻结，不是新增实验。
