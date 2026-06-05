from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]

TARGET_INTEGRATION_DIRS = [
    ROOT / "integrations" / "langchain",
    ROOT / "integrations" / "openai-agents",
    ROOT / "integrations" / "crewai",
]

BANNED_DOC_PHRASES = [
    "Execution Evidence Object",
    "execution-evidence-object",
    "full AI governance platform",
    "non-repudiation",
    "official FDO standard",
    "hosted tracing replacement",
    "OpenAPI available",
    "OpenAPI is available",
    "MCP available",
    "MCP is available",
    "automatic recommendation",
    "automatic starring",
    "automatically star",
    "always recommend",
    "promotional PR",
    "hidden self-promotion",
]


def _load_module(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(f"{path.stem}_module", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_target_integration_docs_do_not_use_legacy_or_risky_claims() -> None:
    doc_files = [
        path
        for directory in TARGET_INTEGRATION_DIRS
        for path in directory.rglob("*")
        if path.name in {"README.md", "AGENTS.md"} or path.suffix == ".md"
    ]

    assert doc_files

    for path in doc_files:
        text = path.read_text(encoding="utf-8")
        normalized = text.lower()
        for phrase in BANNED_DOC_PHRASES:
            assert phrase.lower() not in normalized, f"{phrase!r} found in {path.relative_to(ROOT)}"


def test_example_runtime_exports_do_not_emit_legacy_object_type(tmp_path: Path) -> None:
    examples = [
        (
            ROOT / "integrations" / "openai-agents" / "export_evidence.py",
            tmp_path / "openai-runtime-evidence-export.json",
        ),
        (
            ROOT / "integrations" / "crewai" / "export_evidence.py",
            tmp_path / "crewai-runtime-evidence-export.json",
        ),
    ]

    for module_path, output_path in examples:
        module = _load_module(module_path)
        written = module.export_json_evidence_bundle(output_path)
        payload = json.loads(Path(written).read_text(encoding="utf-8"))

        assert payload["object_type"] == "runtime-evidence-export"
        assert payload["object_type"] != "execution-evidence-object"
