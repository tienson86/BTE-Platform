"""Acceptance tests for Registry Compiler (Sprint 5)."""

from __future__ import annotations

from pathlib import Path

from registry.compiler.registry_cache import RegistryCache
from registry.compiler.registry_compiler import RegistryCompiler, compile_registry
from registry.compiler.io_utils import read_json, sha256_file


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_registry_compiler_modules_exist() -> None:
    """TASK 01: required compiler modules exist."""
    root = _root()
    for name in (
        "registry_loader.py",
        "registry_indexer.py",
        "registry_compiler.py",
        "registry_cache.py",
        "registry_manifest.py",
    ):
        assert (root / "registry" / "compiler" / name).is_file()


def test_compile_generates_required_artifacts() -> None:
    """TASK 02/03/05: compile generates indexes, lookups, stats, reports."""
    root = _root()
    summary = compile_registry(project_root=root, timestamp="2026-08-01T00:00:00Z")
    assert summary["status"] == "COMPILER_READY"
    generated = root / "knowledge" / "generated"
    for name in (
        "registry_index.json",
        "registry_lookup.json",
        "registry_reverse_lookup.json",
        "registry_statistics.json",
        "registry_build_report.md",
        "registry_statistics.md",
        "registry_inventory.md",
        "indexes/id_index.json",
        "indexes/name_index.json",
        "indexes/category_index.json",
        "indexes/ontology_index.json",
        "indexes/dependency_index.json",
        "indexes/relationship_index.json",
        "cache/registry_cache.json",
    ):
        assert (generated / name).is_file(), name


def test_indexes_have_expected_structure() -> None:
    """TASK 03: all six indexes are present and structured."""
    root = _root()
    generated = root / "knowledge" / "generated"
    id_index = read_json(generated / "indexes" / "id_index.json")
    name_index = read_json(generated / "indexes" / "name_index.json")
    category_index = read_json(generated / "indexes" / "category_index.json")
    ontology_index = read_json(generated / "indexes" / "ontology_index.json")
    dependency_index = read_json(generated / "indexes" / "dependency_index.json")
    relationship_index = read_json(generated / "indexes" / "relationship_index.json")
    assert id_index["count"] >= 8  # at least domain descriptors
    assert name_index["count"] >= 1
    assert category_index["count"] >= 1
    assert ontology_index["statistics"]["class_count"] >= 1
    assert len(ontology_index.get("classes", {})) >= 1
    assert dependency_index["edge_count"] >= 1
    assert relationship_index["relationship_count"] >= 0


def test_registry_cache_memory_persistent_version() -> None:
    """TASK 04: memory, persistent, and version cache work."""
    root = _root()
    cache_path = root / "knowledge" / "generated" / "cache" / "test_cache.json"
    cache = RegistryCache(persistent_path=cache_path, version="1.0.0")
    cache.set("sample", {"ok": True}, checksum="abc")
    assert cache.get("sample") == {"ok": True}
    cache.save_persistent()
    assert cache_path.is_file()
    restored = RegistryCache(persistent_path=cache_path)
    assert restored.load_persistent() >= 1
    snapshot = restored.version_snapshot()
    assert "sample" in snapshot["keys"]
    cache_path.unlink(missing_ok=True)


def test_compile_is_deterministic() -> None:
    """Acceptance: repeated compile yields identical core artifact checksums."""
    root = _root()
    compiler = RegistryCompiler(project_root=root, timestamp="2026-08-01T00:00:00Z")
    compiler.compile()
    generated = root / "knowledge" / "generated"
    targets = [
        generated / "registry_index.json",
        generated / "registry_lookup.json",
        generated / "registry_reverse_lookup.json",
        generated / "registry_statistics.json",
        generated / "indexes" / "id_index.json",
    ]
    first = {path.name: sha256_file(path) for path in targets}
    compiler.compile()
    second = {path.name: sha256_file(path) for path in targets}
    assert first == second


def test_no_registry_or_kr_mutation() -> None:
    """Acceptance: compile does not modify registry or KR sources."""
    root = _root()
    reg_files = sorted(
        (root / "knowledge" / "registry").rglob("*.json")
    )
    # Exclude nothing under generated; only source registry tree.
    before_reg = {p: sha256_file(p) for p in reg_files if "generated" not in p.parts}
    kr_dir = root / "knowledge" / "bazi" / "01_fundamental_knowledge" / "records"
    before_kr = {p.name: sha256_file(p) for p in sorted(kr_dir.glob("KR-*.md"))}
    compile_registry(project_root=root, timestamp="2026-08-01T00:00:00Z")
    after_reg = {
        p: sha256_file(p)
        for p in sorted((root / "knowledge" / "registry").rglob("*.json"))
        if "generated" not in p.parts
    }
    after_kr = {p.name: sha256_file(p) for p in sorted(kr_dir.glob("KR-*.md"))}
    assert before_reg == after_reg
    assert before_kr == after_kr


def test_cli_compile() -> None:
    """CLI python -m registry compile succeeds."""
    from registry.__main__ import main

    root = _root()
    assert main(["--project-root", str(root), "compile"]) == 0
