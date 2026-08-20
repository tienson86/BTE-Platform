"""G1-06 Useful God overlay, flow predicate, mapping, and CASE-0001 winner."""

from __future__ import annotations

from applications.api.services.orchestrator import OrchestratorService
from engines.bazi_engine.engine import BaziEngine
from engines.bazi_engine.ten_god import stem_element, stem_for_ten_god, ten_god_name
from engines.calendar_engine.engine import CalendarEngine
from engines.pattern_engine.engine import PatternEngine
from engines.pattern_engine.utils.context_builder import build_pattern_context
from engines.strength_engine.engine import StrengthEngine
from engines.strength_engine.utils.context_builder import build_strength_context
from engines.temperature_engine.engine import TemperatureEngine
from engines.temperature_engine.utils.context_builder import build_temperature_context
from engines.useful_god_engine.context import UsefulGodContext
from engines.useful_god_engine.engine import UsefulGodEngine
from engines.useful_god_engine.matcher import UsefulGodMatcher
from engines.useful_god_engine.priority import PriorityResolver
from engines.useful_god_engine.utils.context_builder import build_useful_god_context


def _case_0001_chart() -> tuple[object, object]:
    calendar = CalendarEngine().build(1987, 1, 21, 4, 30)
    chart = BaziEngine().build(calendar, gender="male")
    return calendar, chart


def _calculate(context: UsefulGodContext):
    return UsefulGodEngine().calculate(context)


def _candidate_ids(result) -> list[str]:
    return [str(item.get("rule_id") or "") for item in result.candidate_list]


def test_case_0001_overlay_reads_cold_not_score() -> None:
    calendar, chart = _case_0001_chart()
    strength = StrengthEngine().calculate(build_strength_context(chart, calendar=calendar))
    temperature = TemperatureEngine().calculate(
        build_temperature_context(
            chart,
            calendar=calendar,
            strength_level=strength.strength_level,
            strength_score=strength.strength_score,
        )
    )
    assert abs(float(temperature.temperature_score) - 0.72) < 0.02
    assert temperature.climate_state == "cold"
    assert temperature.useful_god_temperature_overlay() == "cold"
    assert temperature.useful_god_temperature_overlay() == temperature.to_pattern_temperature_type()
    assert temperature.useful_god_temperature_overlay() != "hot"
    pattern_context = build_pattern_context(chart, calendar=calendar)
    pattern_context.strength_level = strength.strength_level
    pattern_context.strength_score = strength.strength_score
    pattern_context.temperature_type = temperature.useful_god_temperature_overlay()
    pattern = PatternEngine().calculate(pattern_context)
    useful_context = build_useful_god_context(pattern_context, pattern)
    assert useful_context.temperature_type == "cold"
    assert useful_context.season == "winter"
    assert useful_context.strength_level == "strong"


def test_case_0001_candidate_set_and_winner() -> None:
    calendar, chart = _case_0001_chart()
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
    result = _calculate(build_useful_god_context(pattern_context, pattern))
    ids = _candidate_ids(result)
    assert ids == ["str_004", "sea_001", "tmp_001"]
    assert "tmp_002" not in ids
    assert not any(item.startswith("flo_") for item in ids)
    by_id = {item["rule_id"]: item for item in result.candidate_list}
    assert by_id["str_004"]["rule_group"] == "strength"
    assert by_id["str_004"]["useful_god"] == "Thực Thần"
    assert by_id["str_004"]["stem"] == "Nhâm"
    assert by_id["str_004"]["element"] == "Thủy"
    assert by_id["str_004"]["priority"] == 76
    assert by_id["sea_001"]["rule_group"] == "season"
    assert by_id["sea_001"]["useful_god"] == "Bính"
    assert by_id["sea_001"]["ten_god"] == "Thất Sát"
    assert by_id["sea_001"]["element"] == "Hỏa"
    assert by_id["tmp_001"]["useful_god"] == "Đinh"
    assert result.winning_rule_id == "sea_001"
    assert result.winning_rule_group == "season"
    assert result.useful_god == "Bính"
    assert result.useful_ten_god == "Thất Sát"
    assert result.useful_stem == "Bính"
    assert result.useful_element == "Hỏa"
    assert result.useful_display == "Hỏa · Bính · Thất Sát"
    assert result.favorable_gods == ["Bính", "Đinh", "Giáp"]
    assert result.unfavorable_gods == ["Nhâm", "Quý"]
    assert "Thực Thần" in result.unfavorable_display
    assert result.useful_ten_god != "Thực Thần"


