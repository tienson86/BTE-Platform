"""QC-4 baseline tests. Read-only over QC-1/2/3 and frozen release indexes."""
from __future__ import annotations

import json
from pathlib import Path

QC4 = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[4]
RELEASE = REPO / "knowledge" / "releases" / "v1.0"
QC1 = REPO / "knowledge" / "quality" / "qc1"
QC2 = REPO / "knowledge" / "quality" / "qc2"
QC3 = REPO / "knowledge" / "quality" / "qc3"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_baseline_versions_match_frozen_indexes() -> None:
    baseline = _load(QC4 / "reports" / "baseline.json")
    rc = _load(QC4 / "reports" / "release_candidate.json")
    manifest = _load(RELEASE / "RELEASE_MANIFEST.json")
    pipelines = _load(RELEASE / "PIPELINE_INDEX.json")
    packages = _load(RELEASE / "PACKAGE_INDEX.json")
    inventory = _load(QC1 / "reports" / "ecosystem_inventory.json")

    assert rc["rc_id"] == "BTE-RC-1.0.0"
    assert rc["baseline_id"] == baseline["baseline_id"] == "BSL-QC4-1.0.0"
    assert rc["platform_version"] == manifest["platform_version"] == "1.0.0"
    assert rc["foundation_version"] == manifest["foundation_version"] == "1.0.0"
    assert rc["knowledge_version"] == manifest["knowledge_version"] == "1.0.0"
    assert rc["runtime_changes"] is False
    assert rc["certification_date"] is None
    assert rc["certification_date_placeholder"] == "PENDING_RELEASE_MANAGER"

    expected_pipelines = {item["pipeline_id"]: item["version"] for item in pipelines["pipelines"]}
    assert rc["pipeline_versions"] == expected_pipelines
    assert len(baseline["af1_packages"]) == len(packages["packages"]) == 9
    assert baseline["knowledge_ecosystem_package_count"] == inventory["counts"]["packages"] == 23
    assert all(value is False for value in baseline["mutated"].values())


def test_qc_inputs_are_present_and_unexecuted() -> None:
    baseline = _load(QC4 / "reports" / "baseline.json")
    coverage = _load(QC2 / "reports" / "coverage_report.json")
    qc3 = _load(QC3 / "reports" / "pipeline_status.json")
    handoff = _load(QC3 / "reports" / "handoff_matrix.json")

    assert baseline["qc2"]["scenarios"] == coverage["scenarios"] == 13
    assert baseline["qc2"]["snapshots"] == coverage["snapshots"] == 65
    assert baseline["qc2"]["engines_replayed"] == 0
    assert baseline["qc3"]["pipeline_count"] == 5
    assert baseline["qc3"]["missing_contracts"] == handoff["missing_contract_count"] == 0
    assert baseline["qc3"]["engine_executed"] is False
    assert qc3["engine_executed"] is False
    for key in (
        "knowledge",
        "pipelines",
        "contracts",
        "engines",
        "interpretation",
        "presentation",
        "documentation",
        "validation",
        "testing",
        "quality",
        "governance",
        "compatibility",
        "versioning",
        "checksums",
        "release_readiness",
    ):
        assert baseline["scope"][key] is True
