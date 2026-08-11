"""Source verification workflow tests."""

from __future__ import annotations

from .helpers import ROOT, TEMPLATES, load_json


def test_source_template_fields() -> None:
    data = load_json(TEMPLATES / "source_verification.json")
    for field in (
        "source_type",
        "source_authorization",
        "source_reliability",
        "source_reference",
        "source_notes",
        "verification_status",
    ):
        assert field in data


def test_source_statuses_documented() -> None:
    text = (ROOT / "SOURCE_VERIFICATION.md").read_text(encoding="utf-8")
    for status in ("verified", "partially_verified", "unverified", "rejected"):
        assert status in text
