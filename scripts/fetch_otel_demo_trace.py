#!/usr/bin/env python3
"""Fetch the official OpenTelemetry OTLP JSON trace example.

The downloaded fixture is a public OpenTelemetry protocol example. It is used
as a repository-local real-format trace grounding input, not as production
telemetry or external validation.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen


DEFAULT_URL = (
    "https://raw.githubusercontent.com/open-telemetry/opentelemetry-proto/"
    "main/examples/trace.json"
)
DEFAULT_OUTPUT = Path("data/otel/raw_demo_trace.json")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=DEFAULT_URL, help="Raw OTLP JSON trace URL.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output JSON path. Default: {DEFAULT_OUTPUT}",
    )
    return parser.parse_args()


def load_remote_json(url: str) -> dict:
    with urlopen(url, timeout=30) as response:
        payload = response.read().decode("utf-8")
    data = json.loads(payload)
    if not isinstance(data, dict) or not isinstance(data.get("resourceSpans"), list):
        raise ValueError("downloaded payload is not an OTLP JSON trace with resourceSpans")
    return data


def main() -> int:
    args = parse_args()
    trace = load_remote_json(args.url)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(trace, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    provenance = {
        "source_url": args.url,
        "output": str(args.output),
        "fetched_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "boundary": (
            "Public OTLP JSON example used as local trace-format grounding; "
            "not production telemetry or external validation."
        ),
    }
    provenance_path = args.output.with_suffix(".provenance.json")
    provenance_path.write_text(
        json.dumps(provenance, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {args.output}")
    print(f"wrote {provenance_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
