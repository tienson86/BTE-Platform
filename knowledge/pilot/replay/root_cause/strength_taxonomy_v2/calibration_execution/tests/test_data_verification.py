"""Data verification precision rules."""

from __future__ import annotations

from .helpers import ROOT, TEMPLATES, load_json


def test_data_template_precision_fields() -> None:
    data = load_json(TEMPLATES / "data_verification.json")
    assert "time_precision" in data
    assert "date_precision" in data
    assert "place_precision" in data
    assert "approximate" in data["notes"] or "exact" in data["notes"]


def test_no_silent_time_conversion_rule() -> None:
    text = (ROOT / "DATA_VERIFICATION.md").read_text(encoding="utf-8")
    assert "Do not silently convert approximate time into exact time" in text
    for token in ("exact", "approximate", "unknown"):
        assert token in text
