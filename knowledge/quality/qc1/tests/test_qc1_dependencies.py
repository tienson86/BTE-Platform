"""QC-1 dependency tests. Read-only."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
PACKAGES = REPO / "knowledge" / "packages"
REPORTS = Path(__file__).resolve().parents[1] / "reports"


def _load_deps() -> dict[str, dict]:
    mapping = {}
    for path in PACKAGES.glob("**/DEPENDENCIES.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        mapping[data["package_id"]] = data
    return mapping


def _cycles(edges: dict[str, list[str]]) -> list[list[str]]:
    cycles: list[list[str]] = []
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []

    def dfs(node: str) -> None:
        visiting.add(node)
        stack.append(node)
        for nxt in edges.get(node, []):
            if nxt in visiting:
                cycles.append(stack[stack.index(nxt) :] + [nxt])
            elif nxt not in visited:
                dfs(nxt)
        stack.pop()
        visiting.remove(node)
        visited.add(node)

    for node in list(edges):
        if node not in visited:
            dfs(node)
    return cycles


def test_no_required_dependencies() -> None:
    for package_id, data in _load_deps().items():
        assert data.get("required") == [], package_id


def test_no_dependency_cycles() -> None:
    deps = _load_deps()
    ids = set(deps)
    edges: dict[str, list[str]] = defaultdict(list)
    for package_id, data in deps.items():
        for item in data.get("optional") or []:
            target = item["package_id"]
            assert target in ids, f"{package_id} -> {target}"
            edges[package_id].append(target)
    assert _cycles(dict(edges)) == []


def test_dependency_report_matches_scan() -> None:
    report = json.loads((REPORTS / "dependency_graph.json").read_text(encoding="utf-8"))
    assert report["cycles"] == []
    assert report["independently_deployable"] is True
    assert report["unknown_dependencies"] == []
