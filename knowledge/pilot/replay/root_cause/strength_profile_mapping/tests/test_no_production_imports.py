"""Ensure reference mapper does not import production Strength runtime modules."""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPPER_DIR = ROOT / "reference_mapper"

FORBIDDEN_PREFIXES = (
    "engines.strength_engine",
    "engines.score_engine",
    "applications.",
    "pipelines.",
)


def test_no_production_strength_imports() -> None:
    for path in MAPPER_DIR.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    for prefix in FORBIDDEN_PREFIXES:
                        assert not alias.name.startswith(prefix), f"{path.name}: {alias.name}"
            elif isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                for prefix in FORBIDDEN_PREFIXES:
                    assert not mod.startswith(prefix), f"{path.name}: {mod}"


def test_mapper_package_is_under_pilot_path() -> None:
    parts = ROOT.parts
    assert "knowledge" in parts
    assert "pilot" in parts
    assert "strength_profile_mapping" in parts
    assert "engines" not in parts[-3:]
