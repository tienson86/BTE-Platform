"""PresentationBuilder tests (N-IMP-09)."""

from __future__ import annotations

from typing import Any

import pytest

from engines.narrative_v2.action.action_model import ActionPlanNarrative
from engines.narrative_v2.interpretation.interpretation_model import InterpretationNarrative
from engines.narrative_v2.presentation import (
    NarrativeV2Presentation,
    PresentationBuilder,
    PresentationError,
)
from engines.narrative_v2.summary.summary_model import OverviewSummary


def test_p1_builder_accepts_narrative_outputs_only(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
) -> None:
    overview, interpretation, action_plan = case_0001_narratives
    presentation = PresentationBuilder().build(overview, interpretation, action_plan, None)
    assert isinstance(presentation, NarrativeV2Presentation)


def test_p2_rejects_raw_canonical_analysis(
    case_0001_canonical: dict[str, Any],
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
) -> None:
    _, interpretation, action_plan = case_0001_narratives
    with pytest.raises(PresentationError, match="OverviewSummary"):
        PresentationBuilder().build(case_0001_canonical, interpretation, action_plan, None)


def test_p3_returns_narrative_v2_presentation(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
) -> None:
    overview, interpretation, action_plan = case_0001_narratives
    presentation = PresentationBuilder().build(overview, interpretation, action_plan)
    assert type(presentation) is NarrativeV2Presentation


def test_p5_overview_copied_without_rewrite(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
) -> None:
    overview, interpretation, action_plan = case_0001_narratives
    presentation = PresentationBuilder().build(overview, interpretation, action_plan)
    assert presentation.overview is not None
    assert presentation.overview.headline == overview.headline
    assert presentation.overview.summary == overview.summary
    assert presentation.overview.identity is overview.identity
    assert presentation.overview.balance is overview.balance
    assert presentation.overview.conclusion is overview.conclusion


def test_p6_interpretation_copied_without_rewrite(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
) -> None:
    overview, interpretation, action_plan = case_0001_narratives
    presentation = PresentationBuilder().build(overview, interpretation, action_plan)
    assert presentation.interpretation is not None
    assert presentation.interpretation.overview == interpretation.overview
    assert presentation.interpretation.observation == interpretation.observation
    assert presentation.interpretation.reasoning == interpretation.reasoning
    assert presentation.interpretation.impact == interpretation.impact
    assert presentation.interpretation.recommendation == interpretation.recommendation
    assert presentation.interpretation.closing == interpretation.closing


def test_p7_action_copied_without_rewrite(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
) -> None:
    overview, interpretation, action_plan = case_0001_narratives
    presentation = PresentationBuilder().build(overview, interpretation, action_plan)
    assert presentation.action_plan is not None
    assert action_plan.top_priority is not None
    assert presentation.action_plan.top_priority is not None
    assert presentation.action_plan.top_priority.title == action_plan.top_priority.title
    assert presentation.action_plan.top_priority.description == action_plan.top_priority.description
    assert len(presentation.action_plan.actions) == len(action_plan.actions)
    for copied, source in zip(presentation.action_plan.actions, action_plan.actions, strict=True):
        assert copied.title == source.title
        assert copied.description == source.description
        assert copied.category == source.category


def test_p8_commercial_optional(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
) -> None:
    overview, interpretation, action_plan = case_0001_narratives
    presentation = PresentationBuilder().build(overview, interpretation, action_plan, None)
    assert presentation.commercial is None
    with pytest.raises(PresentationError, match="not implemented"):
        PresentationBuilder().build(overview, interpretation, action_plan, commercial="fake")


def test_builder_does_not_generate_new_customer_text(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
) -> None:
    overview, interpretation, action_plan = case_0001_narratives
    presentation = PresentationBuilder().build(overview, interpretation, action_plan)
    assert presentation.overview is not None
    assert presentation.overview.headline == overview.headline
    assert presentation.interpretation is not None
    assert presentation.interpretation.recommendation == interpretation.recommendation
    assert presentation.action_plan is not None
    assert presentation.action_plan.actions[0].description == action_plan.actions[0].description
