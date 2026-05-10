#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from hashlib import sha256
from pathlib import Path

DEMO_ROOT = Path(__file__).resolve().parent
REPO_ROOT = DEMO_ROOT.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agent_evidence.media_profile import PROFILE_LABEL, validate_media_profile_file  # noqa: E402

OUTPUT_DIR = DEMO_ROOT / "output" / "media_evidence_demo"


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def create_subject() -> dict[str, str]:
    return {
        "id": "subject:demo-media-scene-runtime",
        "type": "media-observed-event",
        "label": "runtime generated declared demo scene",
    }


def profile_precheck(subject: dict[str, str]) -> list[str]:
    issues: list[str] = []
    for field in ("id", "type", "label"):
        if not subject.get(field):
            issues.append(f"missing subject field: {field}")
    return issues


def write_demo_artifacts() -> tuple[Path, Path]:
    media_path = OUTPUT_DIR / "demo-media.bin"
    manifest_path = OUTPUT_DIR / "c2pa-manifest-placeholder.json"

    media_path.write_bytes(
        b"AEP-Media runtime demo payload\nframe_count=1\ndeclared_time=2026-04-26T08:10:00Z\n"
    )
    write_json(
        manifest_path,
        {
            "placeholder": True,
            "profile": PROFILE_LABEL,
            "note": "Runtime demo placeholder; not a real C2PA signature.",
        },
    )
    return media_path, manifest_path


def build_statement(
    subject: dict[str, str],
    media_path: Path,
    manifest_path: Path,
) -> dict[str, object]:
    return {
        "profile": {
            "name": "aep-media-evidence-profile",
            "version": "0.1",
        },
        "statement_id": "aep-media:statement:runtime-demo-001",
        "timestamp": "2026-04-26T08:10:05Z",
        "actor": {
            "id": "actor:runtime-demo-media-agent",
            "type": "agent",
            "label": "runtime demo media evidence agent",
        },
        "subject": subject,
        "operation": {
            "id": "operation:runtime-media-capture-demo-001",
            "type": "media.capture.declared_demo",
            "subject_ref": subject["id"],
            "policy_ref": "policy:runtime-media-hash-and-time-v0",
            "media_refs": [
                "media:runtime-demo-primary",
                "media:runtime-demo-c2pa-placeholder",
            ],
            "evidence_refs": [
                "evidence:runtime-media-capture-demo-001",
            ],
            "status": "succeeded",
        },
        "policy": {
            "id": "policy:runtime-media-hash-and-time-v0",
            "label": "runtime demo hash and declared time context required",
            "constraint_refs": [
                "constraint:runtime-media-hash-required",
                "constraint:runtime-time-context-required",
                "constraint:runtime-manifest-reference-closed",
            ],
        },
        "constraints": [
            {
                "id": "constraint:runtime-media-hash-required",
                "type": "media_hash",
                "rule": "Every local media artifact must include a recomputable sha256 digest.",
            },
            {
                "id": "constraint:runtime-time-context-required",
                "type": "time_context",
                "rule": "Primary media must resolve to the declared statement time context.",
            },
            {
                "id": "constraint:runtime-manifest-reference-closed",
                "type": "manifest_reference",
                "rule": "Declared manifest references must resolve to media artifacts.",
            },
        ],
        "time_context": {
            "id": "time:runtime-declared-demo-001",
            "source": "declared_demo",
            "sync_status": "declared",
            "start_utc": "2026-04-26T08:10:00Z",
            "end_utc": "2026-04-26T08:10:03Z",
            "clock_trace_refs": [],
        },
        "media": {
            "artifacts": [
                {
                    "id": "media:runtime-demo-primary",
                    "role": "primary_media",
                    "path": media_path.name,
                    "sha256": file_sha256(media_path),
                    "mime_type": "application/octet-stream",
                    "size_bytes": media_path.stat().st_size,
                    "time_context_ref": "time:runtime-declared-demo-001",
                    "container": "demo-binary",
                    "timing": {
                        "prft_declared": False,
                        "timecode_declared": False,
                    },
                },
                {
                    "id": "media:runtime-demo-c2pa-placeholder",
                    "role": "sidecar_manifest",
                    "path": manifest_path.name,
                    "sha256": file_sha256(manifest_path),
                    "mime_type": "application/json",
                    "size_bytes": manifest_path.stat().st_size,
                    "time_context_ref": "time:runtime-declared-demo-001",
                    "container": "json",
                    "timing": {
                        "prft_declared": False,
                        "timecode_declared": False,
                    },
                },
            ]
        },
        "provenance": {
            "id": "provenance:runtime-media-capture-demo-001",
            "actor_ref": "actor:runtime-demo-media-agent",
            "subject_ref": subject["id"],
            "operation_ref": "operation:runtime-media-capture-demo-001",
            "media_refs": [
                "media:runtime-demo-primary",
                "media:runtime-demo-c2pa-placeholder",
            ],
            "c2pa_manifest_ref": "media:runtime-demo-c2pa-placeholder",
            "claim_generator": "agent-evidence runtime demo placeholder",
        },
        "evidence": {
            "id": "evidence:runtime-media-capture-demo-001",
            "policy_refs": [
                "policy:runtime-media-hash-and-time-v0",
            ],
            "artifact_refs": [
                "media:runtime-demo-primary",
                "media:runtime-demo-c2pa-placeholder",
            ],
            "notes": (
                "Runtime declared demo-level media evidence object. It does not verify a "
                "real C2PA signature, MP4 PRFT box, or PTP clock trace."
            ),
        },
        "validation": {
            "method": "schema+reference+media-hash+declared-time",
            "validator": "agent-evidence validate-media-profile",
            "required_checks": [
                "schema_conformance",
                "reference_closure",
                "media_hash_recomputation",
                "time_context_completeness",
                "provenance_manifest_reference",
            ],
            "expected_result": "pass",
        },
    }


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Step 1: object load or creation")
    subject = create_subject()
    print(f"- created {subject['id']}")

    print("Step 2: profile check")
    precheck_issues = profile_precheck(subject)
    if precheck_issues:
        for issue in precheck_issues:
            print(f"- {issue}")
        return 1
    print("- subject is ready for AEP-Media v0.1")

    print("Step 3: operation call")
    media_path, manifest_path = write_demo_artifacts()
    print(f"- wrote {media_path.name}")
    print(f"- wrote {manifest_path.name}")

    print("Step 4: evidence generation")
    statement = build_statement(subject, media_path, manifest_path)
    statement_path = OUTPUT_DIR / "media-evidence.json"
    write_json(statement_path, statement)
    print(f"- wrote {statement_path.name}")

    print("Step 5: validator verification")
    report = validate_media_profile_file(statement_path)
    report_path = OUTPUT_DIR / "validation-report.json"
    write_json(report_path, report)
    print(f"- {report['summary']}")

    print("Step 6: output verification result")
    print(f"- evidence: {statement_path}")
    print(f"- report:   {report_path}")
    if report["ok"]:
        print(f"PASS {PROFILE_LABEL} demo")
        return 0
    print(f"FAIL {PROFILE_LABEL} demo")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
