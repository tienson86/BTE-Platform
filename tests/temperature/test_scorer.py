from engines.temperature_engine.analyzer import TemperatureAnalyzer
from engines.temperature_engine.context import TemperatureContext
from engines.temperature_engine.loader import TemperatureLoader
from engines.temperature_engine.matcher import TemperatureMatcher
from engines.temperature_engine.priority import TemperaturePriorityResolver
from engines.temperature_engine.scorer import TemperatureScorer


def test_scorer_produces_scores() -> None:
    ctx = TemperatureContext(climate_type="hot", season="summer", fire_count=3)
    loader = TemperatureLoader("database/11_temperature")
    grouped = loader.load_rule_groups()
    analyzer = TemperatureAnalyzer(TemperatureMatcher())
    primary = analyzer.analyze_primary(ctx, grouped)
    config = loader.load_config()
    level_rules = loader.load_level_rules()
    resolver = TemperaturePriorityResolver(loader.load_priority_rules())
    scored = TemperatureScorer().score(
        ctx, primary, grouped, analyzer, config, level_rules, TemperatureMatcher(), resolver,
    )
    assert 0.0 <= scored["temperature_score"] <= 1.0
    assert scored["warm_score"] >= 0.0
