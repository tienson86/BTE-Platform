"""Timeline registry integrity tests."""

from __future__ import annotations

import pytest

from engines.luck_engine.exceptions import TimelineRegistryError
from engines.luck_engine.timeline import (
    ACTIVE_TIMELINE_LAYERS,
    CANONICAL_LAYER_ORDER,
    RESERVED_TIMELINE_LAYERS,
    TimelineRegistry,
)
from engines.luck_engine.timeline.registry import TimelineLayerRecord


def test_default_registry_order_and_status() -> None:
    """Registry lists natal through hourly with reserved daily/hourly."""
    registry = TimelineRegistry()
    assert [item.layer_id for item in registry.to_list()] == list(CANONICAL_LAYER_ORDER)
    assert tuple(item.layer_id for item in registry.active_layers()) == ACTIVE_TIMELINE_LAYERS
    assert tuple(item.layer_id for item in registry.reserved_layers()) == RESERVED_TIMELINE_LAYERS
    assert registry.is_active("major_luck") is True
    assert registry.is_reserved("daily_luck") is True
    assert registry.parent_of("annual_luck").layer_id == "major_luck"


def test_unknown_layer_raises() -> None:
    """Unknown layer ids fail closed."""
    with pytest.raises(TimelineRegistryError, match="unknown_layer"):
        TimelineRegistry().get("unknown_luck")


def test_duplicate_layer_id_rejected() -> None:
    """Catalog duplicates are invalid."""
    record = TimelineLayerRecord(
        layer_id="major_luck",
        display_name="dup",
        vietnamese_name="dup",
        status="active",
        parent_layer_id=None,
        sequence=1,
        published_output=None,
    )
    with pytest.raises(TimelineRegistryError, match="duplicate_layer_id"):
        TimelineRegistry((record, record))
