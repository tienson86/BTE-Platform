"""Serialization round-trip tests."""

from __future__ import annotations

from typing import Any

from engines.luck_engine.timeline import (
    construct_timeline,
    timeline_from_dict,
    timeline_to_json,
)


def test_json_round_trip(continuous_timeline_payload: dict[str, Any]) -> None:
    """Serialize then rehydrate without changing published identity."""
    original = construct_timeline(**continuous_timeline_payload)
    encoded = timeline_to_json(original)
    restored = timeline_from_dict(__import__("json").loads(encoded))
    assert restored.timeline_id == original.timeline_id
    assert restored.timeline_version == original.timeline_version
    assert restored.natal_chart.day_pillar == original.natal_chart.day_pillar
    assert [p.period_id for p in restored.major_cycles[0].periods] == [
        p.period_id for p in original.major_cycles[0].periods
    ]
    assert encoded == timeline_to_json(restored)
