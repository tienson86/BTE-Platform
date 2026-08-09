"""Regression: released knowledge packages must remain unchanged by AX-1."""

from __future__ import annotations

import json
from pathlib import Path

from engines.analysis_engine.pipeline.package_loader import PackageLoader

REPO = Path(__file__).resolve().parents[2]

EXPECTED = {
    "bz_01_strength_core": {
        "version": "1.2.0",
        "checksum": "74fd4ac82af8c0693e5996536ad755dfc17e79a4e406de6b8d9136fada5f495b",
        "prefix": "SKC",
        "rule_count": 110,
        "reasoning_chains": None,
    },
    "bz_02_seasonal_core": {
        "version": "1.0.0",
        "checksum": "f394ba18da3482c3b1708c3d9caa113a85587a46d16e5030938df4a4f26a786b",
        "prefix": "SEC",
        "rule_count": 110,
        "reasoning_chains": None,
    },
    "bz_03_temperature_core": {
        "version": "1.0.0",
        "checksum": "a2e4826b6beec74c081ceb49fabecdd1fe2e942a000d837dcf1298a12c661427",
        "prefix": "TEC",
        "rule_count": 110,
        "reasoning_chains": (
            "RC-TEC-COLD-001",
            "RC-TEC-HOT-001",
            "RC-TEC-BALANCED-001",
        ),
    },
}


def _package_dir(package_id: str) -> Path:
    name = {
        "bz_01_strength_core": "strength",
        "bz_02_seasonal_core": "seasonal",
        "bz_03_temperature_core": "temperature",
    }[package_id]
    return REPO / "knowledge" / "packages" / name / "core"


def test_released_packages_metadata_unchanged() -> None:
    """Package metadata, versions, and checksums must match the sealed release."""
    loader = PackageLoader()
    loaded = loader.load_core_packages()
    for package_id, expected in EXPECTED.items():
        package = loaded[package_id]
        assert package.package_version == expected["version"]
        assert package.checksum == expected["checksum"]
        assert package.status == "released"
        assert package.schema_version == "2.0.0"
        assert package.rule_count == expected["rule_count"]
        assert all(rule_id.startswith(expected["prefix"]) for rule_id in package.rule_ids)


def test_rule_ids_evidence_and_reasoning_unchanged() -> None:
    """Rule IDs, evidence bundles, and reasoning artifacts must stay intact."""
    for package_id, expected in EXPECTED.items():
        root = _package_dir(package_id)
        package_json = json.loads((root / "PACKAGE.json").read_text(encoding="utf-8"))
        assert package_json["package_id"] == package_id
        assert package_json["package_version"] == expected["version"]
        assert package_json["checksum"]["value"] == expected["checksum"]

        evidence_dir = root / "evidence" / "bundles"
        if evidence_dir.is_dir():
            bundles = sorted(path.stem for path in evidence_dir.glob("*.json"))
            assert len(bundles) == expected["rule_count"]

        reasoning_index = root / "reasoning" / "index.json"
        if expected["reasoning_chains"] is not None:
            index = json.loads(reasoning_index.read_text(encoding="utf-8"))
            assert tuple(index["chains"]) == expected["reasoning_chains"]


def test_ax1_does_not_rewrite_package_files() -> None:
    """AX-1 loader is read-only against package files."""
    root = _package_dir("bz_01_strength_core")
    package_path = root / "PACKAGE.json"
    before = package_path.read_bytes()
    PackageLoader().load("bz_01_strength_core")
    after = package_path.read_bytes()
    assert before == after
