"""Acceptance tests for Knowledge Search Engine (Sprint 7)."""

from __future__ import annotations

import time
from pathlib import Path

from knowledge.search.constants import PERFORMANCE_BUDGET_MS
from knowledge.search.models import read_json, sha256_file
from knowledge.search.search_engine import SearchEngine, build_search_index


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_search_modules_exist() -> None:
    """Required search modules exist under knowledge/search/."""
    root = _root()
    for name in (
        "search_engine.py",
        "entity_search.py",
        "relationship_search.py",
        "rule_search.py",
        "context_search.py",
        "registry_search.py",
    ):
        assert (root / "knowledge" / "search" / name).is_file(), name


def test_build_generates_index_and_statistics() -> None:
    """Generate search_index.json and search_statistics.json."""
    root = _root()
    summary = build_search_index(project_root=root, timestamp="2026-08-01T00:00:00Z")
    assert summary["status"] == "SEARCH_READY"
    assert summary["document_count"] > 0
    search_dir = root / "knowledge" / "search"
    assert (search_dir / "search_index.json").is_file()
    assert (search_dir / "search_statistics.json").is_file()
    stats = read_json(search_dir / "search_statistics.json")
    assert stats["document_count"] == summary["document_count"]
    assert "exact" in stats["supported_modes"]


def test_search_correctness_modes() -> None:
    """Exact/prefix/fuzzy/ontology/dependency/relationship searches work."""
    root = _root()
    engine = SearchEngine(project_root=root, timestamp="2026-08-01T00:00:00Z")
    engine.build_index()

    exact = engine.exact("KR-000001")
    assert exact.total >= 1
    assert exact.hits[0].doc_id == "KR-000001"

    prefix = engine.prefix("KR-00000")
    assert prefix.total >= 1
    assert any(hit.doc_id.startswith("KR-") for hit in prefix.hits)

    fuzzy = engine.fuzzy("Yin Yang")
    assert fuzzy.total >= 1

    ontology = engine.search("Principle", mode="ontology")
    assert ontology.total >= 1

    dependency = engine.search("KR-000001", mode="dependency")
    assert dependency.total >= 1

    relationship = engine.search("Relationship", mode="relationship")
    assert relationship.total >= 1

    rules = engine.search("VAL-", mode="prefix", kind="rule")
    assert rules.total >= 1

    context = engine.search("Seasonal", mode="prefix", kind="context")
    assert context.total >= 1

    registry = engine.search("knowledge_registry", mode="exact", kind="registry")
    assert registry.total >= 1


def test_search_performance_under_100ms() -> None:
    """Acceptance: search completes under 100ms after index load."""
    root = _root()
    engine = SearchEngine(project_root=root, timestamp="2026-08-01T00:00:00Z")
    engine.build_index()
    engine.load_index()

    # Warm-up + keep fuzzy queries short for budgeted path.
    engine.search("KR-000001", mode="exact")
    engine.search("Yin", mode="fuzzy")

    samples = []
    queries = [
        ("KR-000001", "exact"),
        ("KR-000", "prefix"),
        ("Yin", "fuzzy"),
        ("Principle", "ontology"),
        ("KR-000003", "dependency"),
        ("Relationship", "relationship"),
    ]
    for query, mode in queries:
        started = time.perf_counter()
        result = engine.search(query, mode=mode)
        elapsed = (time.perf_counter() - started) * 1000.0
        samples.append(elapsed)
        assert result.elapsed_ms < PERFORMANCE_BUDGET_MS
        assert elapsed < PERFORMANCE_BUDGET_MS
    assert max(samples) < PERFORMANCE_BUDGET_MS


def test_index_validation() -> None:
    """Index validation: unique IDs, required fields, deterministic ordering."""
    root = _root()
    build_search_index(project_root=root, timestamp="2026-08-01T00:00:00Z")
    index = read_json(root / "knowledge" / "search" / "search_index.json")
    docs = index["documents"]
    ids = [doc["doc_id"] for doc in docs]
    assert len(ids) == len(set(ids))
    assert ids == sorted(ids)
    for doc in docs:
        assert doc["doc_id"]
        assert doc["kind"]
        assert doc["canonical_name"]


def test_reproducible_index_checksums() -> None:
    """Acceptance: rebuild yields identical search_index checksum."""
    root = _root()
    path = root / "knowledge" / "search" / "search_index.json"
    build_search_index(project_root=root, timestamp="2026-08-01T00:00:00Z")
    first = sha256_file(path)
    build_search_index(project_root=root, timestamp="2026-08-01T00:00:00Z")
    second = sha256_file(path)
    assert first == second


def test_cli_build_and_search() -> None:
    """CLI build/search commands succeed."""
    from knowledge.search.__main__ import main

    root = _root()
    assert main(["--project-root", str(root), "build", "--timestamp", "2026-08-01T00:00:00Z"]) == 0
    assert main(["--project-root", str(root), "search", "KR-000001", "--mode", "exact"]) == 0


def test_deterministic_hit_ordering() -> None:
    """Same query returns identical ordered hit IDs across runs."""
    root = _root()
    engine = SearchEngine(project_root=root, timestamp="2026-08-01T00:00:00Z")
    engine.build_index()
    first = [hit.doc_id for hit in engine.search("KR-000", mode="prefix").hits]
    second = [hit.doc_id for hit in engine.search("KR-000", mode="prefix").hits]
    assert first == second
