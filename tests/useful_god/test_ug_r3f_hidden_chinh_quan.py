"""UG-R3F — hidden Chính Quan reachability for str_003. No new theory."""

from __future__ import annotations

from applications.api.services.orchestrator import OrchestratorService
from engines.bazi_engine.engine import BaziEngine
from engines.bazi_engine.ten_god import ten_god_name
from engines.calendar_engine.engine import CalendarEngine
from engines.pattern_engine.engine import PatternEngine
from engines.pattern_engine.utils.context_builder import build_pattern_context
from engines.strength_engine.engine import StrengthEngine
from engines.strength_engine.utils.context_builder import build_strength_context
from engines.temperature_engine.engine import TemperatureEngine
from engines.temperature_engine.utils.context_builder import build_temperature_context
from engines.useful_god_engine.engine import UsefulGodEngine
from engines.useful_god_engine.utils.context_builder import build_useful_god_context


def _tuyen_pipeline():
    calendar = CalendarEngine().build(1984, 7, 13, 21, 1)
    chart = BaziEngine().build(calendar, gender="female")
    strength = StrengthEngine().calculate(build_strength_context(chart, calendar=calendar))
    temperature = TemperatureEngine().calculate(
        build_temperature_context(
            chart,
            calendar=calendar,
            strength_level=strength.strength_level,
            strength_score=strength.strength_score,
        )
    )
    pattern_context = build_pattern_context(chart, calendar=calendar)
    pattern_context.strength_level = strength.strength_level
    pattern_context.strength_score = strength.strength_score
    pattern_context.temperature_type = temperature.useful_god_temperature_overlay()
    pattern = PatternEngine().calculate(pattern_context)
    useful_context = build_useful_god_context(pattern_context, pattern)
    result = UsefulGodEngine().calculate(useful_context)
    return chart, pattern_context, useful_context, result


def test_str_003_token_unchanged() -> None:
    from engines.useful_god_engine.engine import DEFAULT_DATABASE_PATH
    from engines.useful_god_engine.loader import UsefulGodLoader

    rules = UsefulGodLoader(DEFAULT_DATABASE_PATH).load_rule_groups()["strength"]
    str_003 = next(item for item in rules if item["rule_id"] == "str_003")
    assert str_003["useful_god"] == "Chính Quan"
    assert str_003["priority"] == 82
    conditions = str_003["conditions"]
    if isinstance(conditions, str):
        import json

        conditions = json.loads(conditions)
    officer = next(item for item in conditions if item["field"] == "officer_elements")
    assert officer["value"] == "Chính Quan"
    assert officer["value"] != "Thất Sát"


def test_pattern_officer_elements_remain_visible_only() -> None:
    _, pattern_context, useful_context, _ = _tuyen_pipeline()
    assert "Chính Quan" not in pattern_context.officer_elements
    assert "Thất Sát" in pattern_context.officer_elements
    assert useful_context.officer_elements.count("Chính Quan") == 1
    assert "Chính Quan" in useful_context.officer_elements


def test_tuyen_hidden_at_is_chinh_quan() -> None:
    chart, pattern_context, useful_context, result = _tuyen_pipeline()
    assert chart.day_master == "Mậu"
    assert ten_god_name("Mậu", "Ất") == "Chính Quan"
    assert "Ất" in pattern_context.month_hidden_stems
    hidden = [
        item
        for item in useful_context.officer_provenance
        if item["visibility"] == "hidden" and item["stem"] == "Ất"
    ]
    assert hidden
    assert hidden[0]["branch"] == "Mùi"
    assert hidden[0]["pillar"] == "month"
    ids = [str(item.get("rule_id") or "") for item in result.overall_candidate_list]
    assert ids.count("str_003") == 1
    assert "str_003" in ids
    assert "str_004" in ids
    assert result.winning_rule_id == "str_003"
    assert result.useful_ten_god == "Chính Quan"
    assert result.useful_stem == "Ất"
    assert result.useful_element == "Mộc"
    assert result.favorable_gods == ["Chính Quan", "Thực Thần"]
    assert result.unfavorable_gods == ["Tỷ Kiên", "Kiếp Tài"]
    assert result.climate_rule_id == "sea_002"
    assert result.climate_element == "Thủy"
    assert result.winning_rule_group not in {"season", "temperature"}


def test_visible_plus_hidden_does_not_duplicate_officer_token() -> None:
    calendar = CalendarEngine().build(1987, 1, 21, 4, 30)
    chart = BaziEngine().build(calendar, gender="male")
    pattern_context = build_pattern_context(chart, calendar=calendar)
    pattern_context.officer_elements = ["Chính Quan", "Thất Sát"]
    useful_context = build_useful_god_context(pattern_context)
    assert useful_context.officer_elements.count("Chính Quan") == 1


def test_api_tuyen_hy_ky_follow_new_winner() -> None:
    payload = OrchestratorService().analyze(
        year=1984, month=7, day=13, hour=21, minute=1, gender="female"
    )
    useful = payload["useful_god"]
    assert useful["winning_rule_id"] == "str_003"
    assert useful["useful_display"] == "Mộc · Ất · Chính Quan"
    assert useful["favorable_gods"] == ["Chính Quan", "Thực Thần"]
    assert useful["unfavorable_gods"] == ["Tỷ Kiên", "Kiếp Tài"]
    assert "Thực Thần" in useful["favorable_display"]
    assert "Tỷ Kiên" in useful["unfavorable_display"]
    assert useful["climate_rule_id"] == "sea_002"
    assert useful["useful_god"] != useful["climate_candidate"]
    assert abs(float(payload["strength"]["strength_score"]) - 0.66) < 0.02
    assert payload["strength"]["strength_level"] == "strong"
    assert payload["pattern"]["cach_cuc"] == "Kiếp Tài"
