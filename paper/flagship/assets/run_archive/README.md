# Run Archive

## 用途

这个目录用于冻结当前 appendix state 下实际执行过的 validation runs，供后续 appendix / rebuttal / reviewer inspection 使用。

它的原则是：

- 只记录 actually run 的内容
- 把实际运行和 future plan 分开
- 不把 clean alignment 写成既成事实

## 文件说明

- `00_scope_and_status.md`
  - 当前 run archive 的范围与状态
- `01_commands_used.md`
  - 当前冻结状态下实际使用的命令
- `02_reference_validator_outputs.md`
  - reference validator 的归档输出摘要
- `03_independent_checker_outputs.md`
  - independent checker 的归档输出摘要
- `04_pass_fail_matrix.md`
  - broader corpus 的 pass/fail matrix
- `05_divergence_notes.md`
  - 当前 divergence 的含义与边界
- `json/`
  - 由当前 frozen matrix 投影出的 machine-readable result files

## 当前性质

这是 reviewer-facing appendix material 的 cleaned freeze，不是最终 artifact appendix。
