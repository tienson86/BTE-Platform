"""G1-05 canonical Five Elements structural distribution (19-count)."""

from __future__ import annotations

from applications.api.services.five_elements_truth import build_five_elements_payload
from applications.api.services.orchestrator import OrchestratorService
from engines.bazi_engine.engine import HIDDEN, BaziChart, BaziEngine, Pillar
from engines.calendar_engine.engine import CalendarEngine
from engines.pattern_engine.utils.context_builder import build_pattern_context
from engines.rule_contract.context_builder import (
    BRANCH_ELEMENT,
    STEM_ELEMENT,
    RuleContextBuilder,
)
from engines.strength_engine.utils.context_builder import build_strength_context
from engines.useful_god_engine.utils.context_builder import build_useful_god_context


def _case_0001_chart() -> tuple[object, object]:
    calendar = CalendarEngine().build(1987, 1, 21, 4, 30)
    chart = BaziEngine().build(calendar, gender="male")
    return calendar, chart


def _counts(chart: object, calendar: object | None = None) -> dict[str, int]:
    context = RuleContextBuilder().build(calendar=calendar, bazi=chart)
    return dict(context["wuxing"]["counts"])


def test_case_0001_exact_counts() -> None:
    calendar, chart = _case_0001_chart()
    counts = _counts(chart, calendar)
    assert counts == {"wood": 4, "fire": 5, "earth": 6, "metal": 3, "water": 1}
    assert sum(counts.values()) == 19


def test_total_invariant_equals_stems_branches_hidden() -> None:
    calendar, chart = _case_0001_chart()
    counts = _counts(chart, calendar)
    hidden = list(getattr(chart, "hidden_stems") or [])
    assert len(list(chart.pillars)) == 4
    assert sum(counts.values()) == 8 + len(hidden)
    assert len(hidden) == 11


def test_case_0001_reconstruction_matches_visible_branch_hidden() -> None:
    calendar, chart = _case_0001_chart()
    stems = [pillar.stem for pillar in chart.pillars]
    branches = [pillar.branch for pillar in chart.pillars]
    hidden = list(chart.hidden_stems)
    assert stems == ["Bính", "Tân", "Canh", "Mậu"]
    assert branches == ["Dần", "Sửu", "Ngọ", "Dần"]
    assert hidden == [
        "Giáp",
        "Bính",
        "Mậu",
        "Kỷ",
        "Quý",
        "Tân",
        "Đinh",
        "Kỷ",
        "Giáp",
        "Bính",
        "Mậu",
    ]
    rebuilt = {"wood": 0, "fire": 0, "earth": 0, "metal": 0, "water": 0}
    for stem in stems:
        rebuilt[STEM_ELEMENT[stem]] += 1
    for branch in branches:
        rebuilt[BRANCH_ELEMENT[branch]] += 1
    for item in hidden:
        rebuilt[STEM_ELEMENT[item]] += 1
    assert rebuilt == _counts(chart, calendar)
    assert rebuilt == {"wood": 4, "fire": 5, "earth": 6, "metal": 3, "water": 1}


def test_duplicated_branches_remain_deterministic() -> None:
    calendar, chart = _case_0001_chart()
    branches = [pillar.branch for pillar in chart.pillars]
    assert branches.count("Dần") == 2
    first = _counts(chart, calendar)
    second = _counts(chart, calendar)
    assert first == second
    assert chart.hidden_stems.count("Giáp") == 2
    assert chart.hidden_stems.count("Bính") == 2
    assert chart.hidden_stems.count("Mậu") == 2


def test_repeated_hidden_stems_counted_per_occurrence() -> None:
    _, chart = _case_0001_chart()
    assert chart.hidden_stems.count("Kỷ") == 2
    earth_from_hidden = sum(
        1 for stem in chart.hidden_stems if STEM_ELEMENT[stem] == "earth"
    )
    assert earth_from_hidden == 4


def test_zero_count_element_is_structural_absence() -> None:
    chart = BaziChart(
        year_pillar=Pillar("Giáp", "Dần"),
        month_pillar=Pillar("Ất", "Mão"),
        day_pillar=Pillar("Bính", "Ngọ"),
        hour_pillar=Pillar("Đinh", "Tỵ"),
        hidden_stems=[
            *HIDDEN["Dần"],
            *HIDDEN["Mão"],
            *HIDDEN["Ngọ"],
            *HIDDEN["Tỵ"],
        ],
    )
    counts = _counts(chart)
    payload = build_five_elements_payload({"counts": counts})
    assert counts["water"] == 0
    assert "water" in payload["missing"]
    assert payload["counts"]["water"] == 0
    assert payload["unit_total"] == sum(counts.values())


def test_wuxing_score_does_not_override_counts() -> None:
    payload = OrchestratorService().analyze(
        year=1987, month=1, day=21, hour=4, minute=30, gender="male"
    )
    counts = payload["five_elements"]["counts"]
    assert counts == {"wood": 4, "fire": 5, "earth": 6, "metal": 3, "water": 1}
    assert payload["five_elements"]["unit_total"] == 19
    assert payload["five_elements"]["method_note"] == (
        "Tính theo Thiên can · bản hành Địa chi · Tàng can"
    )
    assert float(payload["score"]["wuxing_score"]) == 0.0
    assert payload["score"]["grade"]
    assert payload["score"]["grade"] not in str(payload["five_elements"]["counts"])


def test_analytical_15_tally_is_not_customer_distribution() -> None:
    calendar, chart = _case_0001_chart()
    pattern_ctx = build_pattern_context(chart, calendar=calendar)
    strength_ctx = build_strength_context(chart, calendar=calendar)
    useful_ctx = build_useful_god_context(pattern_ctx)
    customer = sum(_counts(chart, calendar).values())
    pattern_total = sum(pattern_ctx.element_distribution.values())
    strength_total = sum(strength_ctx.element_distribution.values())
    useful_total = sum(useful_ctx.element_distribution.values())
    assert customer == 19
    assert pattern_total == 15
    assert useful_total == 15
    assert strength_total != customer
    assert customer != pattern_total


def test_strength_pattern_temperature_ten_gods_useful_god_unchanged() -> None:
    payload = OrchestratorService().analyze(
        year=1987, month=1, day=21, hour=4, minute=30, gender="male"
    )
    strength = payload["strength"]
    assert abs(float(strength["strength_score"]) - 0.87) < 0.01
    assert strength["strength_level"] == "strong"
    assert payload["pattern"]["cach_cuc"] == "Chính Ấn"
    assert payload["pattern"]["pattern"] == "chinh_an"
    assert payload["temperature"]["climate_state"] == "cold"
    assert payload["temperature"]["balancing_need"] == "warming"
    assert payload["useful_god"]["useful_god"] == "Chính Quan"
    assert payload["useful_god"]["useful_display"] == "Hỏa · Đinh · Chính Quan"
    assert payload["useful_god"]["climate_display"] == "Hỏa · Bính · Thất Sát"
    ten_gods = payload.get("ten_gods") or {}
    visible = ten_gods.get("visible") or []
    stems = [str(item.get("stem") or "") for item in visible if isinstance(item, dict)]
    assert payload["bazi"]["day_master"] == "Canh"
    assert stems == ["Bính", "Tân", "Canh", "Mậu"]
