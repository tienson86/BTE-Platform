"""Acceptance tests for Knowledge Graph Builder V2."""

from __future__ import annotations

from pathlib import Path

from graph.builder import GraphBuilder, build_all_graphs
from graph.constants import EXPORT_FORMATS, GRAPH_TYPES
from graph.graph_exporter import GraphExporter
from graph.graph_optimizer import GraphOptimizer
from graph.io_utils import read_json, sha256_file
from graph.models import GraphEdge, GraphNode, KnowledgeGraph
from graph.traversal import bfs, dfs, reachable
from graph.validator import GraphValidator


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_graph_modules_exist() -> None:
    """Required Graph Builder V2 modules exist."""
    root = _root()
    for name in (
        "builder.py",
        "node_builder.py",
        "edge_builder.py",
        "graph_optimizer.py",
        "graph_exporter.py",
        "graph_cache.py",
    ):
        assert (root / "graph" / name).is_file(), name


def test_build_five_graph_types_all_formats() -> None:
    """Five graph types are generated in all supported formats."""
    root = _root()
    summary = build_all_graphs(project_root=root, timestamp="2026-08-01T00:00:00Z")
    assert summary["status"] == "GRAPH_BUILDER_READY"
    assert summary["validation_ok"] is True
    out = root / "knowledge" / "graph" / "generated" / "v2"
    for graph_type in GRAPH_TYPES:
        for fmt in EXPORT_FORMATS:
            path = out / f"{graph_type}.{fmt}"
            assert path.is_file(), path.name
            assert path.stat().st_size > 0
    for name in (
        "graph_statistics.json",
        "graph_inventory.json",
        "graph_manifest.json",
    ):
        assert (out / name).is_file()


def test_exporter_formats() -> None:
    """Exporter produces GraphML, DOT, JSON, Mermaid, JSON-LD."""
    graph = KnowledgeGraph(
        graph_id="GRAPH-TEST-000001",
        graph_type="test_graph",
        title="Test",
        nodes=[GraphNode("A", "Concept", "Alpha"), GraphNode("B", "Concept", "Beta")],
        edges=[GraphEdge("E1", "A", "B", "DEPENDS_ON")],
        timestamp="2026-08-01T00:00:00Z",
    )
    exports = GraphExporter().export_all(graph)
    assert "@context" in exports["jsonld"]
    assert "<graphml" in exports["graphml"]
    assert "digraph" in exports["dot"]
    assert "flowchart" in exports["mmd"]
    assert '"graph_id"' in exports["json"]


def test_traversal_bfs_dfs() -> None:
    """Traversal helpers walk the graph deterministically."""
    root = _root()
    builder = GraphBuilder(project_root=root, timestamp="2026-08-01T00:00:00Z")
    graph = builder.optimizer.optimize(builder.build_dependency_graph())
    order = bfs(graph, "KR-000001")
    assert order[0] == "KR-000001"
    dfs_order = dfs(graph, "KR-000001")
    assert dfs_order[0] == "KR-000001"
    # KR-000002 depends on KR-000001, so from KR-000002 we can reach KR-000001.
    assert "KR-000001" in reachable(graph, "KR-000002")


def test_optimization_removes_duplicates() -> None:
    """Optimizer removes duplicate nodes/edges."""
    graph = KnowledgeGraph(
        graph_id="GRAPH-OPT-000001",
        graph_type="test",
        title="opt",
        nodes=[
            GraphNode("A", "Concept", "A"),
            GraphNode("A", "Concept", "A-dup"),
            GraphNode("B", "Concept", "B"),
        ],
        edges=[
            GraphEdge("E1", "A", "B", "DEPENDS_ON"),
            GraphEdge("E1", "A", "B", "DEPENDS_ON"),
            GraphEdge("E2", "A", "B", "DEPENDS_ON"),
        ],
    )
    optimized = GraphOptimizer().optimize(graph)
    assert len(optimized.nodes) == 2
    assert len(optimized.edges) == 1


def test_validation_passes_for_built_graphs() -> None:
    """Validation passes for all built graph types."""
    root = _root()
    builder = GraphBuilder(project_root=root, timestamp="2026-08-01T00:00:00Z")
    validator = GraphValidator()
    for build_fn in (
        builder.build_academic_graph,
        builder.build_ontology_graph,
        builder.build_dependency_graph,
        builder.build_registry_graph,
        builder.build_runtime_graph,
    ):
        graph = builder.optimizer.optimize(build_fn())
        result = validator.validate(graph)
        assert result.ok, result.findings


def test_exports_deterministic() -> None:
    """Rebuild yields identical checksums for JSON exports."""
    root = _root()
    out = root / "knowledge" / "graph" / "generated" / "v2"
    build_all_graphs(project_root=root, timestamp="2026-08-01T00:00:00Z")
    first = {
        name: sha256_file(out / f"{name}.json") for name in GRAPH_TYPES
    }
    build_all_graphs(project_root=root, timestamp="2026-08-01T00:00:00Z")
    second = {
        name: sha256_file(out / f"{name}.json") for name in GRAPH_TYPES
    }
    assert first == second


def test_cli_build() -> None:
    """CLI python -m graph build succeeds."""
    from graph.__main__ import main

    root = _root()
    assert main(["--project-root", str(root), "build"]) == 0


def test_manifest_and_statistics() -> None:
    """Manifest/statistics/inventory exist and reference five graphs."""
    root = _root()
    out = root / "knowledge" / "graph" / "generated" / "v2"
    stats = read_json(out / "graph_statistics.json")
    inventory = read_json(out / "graph_inventory.json")
    manifest = read_json(out / "graph_manifest.json")
    assert stats["graph_count"] == 5
    assert set(inventory["graph_types"]) == set(GRAPH_TYPES)
    assert manifest["compiler_ready"] is True
    assert set(manifest["graph_types"]) == set(GRAPH_TYPES)
