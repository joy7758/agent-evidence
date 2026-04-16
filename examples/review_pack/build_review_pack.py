from __future__ import annotations

import argparse
import json
from pathlib import Path

from agent_evidence.review_pack import ReviewPackAssembler

DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[1] / "artifacts" / "review-pack"


def _supporting_files_from_args(args: argparse.Namespace) -> dict[str, Path]:
    supporting_files: dict[str, Path] = {}
    for name in ("manifest", "public_key", "runtime_events", "private_key"):
        value = getattr(args, f"{name}_path")
        if value is not None:
            supporting_files[name] = value
    return supporting_files


def build_review_pack(args: argparse.Namespace) -> dict[str, object]:
    assembler = ReviewPackAssembler.for_output_dir(args.output_dir)
    pack = assembler.assemble(
        bundle_path=args.bundle_path,
        receipt_path=args.receipt_path,
        summary_path=args.summary_path,
        supporting_files=_supporting_files_from_args(args),
        include_private_key=args.include_private_key,
    )

    result = {
        "pack_dir": str(pack.pack_dir),
        "index_path": str(pack.index_path),
        "report_path": str(pack.report_path),
        "primary_files": {name: str(path) for name, path in pack.primary_files.items()},
        "supporting_files": {name: str(path) for name, path in pack.supporting_files.items()},
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build a Review Pack from an existing bundle, receipt, and summary "
            "without changing their schemas."
        )
    )
    parser.add_argument("--bundle-path", type=Path, required=True, help="Path to the bundle.")
    parser.add_argument(
        "--receipt-path",
        type=Path,
        required=True,
        help="Path to the machine-readable receipt.",
    )
    parser.add_argument(
        "--summary-path",
        type=Path,
        required=True,
        help="Path to the reviewer-facing summary.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory for the assembled review pack. Default: {DEFAULT_OUTPUT_DIR}",
    )
    parser.add_argument(
        "--manifest-path",
        type=Path,
        help="Optional path to the manifest sidecar to include as supporting material.",
    )
    parser.add_argument(
        "--public-key-path",
        type=Path,
        help="Optional path to the verification public key to include as supporting material.",
    )
    parser.add_argument(
        "--runtime-events-path",
        type=Path,
        help="Optional path to runtime JSONL capture to include as supporting material.",
    )
    parser.add_argument(
        "--private-key-path",
        type=Path,
        help=(
            "Optional path to the local signing private key. It is excluded by default and "
            "only copied if --include-private-key is also set."
        ),
    )
    parser.add_argument(
        "--include-private-key",
        action="store_true",
        help="Include the private key supporting file. Default is excluded.",
    )
    args = parser.parse_args()

    result = build_review_pack(args)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
