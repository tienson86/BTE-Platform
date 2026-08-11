"""Adjudication protocol: preserve originals, no manufactured consensus."""

from __future__ import annotations

from .helpers import ROOT


def test_adjudication_preserves_originals() -> None:
    text = (ROOT / "ADJUDICATION_PROTOCOL.md").read_text(encoding="utf-8")
    for token in (
        "expert_a original",
        "expert_b original",
        "disagreement",
        "adjudicator judgment",
        "Never overwrite original expert judgments",
    ):
        assert token in text


def test_no_manufactured_consensus() -> None:
    text = (ROOT / "ADJUDICATION_PROTOCOL.md").read_text(encoding="utf-8")
    assert "Never manufacture consensus" in text
    assert "Never choose runtime label" in text


def test_adjudication_only_when_material() -> None:
    text = (ROOT / "ADJUDICATION_PROTOCOL.md").read_text(encoding="utf-8")
    assert "disagree materially" in text or "flagged ambiguous" in text
