from engines.context_engine.builder import UnifiedContextBuilder
from engines.context_engine.models import StrengthSection, TemperatureSection


def test_builder_normalizes_strength_fields() -> None:
    strength = {
        "strength_level": "strong",
        "strength_score": 0.72,
        "season_score": 0.35,
        "matched_rules": ["sea_001"],
        "success": True,
    }
    ctx = UnifiedContextBuilder().build(strength=strength)
    assert ctx.strength.level == "strong"
    assert ctx.strength.score == 0.72
    assert ctx.strength.matched_rules == ["sea_001"]


def test_builder_normalizes_temperature_type() -> None:
    temperature = {
        "temperature_level": "hot",
        "temperature_score": 0.68,
        "warm_score": 0.4,
        "type": "hot",
    }
    ctx = UnifiedContextBuilder().build(temperature=temperature)
    assert ctx.temperature.level == "hot"
    assert ctx.temperature.type == "hot"


def test_builder_useful_god_primary() -> None:
    ug = {"useful_god": "Bính", "favorable_gods": ["Bính"], "unfavorable_gods": ["Nhâm"]}
    ctx = UnifiedContextBuilder().build(useful_god=ug)
    assert ctx.useful_god.primary == "Bính"
    assert "Bính" in ctx.useful_god.favorable
