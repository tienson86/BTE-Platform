"""Acceptance tests for Knowledge Package Builder (Sprint 8)."""

from __future__ import annotations

from pathlib import Path

from knowledge.package.io_utils import read_json, sha256_file
from knowledge.package.package_builder import PackageBuilder, build_pack
from knowledge.package.package_exporter import PackageExporter
from knowledge.package.package_validator import PackageValidator


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_package_modules_exist() -> None:
    """Required package modules exist."""
    root = _root()
    for name in (
        "package_builder.py",
        "package_manifest.py",
        "package_validator.py",
        "package_signer.py",
        "package_exporter.py",
    ):
        assert (root / "knowledge" / "package" / name).is_file(), name


def test_pack01_build_exportable() -> None:
    """Pack 01 builds and exports .pack/.zip/.tar.gz."""
    root = _root()
    summary = build_pack(
        "PACK_01",
        project_root=root,
        timestamp="2026-08-01T00:00:00Z",
    )
    assert summary["status"] == "PACKAGE_READY"
    assert summary["validation"]["ok"] is True
    dist = root / "knowledge" / "package" / "dist"
    assert (dist / "package_manifest.json").is_file()
    assert (dist / "package_inventory.json").is_file()
    assert (dist / "package_statistics.json").is_file()
    assert (dist / "PACK_01-1.0.0.pack").is_file()
    assert (dist / "PACK_01-1.0.0.zip").is_file()
    assert (dist / "PACK_01-1.0.0.tar.gz").is_file()
    package_dir = dist / "PACK_01-1.0.0"
    assert (package_dir / "content" / "records").is_dir()
    assert len(list((package_dir / "content" / "records").glob("KR-*.md"))) == 15


def test_package_validation() -> None:
    """Package directory and archives validate successfully."""
    root = _root()
    dist = root / "knowledge" / "package" / "dist"
    validator = PackageValidator()
    dir_result = validator.validate_directory(dist / "PACK_01-1.0.0")
    assert dir_result.ok, dir_result.findings
    for name in ("PACK_01-1.0.0.zip", "PACK_01-1.0.0.pack", "PACK_01-1.0.0.tar.gz"):
        result = validator.validate_archive(dist / name)
        assert result.ok, result.findings


def test_package_import_export() -> None:
    """Export then import round-trip validates."""
    root = _root()
    dist = root / "knowledge" / "package" / "dist"
    builder = PackageBuilder(project_root=root, timestamp="2026-08-01T00:00:00Z")
    imported = builder.import_package(
        dist / "PACK_01-1.0.0.zip",
        dist / "imported" / "PACK_01-1.0.0",
    )
    assert imported["validation"]["ok"] is True
    # Re-export imported package.
    exporter = PackageExporter()
    out = dist / "imported" / "PACK_01-1.0.0-reexport"
    archives = exporter.export_all(dist / "imported" / "PACK_01-1.0.0", out)
    assert archives["zip"].is_file()
    assert archives["pack"].is_file()
    assert archives["tar.gz"].is_file()


def test_pack02_compatible_definition() -> None:
    """Future Pack 02 definition is accepted by the builder API."""
    from knowledge.package.constants import PACK_DEFINITIONS

    assert "PACK_02" in PACK_DEFINITIONS
    assert PACK_DEFINITIONS["PACK_02"]["pack_id"] == "PACK_02"
    # Planned pack with zero records should still produce a valid empty package.
    root = _root()
    summary = build_pack(
        "PACK_02",
        project_root=root,
        version="0.0.0",
        timestamp="2026-08-01T00:00:00Z",
    )
    assert summary["status"] == "PACKAGE_READY"
    assert summary["statistics"]["record_count"] == 0


def test_deterministic_archives() -> None:
    """Rebuild yields identical zip checksums."""
    root = _root()
    zip_path = root / "knowledge" / "package" / "dist" / "PACK_01-1.0.0.zip"
    build_pack("PACK_01", project_root=root, timestamp="2026-08-01T00:00:00Z")
    first = sha256_file(zip_path)
    build_pack("PACK_01", project_root=root, timestamp="2026-08-01T00:00:00Z")
    second = sha256_file(zip_path)
    assert first == second


def test_no_kr_modification() -> None:
    """Packaging must not modify Knowledge Record sources."""
    root = _root()
    records = root / "knowledge" / "bazi" / "01_fundamental_knowledge" / "records"
    before = {path.name: sha256_file(path) for path in sorted(records.glob("KR-*.md"))}
    build_pack("PACK_01", project_root=root, timestamp="2026-08-01T00:00:00Z")
    after = {path.name: sha256_file(path) for path in sorted(records.glob("KR-*.md"))}
    assert before == after


def test_cli_build_and_validate() -> None:
    """CLI build/validate commands succeed."""
    from knowledge.package.__main__ import main

    root = _root()
    assert (
        main(
            [
                "--project-root",
                str(root),
                "build",
                "--pack-id",
                "PACK_01",
                "--timestamp",
                "2026-08-01T00:00:00Z",
            ]
        )
        == 0
    )
    package_dir = root / "knowledge" / "package" / "dist" / "PACK_01-1.0.0"
    assert main(["--project-root", str(root), "validate", str(package_dir)]) == 0


def test_manifest_statistics_inventory_fields() -> None:
    """Generated package metadata contains required fields."""
    root = _root()
    dist = root / "knowledge" / "package" / "dist"
    manifest = read_json(dist / "package_manifest.json")
    inventory = read_json(dist / "package_inventory.json")
    statistics = read_json(dist / "package_statistics.json")
    assert manifest["pack_id"] == "PACK_01"
    assert manifest["record_count"] == 15
    assert inventory["count"] >= 15
    assert statistics["record_count"] == 15
    assert "pack" in statistics["formats"]
