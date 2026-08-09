"""QC-4 version, checksum, documentation, and serialization consistency."""
from __future__ import annotations

import json
from pathlib import Path

QC4 = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[4]
RELEASE = REPO / "knowledge" / "releases" / "v1.0"
QC1 = REPO / "knowledge" / "quality" / "qc1"
QC3 = REPO / "knowledge" / "quality" / "qc3"

REQUIRED_ROOT = [
    "README.md",
    "RELEASE_CANDIDATE.md",
    "CERTIFICATION_REPORT.md",
    "PLATFORM_BASELINE.md",
    "QUALITY_BASELINE.md",
    "FINAL_RISK_REVIEW.md",
    "FINAL_RELEASE_CHECKLIST.md",
    "CERTIFICATION_DECISION.md",
    "PLATFORM_READINESS.md",
    "LONG_TERM_SUPPORT.md",
    "QC4_SUMMARY.md",
]
REQUIRED_DOCS = [
    "overview.md",
    "certification_methodology.md",
    "release_process.md",
    "baseline_definition.md",
    "quality_policy.md",
    "limitations.md",
    "future_releases.md",
]
REQUIRED_REPORTS = [
    "release_candidate.json",
    "baseline.json",
    "quality_baseline.json",
    "risk_baseline.json",
    "certification.json",
    "platform_readiness.json",
    "lifecycle.json",
]


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_version_and_checksum_consistency() -> None:
    manifest = _load(RELEASE / "RELEASE_MANIFEST.json")
    matrix = _load(RELEASE / "VERSION_MATRIX.json")
    pipelines = _load(RELEASE / "PIPELINE_INDEX.json")
    engines = _load(RELEASE / "ENGINE_INDEX.json")
    contracts = _load(RELEASE / "CONTRACT_INDEX.json")
    checksums = _load(RELEASE / "COMPONENT_CHECKSUMS.json")
    rc = _load(QC4 / "reports" / "release_candidate.json")
    qc3 = _load(QC3 / "reports" / "pipeline_status.json")

    assert matrix["platform_version"] == manifest["platform_version"] == rc["platform_version"]
    assert matrix["compatible"]["foundation"] == manifest["foundation_version"]
    for pipe in pipelines["pipelines"]:
        assert matrix["compatible"][pipe["pipeline_id"]] == pipe["version"]
        listed = next(item for item in manifest["pipelines"] if item["pipeline_id"] == pipe["pipeline_id"])
        assert listed["version"] == pipe["version"]
        assert rc["pipeline_versions"][pipe["pipeline_id"]] == pipe["version"]
    for engine in engines["canonical_engines"]:
        listed = next(item for item in manifest["engines"] if item["engine_id"] == engine["engine_id"])
        assert listed["version"] == engine["version"]
        assert rc["engine_versions"][engine["engine_id"]] == engine["version"]
    for contract in contracts["contracts"]:
        assert checksums["contract_checksums"][contract["contract_id"]] == contract["checksum_sha256"]
        assert len(contract["checksum_sha256"]) == 64
    assert all(row["index_match"] for row in qc3["rows"])


def test_quality_scores_are_derived_from_qc_sprints() -> None:
    quality = _load(QC4 / "reports" / "quality_baseline.json")
    qc1 = _load(QC1 / "reports" / "quality_scorecard.json")
    qc3 = _load(QC3 / "reports" / "quality_metrics.json")
    metrics = quality["metrics"]
    assert metrics["knowledge_score"] == qc1["overall"]
    assert metrics["integration_score"] == qc3["metrics"]["overall_integration_score"]
    assert metrics["documentation_score"] == qc1["dimensions"]["documentation"]
    assert metrics["governance_score"] == qc1["dimensions"]["governance"]
    assert metrics["release_score"] == qc1["dimensions"]["compatibility"]
    assert metrics["architecture_score"] == 100
    expected = round(
        sum(
            [
                metrics["architecture_score"],
                metrics["knowledge_score"],
                metrics["integration_score"],
                metrics["documentation_score"],
                metrics["governance_score"],
                metrics["release_score"],
            ]
        )
        / 6
    )
    assert metrics["overall_platform_score"] == expected
    for value in metrics.values():
        assert 0 <= value <= 100


def test_documentation_and_serialization() -> None:
    for name in REQUIRED_ROOT:
        assert (QC4 / name).is_file(), name
    for name in REQUIRED_DOCS:
        assert (QC4 / "documentation" / name).is_file(), name
    for name in REQUIRED_REPORTS:
        payload = _load(QC4 / "reports" / name)
        encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        assert json.loads(encoded)
    validation = _load(QC4 / "validation" / "VALIDATION.json")
    profile = _load(QC4 / "validation" / "profile.json")
    assert validation["counts"]["errors"] == 0
    assert validation["status"] == "pass_with_warnings"
    assert profile["validation_profile"] == "PVP-RELEASE"
    assert "baseline_integrity" in profile["checks"]
    assert "serialization" in profile["checks"]
