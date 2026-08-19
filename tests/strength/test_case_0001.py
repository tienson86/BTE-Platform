"""CASE-0001 canonical Strength Engine golden."""

from __future__ import annotations

from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.engine import CalendarEngine
from engines.strength_engine.engine import StrengthEngine
from engines.strength_engine.labels import strength_level_label
from engines.strength_engine.utils.context_builder import build_strength_context


def test_case_0001_canonical_strength_score() -> None:
    """Live CASE-0001 must keep raw 37 and public score 0.87."""
    calendar = CalendarEngine().build(1987, 1, 21, 4, 30)
    chart = BaziEngine().build(calendar, gender="male")
    result = StrengthEngine().calculate(build_strength_context(chart, calendar=calendar))
    trace = result.metadata["trace"]["scoring"]

    assert result.success
    assert trace["raw_total"] == 37.0
    assert result.raw_total == 37.0
    assert abs(result.strength_score - 0.87) < 0.001
    assert result.strength_level == "strong"
    assert strength_level_label(result.strength_level) == "Thân vượng"
    assert abs(result.confidence - 1.0) < 0.001
    assert "spc_004" in result.matched_rules
    assert result.evidence_compact
    assert "Ấn mùa lạnh" in result.evidence_compact
