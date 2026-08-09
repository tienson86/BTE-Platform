"""AX-1 dependency order tests against ANALYSIS_DEPENDENCY_MAP."""

from __future__ import annotations

import pytest

from engines.analysis_engine.exceptions.pipeline_error import DependencyViolationError
from engines.analysis_engine.pipeline.dependency_resolver import (
    ACTIVE_KNOWLEDGE_STAGES,
    CANONICAL_STAGE_ORDER,
    PLACEHOLDER_STAGES,
    DependencyResolver,
)


def test_active_order_matches_dependency_map() -> None:
    """Active AX-1 stages follow Seasonal → Strength → Temperature."""
    resolver = DependencyResolver()
    order = resolver.resolve_order(ACTIVE_KNOWLEDGE_STAGES)
    assert order == (
        "calendar",
        "four_pillars",
        "seasonal",
        "strength",
        "temperature",
    )


def test_canonical_order_includes_future_placeholders() -> None:
    """Future stages remain reserved after Temperature."""
    assert CANONICAL_STAGE_ORDER.index("temperature") < CANONICAL_STAGE_ORDER.index(
        "pattern"
    )
    assert "useful_god" in PLACEHOLDER_STAGES
    assert "luck_cycle" in PLACEHOLDER_STAGES
    resolver = DependencyResolver()
    full = resolver.resolve_order(CANONICAL_STAGE_ORDER)
    assert full == CANONICAL_STAGE_ORDER


def test_shuffled_request_is_normalized() -> None:
    """Requested stages are reordered deterministically."""
    resolver = DependencyResolver()
    order = resolver.resolve_order(("temperature", "calendar", "strength", "seasonal", "four_pillars"))
    assert order == ACTIVE_KNOWLEDGE_STAGES


def test_strength_before_seasonal_is_rejected_when_incomplete() -> None:
    """Strength cannot run without Seasonal."""
    resolver = DependencyResolver()
    with pytest.raises(DependencyViolationError, match="missing_prerequisite"):
        resolver.resolve_order(("strength", "temperature"))


def test_unknown_stage_rejected() -> None:
    """Unknown stage identifiers are dependency violations."""
    resolver = DependencyResolver()
    with pytest.raises(DependencyViolationError, match="unknown_stages"):
        resolver.resolve_order(("calendar", "not_a_stage"))


def test_duplicate_stage_request_rejected() -> None:
    """Duplicate execution requests are rejected at resolve time."""
    resolver = DependencyResolver()
    with pytest.raises(DependencyViolationError, match="duplicate_stages"):
        resolver.resolve_order(("calendar", "calendar"))
