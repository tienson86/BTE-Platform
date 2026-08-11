"""Eligibility rules tests."""

from __future__ import annotations

from .helpers import ROOT


def test_eligibility_checklist() -> None:
    text = (ROOT / "ELIGIBILITY_RULES.md").read_text(encoding="utf-8")
    for fragment in (
        "source is authorized",
        "birth date",
        "birth time",
        "birth place",
        "timezone",
        "calendar is verified",
        "not synthetic",
        "not duplicated",
        "privacy",
    ):
        assert fragment.lower() in text.lower()


def test_eligibility_report_required() -> None:
    text = (ROOT / "ELIGIBILITY_RULES.md").read_text(encoding="utf-8")
    assert "eligibility report" in text.lower()
