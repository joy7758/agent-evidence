import json
import subprocess
import sys
from pathlib import Path

from agent_evidence.media_profile import validate_media_profile_file

ROOT = Path(__file__).resolve().parents[1]
MEDIA_EXAMPLES = ROOT / "examples" / "media"
DEMO_SCRIPT = ROOT / "demo" / "run_media_evidence_demo.py"
DEMO_OUTPUT = ROOT / "demo" / "output" / "media_evidence_demo"


def issue_codes(report: dict[str, object]) -> set[str]:
    return {issue["code"] for issue in report["issues"]}  # type: ignore[index]


def test_valid_media_profile_passes() -> None:
    report = validate_media_profile_file(MEDIA_EXAMPLES / "minimal-valid-media-evidence.json")

    assert report["ok"] is True
    assert report["issue_count"] == 0


def test_missing_time_context_fails() -> None:
    report = validate_media_profile_file(MEDIA_EXAMPLES / "invalid-missing-time-context.json")

    assert report["ok"] is False
    assert "missing_time_context" in issue_codes(report)


def test_broken_media_hash_fails() -> None:
    report = validate_media_profile_file(MEDIA_EXAMPLES / "invalid-broken-media-hash.json")

    assert report["ok"] is False
    assert "media_hash_mismatch" in issue_codes(report)


def test_unresolved_policy_ref_fails() -> None:
    report = validate_media_profile_file(MEDIA_EXAMPLES / "invalid-unresolved-policy-ref.json")

    assert report["ok"] is False
    assert "unresolved_policy_ref" in issue_codes(report)


def test_media_demo_runs() -> None:
    result = subprocess.run(
        [sys.executable, str(DEMO_SCRIPT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    evidence_path = DEMO_OUTPUT / "media-evidence.json"
    report_path = DEMO_OUTPUT / "validation-report.json"
    assert evidence_path.exists()
    assert report_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["ok"] is True
