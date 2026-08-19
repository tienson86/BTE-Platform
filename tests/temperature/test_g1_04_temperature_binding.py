"""G1-04 canonical Temperature / Điều hậu: climate direction, not score axis."""

from __future__ import annotations

from applications.api.services.orchestrator import OrchestratorService
from applications.api.services.temperature_truth import build_temperature_view
from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.engine import CalendarEngine
from engines.pattern_engine.engine import PatternEngine
from engines.pattern_engine.utils.context_builder import build_pattern_context
from engines.strength_engine.engine import StrengthEngine
from engines.strength_engine.utils.context_builder import build_strength_context
from engines.temperature_engine.context import TemperatureContext
from engines.temperature_engine.engine import TemperatureEngine
from engines.temperature_engine.utils.context_builder import build_temperature_context
from engines.useful_god_engine.engine import UsefulGodEngine
from engines.useful_god_engine.utils.context_builder import build_useful_god_context

_SEASONAL_MATRIX: tuple[tuple[str, str, str, str], ...] = (
    ("Dần", "spring", "warm", "balance"),
    ("Mão", "spring", "warm", "balance"),
    ("Thìn", "spring", "warm", "balance"),
    ("Tỵ", "summer", "hot", "cooling"),
    ("Ngọ", "summer", "hot", "cooling"),
    ("Mùi", "summer", "hot", "cooling"),
    ("Thân", "autumn", "cool", "warming"),
    ("Dậu", "autumn", "cool", "warming"),
    ("Tuất", "autumn", "cool", "warming"),
    ("Hợi", "winter", "cold", "warming"),
    ("Tý", "winter", "cold", "warming"),
    ("Sửu", "winter", "cold", "warming"),
)


def _case_0001_chart() -> tuple[object, object]:
    calendar = CalendarEngine().build(1987, 1, 21, 4, 30)
    chart = BaziEngine().build(calendar, gender="male")
    return calendar, chart


def _temperature_for_branch(
    month_branch: str,
    season: str,
    climate_type: str,
    *,
    fire_count: int = 0,
    water_count: int = 0,
    day_master: str = "Canh",
    day_master_element: str = "Kim",
) -> object:
    ctx = TemperatureContext(
        day_master=day_master,
        day_master_element=day_master_element,
        month_branch=month_branch,
        season=season,
        climate_type=climate_type,
        fire_count=fire_count,
        water_count=water_count,
        dryness_level="normal",
        humidity_level="normal",
    )
    return TemperatureEngine(database_path="database/11_temperature").calculate(ctx)


def test_seasonal_climate_direction_not_inverted() -> None:
    """Month-branch climate facts keep seasonal cold/hot direction."""
    for branch, season, climate, need in _SEASONAL_MATRIX:
        result = _temperature_for_branch(branch, season, climate)
        assert result.success
        assert result.climate_state == climate
        assert result.temperature_level == climate
        assert result.season == season
        assert result.month_branch == branch
        assert result.balancing_need == need
        assert result.score_semantic == "imbalance_intensity"
        assert result.to_pattern_temperature_type() == climate
        assert "Nhiệt khí nặng" not in (result.reasoning or "")
        recs = " ".join(result.recommendations)
        if climate in {"cold", "cool"}:
            assert "nhuận hạ" not in recs.lower()
        if climate == "hot":
            assert "ôn dưỡng" not in recs.lower()


def test_cold_season_fire_count_does_not_flip_climate() -> None:
    """No CSV rule maps fire_count → hot. Strong Fire must not invert Sửu."""
    cold = _temperature_for_branch("Sửu", "winter", "cold", fire_count=0)
    fiery = _temperature_for_branch("Sửu", "winter", "cold", fire_count=8)
    assert cold.climate_state == "cold"
    assert fiery.climate_state == "cold"
    assert fiery.balancing_need == "warming"


