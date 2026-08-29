"""Shadow-mode tests for Narrative V2 runtime skeleton (N-IMP-01).

Narrative V2 must never replace Pack05. Portal stays on Pack05.
"""

from __future__ import annotations

import ast
from pathlib import Path

from engines.narrative_v2.runtime import SHADOW_MODE, NarrativeRuntime

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_DIR = PROJECT_ROOT / "engines" / "narrative_v2" / "runtime"
NARRATIVE_V2_DIR = PROJECT_ROOT / "engines" / "narrative_v2"


def _python_files(root: Path) -> list[Path]:
    return sorted(root.rglob("*.py"))


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def test_shadow_mode_is_enabled() -> None:
    assert SHADOW_MODE is True
    runtime = NarrativeRuntime()
    assert runtime.SHADOW_MODE is True
    assert runtime.shadow_mode is True
    assert runtime.replaces_pack05 is False
    assert runtime.portal_connected is False


def test_runtime_metadata_declares_shadow_mode() -> None:
    result = NarrativeRuntime().run({"source": "canonical_analysis_placeholder"})
    assert result.runtime_metadata["shadow_mode"] is True
    assert result.runtime_metadata["replaces_pack05"] is False
    assert result.runtime_metadata["portal_connected"] is False
    assert result.presentation is None


def test_narrative_v2_does_not_import_pack05() -> None:
    forbidden = (
        "engines.narrative_engine",
        "applications.customer_portal",
        "applications.api",
    )
    for path in _python_files(NARRATIVE_V2_DIR):
        imported = _imported_modules(path)
        for name in forbidden:
            assert not any(
                item == name or item.startswith(name + ".")
                for item in imported
            ), f"{path} imports {name}"


def test_no_builder_implementation_files() -> None:
    names = {path.name for path in RUNTIME_DIR.glob("*.py")}
    forbidden = {
        "evidence_builder.py",
        "reasoning_builder.py",
        "knowledge_resolver.py",
        "commercial_rewrite.py",
        "summary_builder.py",
        "interpretation_builder.py",
        "action_builder.py",
        "commercial_builder.py",
    }
    assert forbidden.isdisjoint(names)


def test_production_api_still_uses_pack05() -> None:
    truth = (
        PROJECT_ROOT
        / "applications"
        / "api"
        / "services"
        / "narrative_result_truth.py"
    ).read_text(encoding="utf-8")
    assert "engines.narrative_engine" in truth
    assert "NarrativeEngine" in truth
    assert "engines.narrative_v2" not in truth


def test_portal_adapter_still_reads_pack05_contract() -> None:
    adapter = (
        PROJECT_ROOT
        / "applications"
        / "customer_portal"
        / "src"
        / "adapters"
        / "narrativeResultAdapter.ts"
    ).read_text(encoding="utf-8")
    assert "pack05_narrative_result_v1" in adapter
    assert "narrative_v2" not in adapter
