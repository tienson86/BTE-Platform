"""Freeze / immutability tests (N-IMP-09)."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from engines.narrative_v2.action.action_model import ActionPlanNarrative
from engines.narrative_v2.interpretation.interpretation_model import InterpretationNarrative
from engines.narrative_v2.presentation import PresentationBuilder, freeze
from engines.narrative_v2.summary.summary_model import OverviewSummary


def test_p18_freeze_immutable(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
) -> None:
    overview, interpretation, action_plan = case_0001_narratives
    presentation = freeze(PresentationBuilder().build(overview, interpretation, action_plan))
    with pytest.raises(FrozenInstanceError):
        presentation.status = "complete"  # type: ignore[misc]
    assert presentation.overview is not None
    with pytest.raises(FrozenInstanceError):
        presentation.overview.headline = "new headline"  # type: ignore[misc]
    assert presentation.action_plan is not None
    with pytest.raises(FrozenInstanceError):
        presentation.action_plan.actions = ()  # type: ignore[misc]
