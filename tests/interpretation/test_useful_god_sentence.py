"""Interpretation must not emit a false Useful God missing-status."""

from __future__ import annotations

from engines.interpretation_engine.legacy_builder import InterpretationBuilder


def test_present_useful_god_does_not_emit_missing_contradiction() -> None:
    """I. Present Useful God must not render 'Đinh (Không có Dụng thần)'."""
    builder = InterpretationBuilder()
    sections = builder.seed_sections()
    builder._enrich_from_context(
        sections,
        {
            "useful_god": {
                "name": "Đinh",
                "status": "Không có Dụng thần",
            }
        },
    )
    texts = [str(rule.get("sentence") or "") for rule in sections["useful_god"].rules]
    assert texts
    assert all("Không có Dụng thần" not in text for text in texts)
    assert any(text.startswith("Dụng thần: Đinh") for text in texts)


def test_present_status_is_kept_when_accurate() -> None:
    """Accurate location status may still appear next to the selected name."""
    builder = InterpretationBuilder()
    sections = builder.seed_sections()
    builder._enrich_from_context(
        sections,
        {
            "useful_god": {
                "name": "Đinh",
                "status": "Dụng thần xuất hiện Thiên Can",
            }
        },
    )
    texts = [str(rule.get("sentence") or "") for rule in sections["useful_god"].rules]
    assert texts == ["Dụng thần: Đinh (Dụng thần xuất hiện Thiên Can)."]
