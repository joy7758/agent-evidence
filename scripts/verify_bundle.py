#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from agent_evidence.aep import verify_bundle


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify an Agent Evidence Profile bundle.")
    parser.add_argument("bundle_dir", type=Path, help="Path to the bundle directory.")
    args = parser.parse_args()

    result = verify_bundle(args.bundle_dir)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
