"""AX-2 canonical execution order tests."""

from __future__ import annotations

import pytest

from engines.analysis_engine.exceptions.pipeline_error import DependencyViolationError
from engines.analysis_engine.pipeline.canonical_pipeline import CanonicalPipeline
from engines.analysis_engine.pipeline.diagnostics import DIAG_DISABLED_STAGE
from engines.analysis_engine.pipeline.stage_registry import (
    ACTIVE_CANONICAL_STAGES,
    CANONICAL_STAGE_ORDER_V2,
    INACTIVE_FUTURE_STAGES,
    CanonicalStageRegistry,
)


def test_registry_catalog_declares_required_fields() -> None:
    """Every stage record must expose the AX-2 catalog contract."""
    registry = CanonicalStageRegistry.default()
    for record in registry.list_stages():
        assert record.stage_id
        assert record.version
        assert isinstance(record.dependencies, tuple)
        assert isinstance(record.produced_outputs, tuple)
        assert isinstance(record.consumed_outputs, tuple)
        assert isinstance(record.enabled, bool)


def test_active_order_is_canonical_through_useful_god() -> None:
    """Enabled stages follow Calendar → … → Useful God."""
    registry = CanonicalStageRegistry.default()
    order = registry.resolve_order(ACTIVE_CANONICAL_STAGES)
    assert order == ACTIVE_CANONICAL_STAGES
    assert order[-1] == "useful_god"
    assert "pattern_evaluation" in order
    assert order.index("pattern") < order.index("pattern_evaluation")
    assert order.index("pattern_evaluation") < order.index("useful_god")


def test_future_stages_registered_but_inactive() -> None:
    """Luck Cycle, Interpretation, and Report stay registered and disabled."""
    registry = CanonicalStageRegistry.default()
    assert registry.canonical_order == CANONICAL_STAGE_ORDER_V2
    assert registry.disabled_stage_ids() == INACTIVE_FUTURE_STAGES
    for stage_id in INACTIVE_FUTURE_STAGES:
        assert registry.get(stage_id).enabled is False


def test_shuffled_request_is_normalized() -> None:
    """Requested stages are reordered deterministically."""
    registry = CanonicalStageRegistry.default()
    order = registry.resolve_order(
        (
            "useful_god",
            "calendar",
            "pattern_evaluation",
            "temperature",
            "pattern",
            "strength",
            "seasonal",
            "four_pillars",
        )
    )
    assert order == ACTIVE_CANONICAL_STAGES


def test_unknown_and_duplicate_stage_requests_rejected() -> None:
    """Unknown and duplicate identifiers are dependency violations."""
    registry = CanonicalStageRegistry.default()
    with pytest.raises(DependencyViolationError, match="unknown_stages"):
        registry.resolve_order(("calendar", "not_a_stage"))
    with pytest.raises(DependencyViolationError, match="duplicate_stages"):
        registry.resolve_order(("calendar", "calendar"))


def test_pipeline_emits_disabled_stage_diagnostics() -> None:
    """A successful run must report inactive future stages."""
    result = CanonicalPipeline().run({"month_branch": "wei"})
    assert result.success is True
    disabled = {
        item.stage_id
        for item in result.diagnostics
        if item.code == DIAG_DISABLED_STAGE
    }
    assert disabled == set(INACTIVE_FUTURE_STAGES)
    executed = {entry.stage_id for entry in result.execution_trace.stages}
    assert executed.isdisjoint(INACTIVE_FUTURE_STAGES)
