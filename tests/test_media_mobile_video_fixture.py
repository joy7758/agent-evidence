from pathlib import Path

from agent_evidence.media_bundle import build_media_bundle, verify_media_bundle
from agent_evidence.media_profile import validate_media_profile_file

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "examples" / "media" / "use_cases" / "mobile_video_network_timing"
VALID_STATEMENT = FIXTURE_DIR / "mobile-video-operation-evidence.json"
INVALID_DIR = FIXTURE_DIR / "invalid"


def issue_codes(report: dict[str, object]) -> set[str]:
    codes = {issue["code"] for issue in report.get("issues", [])}  # type: ignore[index]
    time_report = report.get("time_profile_report")
    if isinstance(time_report, dict):
        codes.update(issue["code"] for issue in time_report.get("issues", []))
    return codes


def test_mobile_video_fixture_profile_validation_passes() -> None:
    report = validate_media_profile_file(VALID_STATEMENT)

    assert report["ok"] is True
    assert report["issue_count"] == 0


def test_mobile_video_fixture_build_and_verify_passes(tmp_path: Path) -> None:
    bundle_dir = tmp_path / "mobile-video-bundle"

    summary = build_media_bundle(VALID_STATEMENT, bundle_dir)
    report = verify_media_bundle(bundle_dir)

    assert summary["ok"] is True
    assert report["ok"] is True
    assert report["bundle_checksum_ok"] is True
    assert report["media_profile_ok"] is True


def test_mobile_video_fixture_strict_time_verify_passes(tmp_path: Path) -> None:
    bundle_dir = tmp_path / "mobile-video-strict-time-bundle"

    build_media_bundle(VALID_STATEMENT, bundle_dir)
    report = verify_media_bundle(bundle_dir, strict_time=True)

    assert report["ok"] is True
    assert report["strict_time"] is True
    assert report["time_profile_ok"] is True


def test_mobile_video_broken_hash_reports_media_hash_mismatch() -> None:
    report = validate_media_profile_file(INVALID_DIR / "invalid-mobile-video-broken-hash.json")

    assert report["ok"] is False
    assert "media_hash_mismatch" in issue_codes(report)


def test_mobile_video_missing_clock_trace_ref_reports_expected_code(tmp_path: Path) -> None:
    bundle_dir = tmp_path / "mobile-video-missing-clock-bundle"
    statement_path = INVALID_DIR / "invalid-mobile-video-missing-timing-ref.json"

    build_media_bundle(statement_path, bundle_dir)
    report = verify_media_bundle(bundle_dir, strict_time=True)

    assert report["ok"] is False
    assert "missing_clock_trace_ref" in issue_codes(report)


def test_mobile_video_unresolved_actor_ref_reports_expected_code() -> None:
    report = validate_media_profile_file(
        INVALID_DIR / "invalid-mobile-video-unresolved-provenance-ref.json"
    )

    assert report["ok"] is False
    assert "unresolved_actor_ref" in issue_codes(report)
