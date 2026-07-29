"""Production-aligned engine stack for Phase 3–6 unified ViewModel tests.

Mirrors OrchestratorService Stage 3.5 → 5 (strength → temperature → pattern →
useful-god overlay) so engine helpers agree with API / orchestrator payloads.
"""

from __future__ import annotations

from typing import Any

from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.engine import CalendarEngine
from engines.interpretation_engine.engine import InterpretationEngine
from engines.pattern_engine.engine import PatternEngine, PatternResult
from engines.pattern_engine.rule_context_bridge import (
    enrich_result_from_rule_context,
    enrich_rule_context_summaries,
    merge_upstream_into_rule_context,
)
from engines.pattern_engine.utils.context_builder import build_pattern_context
from engines.score_engine.engine import ScoreEngine
from engines.score_engine.result import ScoreResult
from engines.strength_engine.engine import StrengthEngine
from engines.strength_engine.utils.context_builder import build_strength_context
from engines.temperature_engine.engine import TemperatureEngine
from engines.temperature_engine.utils.context_builder import build_temperature_context
from engines.useful_god_engine.engine import UsefulGodEngine
from engines.useful_god_engine.utils.context_builder import build_useful_god_context

CRITICAL = {
    "year": 1987,
    "month": 1,
    "day": 21,
    "hour": 4,
    "minute": 30,
    "gender": "male",
}


def _birth_calendar_chart() -> tuple[Any, Any]:
    calendar = CalendarEngine().build(
        CRITICAL["year"],
        CRITICAL["month"],
        CRITICAL["day"],
        CRITICAL["hour"],
        CRITICAL["minute"],
    )
    chart = BaziEngine().build(calendar, gender=CRITICAL["gender"])
    return calendar, chart


def production_pattern_stage() -> tuple[PatternResult, Any, Any]:
    """
    Pattern stage parity with orchestrator stop_at=pattern.

    Strength / temperature feed PatternContext; useful-god is computed but not
    merged into PatternResult (Stage 5 only).
    """
    calendar, chart = _birth_calendar_chart()
    pattern_context = build_pattern_context(chart, calendar=calendar)

    strength_result = StrengthEngine().calculate(
        build_strength_context(chart, calendar=calendar)
    )
    pattern_context.strength_level = strength_result.strength_level
    pattern_context.strength_score = strength_result.strength_score

    temperature_result = TemperatureEngine().calculate(
        build_temperature_context(
            chart,
            calendar=calendar,
            strength_level=strength_result.strength_level,
            strength_score=strength_result.strength_score,
        )
    )
    pattern_context.temperature_type = temperature_result.to_pattern_temperature_type()

    pattern = PatternEngine().calculate(pattern_context)
    return pattern, chart, calendar


def production_rule_context() -> tuple[dict[str, Any], Any, PatternResult]:
    """Stage 5 RuleContext: Pattern-published RC + useful-god / strength / temp."""
    calendar, chart = _birth_calendar_chart()
    pattern_context = build_pattern_context(chart, calendar=calendar)

    strength_result = StrengthEngine().calculate(
        build_strength_context(chart, calendar=calendar)
    )
    pattern_context.strength_level = strength_result.strength_level
    pattern_context.strength_score = strength_result.strength_score

    temperature_result = TemperatureEngine().calculate(
        build_temperature_context(
            chart,
            calendar=calendar,
            strength_level=strength_result.strength_level,
            strength_score=strength_result.strength_score,
        )
    )
    pattern_context.temperature_type = temperature_result.to_pattern_temperature_type()

    pattern = PatternEngine().calculate(pattern_context)
    useful_god_result = UsefulGodEngine().calculate(
        build_useful_god_context(pattern_context, pattern)
    )

    rule_context = dict(pattern.rule_context or {})
    merge_upstream_into_rule_context(
        rule_context,
        useful_god=useful_god_result,
        strength=strength_result,
        temperature=temperature_result,
    )
    enrich_rule_context_summaries(rule_context, pattern=pattern)
    enrich_result_from_rule_context(pattern, rule_context)
    return rule_context, chart, pattern


def production_score_stage() -> tuple[dict[str, Any], ScoreResult, Any, PatternResult]:
    rule_context, chart, pattern = production_rule_context()
    score = ScoreEngine().calculate(rule_context)
    ScoreEngine().append_score_to_rule_context(rule_context, score)
    return rule_context, score, chart, pattern


def production_interpretation_stage() -> tuple[Any, dict[str, Any], Any, PatternResult, ScoreResult]:
    rule_context, score, chart, pattern = production_score_stage()
    interpretation = InterpretationEngine().run(rule_context)
    return interpretation, rule_context, chart, pattern, score
