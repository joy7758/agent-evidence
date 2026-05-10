from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from hashlib import sha256
from pathlib import Path
from typing import Any

ADAPTER_NAME = "ffmpeg_prft"
ADAPTER_VERSION = "0.1"
ADAPTER_LABEL = "aep-media-ffmpeg-prft-adapter@0.1"
REPORT_PROFILE = {
    "name": "aep-media-adapter-ingestion-report",
    "version": "0.1",
}


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("ffprobe payload must be a JSON object")
    return payload


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
    tool_available: bool,
    external_verification_performed: bool,
) -> dict[str, Any]:
    normalized_output: dict[str, Any] = {
        "kind": "aep-media-ffmpeg-prft-metadata",
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
            "mode": "optional_external_smoke"
            if external_verification_performed
            else "fixture_ingestion",
        },
        "source": {
            "kind": "ffprobe_external_probe"
            if external_verification_performed
            else "ffprobe_json_fixture",
            "input_path": _display_path(input_path),
            "tool_available": tool_available,
            "external_verification_performed": external_verification_performed,
        },
        "normalized_output": normalized_output,
        "claim_boundary": {
            "adapter_ingestion": True,
            "external_verification": external_verification_performed,
            "local_validation_only": not external_verification_performed,
        },
        "ok": ok,
        "issue_count": len(issues),
        "issues": issues,
        "summary": f"{'PASS' if ok else 'FAIL'} {ADAPTER_LABEL}",
    }


def _iter_dicts(value: Any) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(value, dict):
        found.append(value)
        for item in value.values():
            found.extend(_iter_dicts(item))
    elif isinstance(value, list):
        for item in value:
            found.extend(_iter_dicts(item))
    return found


def _has_prft_marker(value: Any) -> bool:
    for item in _iter_dicts(value):
        side_data_type = str(item.get("side_data_type", "")).lower()
        if "producer reference time" in side_data_type or "prft" in side_data_type:
            return True
        tags = item.get("tags")
        if isinstance(tags, dict):
            lowered_keys = {str(key).lower() for key in tags}
            if {"prft_time", "producer_reference_time_utc"} & lowered_keys:
                return True
    return False


def _has_timecode(value: Any) -> bool:
    for item in _iter_dicts(value):
        tags = item.get("tags")
        if isinstance(tags, dict) and any(str(key).lower() == "timecode" for key in tags):
            return True
    return False


def _producer_time(value: Any) -> str | None:
    keys = (
        "producer_reference_time_utc",
        "prft_time",
        "wallclock",
        "wallclock_utc",
    )
    for item in _iter_dicts(value):
        for key in keys:
            raw = item.get(key)
            if isinstance(raw, str) and raw:
                return raw
        tags = item.get("tags")
        if isinstance(tags, dict):
            for key in keys:
                raw = tags.get(key)
                if isinstance(raw, str) and raw:
                    return raw
    return None


def _frame_count(payload: dict[str, Any]) -> int:
    frames = payload.get("frames")
    if isinstance(frames, list):
        return len(frames)
    count = 0
    for stream in payload.get("streams", []):
        if isinstance(stream, dict):
            raw = stream.get("nb_frames")
            if isinstance(raw, int):
                count += raw
            elif isinstance(raw, str) and raw.isdigit():
                count += int(raw)
    return count


def parse_ffprobe_prft_json(payload: dict[str, Any]) -> dict[str, Any]:
    format_payload = payload.get("format") if isinstance(payload.get("format"), dict) else {}
    streams = payload.get("streams") if isinstance(payload.get("streams"), list) else []
    prft_detected = _has_prft_marker(payload)
    timecode_detected = _has_timecode(payload)
    return {
        "profile": {
            "name": "aep-media-ffmpeg-prft-metadata",
            "version": "0.1",
        },
        "source": {
            "kind": "ffprobe_json_fixture",
            "media_path": format_payload.get("filename", "demo-media.mp4"),
            "container": "mp4",
        },
        "timing": {
            "prft_detected": prft_detected,
            "timecode_detected": timecode_detected,
            "producer_reference_time_utc": _producer_time(payload),
            "stream_count": len(streams),
            "frame_count": _frame_count(payload),
        },
        "raw_summary": {
            "format_name": format_payload.get("format_name", "unknown"),
            "duration": format_payload.get("duration", "unknown"),
        },
        "claim_boundary": {
            "ffprobe_style_metadata_ingested": True,
            "mp4_boxes_parsed_directly": False,
            "local_validation_only": True,
        },
    }


