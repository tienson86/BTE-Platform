"""Regression: released Useful God decision packages must remain unchanged by AX-3."""

from __future__ import annotations

import json
from pathlib import Path

from engines.decision_engine.pipeline.package_loader import DecisionPackageLoader

REPO = Path(__file__).resolve().parents[2]

EXPECTED = {
    "bz_06_useful_god_foundation": {
        "path": ("knowledge", "packages", "useful_god", "foundation"),
        "version": "1.0.0",
        "checksum": "78a6f7c8701db6d64171b2f13efb034aaec7f7f26e9f96487ba64055bae96dbd",
        "prefix": "UGD",
        "rule_count": 109,
        "reasoning_chains": (
            "RC-UGD-STRONG-001",
            "RC-UGD-WEAK-001",
            "RC-UGD-CONFLICT-001",
        ),
    },
    "bz_07_useful_god_priority": {
        "path": ("knowledge", "packages", "useful_god", "priority"),
        "version": "1.0.0",
        "checksum": "0bd558416116f5267d0e0a4ae6c85316efa4b19bae34f85c0c4b53fc1c274789",
        "prefix": "UGP",
        "rule_count": 110,
        "reasoning_chains": (
            "RC-UGP-SINGLE-001",
            "RC-UGP-MULTIPLE-001",
            "RC-UGP-CONFLICT-001",
            "RC-UGP-TIE-001",
            "RC-UGP-LOWCONF-001",
        ),
    },
    "bz_08_useful_god_override": {
        "path": ("knowledge", "packages", "useful_god", "override"),
        "version": "1.0.0",
        "checksum": "ce73017c02f05cc5c0be37c09bf9dddf9b65cc00a74614c1d9637350e21c3093",
        "prefix": "UGO",
        "rule_count": 110,
        "reasoning_chains": (
            "RC-UGO-NOOVERRIDE-001",
            "RC-UGO-FOLLOW-001",
            "RC-UGO-TRANSFORM-001",
            "RC-UGO-CONTRADICTION-001",
            "RC-UGO-LOWCONF-001",
        ),
    },
}


def _package_dir(package_id: str) -> Path:
    return REPO.joinpath(*EXPECTED[package_id]["path"])


def test_released_decision_packages_checksum_and_rules_unchanged() -> None:
    """Checksums, rule ids, evidence, reasoning, and contracts stay sealed."""
    loader = DecisionPackageLoader()
    for package_id, expected in EXPECTED.items():
        package = loader.load(package_id)
        assert package.package_version == expected["version"]
        assert package.checksum == expected["checksum"]
        assert package.status == "released"
        assert package.schema_version == "2.0.0"
        assert package.package_type == "decision"
        assert package.rule_count == expected["rule_count"]
        assert all(rule_id.startswith(expected["prefix"]) for rule_id in package.rule_ids)

        root = _package_dir(package_id)
        package_json = json.loads((root / "PACKAGE.json").read_text(encoding="utf-8"))
        assert package_json["checksum"]["value"] == expected["checksum"]

        evidence_dir = root / "evidence" / "bundles"
        bundles = sorted(path.stem for path in evidence_dir.glob("*.json"))
        assert len(bundles) == expected["rule_count"]

        index = json.loads((root / "reasoning" / "index.json").read_text(encoding="utf-8"))
        assert tuple(index["chains"]) == expected["reasoning_chains"]

        assert (root / "assets" / "published_inputs.json").is_file()
        assert (root / "assets" / "published_outputs.json").is_file()


def test_ax3_loader_does_not_rewrite_packages() -> None:
    """Decision loader remains read-only against Override files."""
    root = _package_dir("bz_08_useful_god_override")
    package_path = root / "PACKAGE.json"
    before = package_path.read_bytes()
    DecisionPackageLoader().load("bz_08_useful_god_override")
    after = package_path.read_bytes()
    assert before == after
