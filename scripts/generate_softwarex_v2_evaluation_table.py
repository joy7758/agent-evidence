#!/usr/bin/env python3
"""Generate the SoftwareX v2 evaluation summary table from experiment receipts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_INPUT = Path("experiments/results")
DEFAULT_OUTPUT = Path("paper/figures/evaluation_table.md")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def load_results(input_dir: Path) -> list[dict]:
    results = []
    for path in sorted(input_dir.glob("exp*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if "experiment_id" in payload:
            results.append(payload)
    if not results:
        raise FileNotFoundError(f"no experiment result JSON files found in {input_dir}")
    return results


def render_table(results: list[dict]) -> str:
    lines = [
        "# Evaluation Table",
        "",
        "Affected clauses: EEOAP-001, EEOAP-002, EEOAP-003, EEOAP-004, EEOAP-005.",
        "",
        "| Experiment | Source | Span count | Validator ok | Issue count | Output |",
        "| --- | --- | ---: | --- | ---: | --- |",
    ]
    for result in results:
        lines.append(
            "| {experiment_id} | {source_type} | {span_count} | {validator_ok} | "
            "{issue_count} | `{output_profile}` |".format(**result)
        )
    lines.extend(
        [
            "",
            "Boundary: these are local experiment receipts. They do not claim external",
            "validation, certification, production deployment, publication status, or",
            "legal non-repudiation.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    results = load_results(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_table(results), encoding="utf-8")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
