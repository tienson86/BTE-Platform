"""Expert review protocol completeness."""

from __future__ import annotations

from .helpers import ROOT


def test_protocol_has_seven_questions() -> None:
    text = (ROOT / "EXPERT_REVIEW_PROTOCOL.md").read_text(encoding="utf-8")
    for fragment in (
        "Overall Strength level",
        "supporting factors",
        "opposing factors",
        "boundary",
        "Structural conflicts",
        "Confidence",
        "would change",
    ):
        assert fragment.lower() in text.lower() or fragment in text


def test_candidate_vocabulary_present() -> None:
    text = (ROOT / "EXPERT_REVIEW_PROTOCOL.md").read_text(encoding="utf-8")
    for level in (
        "very_weak",
        "weak",
        "slightly_weak",
        "balanced",
        "slightly_strong",
        "strong",
        "very_strong",
    ):
        assert level in text


def test_templates_require_core_fields() -> None:
    for name in ("EXPERT_A_TEMPLATE.md", "EXPERT_B_TEMPLATE.md"):
        text = (ROOT / name).read_text(encoding="utf-8")
        for field in (
            "strength_level",
            "confidence",
            "rationale",
            "key_supporting_evidence",
            "key_opposing_evidence",
            "boundary_notes",
            "uncertainty_notes",
        ):
            assert field in text


def test_protocol_does_not_require_runtime_match() -> None:
    text = (ROOT / "EXPERT_REVIEW_PROTOCOL.md").read_text(encoding="utf-8")
    assert "Do not instruct experts to match runtime" in text
    assert "NOT runtime taxonomy" in text
