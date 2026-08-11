"""Calendar verification workflow tests."""

from __future__ import annotations

from .helpers import ROOT, TEMPLATES, load_json


def test_calendar_template_fields() -> None:
    data = load_json(TEMPLATES / "calendar_verification.json")
    for field in (
        "year_pillar",
        "month_pillar",
        "day_pillar",
        "hour_pillar",
        "solar_term_boundary_checked",
        "solar_term_ambiguity",
        "timezone_verified",
        "local_time_interpretation",
        "calendar_status",
    ):
        assert field in data


def test_calendar_statuses_and_ambiguity_gate() -> None:
    text = (ROOT / "CALENDAR_VERIFICATION.md").read_text(encoding="utf-8")
    for status in ("verified", "partially_verified", "ambiguous", "unverified", "rejected"):
        assert status in text
    assert "solar-term" in text.lower() or "solar_term" in text
