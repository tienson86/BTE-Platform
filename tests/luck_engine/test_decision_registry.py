"""Luck Decision registry integrity tests."""

from __future__ import annotations

import pytest

from engines.luck_engine.decision.decision_registry import (
    LuckDecisionRegistry,
    LuckDecisionStageRecord,
)
from engines.luck_engine.decision_constants import CANONICAL_DECISION_ORDER
from engines.luck_engine.exceptions import LuckDecisionRegistryError


def test_default_registry_order_and_fields() -> None:
    """Registry lists five enabled decision stages in canonical order."""
    registry = LuckDecisionRegistry()
    assert registry.canonical_order() == CANONICAL_DECISION_ORDER
    opportunity = registry.get("opportunity_evaluation")
    assert opportunity.dependencies == ()
    assert opportunity.published_outputs == ("opportunity_score",)
    assert registry.get("risk_evaluation").dependencies == ("opportunity_score",)
    assert [item["stage_id"] for item in registry.to_list()] == list(CANONICAL_DECISION_ORDER)


def test_unknown_and_duplicate_stage() -> None:
    """Unknown ids and duplicate catalog entries fail closed."""
    with pytest.raises(LuckDecisionRegistryError, match="unknown_stage"):
        LuckDecisionRegistry().get("fortune_stage")
    record = LuckDecisionStageRecord(
        stage_id="opportunity_evaluation",
        dependencies=(),
        consumed_inputs=(),
        published_outputs=("opportunity_score",),
        version="1.0.0",
        enabled=True,
    )
    with pytest.raises(LuckDecisionRegistryError, match="duplicate_stage_id"):
        LuckDecisionRegistry((record, record))
