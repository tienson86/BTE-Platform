"""Expert-B blinding requirements."""

from __future__ import annotations

from .helpers import ROOT


def test_expert_b_blinding_checklist() -> None:
    text = (ROOT / "EXPERT_B_TEMPLATE.md").read_text(encoding="utf-8")
    for item in (
        "Expert-A label hidden",
        "Expert-A rationale hidden",
        "runtime score hidden",
        "runtime v1 band hidden",
        "taxonomy thresholds hidden",
        "adjudication result hidden",
    ):
        assert item in text


def test_blinding_mentioned_in_protocol_context() -> None:
    # Round-3 docs must state Expert-B receives verified chart + protocol only.
    text = (ROOT / "EXPERT_B_TEMPLATE.md").read_text(encoding="utf-8")
    assert "verified chart" in text.lower()
    assert "review protocol" in text.lower()
