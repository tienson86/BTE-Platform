"""Determinism tests for Presentation (N-IMP-09)."""

from __future__ import annotations

from engines.narrative_v2.action.action_model import ActionPlanNarrative
from engines.narrative_v2.interpretation.interpretation_model import InterpretationNarrative
from engines.narrative_v2.presentation import PresentationBuilder, serialize_customer
from engines.narrative_v2.summary.summary_model import OverviewSummary


def test_p19_same_input_same_presentation(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
) -> None:
    overview, interpretation, action_plan = case_0001_narratives
    first = PresentationBuilder().build(overview, interpretation, action_plan)
    second = PresentationBuilder().build(overview, interpretation, action_plan)
    assert serialize_customer(first) == serialize_customer(second)
    assert first.status == second.status
    assert first.metadata.created_at == second.metadata.created_at
    assert first.overview == second.overview
    assert first.interpretation == second.interpretation
    assert first.action_plan == second.action_plan
    assert first.commercial is None
    assert second.commercial is None
