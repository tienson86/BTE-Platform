"""No fabricated cases or expert judgments."""

from __future__ import annotations

import re

from .helpers import EXECUTION, PACKETS, REPORTS, ROOT, TEMPLATES, VALIDATION, load_json

FORBIDDEN_HAN = re.compile(r"[\u4e00-\u9fff]")


def test_no_cal_case_files_created() -> None:
    assert list(ROOT.rglob("CAL-*.json")) == []
    assert list(PACKETS.rglob("*.json")) == []
    assert list(EXECUTION.rglob("*.json")) == []


def test_templates_are_empty_shells_not_filled_judgments() -> None:
    a = load_json(TEMPLATES / "expert_a_review.json")
    b = load_json(TEMPLATES / "expert_b_review.json")
    assert a["strength_level"] is None
    assert b["strength_level"] is None
    assert a["rationale"] is None
    assert b["rationale"] is None


def test_summary_status_block() -> None:
    text = (ROOT / "PILOT_1M_SUMMARY.md").read_text(encoding="utf-8")
    assert "NEW_REAL_CASES_ACQUIRED: 0" in text
    assert "NEW_DUAL_REVIEWED_CASES: 0" in text
    assert "EXISTING_DUAL_REVIEWED_CASES: 2" in text
    assert "NO_DATA_CONTINGENCY_VALIDATED: YES" in text
    assert "BLINDING_VALIDATED: YES" in text
    assert "Final Decision:\nCALIBRATION_PARTIAL" in text
    assert "CALIBRATION_COMPLETE" not in text.split("Final Decision:")[-1]


def test_no_han_in_machine_readable_json() -> None:
    for path in ROOT.rglob("*.json"):
        assert FORBIDDEN_HAN.search(path.read_text(encoding="utf-8")) is None, path


def test_validation_no_fabrication() -> None:
    data = load_json(VALIDATION / "VALIDATION.json")
    assert data["no_fabricated_cases"] is True
    assert data["no_fabricated_expert_judgments"] is True


def test_intake_status_zero() -> None:
    data = load_json(REPORTS / "intake_status.json")
    assert data["intake_records_received"] == 0
    assert data["status"] == "no_data"
