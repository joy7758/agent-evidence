from __future__ import annotations

import csv
import io
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

OPTIONAL_TOOL_PROFILE = "aep-media-optional-tool-evaluation@0.1"


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _tool_case(tool: str, args: list[str], *, case_id: str, note: str) -> dict[str, Any]:
    executable = shutil.which(tool)
    command = [tool, *args]
    if executable is None:
        return {
            "case_id": case_id,
            "category": "optional_tool_integration",
            "input": " ".join(command),
            "expected": "optional",
            "observed_ok": True,
            "matched_expectation": True,
            "primary_codes": ["optional_tool_not_available"],
            "issue_count": 1,
            "report_path": f"optional-tool-reports/{case_id}.json",
            "status": "skipped",
            "tool": tool,
            "tool_path": None,
            "external_verification_performed": False,
            "issues": [
                {
                    "code": "optional_tool_not_available",
                    "message": f"{tool} is not installed or not in PATH.",
                    "path": "tool",
                }
            ],
            "note": note,
        }

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {
            "case_id": case_id,
            "category": "optional_tool_integration",
            "input": " ".join(command),
            "expected": "optional",
            "observed_ok": False,
            "matched_expectation": True,
            "primary_codes": ["optional_tool_probe_failed"],
            "issue_count": 1,
            "report_path": f"optional-tool-reports/{case_id}.json",
            "status": "failed",
            "tool": tool,
            "tool_path": executable,
            "external_verification_performed": False,
            "issues": [
                {
                    "code": "optional_tool_probe_failed",
                    "message": f"{tool} version probe failed: {exc}",
                    "path": "tool",
                }
            ],
            "note": note,
        }

    output = (result.stdout or result.stderr).strip().splitlines()
    version_excerpt = output[0] if output else ""
    ok = result.returncode == 0
    return {
        "case_id": case_id,
        "category": "optional_tool_integration",
        "input": " ".join(command),
        "expected": "optional",
        "observed_ok": ok,
        "matched_expectation": True,
        "primary_codes": [] if ok else ["optional_tool_probe_failed"],
        "issue_count": 0 if ok else 1,
        "report_path": f"optional-tool-reports/{case_id}.json",
        "status": "available" if ok else "failed",
        "tool": tool,
        "tool_path": executable,
        "external_verification_performed": False,
        "version_excerpt": version_excerpt,
        "issues": []
        if ok
        else [
            {
                "code": "optional_tool_probe_failed",
                "message": f"{tool} version command returned {result.returncode}.",
                "path": "tool",
            }
        ],
        "note": note,
    }


def _write_csv(path: Path, cases: list[dict[str, Any]]) -> None:
    fieldnames = [
        "case_id",
        "category",
        "input",
        "expected",
        "observed_ok",
        "matched_expectation",
        "primary_codes",
        "issue_count",
        "report_path",
        "status",
    ]
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for case in cases:
        row = dict(case)
        row["primary_codes"] = "|".join(case.get("primary_codes", []))
        writer.writerow({field: row.get(field, "") for field in fieldnames})
    path.write_text(output.getvalue(), encoding="utf-8")


def _write_md(path: Path, cases: list[dict[str, Any]]) -> None:
    lines = [
        "# AEP-Media Optional Tool Evaluation v0.1",
        "",
        "These checks only probe optional external tool availability. Missing tools are "
        "recorded as skipped, not as failures of the reproducible fixture path.",
        "",
        "case_id | tool | status | primary codes",
        "--- | --- | --- | ---",
    ]
    for case in cases:
        lines.append(
            f"{case['case_id']} | {case['tool']} | {case['status']} | "
            f"{', '.join(case.get('primary_codes', []))}"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_optional_tool_evaluation(out_dir: str | Path) -> dict[str, Any]:
    resolved_out_dir = Path(out_dir).resolve()
    resolved_out_dir.mkdir(parents=True, exist_ok=True)
    reports_dir = resolved_out_dir / "optional-tool-reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    cases = [
        _tool_case(
            "ptp4l",
            ["-v"],
            case_id="optional_linuxptp_ptp4l_version",
            note="Version probe only. Real ptp4l clock discipline is not started automatically.",
        ),
        _tool_case(
            "phc2sys",
            ["-v"],
            case_id="optional_linuxptp_phc2sys_version",
            note="Version probe only. phc2sys can affect clocks and is not started automatically.",
        ),
        _tool_case(
            "ffmpeg",
            ["-version"],
            case_id="optional_ffmpeg_version",
            note="Version probe only. Real media probing requires a user-supplied media file.",
        ),
        _tool_case(
            "ffprobe",
            ["-version"],
            case_id="optional_ffprobe_version",
            note="Version probe only. The adapter can call ffprobe when a media file is supplied.",
        ),
        _tool_case(
            "c2pa",
            ["--version"],
            case_id="optional_c2pa_version",
            note="Version probe only. Signature verification requires a real C2PA manifest.",
        ),
    ]

    for case in cases:
        _write_json(reports_dir / f"{case['case_id']}.json", case)

    skipped = sum(1 for case in cases if case["status"] == "skipped")
    failed = sum(1 for case in cases if case["status"] == "failed")
    available = sum(1 for case in cases if case["status"] == "available")
    summary = {
        "profile": OPTIONAL_TOOL_PROFILE,
        "ok": True,
        "case_count": len(cases),
        "available_count": available,
        "skipped_count": skipped,
        "failed_count": failed,
        "unexpected_count": 0,
        "cases": cases,
        "claim_boundary": {
            "optional_external_tool_probe": True,
            "external_verification_performed": False,
            "fixture_path_required": False,
        },
        "summary": (
            f"PASS {OPTIONAL_TOOL_PROFILE} available={available} skipped={skipped} failed={failed}"
        ),
    }
    _write_json(resolved_out_dir / "optional-tool-summary.json", summary)
    _write_json(
        resolved_out_dir / "optional-tool-matrix.json",
        {
            "profile": OPTIONAL_TOOL_PROFILE,
            "case_count": len(cases),
            "cases": cases,
        },
    )
    _write_md(resolved_out_dir / "optional-tool-matrix.md", cases)
    _write_csv(resolved_out_dir / "optional-tool-matrix.csv", cases)
    return summary
