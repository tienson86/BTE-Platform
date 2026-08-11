"""Queue integrity: required docs, matrix columns, no empty CAL placeholders."""

from __future__ import annotations

import json

from .helpers import CASES, LEVELS, REPORTS, REQUIRED_DOCS, ROOT, VALIDATION


def test_required_docs_exist() -> None:
    missing = [name for name in REQUIRED_DOCS if not (ROOT / name).is_file()]
    assert missing == [], missing


def test_cases_and_expert_readmes_exist() -> None:
    assert (CASES / "README.md").is_file()
    assert (ROOT / "expert_review" / "README.md").is_file()


def test_coverage_matrix_columns() -> None:
    data = json.loads((REPORTS / "coverage_matrix.json").read_text(encoding="utf-8"))
    required = {
        "level",
        "dual_reviewed_count",
        "expert_a_count",
        "expert_b_count",
        "verified_real_count",
        "data_gap",
        "priority",
        "minimum_target",
        "remaining_needed",
        "status",
    }
    assert len(data["rows"]) == len(LEVELS)
    for row in data["rows"]:
        assert required.issubset(row.keys())
        assert row["level"] in LEVELS
        assert row["minimum_target"] == 5


def test_queue_uses_acq_not_cal_placeholders() -> None:
    text = (ROOT / "ROUND_3_QUEUE.md").read_text(encoding="utf-8")
    assert "ACQ-R3-001" in text
    assert "ACQUISITION_TARGET_ONLY" in text
    # no fabricated CAL case folders
    assert list(CASES.glob("CAL-*")) == []
    assert "CAL-000008" in text  # mentioned as next free, not created


def test_validation_records_zero_new_cases() -> None:
    data = json.loads((VALIDATION / "VALIDATION.json").read_text(encoding="utf-8"))
    assert data["new_real_cases_acquired"] == 0
    assert data["new_verified_cases"] == 0
    assert data["new_dual_reviewed_cases"] == 0
    assert data["existing_dual_reviewed_cases"] == 2
    assert data["final_decision"] == "CALIBRATION_PARTIAL"
    assert data["readiness"] == "DATA_GAP"


def test_status_doc_aligns() -> None:
    text = (ROOT / "ROUND_3_STATUS.md").read_text(encoding="utf-8")
    assert "CALIBRATION_PARTIAL" in text
    assert "DATA_GAP" in text
    assert "CAL-000008" in text
