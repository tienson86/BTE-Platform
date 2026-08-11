"""Agreement execution tests."""

from __future__ import annotations

from .helpers import ROOT, TEMPLATES, load_json


def test_agreement_categories() -> None:
    text = (ROOT / "AGREEMENT_EXECUTION.md").read_text(encoding="utf-8")
    for cat in ("exact_match", "adjacent_level", "non_adjacent", "conflicting"):
        assert cat in text
    assert "Do **not** automatically convert `adjacent_level` into agreement" in text or (
        "Do not automatically convert" in text and "adjacent_level" in text
    )


def test_agreement_template() -> None:
    data = load_json(TEMPLATES / "agreement_record.json")
    assert "label_agreement" in data
    assert "confidence_agreement" in data
    assert "adjacent_level" in data["notes"]
