"""AX-2 package contract integrity and released-package regression."""

from __future__ import annotations

import json
from pathlib import Path

from engines.analysis_engine.contracts.analysis_contract import (
    ANALYSIS_RESULT_FIELDS,
    analysis_result_contract,
)
from engines.analysis_engine.pipeline.canonical_pipeline import CanonicalPipeline
from engines.analysis_engine.pipeline.package_loader import PackageLoader
from engines.analysis_engine.pipeline.stage_registry import CanonicalStageRegistry

REPO = Path(__file__).resolve().parents[2]

EXPECTED_PACKAGES = {
    "bz_01_strength_core": {
        "path": ("knowledge", "packages", "strength", "core"),
        "version": "1.2.0",
        "checksum": "74fd4ac82af8c0693e5996536ad755dfc17e79a4e406de6b8d9136fada5f495b",
        "prefix": "SKC",
        "rule_count": 110,
        "reasoning_chains": None,
    },
    "bz_02_seasonal_core": {
        "path": ("knowledge", "packages", "seasonal", "core"),
        "version": "1.0.0",
        "checksum": "f394ba18da3482c3b1708c3d9caa113a85587a46d16e5030938df4a4f26a786b",
        "prefix": "SEC",
        "rule_count": 110,
        "reasoning_chains": None,
    },
    "bz_03_temperature_core": {
        "path": ("knowledge", "packages", "temperature", "core"),
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
    "bz_04_pattern_core": {
        "path": ("knowledge", "packages", "pattern", "core"),
        "version": "1.0.0",
        "checksum": "24911267dad714946b23733f38204efc7052a67d42ede1faec066b8fe073fc34",
        "prefix": "PAT",
        "rule_count": 110,
        "reasoning_chains": (
            "RC-PAT-PRINCIPAL-001",
            "RC-PAT-CONFLICT-001",
            "RC-PAT-CONFIRMATION-001",
        ),
    },
    "bz_05_pattern_evaluation": {
        "path": ("knowledge", "packages", "pattern", "evaluation"),
        "version": "1.0.0",
        "checksum": "c4fa911d45002cff65477d8096209834c582e71791dbd9e46d8d33346b92c901",
        "prefix": "PEV",
        "rule_count": 110,
        "reasoning_chains": (
            "RC-PEV-HIGH-001",
            "RC-PEV-WEAK-001",
            "RC-PEV-BROKEN-001",
        ),
    },
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
}


def _package_dir(package_id: str) -> Path:
    return REPO.joinpath(*EXPECTED_PACKAGES[package_id]["path"])


def test_analysis_result_contract_fields() -> None:
    """Canonical Analysis Result must publish the AX-2 field set."""
    contract = analysis_result_contract()
    assert contract["pipeline_version"] == "2.0.0"
    for field_name in ANALYSIS_RESULT_FIELDS:
        assert field_name in contract["fields"]
    result = CanonicalPipeline().run({"month_branch": "zi"})
    payload = result.to_dict()
    for field_name in (
        "seasonal",
        "strength",
        "temperature",
        "pattern",
        "pattern_evaluation",
        "useful_god",
        "diagnostics",
        "execution_trace",
        "pipeline_version",
        "package_versions",
    ):
        assert field_name in payload


def test_useful_god_input_output_contracts_match_registry() -> None:
    """Useful God registry I/O must match the published package contract."""
    registry = CanonicalStageRegistry.default()
    stage = registry.get("useful_god")
    root = _package_dir("bz_06_useful_god_foundation")
    inputs = json.loads((root / "assets" / "published_inputs.json").read_text(encoding="utf-8"))
    outputs = json.loads((root / "assets" / "published_outputs.json").read_text(encoding="utf-8"))
    assert tuple(item["name"] for item in inputs["inputs"]) == stage.consumed_outputs
    assert tuple(item["name"] for item in outputs["outputs"]) == stage.produced_outputs


def test_pattern_evaluation_output_contract_match_registry() -> None:
    """Pattern Evaluation published outputs must be declared by the registry."""
    registry = CanonicalStageRegistry.default()
    stage = registry.get("pattern_evaluation")
    root = _package_dir("bz_05_pattern_evaluation")
    outputs = json.loads((root / "assets" / "published_outputs.json").read_text(encoding="utf-8"))
    names = tuple(item["name"] for item in outputs["outputs"])
    assert set(names) <= set(stage.produced_outputs)


def test_released_packages_checksum_rule_ids_unchanged() -> None:
    """Released package checksums, rule ids, evidence, and reasoning stay sealed."""
    loader = PackageLoader()
    for package_id, expected in EXPECTED_PACKAGES.items():
        package = loader.load(package_id)
        assert package.package_version == expected["version"]
        assert package.checksum == expected["checksum"]
        assert package.status == "released"
        assert package.schema_version == "2.0.0"
        assert package.rule_count == expected["rule_count"]
        assert all(rule_id.startswith(expected["prefix"]) for rule_id in package.rule_ids)

        root = _package_dir(package_id)
        package_json = json.loads((root / "PACKAGE.json").read_text(encoding="utf-8"))
        assert package_json["checksum"]["value"] == expected["checksum"]

        evidence_dir = root / "evidence" / "bundles"
        if evidence_dir.is_dir():
            bundles = sorted(path.stem for path in evidence_dir.glob("*.json"))
            assert len(bundles) == expected["rule_count"]

        chains = expected["reasoning_chains"]
        if chains is not None:
            index = json.loads((root / "reasoning" / "index.json").read_text(encoding="utf-8"))
            assert tuple(index["chains"]) == chains


def test_ax2_loader_does_not_rewrite_packages() -> None:
    """Canonical loader remains read-only against Useful God files."""
    root = _package_dir("bz_06_useful_god_foundation")
    package_path = root / "PACKAGE.json"
    before = package_path.read_bytes()
    PackageLoader().load("bz_06_useful_god_foundation")
    CanonicalPipeline().load_packages()
    after = package_path.read_bytes()
    assert before == after
