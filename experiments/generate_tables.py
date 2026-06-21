#!/usr/bin/env python3
"""Generate paper tables through the packaged experiment entrypoint."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.generate_softwarex_v2_evaluation_table import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
