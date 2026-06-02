# ruff: noqa: E402,I001

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.se_case_common import build_statement, read_json, schema_only


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", type=Path)
    args = parser.parse_args()
    fixture = read_json(args.fixture)
    print(json.dumps(schema_only(build_statement(fixture)), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
