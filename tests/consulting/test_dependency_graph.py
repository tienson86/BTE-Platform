"""Dependency graph tests. Architecture only. No business assertions."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MARRIAGE_ROOT = ROOT / "consulting" / "marriage"
FORBIDDEN_CANONICAL_IMPORTS = (
    "engines.calendar_engine",
    "engines.bazi_engine",
    "engines.strength_engine",
    "engines.pattern_engine",
    "engines.useful_god_engine",
    "engines.decision_engine",
    "engines.score_engine",
    "engines.report_engine",
    "engines.narrative_engine",
    "engines.narrative_v2",
    "knowledge.consulting",
)

# Higher layers must not be imported by lower layers.
FORBIDDEN_INTERNAL_EDGES: dict[str, tuple[str, ...]] = {
    "models": (
        "dto",
        "adapters",
        "repository",
        "policy",
        "evidence",
        "finding",
        "decision",
        "recommendation",
        "report",
        "presentation",
        "api",
        "ui",
        "validation",
        "runtime",
        "orchestrator",
        "contracts",
    ),
    "dto": (
        "adapters",
        "repository",
        "policy",
        "evidence",
        "finding",
        "decision",
        "recommendation",
        "report",
        "presentation",
        "api",
        "ui",
        "validation",
        "runtime",
        "orchestrator",
        "contracts",
    ),
    "evidence": (
        "finding",
        "decision",
        "recommendation",
        "report",
        "presentation",
        "api",
        "ui",
        "orchestrator",
    ),
    "finding": (
        "decision",
        "recommendation",
        "report",
        "presentation",
        "api",
        "ui",
        "orchestrator",
    ),
    "decision": (
        "recommendation",
        "report",
        "presentation",
        "api",
        "ui",
        "orchestrator",
    ),
    "recommendation": (
        "report",
        "presentation",
        "api",
        "ui",
        "orchestrator",
    ),
    "report": ("presentation", "api", "ui", "orchestrator"),
    "presentation": ("api", "ui", "orchestrator"),
    "policy": ("recommendation", "report", "presentation", "api", "ui", "orchestrator"),
}


def _iter_python_files(root: Path) -> list[Path]:
    """Return Python files under root."""
    return [path for path in root.rglob("*.py") if path.is_file()]


def _module_name(path: Path) -> str:
    """Return dotted module name relative to the repo root."""
    relative = path.relative_to(ROOT).with_suffix("")
    return ".".join(relative.parts)


def _layer_of(module_name: str) -> str | None:
    """Return the TV-01 layer name for a marriage module."""
    prefix = "consulting.marriage."
    if not module_name.startswith(prefix):
        if module_name == "consulting.marriage":
            return "root"
        return None
    remainder = module_name[len(prefix) :]
    return remainder.split(".", 1)[0]


def _imported_modules(path: Path) -> list[str]:
    """Return absolute and relative import targets from a file."""
    source = path.read_text(encoding="utf-8-sig")
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError:
        return []
    current = _module_name(path)
    imported: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                parent_parts = current.split(".")
                package_parts = parent_parts[: len(parent_parts) - node.level]
                if node.module:
                    imported.append(".".join([*package_parts, node.module]))
                else:
                    imported.append(".".join(package_parts))
            elif node.module:
                imported.append(node.module)
    return imported


def _marriage_import_graph() -> dict[str, set[str]]:
    """Build consulting.marriage module import graph."""
    graph: dict[str, set[str]] = {}
    for path in _iter_python_files(MARRIAGE_ROOT):
        source = _module_name(path)
        graph.setdefault(source, set())
        for target in _imported_modules(path):
            if target == "consulting.marriage" or target.startswith("consulting.marriage."):
                graph[source].add(target)
    return graph


def _cycles(graph: dict[str, set[str]]) -> list[list[str]]:
    """Return cycles in a directed graph."""
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []
    found: list[list[str]] = []

    def dfs(node: str) -> None:
        if node in visited:
            return
        if node in visiting:
            cycle_start = stack.index(node)
            found.append([*stack[cycle_start:], node])
            return
        visiting.add(node)
        stack.append(node)
        for nxt in graph.get(node, set()):
            dfs(nxt)
        stack.pop()
        visiting.remove(node)
        visited.add(node)

    for start in graph:
        dfs(start)
    return found


def test_no_circular_imports_inside_marriage() -> None:
    """TV-01 modules must not form an import cycle."""
    cycles = _cycles(_marriage_import_graph())
    assert cycles == []


def test_internal_layers_are_one_way() -> None:
    """Lower layers must not import higher TV-01 layers."""
    violations: list[str] = []
    for path in _iter_python_files(MARRIAGE_ROOT):
        source_layer = _layer_of(_module_name(path))
        forbidden = FORBIDDEN_INTERNAL_EDGES.get(source_layer or "", ())
        if not forbidden:
            continue
        for target in _imported_modules(path):
            target_layer = _layer_of(target)
            if target_layer in forbidden:
                violations.append(f"{_module_name(path)} -> {target}")
    assert violations == []


def test_marriage_does_not_import_canonical_engines() -> None:
    """TV-01 skeleton must not import Canonical or Decision engines."""
    violations: list[str] = []
    for path in _iter_python_files(MARRIAGE_ROOT):
        for target in _imported_modules(path):
            if any(
                target == prefix or target.startswith(prefix + ".")
                for prefix in FORBIDDEN_CANONICAL_IMPORTS
            ):
                violations.append(f"{_module_name(path)} -> {target}")
    assert violations == []


@pytest.mark.parametrize(
    "scan_root",
    (
        ROOT / "engines",
        ROOT / "runtime",
        ROOT / "applications",
        ROOT / "api",
        ROOT / "services",
    ),
)
def test_canonical_and_apps_do_not_import_tv01(scan_root: Path) -> None:
    """Canonical Runtime and existing apps must not reference TV-01."""
    if not scan_root.exists():
        pytest.skip(f"{scan_root} is not present")
    violations: list[str] = []
    for path in _iter_python_files(scan_root):
        for target in _imported_modules(path):
            if target == "consulting.marriage" or target.startswith("consulting.marriage."):
                violations.append(f"{_module_name(path)} -> {target}")
    assert violations == []
