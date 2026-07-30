"""Unit tests for Knowledge indexes and CLI."""

from __future__ import annotations

from pathlib import Path

import knowledge_cli
import pytest

from services.knowledge.dependency_index import DependencyIndex
from services.knowledge.exceptions import KnowledgeQueryError
from services.knowledge.knowledge_index import KnowledgeIndex
from services.knowledge.knowledge_loader import KnowledgeLoader
from services.knowledge.relationship_index import RelationshipIndex
from services.knowledge.search_index import SearchIndex


def test_indexes(loader: KnowledgeLoader) -> None:
    records = loader.load_records()
    kidx = KnowledgeIndex().build(records)
    assert kidx.get("KNO-000001") is not None
    assert "KNO-000001" in kidx.list_ids(domain_dir="01_five_elements")
    deps = DependencyIndex().build(records)
    assert "KNO-000001" in deps.dependencies_of("KNO-000002")
    assert "KNO-000002" in deps.dependents_of("KNO-000001")
    rel = RelationshipIndex().build(records)
    assert rel.edges_for("KNO-000001")
    hits = SearchIndex().build(records).search("Wood")
    assert hits and hits[0].knowledge_id == "KNO-000001"
    with pytest.raises(KnowledgeQueryError):
        SearchIndex().build(records).search("  ")


def test_cli_validate_stats_list_search(
    project_root: Path,
    canon_root: Path,
    schema_root: Path,
) -> None:
    common = [
        "--project-root",
        str(project_root),
        "--canon-root",
        str(canon_root),
        "--schema-root",
        str(schema_root),
    ]
    assert knowledge_cli.main([*common, "validate"]) == 0
    assert knowledge_cli.main([*common, "stats"]) == 0
    assert knowledge_cli.main([*common, "list", "--domain", "01_five_elements"]) == 0
    assert knowledge_cli.main([*common, "search", "Fire"]) == 0


def test_cli_graph_export(
    project_root: Path,
    canon_root: Path,
    schema_root: Path,
    tmp_path: Path,
) -> None:
    common = [
        "--project-root",
        str(project_root),
        "--canon-root",
        str(canon_root),
        "--schema-root",
        str(schema_root),
    ]
    assert (
        knowledge_cli.main(
            [
                *common,
                "graph",
                "--include-relationships",
                "--knowledge-id",
                "KNO-000001",
            ]
        )
        == 0
    )
    out = tmp_path / "bundle.json"
    assert knowledge_cli.main([*common, "export", "--output", str(out)]) == 0
    assert out.exists()


def test_cli_real_scaffold(project_root: Path) -> None:
    assert (
        knowledge_cli.main(
            ["--project-root", str(project_root), "validate"]
        )
        == 0
    )
