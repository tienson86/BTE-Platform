"""Registry integration for Number Energy Engine V1."""

from __future__ import annotations

from engines.core.register_engines import is_registered, register_all_engines
from engines.core.registry import registry
from engines.number_energy.engine import NumberEnergyEngine


def test_number_energy_is_registered() -> None:
    register_all_engines()
    assert is_registered("number_energy")
    engine = registry.get("number_energy")
    assert isinstance(engine, NumberEnergyEngine)
    result = engine.analyze("103")
    assert result.occurrences[0].display_name == "Thiên Y"
    assert result.occurrences[0].state == "HIDDEN"