def test_flow_predicate_evaluates_values_not_key_presence() -> None:
    matcher = UsefulGodMatcher()
    below = {"Mộc": 2, "Hỏa": 4, "Thổ": 5, "Kim": 3, "Thủy": 1}
    above = {"Mộc": 8, "Hỏa": 1, "Thổ": 1, "Kim": 1, "Thủy": 1}
    assert matcher.evaluate(below, "contains", "Thủy") is False
    assert matcher.evaluate(below, "contains", "Thổ") is True
    assert matcher.evaluate(above, "contains", "Mộc") is True
    assert matcher.evaluate(above, "contains", "Hỏa") is False
    tied = {"Mộc": 5, "Hỏa": 5, "Thổ": 1}
    assert matcher.evaluate(tied, "contains", "Mộc") is False
    assert matcher.evaluate(tied, "contains", "Hỏa") is False
    assert matcher.evaluate(["Chính Quan"], "contains", "Chính Quan") is True


def test_flow_element_below_and_above_unique_max() -> None:
    below = _calculate(
        UsefulGodContext(
            day_master="Canh",
            element_distribution={"Mộc": 2, "Hỏa": 4, "Thổ": 5, "Kim": 3, "Thủy": 1},
        )
    )
    assert not any(item.startswith("flo_") for item in _candidate_ids(below))
    above = _calculate(
        UsefulGodContext(
            day_master="Canh",
            element_distribution={"Mộc": 8, "Hỏa": 1, "Thổ": 1, "Kim": 1, "Thủy": 1},
        )
    )
    assert "flo_001" in _candidate_ids(above)
    assert "flo_004" not in _candidate_ids(above)


def test_strong_chart_selects_strength_fallback() -> None:
    result = _calculate(
        UsefulGodContext(
            day_master="Canh",
            strength_level="strong",
            season="spring",
            temperature_type="warm",
            element_distribution={"Mộc": 2, "Hỏa": 2, "Thổ": 2, "Kim": 2, "Thủy": 2},
        )
    )
    assert result.winning_rule_id == "str_004"
    assert result.useful_ten_god == "Thực Thần"
    assert result.useful_stem == "Nhâm"
    assert result.useful_element == "Thủy"


def test_weak_chart_selects_resource_or_fallback() -> None:
    with_resource = _calculate(
        UsefulGodContext(
            day_master="Canh",
            strength_level="weak",
            season="spring",
            temperature_type="warm",
            resource_elements=["Chính Ấn"],
            element_distribution={"Mộc": 2, "Hỏa": 2, "Thổ": 2, "Kim": 2, "Thủy": 2},
        )
    )
    assert with_resource.winning_rule_id == "str_001"
    assert with_resource.useful_ten_god == "Chính Ấn"
    without_resource = _calculate(
        UsefulGodContext(
            day_master="Canh",
            strength_level="weak",
            season="spring",
            temperature_type="warm",
            element_distribution={"Mộc": 2, "Hỏa": 2, "Thổ": 2, "Kim": 2, "Thủy": 2},
        )
    )
    assert without_resource.winning_rule_id == "str_002"
    assert without_resource.useful_ten_god == "Thiên Ấn"