def _load_payload(
    input_path: Path,
    *,
    use_external_tool: bool,
) -> tuple[dict[str, Any] | None, list[dict[str, str]], bool, bool]:
    tool_available = shutil.which("ffprobe") is not None
    external_verification_performed = False
    if input_path.suffix.lower() == ".json":
        if not input_path.exists():
            return (
                None,
                [
                    _issue(
                        "ffmpeg_probe_json_not_found",
                        "source.input_path",
                        "ffprobe JSON not found.",
                    )
                ],
                tool_available,
                external_verification_performed,
            )
        try:
            return _read_json(input_path), [], tool_available, external_verification_performed
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            return (
                None,
                [
                    _issue(
                        "ffmpeg_probe_parse_error",
                        "source.input_path",
                        f"could not parse ffprobe JSON: {exc}",
                    )
                ],
                tool_available,
                external_verification_performed,
            )

    if not use_external_tool:
        return (
            None,
            [
                _issue(
                    "ffmpeg_probe_parse_error",
                    "source.input_path",
                    "non-JSON input requires --use-external-tool.",
                )
            ],
            tool_available,
            external_verification_performed,
        )
    if not tool_available:
        return (
            None,
            [_issue("ffmpeg_tool_not_available", "source.input_path", "ffprobe is not available.")],
            tool_available,
            external_verification_performed,
        )

    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            "-show_frames",
            str(input_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    external_verification_performed = result.returncode == 0
    if result.returncode != 0:
        return (
            None,
            [
                _issue(
                    "ffmpeg_probe_parse_error",
                    "source.input_path",
                    result.stderr.strip() or "ffprobe failed.",
                )
            ],
            tool_available,
            external_verification_performed,
        )
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return (
            None,
            [
                _issue(
                    "ffmpeg_probe_parse_error",
                    "source.input_path",
                    f"ffprobe returned invalid JSON: {exc}",
                )
            ],
            tool_available,
            external_verification_performed,
        )
    if not isinstance(payload, dict):
        return (
            None,
            [
                _issue(
                    "ffmpeg_probe_parse_error",
                    "source.input_path",
                    "ffprobe output must be a JSON object.",
                )
            ],
            tool_available,
            external_verification_performed,
        )
    return payload, [], tool_available, external_verification_performed


def ingest_ffmpeg_prft(
    input_path: str | Path,
    out_path: str | Path,
    use_external_tool: bool = False,
) -> dict[str, Any]:
    resolved_input = Path(input_path)
    resolved_output = Path(out_path)
    payload, issues, tool_available, external_verification_performed = _load_payload(
        resolved_input,
        use_external_tool=use_external_tool,
    )
    if payload is None:
        return _adapter_report(
            input_path=resolved_input,
            out_path=resolved_output,
            ok=False,
            issues=issues,
            tool_available=tool_available,
            external_verification_performed=external_verification_performed,
        )

    metadata = parse_ffprobe_prft_json(payload)
    if external_verification_performed:
        metadata["source"]["kind"] = "ffprobe_external_probe"
        metadata["claim_boundary"]["local_validation_only"] = False
    write_issue: list[dict[str, str]] = []
    try:
        _write_json(resolved_output, metadata)
    except OSError as exc:
        write_issue = [
            _issue(
                "ffmpeg_timing_metadata_write_failed",
                "normalized_output.path",
                f"could not write metadata: {exc}",
            )
        ]

    if not metadata["timing"]["prft_detected"]:
        issues.append(
            _issue(
                "ffmpeg_prft_not_found",
                "normalized_output.timing.prft_detected",
                "PRFT marker was not found.",
            )
        )
    issues.extend(write_issue)
    return _adapter_report(
        input_path=resolved_input,
        out_path=resolved_output,
        ok=not issues,
        issues=issues,
        tool_available=tool_available,
        external_verification_performed=external_verification_performed,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Ingest ffprobe-style PRFT timing metadata.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--use-external-tool", action="store_true")
    args = parser.parse_args(argv)

    report = ingest_ffmpeg_prft(args.input, args.out, use_external_tool=args.use_external_tool)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
