"""Synthetic expectation audit tests for PILOT-1H."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
SYN_DIR = ROOT.parents[1] / "synthetic_strength" / "datasets"


def test_synthetic_audit_covers_21() -> None:
    data = json.loads((REPORTS / "synthetic_audit.json").read_text(encoding="utf-8"))
    assert data["cases_audited"] == 21
    assert data["promoted_to_calibration"] is False
    assert data["fixtures_modified"] is False


def test_review_flags_documented_not_applied_to_fixtures() -> None:
    data = json.loads((REPORTS / "synthetic_audit.json").read_text(encoding="utf-8"))
    flagged = set(data["review_flagged"])
    assert flagged
    # Fixtures still contain original expectations; audit did not rewrite them.
    for case_id in flagged:
        path = SYN_DIR / f"{case_id}.json"
        case = json.loads(path.read_text(encoding="utf-8"))
        assert case["case_id"] == case_id
        assert case["synthetic_expected_taxonomy"]
        assert case["calibration_eligible"] is False
        assert case["golden_eligible"] is False


def test_audit_markdown_has_review_marker() -> None:
    text = (ROOT / "SYNTHETIC_EXPECTATION_AUDIT.md").read_text(encoding="utf-8")
    assert "SYNTHETIC_EXPECTATION_REVIEW" in text
    assert "Do not promote" in text or "not expert truth" in text.lower()


def test_no_cal_prefix_in_synthetic_audit_ids() -> None:
    data = json.loads((REPORTS / "synthetic_audit.json").read_text(encoding="utf-8"))
    for case_id in data["review_flagged"]:
        assert case_id.startswith("SYN-STR-")
        assert not case_id.startswith("CAL-")
