from __future__ import annotations

import argparse
import json
import math
import re
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any

ADAPTER_NAME = "linuxptp"
ADAPTER_VERSION = "0.1"
ADAPTER_LABEL = "aep-media-linuxptp-adapter@0.1"
REPORT_PROFILE = {
    "name": "aep-media-adapter-ingestion-report",
    "version": "0.1",
}
BASE_SAMPLE_TIME = datetime(2026, 4, 26, 8, 20, 0, tzinfo=timezone.utc)


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha256_file(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.name if path.is_absolute() else path.as_posix()


def _issue(code: str, path: str, message: str) -> dict[str, str]:
    return {
        "code": code,
        "message": message,
        "path": path,
    }


def _adapter_report(
    *,
    input_path: Path,
    out_path: Path,
    ok: bool,
    issues: list[dict[str, str]],
) -> dict[str, Any]:
    normalized_output: dict[str, Any] = {
        "kind": "aep-media-time-trace",
        "path": _display_path(out_path),
        "sha256": None,
        "size_bytes": 0,
    }
    if out_path.exists() and out_path.is_file():
        normalized_output["sha256"] = _sha256_file(out_path)
        normalized_output["size_bytes"] = out_path.stat().st_size

    return {
        "profile": REPORT_PROFILE,
        "adapter": {
            "name": ADAPTER_NAME,
            "version": ADAPTER_VERSION,
            "mode": "fixture_ingestion",
        },
        "source": {
            "kind": "linuxptp_log",
            "input_path": _display_path(input_path),
            "tool_available": False,
            "external_verification_performed": False,
        },
        "normalized_output": normalized_output,
        "claim_boundary": {
            "adapter_ingestion": True,
            "external_verification": False,
            "local_validation_only": True,
        },
        "ok": ok,
        "issue_count": len(issues),
        "issues": issues,
        "summary": f"{'PASS' if ok else 'FAIL'} {ADAPTER_LABEL}",
    }


def _isoformat(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _parse_sample_time(line: str, sample_index: int) -> str:
    match = re.search(r"\b(20\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ)\b", line)
    if match:
        return match.group(1)
    return _isoformat(BASE_SAMPLE_TIME + timedelta(seconds=sample_index))


def _to_ns(value: str, unit: str | None) -> float:
    numeric_value = float(value)
    normalized_unit = (unit or "ns").lower()
    if normalized_unit == "us":
        return numeric_value * 1000
    if normalized_unit == "ms":
        return numeric_value * 1000000
    return numeric_value


def _extract_measurement(line: str, label: str) -> float | None:
    match = re.search(
        rf"\b{label}\s+([+-]?\d+(?:\.\d+)?)\s*(ns|us|ms)?\b",
        line,
        flags=re.IGNORECASE,
    )
    if match:
        return _to_ns(match.group(1), match.group(2))
    match = re.search(
        rf"\b{label}[=:]\s*([+-]?\d+(?:\.\d+)?)\s*(ns|us|ms)?\b",
        line,
        flags=re.IGNORECASE,
    )
    if match:
        return _to_ns(match.group(1), match.group(2))
    return None


def _state_from_line(line: str) -> str:
    lowered = line.lower()
    if "holdover" in lowered:
        return "holdover"
    if "locked" in lowered or " s2 " in lowered or " state s2" in lowered:
        return "locked"
    return "unknown"


def _infer_source(source: str, text: str) -> str:
    if source != "auto":
        return source
    lowered = text.lower()
    if "phc2sys" in lowered:
        return "phc2sys"
    if "ptp4l" in lowered:
        return "ptp4l"
    return "linuxptp"


def _summary(samples: list[dict[str, Any]]) -> dict[str, Any]:
    offsets = [float(sample["offset_ns"]) for sample in samples]
    max_abs_offset = max(abs(offset) for offset in offsets)
    max_jitter = 0.0
    if len(offsets) > 1:
        max_jitter = max(
            abs(offsets[index] - offsets[index - 1]) for index in range(1, len(offsets))
        )
    within_threshold = max_abs_offset <= 1000000 and max_jitter <= 1000000
    return {
        "sample_count": len(samples),
        "max_abs_offset_ns": int(max_abs_offset)
        if math.isfinite(max_abs_offset)
        else max_abs_offset,
        "max_jitter_ns": int(max_jitter) if math.isfinite(max_jitter) else max_jitter,
        "within_threshold": within_threshold,
    }


def parse_linuxptp_log(text: str, source: str = "auto") -> dict[str, Any]:
    """Normalize ptp4l/phc2sys-style log text into an AEP-Media time trace."""

    source_name = _infer_source(source, text)
    samples: list[dict[str, Any]] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        offset = _extract_measurement(line, "offset")
        if offset is None:
            continue
        delay = _extract_measurement(line, "delay")
        sample_time = _parse_sample_time(line, len(samples))
        sample: dict[str, Any] = {
            "sample_utc": sample_time,
            "offset_ns": int(offset) if offset.is_integer() else offset,
            "path_delay_ns": int(delay)
            if isinstance(delay, float) and delay.is_integer()
            else delay or 0,
            "state": _state_from_line(line),
        }
        samples.append(sample)

    if samples:
        start_utc = samples[0]["sample_utc"]
        last_sample_time = datetime.fromisoformat(samples[-1]["sample_utc"].replace("Z", "+00:00"))
        end_utc = _isoformat(last_sample_time + timedelta(seconds=1))
    else:
        start_utc = _isoformat(BASE_SAMPLE_TIME)
        end_utc = _isoformat(BASE_SAMPLE_TIME)

    return {
        "profile": {
            "name": "aep-media-time-trace",
            "version": "0.1",
        },
        "trace_id": f"clock-trace-linuxptp-{source_name}-fixture-001",
        "trace_type": "declared_ptp_trace",
        "collection": {
            "source": "linuxptp_log_fixture",
            "collector": "aep-media-linuxptp-adapter",
            "start_utc": start_utc,
            "end_utc": end_utc,
        },
        "sync": {
            "declared_source": "ptp",
            "sync_status": "declared",
            "ptp_domain": 0,
            "grandmaster_id": "unknown-or-fixture",
        },
        "thresholds": {
            "max_abs_offset_ns": 1000000,
            "max_jitter_ns": 1000000,
        },
        "samples": samples,
        "summary": _summary(samples)
        if samples
        else {
            "sample_count": 0,
            "max_abs_offset_ns": 0,
            "max_jitter_ns": 0,
            "within_threshold": False,
        },
    }


def ingest_linuxptp_trace(
    input_path: str | Path,
    out_path: str | Path,
    source: str = "auto",
) -> dict[str, Any]:
    resolved_input = Path(input_path)
    resolved_output = Path(out_path)
    if not resolved_input.exists():
        issues = [
            _issue("linuxptp_log_not_found", "source.input_path", "LinuxPTP log file not found.")
        ]
        return _adapter_report(
            input_path=resolved_input, out_path=resolved_output, ok=False, issues=issues
        )

    try:
        trace = parse_linuxptp_log(resolved_input.read_text(encoding="utf-8"), source=source)
    except (OSError, ValueError, TypeError) as exc:
        issues = [
            _issue("linuxptp_log_parse_error", "source.input_path", f"could not parse log: {exc}")
        ]
        return _adapter_report(
            input_path=resolved_input, out_path=resolved_output, ok=False, issues=issues
        )

    if not trace["samples"]:
        issues = [
            _issue(
                "linuxptp_no_samples",
                "source.input_path",
                "LinuxPTP log contained no offset samples.",
            )
        ]
        return _adapter_report(
            input_path=resolved_input, out_path=resolved_output, ok=False, issues=issues
        )

    try:
        _write_json(resolved_output, trace)
    except OSError as exc:
        issues = [
            _issue(
                "linuxptp_trace_write_failed",
                "normalized_output.path",
                f"could not write trace: {exc}",
            )
        ]
        return _adapter_report(
            input_path=resolved_input, out_path=resolved_output, ok=False, issues=issues
        )

    return _adapter_report(input_path=resolved_input, out_path=resolved_output, ok=True, issues=[])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Ingest a LinuxPTP-style log fixture.")
    parser.add_argument("input_log", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--source", default="auto", choices=["auto", "ptp4l", "phc2sys"])
    args = parser.parse_args(argv)

    report = ingest_linuxptp_trace(args.input_log, args.out, source=args.source)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
