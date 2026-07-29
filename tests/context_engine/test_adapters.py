from engines.context_engine.adapters import adapt_strength_overlay, adapt_temperature_payload
from engines.context_engine.builder import UnifiedContextBuilder
from engines.context_engine.models import StrengthSection, UnifiedAnalysisContext


def test_strength_overlay_has_level() -> None:
    unified = UnifiedAnalysisContext(
        strength=StrengthSection(level="weak", score=0.3),
    )
    overlay = adapt_strength_overlay(unified)
    assert overlay["level"] == "weak"
    assert overlay["source"] == "strength_engine_v2"


def test_temperature_payload_maps_scores() -> None:
    unified = UnifiedContextBuilder().build(
        temperature={"temperature_level": "cold", "type": "cold", "cold_score": 0.2, "warm_score": 0.05}
    )
    payload = adapt_temperature_payload(unified)
    assert payload["status"] == "cold"
    assert payload["cold_score"] == 0.2
