"""No production imports in design package."""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = ("engines.strength_engine", "engines.score_engine", "applications.", "pipelines.")


def test_no_engine_imports_in_package_python() -> None:
    for path in ROOT.rglob("*.py"):
        if path.name == "build_design_package.py" or "tests" in path.parts:
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        for prefix in FORBIDDEN:
                            assert not alias.name.startswith(prefix)
                elif isinstance(node, ast.ImportFrom):
                    mod = node.module or ""
                    for prefix in FORBIDDEN:
                        assert not mod.startswith(prefix)
            continue
        # no other production python modules expected
        if path.parent == ROOT:
            assert path.name in {"build_design_package.py"}


def test_package_path_is_pilot_only() -> None:
    assert "strength_engine_output_contract" in ROOT.parts
    assert "engines" not in ROOT.parts
