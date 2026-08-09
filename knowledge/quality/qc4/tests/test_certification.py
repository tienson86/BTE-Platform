"""QC-4 certification decision must follow recorded evidence only."""
from __future__ import annotations

import json
from pathlib import Path

QC4 = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[4]
QC1 = REPO / "knowledge" / "quality" / "qc1"
QC2 = REPO / "knowledge" / "quality" / "qc2"
QC3 = REPO / "knowledge" / "quality" / "qc3"
ALLOWED = {"Certified", "Certified with Warnings", "Rejected"}


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_certification_decision_is_evidence_based() -> None:
    cert = _load(QC4 / "reports" / "certification.json")
    risks = _load(QC4 / "reports" / "risk_baseline.json")
    qc1_val = _load(QC1 / "validation" / "VALIDATION.json")
    qc2_val = _load(QC2 / "validation" / "VALIDATION.json")
    qc3_val = _load(QC3 / "validation" / "VALIDATION.json")
    ready = _load(QC1 / "reports" / "release_readiness.json")

    assert cert["decision"] in ALLOWED
    errors = qc1_val["counts"]["errors"] + qc2_val["counts"]["errors"] + qc3_val["counts"]["errors"]
    assert errors == 0
    assert risks["open_critical_high"] == 0
    assert cert["decision"] != "Rejected"
    assert ready["engine_complete"] is False
    assert risks["open_medium"] > 0
    assert cert["decision"] == "Certified with Warnings"
    assert cert["evidence"]["validation_errors"] == 0
    assert cert["evidence"]["engine_complete"] is False
    assert cert["certification_date"] is None


def test_risk_findings_have_required_fields() -> None:
    risks = _load(QC4 / "reports" / "risk_baseline.json")
    required = {"risk_id", "severity", "status", "recommendation", "release_impact"}
    allowed_severity = {"Critical", "High", "Medium", "Low", "Informational"}
    ids = [item["risk_id"] for item in risks["findings"]]
    assert len(ids) == len(set(ids))
    for item in risks["findings"]:
        assert required <= set(item)
        assert item["severity"] in allowed_severity
        assert item["risk_id"].startswith("RSK-QC4-")
    assert risks["counts"]["Critical"] == 0
    assert risks["counts"]["High"] == 0
    assert risks["counts"]["Medium"] == 4