def test_hot_climate_does_not_use_score_axis() -> None:
    result = _calculate(
        UsefulGodContext(
            day_master="Canh",
            strength_level="balanced",
            season="summer",
            temperature_type="hot",
            element_distribution={"Mộc": 2, "Hỏa": 2, "Thổ": 2, "Kim": 2, "Thủy": 2},
        )
    )
    assert result.winning_rule_id == "sea_002"
    assert result.useful_stem == "Nhâm"
    assert result.useful_element == "Thủy"
    assert result.useful_ten_god == "Thực Thần"


def test_cold_climate_seasonal_beats_temperature() -> None:
    result = _calculate(
        UsefulGodContext(
            day_master="Canh",
            strength_level="strong",
            season="winter",
            temperature_type="cold",
            element_distribution={"Mộc": 2, "Hỏa": 2, "Thổ": 2, "Kim": 2, "Thủy": 2},
        )
    )
    ids = _candidate_ids(result)
    assert "sea_001" in ids
    assert "str_004" in ids
    assert "tmp_001" in ids
    assert result.winning_rule_id == "sea_001"


def test_equal_priority_tie_is_deterministic() -> None:
    resolver = PriorityResolver([])
    first = {
        "rule_id": "flo_a",
        "rule_group": "flow",
        "score": 0.76,
        "priority": 74,
    }
    second = {
        "rule_id": "flo_b",
        "rule_group": "flow",
        "score": 0.76,
        "priority": 74,
    }
    winner = resolver.resolve([first, second])
    assert winner is not None
    assert winner["rule_id"] == "flo_a"
    again = resolver.resolve([first, second])
    assert again is not None and again["rule_id"] == winner["rule_id"]


def test_g1_01_mapping_reused_for_canh() -> None:
    assert ten_god_name("Canh", "Nhâm") == "Thực Thần"
    assert ten_god_name("Canh", "Quý") == "Thương Quan"
    assert ten_god_name("Canh", "Canh") == "Tỷ Kiên"
    assert ten_god_name("Canh", "Tân") == "Kiếp Tài"
    assert ten_god_name("Canh", "Bính") == "Thất Sát"
    assert stem_for_ten_god("Canh", "Thực Thần") == "Nhâm"
    assert stem_for_ten_god("Canh", "Thương Quan") == "Quý"
    assert stem_for_ten_god("Canh", "Tỷ Kiên") == "Canh"
    assert stem_for_ten_god("Canh", "Kiếp Tài") == "Tân"
    assert stem_element("Bính") == "Hỏa"
    mapped = _calculate(
        UsefulGodContext(day_master="Canh", strength_level="strong", season="spring")
    )
    assert mapped.useful_god == "Thực Thần"
    assert mapped.useful_stem == "Nhâm"
    assert mapped.useful_element == "Thủy"


def test_api_payload_publishes_rich_fields() -> None:
    payload = OrchestratorService().analyze(
        year=1987, month=1, day=21, hour=4, minute=30, gender="male"
    )
    useful = payload["useful_god"]
    temperature = payload["temperature"]
    assert abs(float(temperature["temperature_score"]) - 0.72) < 0.02
    assert temperature["climate_state"] == "cold"
    assert useful["useful_god"] == "Bính"
    assert useful["useful_display"] == "Hỏa · Bính · Thất Sát"
    assert useful["useful_ten_god"] == "Thất Sát"
    assert useful["useful_stem"] == "Bính"
    assert useful["useful_element"] == "Hỏa"
    assert useful["winning_rule_id"] == "sea_001"
    assert useful["favorable_display"].startswith("Hỏa · Bính · Thất Sát")
    assert useful["unfavorable_display"].startswith("Thủy · Nhâm · Thực Thần")
    assert payload["useful_god_source"]["contract"] == "analysis_result.UsefulGodView@1.1"
    assert payload["strength"]["strength_level"] == "strong"
    assert payload["pattern"]["cach_cuc"] == "Chính Ấn"
