from engines.temperature_engine.analyzer import TemperatureAnalyzer
from engines.temperature_engine.context import TemperatureContext
from engines.temperature_engine.loader import TemperatureLoader
from engines.temperature_engine.matcher import TemperatureMatcher


def test_analyzer_matches_climate_rules() -> None:
    ctx = TemperatureContext(climate_type="hot", season="summer")
    loader = TemperatureLoader("database/11_temperature")
    grouped = loader.load_rule_groups()
    analyzer = TemperatureAnalyzer(TemperatureMatcher())
    result = analyzer.analyze_primary(ctx, grouped)
    assert result["climate_matches"]
    assert any(m["rule_id"] == "cli_001" for m in result["climate_matches"])
