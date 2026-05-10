# ruff: noqa: E501
from __future__ import annotations

import json
import shutil
from hashlib import sha256
from pathlib import Path
from typing import Any

from agent_evidence.media_evaluation import run_media_evaluation

RELEASE_PROFILE = "aep-media-release-pack@0.1"
GENERATED_UTC = "2026-04-26T00:00:00Z"
FORBIDDEN_WORKSPACE_LABEL = "paper-ncs-" + "execution-evidence"

TEXT_SUFFIXES = {".csv", ".json", ".md", ".txt"}
COPY_SUFFIXES = {".bin", ".csv", ".json", ".log", ".md", ".py", ".txt"}


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def _sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as file_obj:
        for chunk in iter(lambda: file_obj.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.name


def _sanitize_text(text: str, *, repo_root: Path, out_dir: Path) -> str:
    replacements = {
        str(repo_root.resolve()): ".",
        str(out_dir.resolve()): "<release-pack>",
        str(Path.home()): "<home>",
        str(Path("/", "Users", "zhangbin")): "<home>",
        FORBIDDEN_WORKSPACE_LABEL: "unrelated paper workspace",
    }
    sanitized = text
    for old, new in replacements.items():
        sanitized = sanitized.replace(old, new)
    return sanitized


def _sanitize_text_files(out_dir: Path, repo_root: Path) -> None:
    for path in out_dir.rglob("*"):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        path.write_text(
            _sanitize_text(text, repo_root=repo_root, out_dir=out_dir), encoding="utf-8"
        )


def _copy_file(source: Path, target: Path, *, repo_root: Path, out_dir: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.suffix in TEXT_SUFFIXES or source.suffix == ".py":
        text = source.read_text(encoding="utf-8")
        target.write_text(
            _sanitize_text(text, repo_root=repo_root, out_dir=out_dir), encoding="utf-8"
        )
    else:
        shutil.copyfile(source, target)


def _copy_tree_filtered(source: Path, target: Path, *, repo_root: Path, out_dir: Path) -> None:
    if not source.exists():
        return
    if target.exists():
        shutil.rmtree(target)
    for path in sorted(source.rglob("*")):
        if not path.is_file() or path.suffix not in COPY_SUFFIXES:
            continue
        parts = set(path.relative_to(source).parts)
        if parts.intersection({".git", ".venv", "__pycache__", "output"}):
            continue
        rel_path = path.relative_to(source)
        _copy_file(path, target / rel_path, repo_root=repo_root, out_dir=out_dir)


def _copy_selected_artifacts(out_dir: Path, repo_root: Path) -> None:
    copied = out_dir / "copied-artifacts"
    for spec_path in sorted((repo_root / "spec").glob("aep-media*.md")):
        _copy_file(
            spec_path, copied / "spec" / spec_path.name, repo_root=repo_root, out_dir=out_dir
        )
    for schema_path in sorted((repo_root / "schema").glob("aep_media*.schema.json")):
        _copy_file(
            schema_path,
            copied / "schema" / schema_path.name,
            repo_root=repo_root,
            out_dir=out_dir,
        )
    _copy_tree_filtered(
        repo_root / "examples" / "media",
        copied / "examples" / "media",
        repo_root=repo_root,
        out_dir=out_dir,
    )
    demo_target = copied / "demo"
    for demo_name in [
        "run_media_evidence_demo.py",
        "run_media_bundle_demo.py",
        "run_media_time_demo.py",
        "run_media_evaluation_demo.py",
        "run_media_adapter_demo.py",
        "build_aep_media_release_pack.py",
    ]:
        demo_path = repo_root / "demo" / demo_name
        if demo_path.exists():
            _copy_file(demo_path, demo_target / demo_name, repo_root=repo_root, out_dir=out_dir)
    reports_target = copied / "docs-reports"
    for report_path in sorted((repo_root / "docs" / "reports").glob("aep_media_*.md")):
        _copy_file(
            report_path,
            reports_target / report_path.name,
            repo_root=repo_root,
            out_dir=out_dir,
        )


def _inventory_entry(path: str, category: str, repo_root: Path) -> dict[str, Any]:
    full_path = repo_root / path
    exists = full_path.exists()
    return {
        "path": path,
        "category": category,
        "exists": exists,
        "sha256": _sha256_file(full_path) if exists and full_path.is_file() else None,
        "size_bytes": full_path.stat().st_size if exists and full_path.is_file() else None,
    }


def _artifact_inventory(repo_root: Path) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    fixed_paths = {
        "profiles/specs": [
            "spec/aep-media-profile-v0.1.md",
            "spec/aep-media-bundle-v0.1.md",
            "spec/aep-media-time-trace-v0.1.md",
            "spec/aep-media-adapters-v0.1.md",
        ],
        "schemas": [
            "schema/aep_media_profile_v0_1.schema.json",
            "schema/aep_media_bundle_v0_1.schema.json",
            "schema/aep_media_time_trace_v0_1.schema.json",
            "schema/aep_media_adapter_report_v0_1.schema.json",
        ],
        "validators": [
            "agent_evidence/media_profile.py",
            "agent_evidence/media_bundle.py",
            "agent_evidence/media_time.py",
            "agent_evidence/media_evaluation.py",
            "agent_evidence/media_optional_tools.py",
            "agent_evidence/media_release_pack.py",
        ],
        "adapters": [
            "agent_evidence/adapters/linuxptp.py",
            "agent_evidence/adapters/ffmpeg_prft.py",
            "agent_evidence/adapters/c2pa_manifest.py",
            "agent_evidence/media_adapter_evaluation.py",
        ],
        "demos": [
            "demo/run_media_evidence_demo.py",
            "demo/run_media_bundle_demo.py",
            "demo/run_media_time_demo.py",
            "demo/run_media_evaluation_demo.py",
            "demo/run_media_adapter_demo.py",
            "demo/build_aep_media_release_pack.py",
        ],
        "tests": [
            "tests/test_media_profile.py",
            "tests/test_media_bundle.py",
            "tests/test_media_time.py",
            "tests/test_media_evaluation.py",
            "tests/test_media_adapters.py",
            "tests/test_media_release_pack.py",
        ],
        "reports": [
            "docs/reports/aep_media_mission002_report.md",
            "docs/reports/aep_media_mission003_report.md",
            "docs/reports/aep_media_mission004_report.md",
            "docs/reports/aep_media_mission005_report.md",
            "docs/reports/aep_media_mission006_report.md",
            "docs/reports/aep_media_mission007_report.md",
            "docs/reports/aep_media_final_claim_boundary.md",
            "docs/reports/aep_media_final_reproducibility_checklist.md",
            "docs/reports/aep_media_final_artifact_inventory.md",
            "docs/reports/aep_media_final_evaluation_summary.md",
        ],
        "paper scaffold": [
            "docs/paper/aep_media_manuscript_draft.md",
            "docs/paper/aep_media_abstract.md",
            "docs/paper/aep_media_methods_section.md",
            "docs/paper/aep_media_evaluation_section.md",
            "docs/paper/aep_media_threats_to_validity.md",
            "docs/paper/aep_media_related_work_notes.md",
        ],
    }
    for category, paths in fixed_paths.items():
        items.extend(_inventory_entry(path, category, repo_root) for path in paths)
    for path in sorted((repo_root / "examples" / "media").rglob("*")):
        if path.is_file():
            rel_path = path.relative_to(repo_root).as_posix()
            category = (
                "fixtures" if "fixtures" in path.parts or "adapters" in path.parts else "examples"
            )
            items.append(_inventory_entry(rel_path, category, repo_root))
    return {
        "profile": "aep-media-artifact-inventory@0.1",
        "generated_utc": GENERATED_UTC,
        "item_count": len(items),
        "items": items,
    }


def _claim_boundary_markdown() -> str:
    rows = [
        (
            "Media evidence profile",
            "implemented and validated with controlled pass/fail examples",
            "complete media forensics or legal evidence sufficiency",
            "profile examples and default evaluation cases",
        ),
        (
            "Offline media bundle",
            "build and verify path implemented with tamper cases",
            "custody-chain legal proof or trusted archival infrastructure",
            "bundle evaluation and tamper reports",
        ),
        (
            "Strict time trace",
            "declared/synthetic or ingested trace validation",
            "hardware clock discipline proof or trusted timestamping",
            "strict-time examples and time tamper matrix",
        ),
        (
            "LinuxPTP adapter",
            "linuxptp-style fixture ingestion and optional tool detection",
            "real PTP synchronization proof in current environment",
            "adapter fixtures and optional tool report",
        ),
        (
            "FFmpeg PRFT adapter",
            "ffprobe-style PRFT fixture ingestion and optional ffprobe path",
            "full MP4 box parser or proven PRFT presence without tool output",
            "adapter fixtures and optional tool report",
        ),
        (
            "C2PA adapter",
            "C2PA-like manifest fixture ingestion and optional CLI detection",
            "real C2PA signature verification unless external CLI actually runs and reports it",
            "adapter fixtures and optional tool report",
        ),
        (
            "Optional external tools",
            "missing tools are detected and skipped without breaking reproducibility",
            "external verification performed when tools are unavailable",
            "optional-tool evaluation summary",
        ),
        (
            "Evaluation pack",
            "default, adapter, optional-tool evidence matrices generated",
            "production deployment or broad generality",
            "evaluation summary and release pack",
        ),
        (
            "Legal / regulatory status",
            "local research artifact",
            "legal admissibility, regulatory approval, or non-repudiation",
            "claim boundary and non-claims matrix",
        ),
    ]
    lines = [
        "# AEP-Media Final Claim Boundary",
        "",
        "Claim surface | Current status | Not claimed | Evidence source",
        "--- | --- | --- | ---",
    ]
    lines.extend(
        f"{surface} | {status} | {not_claimed} | {source}"
        for surface, status, not_claimed, source in rows
    )
    return "\n".join(lines) + "\n"


def _non_claims_markdown() -> str:
    return """# AEP-Media v0.1 Non-claims

This release is a local research artifact. It does not claim legal admissibility, non-repudiation, trusted timestamping, production deployment, or broad forensic coverage.

- No legal admissibility: local declared-demo validation cannot establish legal sufficiency.
- No non-repudiation: v0.1 does not include an external identity trust fabric or required signing chain.
- No trusted timestamping: strict time validation checks declared, synthetic, or ingested trace artifacts only.
- No real PTP proof in the current environment: optional LinuxPTP tools are detected when present, but missing tools are skipped.
- No full MP4 PRFT parser: FFmpeg PRFT support is fixture-style ingestion plus optional ffprobe probing.
- No real C2PA signature verification unless the optional external CLI actually runs and reports it.
- No production deployment: examples and demos remain bounded research fixtures.
- No broad forensic claim: the artifact validates structure, references, hashes, bundles, and declared time trace checks.
"""


def _reproducibility_markdown() -> str:
    return """# AEP-Media Final Reproducibility Checklist

## 1. Environment

Use the repository virtual environment when available. The fixture-only path does not require LinuxPTP, FFmpeg, ffprobe, or C2PA CLI.

## 2. Install

Install the project dependencies in the repository virtual environment if they are not already present.

## 3. Run Core Tests

```bash
./.venv/bin/python -m pytest tests/test_media_profile.py tests/test_media_bundle.py tests/test_media_time.py tests/test_media_evaluation.py tests/test_media_adapters.py -q

./.venv/bin/python -m pytest -q
```

## 4. Run Default Evaluation

```bash
./.venv/bin/agent-evidence run-media-evaluation --out /tmp/aep-media-evaluation-default
```

## 5. Run Adapter Evaluation

```bash
./.venv/bin/agent-evidence run-media-evaluation --out /tmp/aep-media-evaluation-with-adapters --include-adapters
```

## 6. Run Optional-tool Evaluation

```bash
./.venv/bin/agent-evidence run-media-evaluation --out /tmp/aep-media-evaluation-with-tools --include-optional-tools
```

## 7. Build Release Pack

```bash
./.venv/bin/agent-evidence build-aep-media-release-pack --out /tmp/aep-media-release-pack

./.venv/bin/python demo/build_aep_media_release_pack.py
```

## 8. Expected Outputs

- Default evaluation: 18 cases, unexpected=0.
- Adapter evaluation: at least 26 cases, unexpected=0.
- Optional-tool evaluation: at least 23 cases, unexpected=0; missing external tools are skipped.
- Release pack: `release-summary.json`, `claim-boundary.md`, `artifact-inventory.json`, `checksums.sha256`, and paper scaffold.

## 9. Troubleshooting

- If bare python lacks pytest, use `.venv`.
- If `agent-evidence` is not in PATH, use `./.venv/bin/agent-evidence`.
- If ffmpeg, ffprobe, c2pa, or LinuxPTP tools do not exist, optional tools are skipped and fixture-only reproducibility is unaffected.
- On macOS, do not directly run ptp4l or phc2sys clock discipline commands unless there is a clear Linux PTP environment and an explicit run window.
"""


def _paper_files(repo_root: Path) -> dict[str, str]:
    paper_dir = repo_root / "docs" / "paper"
    names = [
        "aep_media_manuscript_draft.md",
        "aep_media_abstract.md",
        "aep_media_methods_section.md",
        "aep_media_evaluation_section.md",
        "aep_media_threats_to_validity.md",
    ]
    files: dict[str, str] = {}
    for name in names:
        path = paper_dir / name
        if path.exists():
            files[name] = path.read_text(encoding="utf-8")
    return files


def _release_summary_markdown(summary: dict[str, Any]) -> str:
    evaluation = summary["evaluation"]
    return f"""# AEP-Media v0.1 Release Summary

Status: `{summary["summary"]}`

## Mission Status

- Mission 001 media profile: {summary["missions"]["mission001_media_profile"]}
- Mission 002 bundle: {summary["missions"]["mission002_bundle"]}
- Mission 003 strict time: {summary["missions"]["mission003_strict_time"]}
- Mission 004 evaluation pack: {summary["missions"]["mission004_evaluation_pack"]}
- Mission 005 adapters: {summary["missions"]["mission005_adapters"]}
- Mission 006 optional tools: {summary["missions"]["mission006_optional_tools"]}

## Evaluation

- Default evaluation cases: {evaluation["default_cases"]}
- Adapter-inclusive evaluation cases: {evaluation["adapter_cases"]}
- Optional-tool evaluation cases: {evaluation["optional_tool_cases"]}
- Combined adapter + optional-tool evaluation: {evaluation["combined_adapter_optional_evaluation"]}
- Unexpected cases: {evaluation["unexpected"]}

## Interpretation

Mission 006 proves the optional external-tool path, tool-missing handling, reporting mechanism, and fixture-only reproducible path. It does not prove real PTP synchronization, real FFmpeg PRFT parsing results, or real C2PA signature verification.
"""


def _checksums(out_dir: Path) -> None:
    checksum_path = out_dir / "checksums.sha256"
    entries: list[tuple[str, str]] = []
    for path in sorted(out_dir.rglob("*")):
        if not path.is_file() or path == checksum_path:
            continue
        entries.append((_sha256_file(path), path.relative_to(out_dir).as_posix()))
    checksum_path.write_text(
        "".join(f"{digest}  {relative_path}\n" for digest, relative_path in entries),
        encoding="utf-8",
    )


def _optional_tool_summary(optional_eval_dir: Path) -> dict[str, Any]:
    summary_path = optional_eval_dir / "optional-tool-evaluation" / "optional-tool-summary.json"
    if summary_path.exists():
        return _read_json(summary_path)
    return {
        "profile": "aep-media-optional-tool-evaluation@0.1",
        "ok": False,
        "case_count": 0,
        "available_count": 0,
        "skipped_count": 0,
        "failed_count": 1,
        "external_verification_performed": False,
        "summary": "FAIL optional tool summary missing",
    }


def _external_verification_performed(tool_summary: dict[str, Any]) -> bool:
    for case in tool_summary.get("cases", []):
        if isinstance(case, dict) and case.get("external_verification_performed"):
            return True
    claim_boundary = tool_summary.get("claim_boundary")
    return bool(
        isinstance(claim_boundary, dict) and claim_boundary.get("external_verification_performed")
    )


def _copy_paper_files(out_dir: Path, repo_root: Path) -> None:
    paper_target = out_dir / "paper"
    for name, text in _paper_files(repo_root).items():
        _write_text(
            paper_target / name,
            _sanitize_text(text, repo_root=repo_root, out_dir=out_dir),
        )


def build_aep_media_release_pack(
    out_dir: str | Path,
    repo_root: str | Path | None = None,
) -> dict[str, Any]:
    resolved_repo_root = (
        Path(repo_root).resolve() if repo_root is not None else Path(__file__).resolve().parents[1]
    )
    resolved_out_dir = Path(out_dir).resolve()
    if resolved_out_dir.exists():
        shutil.rmtree(resolved_out_dir)
    resolved_out_dir.mkdir(parents=True, exist_ok=True)

    evaluation_dir = resolved_out_dir / "evaluation"
    default_eval = run_media_evaluation(
        evaluation_dir / "default-18",
        repo_root=resolved_repo_root,
    )
    adapter_eval = run_media_evaluation(
        evaluation_dir / "with-adapters-26",
        repo_root=resolved_repo_root,
        include_adapters=True,
    )
    optional_eval = run_media_evaluation(
        evaluation_dir / "optional-tools-23",
        repo_root=resolved_repo_root,
        include_optional_tools=True,
    )
    combined_status: int | str = "not_supported_in_v0.1"
    combined_unexpected = 0
    combined_ok = True
    try:
        combined_eval = run_media_evaluation(
            evaluation_dir / "with-adapters-and-optional-tools",
            repo_root=resolved_repo_root,
            include_adapters=True,
            include_optional_tools=True,
        )
    except TypeError:
        combined_eval = None
    if combined_eval is not None:
        combined_status = int(combined_eval.get("case_count", 0))
        combined_unexpected = int(combined_eval.get("unexpected_count", 1))
        combined_ok = bool(combined_eval.get("ok")) and combined_unexpected == 0

    tool_summary = _optional_tool_summary(evaluation_dir / "optional-tools-23")
    external_performed = _external_verification_performed(tool_summary)
    default_ok = (
        bool(default_eval.get("ok"))
        and int(default_eval.get("case_count", 0)) == 18
        and int(default_eval.get("unexpected_count", 1)) == 0
    )
    adapter_ok = (
        bool(adapter_eval.get("ok"))
        and int(adapter_eval.get("case_count", 0)) >= 26
        and int(adapter_eval.get("unexpected_count", 1)) == 0
    )
    optional_ok = (
        bool(optional_eval.get("ok"))
        and int(optional_eval.get("case_count", 0)) >= 23
        and int(optional_eval.get("unexpected_count", 1)) == 0
        and int(tool_summary.get("failed_count", 1)) == 0
    )
    unexpected_total = (
        int(default_eval.get("unexpected_count", 0))
        + int(adapter_eval.get("unexpected_count", 0))
        + int(optional_eval.get("unexpected_count", 0))
        + combined_unexpected
    )
    ok = default_ok and adapter_ok and optional_ok and combined_ok

    summary = {
        "profile": RELEASE_PROFILE,
        "generated_utc": GENERATED_UTC,
        "ok": ok,
        "missions": {
            "mission001_media_profile": "completed",
            "mission002_bundle": "completed",
            "mission003_strict_time": "completed",
            "mission004_evaluation_pack": "completed",
            "mission005_adapters": "completed",
            "mission006_optional_tools": "completed_optional_path",
        },
        "evaluation": {
            "default_cases": int(default_eval.get("case_count", 0)),
            "adapter_cases": int(adapter_eval.get("case_count", 0)),
            "optional_tool_cases": int(optional_eval.get("case_count", 0)),
            "combined_adapter_optional_evaluation": combined_status,
            "unexpected": unexpected_total,
        },
        "external_tools": {
            "available_count": int(tool_summary.get("available_count", 0)),
            "skipped_count": int(tool_summary.get("skipped_count", 0)),
            "failed_count": int(tool_summary.get("failed_count", 0)),
            "external_verification_performed": external_performed,
        },
        "claim_boundary": {
            "local_validation": True,
            "fixture_ingestion": True,
            "optional_external_tool_detection": True,
            "real_ptp_proof": False,
            "real_ffmpeg_prft_proof": False,
            "real_c2pa_signature_proof": False,
            "legal_admissibility": False,
            "non_repudiation": False,
        },
        "summary": f"{'PASS' if ok else 'FAIL'} {RELEASE_PROFILE}",
    }

    _write_json(resolved_out_dir / "release-summary.json", summary)
    _write_text(resolved_out_dir / "release-summary.md", _release_summary_markdown(summary))
    _write_text(resolved_out_dir / "claim-boundary.md", _claim_boundary_markdown())
    _write_text(resolved_out_dir / "non-claims.md", _non_claims_markdown())
    _write_text(resolved_out_dir / "reproducibility-checklist.md", _reproducibility_markdown())
    _write_json(
        resolved_out_dir / "artifact-inventory.json", _artifact_inventory(resolved_repo_root)
    )
    _write_json(resolved_out_dir / "tool-availability.json", tool_summary)
    _copy_paper_files(resolved_out_dir, resolved_repo_root)
    _copy_selected_artifacts(resolved_out_dir, resolved_repo_root)

    _sanitize_text_files(resolved_out_dir, resolved_repo_root)
    _checksums(resolved_out_dir)
    return summary


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Build the AEP-Media v0.1 release pack.")
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args(argv)
    summary = build_aep_media_release_pack(args.out)
    print(summary["summary"])
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
