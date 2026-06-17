from __future__ import annotations

import re
from pathlib import Path

USES_RE = re.compile(r"^\s*uses:\s*([^#\s]+)", re.MULTILINE)
PINNED_REF_RE = re.compile(r"^[^@\s]+@[0-9a-fA-F]{40}$")


def _is_local_action(value: str) -> bool:
    return value.startswith("./") or value.startswith("../")


def unpinned_actions(root: Path) -> list[tuple[Path, str]]:
    workflow_root = root / ".github" / "workflows"
    findings: list[tuple[Path, str]] = []
    for path in sorted(workflow_root.glob("*.yml")) + sorted(workflow_root.glob("*.yaml")):
        text = path.read_text(encoding="utf-8")
        for match in USES_RE.finditer(text):
            value = match.group(1)
            if _is_local_action(value):
                continue
            if not PINNED_REF_RE.match(value):
                findings.append((path, value))
    return findings


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    findings = unpinned_actions(root)
    if findings:
        for path, value in findings:
            print(f"{path.relative_to(root)}: unpinned action {value}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
