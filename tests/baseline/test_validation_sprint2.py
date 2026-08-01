"""Sprint 2 validation infrastructure acceptance tests."""

from __future__ import annotations

from pathlib import Path

from baseline.baseline_builder import BaselineBuilder
from baseline.io_utils import read_json, sha256_file
from baseline.paths import resolve_project_root


def test_validation_snapshot_contents() -> None:
    """TASK 06: validation_snapshot includes stages, rules, coverage, severity."""
    root = resolve_project_root()
    builder = BaselineBuilder(project_root=root, version="1.0.0")
    result = builder.validate_only(persist=True)
    assert result["status"] == "PASS"

    snapshot = read_json(
        root / "knowledge" / "baseline" / "v1.0.0" / "validation_snapshot.json"
    )
    assert "validation_stages" in snapshot
    assert "validation_rules" in snapshot
    assert "coverage" in snapshot
    assert "statistics" in snapshot
    assert "severity" in snapshot
    assert snapshot["coverage"]["validator_coverage_ratio"] == 1.0
    assert snapshot["statistics"]["rule_count"] >= 1
    assert len(snapshot["validation_stages"]) >= 1


def test_governance_metadata_readiness_gates() -> None:
    """TASK 07: governance_metadata includes all readiness gates."""
    root = resolve_project_root()
    metadata = read_json(
        root / "knowledge" / "baseline" / "v1.0.0" / "governance_metadata.json"
    )
    for key in (
        "freeze_readiness",
        "baseline_readiness",
        "compiler_readiness",
        "validation_readiness",
        "release_readiness",
    ):
        assert key in metadata
        assert "ready" in metadata[key]
    mirrored = (
        root / "knowledge" / "governance" / "generated" / "governance_metadata.json"
    )
    assert mirrored.is_file()
    assert metadata["overall_status"] == "READY_FOR_FREEZE"


def test_compiler_validation_report_checks() -> None:
    """TASK 08: compiler validation covers required check dimensions."""
    root = resolve_project_root()
    report = read_json(
        root
        / "knowledge"
        / "baseline"
        / "v1.0.0"
        / "compiler_validation_report.json"
    )
    assert report["status"] == "PASS"
    assert report["error_count"] == 0
    checks = set(report["metadata"]["checks"])
    assert checks == {
        "duplicate_ids",
        "broken_references",
        "compiler_contracts",
        "registry_loading",
        "dependency_resolution",
    }


def test_ontology_validation_report_checks() -> None:
    """TASK 09: ontology validation covers integrity dimensions."""
    root = resolve_project_root()
    report = read_json(
        root
        / "knowledge"
        / "baseline"
        / "v1.0.0"
        / "ontology_validation_report.json"
    )
    assert report["status"] == "PASS"
    assert report["error_count"] == 0
    checks = set(report["metadata"]["checks"])
    assert "ontology_integrity" in checks
    assert "duplicate_ontology_objects" in checks
    assert "semantic_consistency" in checks
    assert "orphan_nodes" in checks


def test_registry_validation_report_checks() -> None:
    """TASK 10: registry validation covers ID/schema/metadata/refs."""
    root = resolve_project_root()
    report = read_json(
        root
        / "knowledge"
        / "baseline"
        / "v1.0.0"
        / "registry_validation_report.json"
    )
    assert report["status"] == "PASS"
    assert report["error_count"] == 0
    checks = set(report["metadata"]["checks"])
    assert checks == {
        "unique_ids",
        "schema_compliance",
        "metadata",
        "cross_references",
    }


def test_validation_reproducible() -> None:
    """Acceptance: repeated validate produces identical report checksums."""
    root = resolve_project_root()
    builder = BaselineBuilder(
        project_root=root,
        version="1.0.0",
        timestamp="2026-08-01T00:00:00Z",
    )
    builder.validate_only(persist=True)
    paths = [
        root / "knowledge" / "baseline" / "v1.0.0" / name
        for name in (
            "validation_snapshot.json",
            "governance_metadata.json",
            "compiler_validation_report.json",
            "ontology_validation_report.json",
            "registry_validation_report.json",
        )
    ]
    first = {path.name: sha256_file(path) for path in paths}
    builder.validate_only(persist=True)
    second = {path.name: sha256_file(path) for path in paths}
    assert first == second


def test_no_kr_or_registry_mutation_from_validate() -> None:
    """Acceptance: validate must not modify KR or registry source files."""
    root = resolve_project_root()
    kr_dir = root / "knowledge" / "bazi" / "01_fundamental_knowledge" / "records"
    reg_dir = root / "knowledge" / "registry" / "knowledge_registry"
    before_kr = {
        p.name: sha256_file(p) for p in sorted(kr_dir.glob("KR-*.md"))
    }
    before_reg = {
        p.name: sha256_file(p) for p in sorted(reg_dir.glob("*.json"))
    }
    BaselineBuilder(project_root=root, version="1.0.0").validate_only(persist=True)
    after_kr = {p.name: sha256_file(p) for p in sorted(kr_dir.glob("KR-*.md"))}
    after_reg = {p.name: sha256_file(p) for p in sorted(reg_dir.glob("*.json"))}
    assert before_kr == after_kr
    assert before_reg == after_reg
