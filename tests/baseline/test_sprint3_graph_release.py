"""Sprint 3 graph and release artifact acceptance tests."""

from __future__ import annotations

from pathlib import Path

from baseline.baseline_builder import BaselineBuilder, build_baseline
from baseline.constants import PACK01_KR_INVENTORY
from baseline.io_utils import read_json, sha256_file
from baseline.paths import resolve_project_root


def test_knowledge_graph_formats_generated() -> None:
    """TASK 11: all knowledge graph export formats exist."""
    root = resolve_project_root()
    build_baseline(project_root=root, version="1.0.0")
    version_dir = root / "knowledge" / "baseline" / "v1.0.0"
    generated = root / "knowledge" / "graph" / "generated"
    for name in (
        "knowledge_graph.json",
        "knowledge_graph.graphml",
        "knowledge_graph.dot",
        "knowledge_graph.mmd",
    ):
        assert (version_dir / name).is_file(), name
        assert (generated / name).is_file(), name

    graph = read_json(version_dir / "knowledge_graph.json")
    assert graph["statistics"]["node_count"] > 0
    assert graph["statistics"]["edge_count"] > 0
    assert "dependencies" in graph
    assert "relationships" in graph
    assert "contexts" in graph
    assert "mappings" in graph
    graphml = (version_dir / "knowledge_graph.graphml").read_text(encoding="utf-8")
    assert "<graphml" in graphml
    assert "digraph" in (version_dir / "knowledge_graph.dot").read_text(
        encoding="utf-8"
    )
    assert "flowchart" in (version_dir / "knowledge_graph.mmd").read_text(
        encoding="utf-8"
    )


def test_graph_validation_report() -> None:
    """TASK 12: graph validation covers cycles/disconnected/duplicates/integrity."""
    root = resolve_project_root()
    report = read_json(
        root / "knowledge" / "baseline" / "v1.0.0" / "graph_validation_report.json"
    )
    assert report["status"] == "PASS"
    assert report["error_count"] == 0
    assert report["statistics"]["cycle_count"] == 0
    assert report["statistics"]["orphan_count"] == 0
    checks = set(report["metadata"]["checks"])
    assert checks == {
        "cycles",
        "disconnected_nodes",
        "duplicate_edges",
        "relationship_integrity",
    }


def test_release_reports_generated() -> None:
    """TASK 13: build/validation/release/freeze reports exist."""
    root = resolve_project_root()
    version_dir = root / "knowledge" / "baseline" / "v1.0.0"
    for name in (
        "build_report.md",
        "validation_report.md",
        "release_candidate.md",
        "freeze_readiness.md",
    ):
        path = version_dir / name
        assert path.is_file(), name
        text = path.read_text(encoding="utf-8")
        assert text.strip()


def test_checksums_cover_kr_registries_snapshots_reports() -> None:
    """TASK 14: checksums include KR, registries, snapshots, and reports."""
    root = resolve_project_root()
    checksums = read_json(
        root / "knowledge" / "baseline" / "v1.0.0" / "checksums.json"
    )
    assert checksums["algorithm"] == "SHA256"
    files = checksums["files"]
    categories = checksums["categories"]
    assert categories["knowledge_records"]["count"] == 15
    assert categories["registries"]["count"] >= 8
    assert categories["snapshots"]["count"] >= 1
    assert categories["reports"]["count"] >= 1
    for entry in PACK01_KR_INVENTORY:
        rel = (
            "knowledge/bazi/01_fundamental_knowledge/records/"
            f"{entry['filename']}"
        )
        assert rel in files
        assert files[rel] == sha256_file(root / rel)


def test_statistics_sprint3_fields() -> None:
    """TASK 15: statistics includes inventory and nested domain stats."""
    root = resolve_project_root()
    stats = read_json(root / "knowledge" / "baseline" / "v1.0.0" / "statistics.json")
    assert stats["knowledge_records"] == 15
    assert stats["registry_count"] == 8
    assert stats["ontology_count"] >= 1
    assert stats["relationship_count"] >= 1
    assert stats["rule_count"] >= 1
    assert "context_count" in stats
    assert "compiler_statistics" in stats
    assert "validation_statistics" in stats
    assert "graph_statistics" in stats
    assert stats["graph_statistics"]["node_count"] > 0
    assert stats["graph_statistics"]["edge_count"] > 0


def test_checksums_deterministic_across_rebuild() -> None:
    """Acceptance: rebuild yields identical KR checksums."""
    root = resolve_project_root()
    first = BaselineBuilder(
        project_root=root,
        version="1.0.0",
        timestamp="2026-08-01T00:00:00Z",
    ).build()
    checksums_path = root / "knowledge" / "baseline" / "v1.0.0" / "checksums.json"
    first_files = read_json(checksums_path)["files"]
    second = BaselineBuilder(
        project_root=root,
        version="1.0.0",
        timestamp="2026-08-01T00:00:00Z",
    ).build()
    second_files = read_json(checksums_path)["files"]
    for entry in PACK01_KR_INVENTORY:
        rel = (
            "knowledge/bazi/01_fundamental_knowledge/records/"
            f"{entry['filename']}"
        )
        assert first_files[rel] == second_files[rel]
    assert first["statistics"]["graph_nodes"] == second["statistics"]["graph_nodes"]


def test_no_kr_modification_after_sprint3_build() -> None:
    """Acceptance: Sprint 3 build does not modify KR documents."""
    root = resolve_project_root()
    kr_dir = root / "knowledge" / "bazi" / "01_fundamental_knowledge" / "records"
    before = {p.name: sha256_file(p) for p in sorted(kr_dir.glob("KR-*.md"))}
    build_baseline(project_root=root, version="1.0.0")
    after = {p.name: sha256_file(p) for p in sorted(kr_dir.glob("KR-*.md"))}
    assert before == after
