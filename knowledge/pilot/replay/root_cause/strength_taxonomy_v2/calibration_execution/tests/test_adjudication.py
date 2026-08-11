"""Adjudication execution tests."""

from __future__ import annotations

from .helpers import ROOT, TEMPLATES, load_json


def test_adjudication_preserves_originals() -> None:
    text = (ROOT / "ADJUDICATION_EXECUTION.md").read_text(encoding="utf-8")
    for token in (
        "Expert-A original",
        "Expert-B original",
        "disagreement",
        "adjudicator",
        "Never overwrite original judgments",
    ):
        assert token in text


def test_adjudication_template() -> None:
    data = load_json(TEMPLATES / "adjudication_record.json")
    assert data["required"] is False
    assert "expert_a_original" in data
    assert "expert_b_original" in data
    assert "unresolved_questions" in data
    assert "Never overwrite" in data["notes"]
