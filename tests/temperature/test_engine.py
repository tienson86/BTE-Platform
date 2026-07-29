from engines.temperature_engine.context import TemperatureContext
from engines.temperature_engine.engine import TemperatureEngine


def test_engine_hot_chart() -> None:
    ctx = TemperatureContext(
        day_master="Bính",
        day_master_element="Hỏa",
        month_branch="Ngọ",
        season="summer",
        climate_type="hot",
        dryness_level="slightly_dry",
        fire_count=3,
        water_count=1,
    )
    engine = TemperatureEngine(database_path="database/11_temperature")
    result = engine.calculate(ctx)
    assert result.success
    assert result.temperature_level in {"hot", "warm"}
    assert result.matched_rules
    assert result.recommendations


def test_engine_cold_chart() -> None:
    ctx = TemperatureContext(
        day_master="Nhâm",
        day_master_element="Thủy",
        month_branch="Tý",
        season="winter",
        climate_type="cold",
        humidity_level="humid",
        water_count=4,
        fire_count=0,
    )
    engine = TemperatureEngine(database_path="database/11_temperature")
    result = engine.calculate(ctx)
    assert result.success
    assert result.temperature_level in {"cold", "cool"}
    assert result.to_pattern_temperature_type() in {"cold", "cool"}
