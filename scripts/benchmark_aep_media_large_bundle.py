from __future__ import annotations

import argparse
import json
import platform
import shutil
import tempfile
import time
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any

from agent_evidence.media_bundle import build_media_bundle, verify_media_bundle

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_CASE_DIR = ROOT / "examples" / "media" / "use_cases" / "mobile_video_network_timing"
TEMPLATE_STATEMENT = TEMPLATE_CASE_DIR / "mobile-video-operation-evidence.json"
PRIMARY_MEDIA_PATH = "artifacts/mobile_video_placeholder.bin"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _write_deterministic_file(path: Path, size_bytes: int) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    digest = sha256()
    block = b"AEP-MEDIA-BENCHMARK-BLOCK-0123456789\n" * 4096
    remaining = size_bytes
    with path.open("wb") as handle:
        while remaining:
            chunk = block[: min(len(block), remaining)]
            handle.write(chunk)
            digest.update(chunk)
            remaining -= len(chunk)
    return digest.hexdigest()


def _copy_template_case(work_dir: Path) -> Path:
    case_dir = work_dir / "mobile_video_network_timing"
    shutil.copytree(TEMPLATE_CASE_DIR, case_dir)
    return case_dir


def _prepare_statement(case_dir: Path, size_mb: int) -> Path:
    statement_path = case_dir / "mobile-video-operation-evidence.json"
    statement: dict[str, Any] = json.loads(statement_path.read_text(encoding="utf-8"))

    size_bytes = size_mb * 1024 * 1024
    digest = _write_deterministic_file(case_dir / PRIMARY_MEDIA_PATH, size_bytes)

    artifacts = statement["media"]["artifacts"]
    primary = next(artifact for artifact in artifacts if artifact["role"] == "primary_media")
    primary["sha256"] = digest
    primary["size_bytes"] = size_bytes
    statement["statement_id"] = f"aep-media:statement:large-bundle-benchmark-{size_mb}mb"
    statement["timestamp"] = "2026-05-10T10:00:03Z"
    statement["evidence"]["notes"] = (
        "Synthetic large-bundle benchmark fixture. The media payload is deterministic "
        "placeholder data generated at benchmark time."
    )

    statement_path.write_text(
        json.dumps(statement, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return statement_path


def _run_one(size_mb: int, root_temp: Path, keep: bool) -> dict[str, Any]:
    case_dir = _copy_template_case(root_temp / f"{size_mb}mb")
    statement_path = _prepare_statement(case_dir, size_mb)
    bundle_dir = root_temp / f"bundle-{size_mb}mb"

    build_start = time.perf_counter()
    build_report = build_media_bundle(statement_path, bundle_dir)
    build_seconds = time.perf_counter() - build_start

    verify_start = time.perf_counter()
    verify_report = verify_media_bundle(bundle_dir)
    verify_seconds = time.perf_counter() - verify_start

    result = {
        "size_mb": size_mb,
        "size_bytes": size_mb * 1024 * 1024,
        "build_seconds": round(build_seconds, 6),
        "verify_seconds": round(verify_seconds, 6),
        "build_throughput_mb_s": round(size_mb / build_seconds, 3) if build_seconds else None,
        "verify_throughput_mb_s": round(size_mb / verify_seconds, 3) if verify_seconds else None,
        "build_ok": bool(build_report.get("ok")),
        "verify_ok": bool(verify_report.get("ok")),
        "verify_issue_count": int(verify_report.get("issue_count", 0)),
        "bundle_dir_kept": str(bundle_dir) if keep else None,
    }
    return result


def _markdown_report(payload: dict[str, Any]) -> str:
    lines = [
        "# Large Bundle Performance Results (R1)",
        "",
        "## Scope",
        "",
        "This benchmark generates deterministic placeholder media files in a temporary directory,",
        "builds AEP-Media bundles, verifies them, and records wall-clock timing. It does not",
        "commit large files and does not compare AEP-Media with AFF4/E01 tools.",
        "",
        "## Environment",
        "",
        f"- Timestamp UTC: `{payload['timestamp_utc']}`",
        f"- Python: `{payload['environment']['python']}`",
        f"- Platform: `{payload['environment']['platform']}`",
        f"- Machine: `{payload['environment']['machine']}`",
        "",
        "## Results",
        "",
        "| Size | Build seconds | Verify seconds | Build MB/s | Verify MB/s | Build ok | "
        "Verify ok | Issues |",
        "|---:|---:|---:|---:|---:|---|---|---:|",
    ]
    for row in payload["results"]:
        lines.append(
            "| {size_mb} MB | {build_seconds} | {verify_seconds} | {build_throughput_mb_s} | "
            "{verify_throughput_mb_s} | {build_ok} | {verify_ok} | {verify_issue_count} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Hash recomputation and bundle verification are O(file size) and are dominated by "
            "local I/O.",
            "- Schema, path, reference, and policy checks scale mainly with the number of "
            "declared records and references.",
            "- Adapter parsing cost is outside this benchmark and depends on fixture size and "
            "parser path.",
            "- These results are local-machine measurements on synthetic placeholder media, "
            "not a production forensic corpus benchmark.",
            "",
            "## Claim Boundary",
            "",
            "The benchmark measures local AEP-Media build/verify overhead only. It does not "
            "claim legal admissibility, chain of custody, production deployment, full MP4 "
            "PRFT parsing, real C2PA signature verification, or real PTP proof.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark AEP-Media large bundle build/verify.")
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "docs" / "paper" / "softwarex" / "r1" / "benchmarks",
    )
    parser.add_argument("--include-1gb", action="store_true")
    parser.add_argument("--keep", action="store_true")
    args = parser.parse_args()

    if not TEMPLATE_STATEMENT.exists():
        parser.error(f"template statement not found: {TEMPLATE_STATEMENT}")

    args.out.mkdir(parents=True, exist_ok=True)
    sizes = [1, 10, 100]
    if args.include_1gb:
        sizes.append(1024)

    root_temp_path: Path | None = None
    try:
        root_temp_path = Path(tempfile.mkdtemp(prefix="aep-media-large-bundle-"))
        results = [_run_one(size_mb, root_temp_path, args.keep) for size_mb in sizes]
        payload = {
            "profile": "aep-media-large-bundle-benchmark-r1",
            "timestamp_utc": _utc_now(),
            "sizes_mb": sizes,
            "temporary_root_kept": str(root_temp_path) if args.keep else None,
            "environment": {
                "python": platform.python_version(),
                "platform": platform.platform(),
                "machine": platform.machine(),
            },
            "results": results,
        }
        (args.out / "large_bundle_performance_results.json").write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (args.out / "large_bundle_performance_results.md").write_text(
            _markdown_report(payload),
            encoding="utf-8",
        )
    finally:
        if root_temp_path is not None and not args.keep:
            shutil.rmtree(root_temp_path, ignore_errors=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
