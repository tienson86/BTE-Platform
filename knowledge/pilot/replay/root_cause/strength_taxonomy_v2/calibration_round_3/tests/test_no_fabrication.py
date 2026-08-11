"""No fabricated cases, expert judgments, or taxonomy implementation."""

from __future__ import annotations

import json
import re

from .helpers import CASES, EXPERT, ROOT, VALIDATION

FORBIDDEN_HAN = re.compile(r"[\u4e00-\u9fff]")
FORBIDDEN_RUNTIME = [
    re.compile(r"def\s+classify_taxonomy_v2\b"),
    re.compile(r"TAXONOMY_V2_THRESHOLDS\s*="),
    re.compile(r"\bT1\s*=\s*0\."),
    re.compile(r"\bT6\s*=\s*0\."),
]


def test_no_cal_case_json_fabricated() -> None:
    assert list(CASES.rglob("*.json")) == []


def test_no_expert_judgment_files_fabricated() -> None:
    assert list(EXPERT.rglob("*.json")) == []
    # only README allowed for now
    files = [p for p in EXPERT.rglob("*") if p.is_file()]
    assert all(p.name == "README.md" for p in files)


def test_validation_flags_no_fabrication() -> None:
    data = json.loads((VALIDATION / "VALIDATION.json").read_text(encoding="utf-8"))
    assert data["no_fabricated_cases"] is True
    assert data["no_fabricated_expert_judgments"] is True
    assert data["taxonomy_v2_implemented"] is False
    assert data["t1_t6_frozen"] is False
    assert data["production_code_changed"] is False


def test_summary_status_block() -> None:
    text = (ROOT / "PILOT_1L_SUMMARY.md").read_text(encoding="utf-8")
    assert "NEW_REAL_CASES_ACQUIRED: 0" in text
    assert "NEW_VERIFIED_CASES: 0" in text
    assert "NEW_DUAL_REVIEWED_CASES: 0" in text
    assert "EXISTING_DUAL_REVIEWED_CASES: 2" in text
    assert "Final Decision:\nCALIBRATION_PARTIAL" in text
    assert "TAXONOMY_V2_IMPLEMENTED: NO" in text
    assert "T1_T6_FROZEN: NO" in text
    assert "PRODUCTION_CODE_CHANGED: NO" in text
    assert "CALIBRATION_COMPLETE" not in text.split("Final Decision:")[-1]


def test_no_han_in_machine_readable_json() -> None:
    for path in ROOT.rglob("*.json"):
        text = path.read_text(encoding="utf-8")
        assert FORBIDDEN_HAN.search(text) is None, path


def test_no_taxonomy_runtime_in_round3_python() -> None:
    for path in ROOT.rglob("*.py"):
        if "tests" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_RUNTIME:
            assert pattern.search(text) is None, (path, pattern.pattern)


def test_privacy_guide_forbids_pii() -> None:
    text = (ROOT / "PRIVACY_GUIDE.md").read_text(encoding="utf-8")
    for token in ("full names", "phone", "email", "government"):
        assert token.lower() in text.lower()


def test_calendar_guide_requires_verified_status() -> None:
    text = (ROOT / "CALENDAR_VERIFICATION_GUIDE.md").read_text(encoding="utf-8")
    assert "calendar_verified" in text
    assert "calendar_unverified" in text
    assert "solar-term" in text.lower() or "solar_term" in text
