"""Sprint 4 baseline lifecycle acceptance tests."""

from __future__ import annotations

import shutil
from pathlib import Path

from baseline.baseline_builder import BaselineBuilder, build_baseline
from baseline.cli import main
from baseline.diff.engine import BaselineDiffEngine, SnapshotLoader, diff_baselines
from baseline.io_utils import read_json, sha256_file, write_json
from baseline.paths import resolve_project_root


def test_diff_engine_modules_importable() -> None:
    """TASK 16: diff engine modules are available."""
    engine = BaselineDiffEngine(project_root=resolve_project_root())
    assert hasattr(engine, "compare")
    assert hasattr(engine, "list_versions")
    assert "v1.0.0" in engine.list_versions()


def test_release_packaging_artifacts() -> None:
    """TASK 17: release packaging artifacts exist for v1.0.0."""
    root = resolve_project_root()
    version_dir = root / "knowledge" / "baseline" / "v1.0.0"
    for name in (
        "release_manifest.json",
        "release_metadata.json",
        "release_inventory.json",
        "release_artifacts.json",
        "freeze_inventory.json",
    ):
        path = version_dir / name
        assert path.is_file(), name
        payload = read_json(path)
        assert isinstance(payload, dict)
    freeze = read_json(version_dir / "freeze_inventory.json")
    assert freeze["policy"]["no_kr_modification"] is True
    assert freeze["policy"]["no_registry_modification"] is True


def test_baseline_builder_capabilities() -> None:
    """TASK 18: builder produces snapshots, reports, graph, metadata, checksums."""
    root = resolve_project_root()
    summary = build_baseline(project_root=root, version="1.0.0")
    assert summary["overall_status"] == "READY_FOR_FREEZE"
    version_dir = root / "knowledge" / "baseline" / "v1.0.0"
    for name in (
        "baseline_manifest.json",
        "ontology_snapshot.json",
        "registry_snapshot.json",
        "dependency_snapshot.json",
        "compiler_snapshot.json",
        "validation_snapshot.json",
        "knowledge_graph.json",
        "governance_metadata.json",
        "checksums.json",
        "statistics.json",
        "release_manifest.json",
    ):
        assert (version_dir / name).is_file(), name
    index = read_json(root / "knowledge" / "baseline" / "versions_index.json")
    assert "1.0.x" in index["supported_patterns"]
    assert any(item["version"] == "1.0.0" for item in index["versions"])


def test_cli_all_commands_operational() -> None:
    """TASK 19: all required CLI commands succeed."""
    root = resolve_project_root()
    assert main(["--project-root", str(root), "build", "--version", "1.0.0"]) == 0
    assert main(["--project-root", str(root), "validate", "--version", "1.0.0"]) == 0
    assert main(["--project-root", str(root), "stats", "--version", "1.0.0"]) == 0
    assert (
        main(
            [
                "--project-root",
                str(root),
                "report",
                "--version",
                "1.0.0",
                "--name",
                "freeze_readiness.md",
            ]
        )
        == 0
    )


def test_diff_cli_and_reports(tmp_path: Path) -> None:
    """TASK 16/19: diff CLI compares versions and writes MD/JSON/HTML."""
    root = resolve_project_root()
    src = root / "knowledge" / "baseline" / "v1.0.0"
    old_dir = tmp_path / "v1.0.0"
    new_dir = tmp_path / "v1.1.0"
    shutil.copytree(src, old_dir)
    shutil.copytree(src, new_dir)

    registry_path = new_dir / "registry_snapshot.json"
    payload = read_json(registry_path)
    payload["version"] = "1.1.0"
    if payload.get("registries"):
        payload["registries"][0]["checksum"] = "sprint4-diff-marker"
        payload["registries"][0]["record_count"] = (
            int(payload["registries"][0].get("record_count") or 0) + 1
        )
    write_json(registry_path, payload)

    out = tmp_path / "diff_out"
    assert (
        main(
            [
                "--project-root",
                str(root),
                "diff",
                str(old_dir),
                str(new_dir),
                "--output-dir",
                str(out),
            ]
        )
        == 0
    )
    assert (out / "baseline_diff.json").is_file()
    assert (out / "baseline_diff.md").is_file()
    assert (out / "baseline_diff.html").is_file()
    result = read_json(out / "baseline_diff.json")
    assert "registry" in result["domains"]
    assert "registry" in result["summary"]["changed_domains"]


def test_future_version_directory_support() -> None:
    """Acceptance: builder supports future version folders without redesign."""
    root = resolve_project_root()
    summary = BaselineBuilder(
        project_root=root,
        version="1.1.0",
        timestamp="2026-08-01T00:00:00Z",
    ).build()
    assert summary["version"] == "1.1.0"
    version_dir = root / "knowledge" / "baseline" / "v1.1.0"
    assert version_dir.is_dir()
    assert (version_dir / "release_manifest.json").is_file()
    result = diff_baselines("1.0.0", "1.1.0", project_root=root)
    assert result["old_version"] == "v1.0.0"
    assert result["new_version"] == "v1.1.0"
    assert (Path(result["output_dir"]) / "baseline_diff.json").is_file()
    index = read_json(root / "knowledge" / "baseline" / "versions_index.json")
    versions = {item["version"] for item in index["versions"]}
    assert {"1.0.0", "1.1.0"} <= versions


def test_snapshot_loader_loads_core_files() -> None:
    """TASK 16/20: snapshot loader reads core baseline snapshots."""
    root = resolve_project_root()
    loader = SnapshotLoader(root / "knowledge" / "baseline" / "v1.0.0")
    loaded = loader.load_all()
    assert "baseline_manifest.json" in loaded
    assert "compiler_snapshot.json" in loaded
    assert "validation_snapshot.json" in loaded
    assert "knowledge_graph.json" in loaded


def test_no_source_mutation_in_lifecycle() -> None:
    """Acceptance: lifecycle tooling does not modify KR or registries."""
    root = resolve_project_root()
    kr_dir = root / "knowledge" / "bazi" / "01_fundamental_knowledge" / "records"
    reg = root / "knowledge" / "registry" / "knowledge_registry" / "knowledge_registry.json"
    before_kr = {p.name: sha256_file(p) for p in sorted(kr_dir.glob("KR-*.md"))}
    before_reg = sha256_file(reg)
    build_baseline(project_root=root, version="1.0.0")
    BaselineDiffEngine(project_root=root).compare("1.0.0", "1.1.0")
    after_kr = {p.name: sha256_file(p) for p in sorted(kr_dir.glob("KR-*.md"))}
    after_reg = sha256_file(reg)
    assert before_kr == after_kr
    assert before_reg == after_reg
