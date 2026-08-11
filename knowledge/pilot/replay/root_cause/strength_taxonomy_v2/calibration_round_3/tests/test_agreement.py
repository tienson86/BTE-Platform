"""Agreement protocol categories."""

from __future__ import annotations

from .helpers import ROOT


def test_agreement_categories() -> None:
    text = (ROOT / "AGREEMENT_PROTOCOL.md").read_text(encoding="utf-8")
    for cat in ("exact_match", "adjacent_level", "non_adjacent", "conflicting"):
        assert cat in text


def test_adjacent_not_auto_agreement() -> None:
    text = (ROOT / "AGREEMENT_PROTOCOL.md").read_text(encoding="utf-8")
    assert "Do not convert adjacent_level into agreement automatically" in text


def test_confidence_tracked_separately() -> None:
    text = (ROOT / "AGREEMENT_PROTOCOL.md").read_text(encoding="utf-8")
    assert "Confidence agreement" in text or "confidence agreement" in text.lower()
