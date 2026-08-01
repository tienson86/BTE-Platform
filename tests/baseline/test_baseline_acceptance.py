"""Acceptance tests for Pack 01 baseline infrastructure."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from baseline.baseline_builder import BaselineBuilder, build_baseline
from baseline.cli import main
from baseline.constants import PACK01_KR_INVENTORY, SNAPSHOT_FILENAMES
from baseline.diff.engine.baseline_diff import BaselineDiffEngine
from baseline.io_utils import read_json, sha256_file, write_json
from baseline.paths import resolve_project_root


@pytest.fixture(scope="module")
def project_root() -> Path:
    """Repository root."""
    return resolve_project_root()


@pytest.fixture(scope="module")
def built_baseline(project_root: Path) -> dict:
    """Build v1.0.0 baseline once for module tests."""
    return build_baseline(project_root=project_root, version="1.0.0")


def test_baseline_generation_creates_version_dir(
    project_root: Path, built_baseline: dict
) -> None:
    """Baseline generation creates knowledge/baseline/v1.0.0."""
    version_dir = project_root / "knowledge" / "baseline" / "v1.0.0"
    assert version_dir.is_dir()
    assert built_baseline["version"] == "1.0.0"
    assert built_baseline["artifact_count"] >= len(SNAPSHOT_FILENAMES) - 5


def test_snapshot_generation(project_root: Path, built_baseline: dict) -> None:
    """Required snapshots exist and are valid JSON."""
    version_dir = project_root / "knowledge" / "baseline" / "v1.0.0"
    required = [
        "baseline_manifest.json",
        "ontology_snapshot.json",
        "registry_snapshot.json",
        "dependency_snapshot.json",
        "compiler_snapshot.json",
        "validation_snapshot.json",
        "statistics.json",
        "checksums.json",
    ]
    for name in required:
        path = version_dir / name
        assert path.is_file(), name
        payload = read_json(path)
        assert isinstance(payload, dict)


def test_graph_generation(project_root: Path, built_baseline: dict) -> None:
    """Knowledge graph exports are generated in all required formats."""
    version_dir = project_root / "knowledge" / "baseline" / "v1.0.0"
    graph = read_json(version_dir / "knowledge_graph.json")
    assert graph["statistics"]["node_count"] > 0
    assert graph["statistics"]["edge_count"] > 0
    assert (version_dir / "knowledge_graph.graphml").is_file()
    assert (version_dir / "knowledge_graph.dot").is_file()
    assert (version_dir / "knowledge_graph.mmd").is_file()
    mirrored = project_root / "knowledge" / "graph" / "generated"
    assert (mirrored / "knowledge_graph.json").is_file()


def test_compiler_and_validation_outputs(
    project_root: Path, built_baseline: dict
) -> None:
    """Compiler and validation outputs are present and PASS."""
    version_dir = project_root / "knowledge" / "baseline" / "v1.0.0"
    compiler_report = read_json(version_dir / "compiler_validation_report.json")
    ontology_report = read_json(version_dir / "ontology_validation_report.json")
    registry_report = read_json(version_dir / "registry_validation_report.json")
    graph_report = read_json(version_dir / "graph_validation_report.json")
    assert compiler_report["status"] == "PASS"
    assert ontology_report["status"] == "PASS"
    assert registry_report["status"] == "PASS"
    assert graph_report["status"] == "PASS"
    assert (
        project_root
        / "knowledge"
        / "compiler"
        / "generated"
        / "compiler_snapshot.json"
    ).is_file()
    assert (
        project_root
        / "knowledge"
        / "validation"
        / "generated"
        / "validation_report.md"
    ).is_file()


def test_checksums_cover_knowledge_records(
    project_root: Path, built_baseline: dict
) -> None:
    """Checksums include every Pack 01 KR file."""
    version_dir = project_root / "knowledge" / "baseline" / "v1.0.0"
    checksums = read_json(version_dir / "checksums.json")
    files = checksums["files"]
    for entry in PACK01_KR_INVENTORY:
        rel = f"knowledge/bazi/01_fundamental_knowledge/records/{entry['filename']}"
        assert rel in files, rel
        abs_path = project_root / rel
        assert files[rel] == sha256_file(abs_path)


def test_deterministic_rebuild(project_root: Path) -> None:
    """Rebuilding with the same timestamp yields identical checksums.json files map."""
    first = BaselineBuilder(
        project_root=project_root,
        version="1.0.0",
        timestamp="2026-08-01T00:00:00Z",
    ).build()
    checksums_path = (
        project_root / "knowledge" / "baseline" / "v1.0.0" / "checksums.json"
    )
    first_payload = read_json(checksums_path)
    # Remove self-hash volatility by comparing source KR checksums only.
    second = BaselineBuilder(
        project_root=project_root,
        version="1.0.0",
        timestamp="2026-08-01T00:00:00Z",
    ).build()
    second_payload = read_json(checksums_path)
    for entry in PACK01_KR_INVENTORY:
        rel = f"knowledge/bazi/01_fundamental_knowledge/records/{entry['filename']}"
        assert first_payload["files"][rel] == second_payload["files"][rel]
    assert first["statistics"]["knowledge_records"] == second["statistics"][
        "knowledge_records"
    ]


def test_diff_engine(project_root: Path, tmp_path: Path) -> None:
    """Diff engine compares two baseline directories and writes reports."""
    src = project_root / "knowledge" / "baseline" / "v1.0.0"
    old_dir = tmp_path / "v1.0.0"
    new_dir = tmp_path / "v1.0.1"
    shutil.copytree(src, old_dir)
    shutil.copytree(src, new_dir)
    # Introduce a deterministic registry snapshot change.
    registry_path = new_dir / "registry_snapshot.json"
    payload = read_json(registry_path)
    payload["version"] = "1.0.1"
    if payload.get("registries"):
        payload["registries"][0]["record_count"] = (
            int(payload["registries"][0].get("record_count") or 0) + 1
        )
        payload["registries"][0]["checksum"] = "diff-test-checksum"
    write_json(registry_path, payload)

    engine = BaselineDiffEngine(project_root=project_root)
    result = engine.compare(
        str(old_dir),
        str(new_dir),
        output_dir=tmp_path / "diff_out",
    )
    assert "registry" in result["domains"]
    assert (tmp_path / "diff_out" / "baseline_diff.json").is_file()
    assert (tmp_path / "diff_out" / "baseline_diff.md").is_file()
    assert (tmp_path / "diff_out" / "baseline_diff.html").is_file()


def test_cli_validate_and_stats(project_root: Path, built_baseline: dict) -> None:
    """CLI validate/stats commands succeed against generated baseline."""
    assert (
        main(
            [
                "--project-root",
                str(project_root),
                "validate",
                "--version",
                "1.0.0",
            ]
        )
        == 0
    )
    assert (
        main(
            [
                "--project-root",
                str(project_root),
                "stats",
                "--version",
                "1.0.0",
            ]
        )
        == 0
    )


def test_cli_report(project_root: Path, built_baseline: dict) -> None:
    """CLI report command prints markdown report."""
    assert (
        main(
            [
                "--project-root",
                str(project_root),
                "report",
                "--version",
                "1.0.0",
                "--name",
                "freeze_readiness.md",
            ]
        )
        == 0
    )


def test_no_source_mutation_markers(project_root: Path) -> None:
    """Governance metadata asserts generated-only policy."""
    metadata = read_json(
        project_root
        / "knowledge"
        / "governance"
        / "generated"
        / "governance_metadata.json"
    )
    assert "freeze_readiness" in metadata
    freeze = read_json(
        project_root / "knowledge" / "baseline" / "v1.0.0" / "freeze_inventory.json"
    )
    assert freeze["policy"]["no_kr_modification"] is True
    assert freeze["policy"]["no_registry_modification"] is True