def test_hot_season_water_count_does_not_flip_climate() -> None:
    """No CSV rule maps water_count → cold. Strong Water must not invert Ngọ."""
    dry = _temperature_for_branch("Ngọ", "summer", "hot", water_count=0)
    wet = _temperature_for_branch("Ngọ", "summer", "hot", water_count=8)
    assert dry.climate_state == "hot"
    assert wet.climate_state == "hot"
    assert wet.balancing_need == "cooling"


def test_case_0001_suu_winter_cold_warming() -> None:
    calendar, chart = _case_0001_chart()
    strength = StrengthEngine().calculate(build_strength_context(chart, calendar=calendar))
    result = TemperatureEngine().calculate(
        build_temperature_context(
            chart,
            calendar=calendar,
            strength_level=strength.strength_level,
            strength_score=strength.strength_score,
        )
    )
    view = build_temperature_view(result)
    assert chart.month_pillar.branch == "Sửu"
    assert result.month_branch == "Sửu"
    assert result.season == "winter"
    assert result.climate_state == "cold"
    assert result.temperature_level == "cold"
    assert result.temperature_level != "hot"
    assert result.balancing_need == "warming"
    assert result.balancing_need_label == "Cần ôn ấm"
    assert result.climate_state_label == "Hàn"
    assert "Nguyệt lệnh Sửu" in result.evidence_compact
    assert "mùa Đông" in result.evidence_compact
    assert view.climate_state == "cold"
    assert view.balancing_need == "warming"
    assert view.to_dict()["temperature_level"] == "cold"
    recs = " ".join(result.recommendations).lower()
    assert "ôn dưỡng" in recs or "ấm" in recs
    assert "nhiệt khí nặng" not in (result.reasoning or "").lower()


def test_case_0001_score_is_intensity_not_heat_axis() -> None:
    calendar, chart = _case_0001_chart()
    result = TemperatureEngine().calculate(build_temperature_context(chart, calendar=calendar))
    assert result.score_semantic == "imbalance_intensity"
    assert result.temperature_score > 0.65
    assert result.climate_state == "cold"


def test_case_0001_strength_pattern_ten_gods_useful_god_unchanged() -> None:
    payload = OrchestratorService().analyze(
        year=1987, month=1, day=21, hour=4, minute=30, gender="male"
    )
    strength = payload["strength"]
    assert abs(float(strength["strength_score"]) - 0.87) < 0.01
    assert strength["strength_level"] == "strong"
    assert payload["pattern"]["cach_cuc"] == "Chính Ấn"
    assert payload["pattern"]["pattern"] == "chinh_an"
    assert payload["useful_god"]["useful_god"] == "Thực Thần"
    assert payload["temperature"]["climate_state"] == "cold"
    assert payload["temperature"]["balancing_need"] == "warming"
    ten_gods = payload.get("ten_gods") or {}
    visible = ten_gods.get("visible") or []
    stems = [str(item.get("stem") or "") for item in visible if isinstance(item, dict)]
    assert payload["bazi"]["day_master"] == "Canh"
    assert stems == ["Bính", "Tân", "Canh", "Mậu"]


def test_case_0001_useful_god_overlay_frozen_until_g1_06() -> None:
    """Climate is cold, but Overall Useful God overlay stays pre-G1-04 until G1-06."""
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
    assert temperature.climate_state == "cold"
    assert temperature.to_pattern_temperature_type() == "cold"
    assert temperature.useful_god_temperature_overlay() == "hot"
    pattern_context = build_pattern_context(chart, calendar=calendar)
    pattern_context.strength_level = strength.strength_level
    pattern_context.strength_score = strength.strength_score
    pattern_context.temperature_type = temperature.useful_god_temperature_overlay()
    pattern = PatternEngine().calculate(pattern_context)
    useful = UsefulGodEngine().calculate(build_useful_god_context(pattern_context, pattern))
    assert useful.useful_god == "Thực Thần"
