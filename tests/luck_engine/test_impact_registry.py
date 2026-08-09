"""Impact registry integrity tests."""

from __future__ import annotations

import pytest

from engines.luck_engine.analysis.impact_registry import ImpactRegistry, ImpactStageRecord
from engines.luck_engine.analysis_constants import CANONICAL_IMPACT_ORDER
from engines.luck_engine.exceptions import ImpactRegistryError


def test_default_registry_order_and_fields() -> None:
    """Registry lists six enabled impact stages in canonical order."""
    registry = ImpactRegistry()
    assert registry.canonical_order() == CANONICAL_IMPACT_ORDER
    seasonal = registry.get("seasonal_impact")
    assert seasonal.dependencies == ()
    assert seasonal.published_outputs == ("seasonal_impact",)
    assert seasonal.enabled is True
    assert registry.get("useful_god_impact").dependencies == ("pattern_evaluation_impact",)
    assert [item["stage_id"] for item in registry.to_list()] == list(CANONICAL_IMPACT_ORDER)


def test_unknown_and_duplicate_stage() -> None:
    """Unknown ids and duplicate catalog entries fail closed."""
    with pytest.raises(ImpactRegistryError, match="unknown_stage"):
        ImpactRegistry().get("fortune_impact")
    record = ImpactStageRecord(
        stage_id="seasonal_impact",
        dependencies=(),
        consumed_inputs=(),
        published_outputs=("seasonal_impact",),
        version="1.0.0",
        enabled=True,
    )
    with pytest.raises(ImpactRegistryError, match="duplicate_stage_id"):
        ImpactRegistry((record, record))
