from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from hashlib import sha256
from pathlib import Path
from typing import Any

ADAPTER_NAME = "c2pa_manifest"
ADAPTER_VERSION = "0.1"
ADAPTER_LABEL = "aep-media-c2pa-manifest-adapter@0.1"
REPORT_PROFILE = {
    "name": "aep-media-adapter-ingestion-report",
    "version": "0.1",
}
SIGNATURE_STATUSES = {
    "declared_valid",
    "declared_invalid",
    "absent",
    "externally_verified_valid",
    "externally_verified_invalid",
    "not_checked",
}


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("C2PA-like manifest must be a JSON object")
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
        "kind": "aep-media-c2pa-manifest-metadata",
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
            "kind": "c2pa_like_manifest",
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


def _manifest_payload(payload: dict[str, Any]) -> dict[str, Any]:
    manifest = payload.get("manifest")
    return manifest if isinstance(manifest, dict) else payload


def parse_c2pa_like_manifest(payload: dict[str, Any]) -> dict[str, Any]:
    manifest = _manifest_payload(payload)
    signature_status = manifest.get("signature_status", "not_checked")
    if signature_status not in SIGNATURE_STATUSES:
        signature_status = "not_checked"
    ingredients = manifest.get("ingredients", payload.get("ingredients", []))
    assertions = manifest.get("assertions", payload.get("assertions", []))
    return {
        "profile": {
            "name": "aep-media-c2pa-manifest-metadata",
            "version": "0.1",
        },
        "manifest": {
            "manifest_id": manifest.get("manifest_id", "unknown"),
            "claim_generator": manifest.get("claim_generator", "unknown"),
            "signature_status": signature_status,
            "external_verification_performed": False,
        },
        "ingredients": ingredients if isinstance(ingredients, list) else [],
        "assertions": assertions if isinstance(assertions, list) else [],
        "claim_boundary": {
            "c2pa_like_manifest_ingested": True,
            "real_signature_verified": False,
            "local_validation_only": True,
        },
    }


def _external_tool_status(
    input_path: Path,
    use_external_tool: bool,
) -> tuple[bool, bool, bool | None, list[dict[str, str]]]:
    tool_available = shutil.which("c2pa") is not None
    if not use_external_tool:
        return tool_available, False, None, []
    if not tool_available:
        return (
            tool_available,
            False,
            None,
            [_issue("c2pa_tool_not_available", "source.input_path", "c2pa CLI is not available.")],
        )

    result = subprocess.run(
        ["c2pa", "verify", "--manifest", str(input_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return tool_available, True, True, []

    message = (result.stderr or result.stdout).strip() or "c2pa verify failed."
    return (
        tool_available,
        True,
        False,
        [_issue("c2pa_external_verification_failed", "source.input_path", message)],
    )


def ingest_c2pa_manifest(
    input_path: str | Path,
    out_path: str | Path,
    use_external_tool: bool = False,
) -> dict[str, Any]:
    resolved_input = Path(input_path)
    resolved_output = Path(out_path)
    tool_available, external_verification_performed, external_signature_ok, issues = (
        _external_tool_status(resolved_input, use_external_tool)
    )
    if not resolved_input.exists():
        issues.append(
            _issue("c2pa_manifest_not_found", "source.input_path", "C2PA-like manifest not found.")
        )
        return _adapter_report(
            input_path=resolved_input,
            out_path=resolved_output,
            ok=False,
            issues=issues,
            tool_available=tool_available,
            external_verification_performed=external_verification_performed,
        )

    try:
        payload = _read_json(resolved_input)
        metadata = parse_c2pa_like_manifest(payload)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        issues.append(
            _issue(
                "c2pa_manifest_parse_error", "source.input_path", f"could not parse manifest: {exc}"
            )
        )
        return _adapter_report(
            input_path=resolved_input,
            out_path=resolved_output,
            ok=False,
            issues=issues,
            tool_available=tool_available,
            external_verification_performed=external_verification_performed,
        )

    if external_signature_ok is True:
        metadata["manifest"]["signature_status"] = "externally_verified_valid"
        metadata["manifest"]["external_verification_performed"] = True
        metadata["claim_boundary"]["real_signature_verified"] = True
        metadata["claim_boundary"]["local_validation_only"] = False
    elif external_signature_ok is False:
        metadata["manifest"]["signature_status"] = "externally_verified_invalid"
        metadata["manifest"]["external_verification_performed"] = True
        metadata["claim_boundary"]["real_signature_verified"] = False
        metadata["claim_boundary"]["local_validation_only"] = False

    if metadata["manifest"]["signature_status"] == "declared_invalid":
        issues.append(
            _issue(
                "c2pa_signature_invalid_declared",
                "manifest.signature_status",
                "fixture declares an invalid C2PA-like signature status.",
            )
        )

    try:
        _write_json(resolved_output, metadata)
    except OSError as exc:
        issues.append(
            _issue(
                "c2pa_metadata_write_failed",
                "normalized_output.path",
                f"could not write metadata: {exc}",
            )
        )

    return _adapter_report(
        input_path=resolved_input,
        out_path=resolved_output,
        ok=not issues,
        issues=issues,
        tool_available=tool_available,
        external_verification_performed=external_verification_performed,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Ingest C2PA-like manifest metadata.")
    parser.add_argument("input_manifest_json", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--use-external-tool", action="store_true")
    args = parser.parse_args(argv)

    report = ingest_c2pa_manifest(
        args.input_manifest_json,
        args.out,
        use_external_tool=args.use_external_tool,
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
