"""NarrativeV2Presentation model tests (N-IMP-09)."""

from __future__ import annotations

from dataclasses import fields

from engines.narrative_v2.action.action_model import ActionPlanNarrative
from engines.narrative_v2.interpretation.interpretation_model import InterpretationNarrative
from engines.narrative_v2.presentation import (
    PRESENTATION_VERSION,
    NarrativeV2Presentation,
    PresentationBuilder,
)
from engines.narrative_v2.presentation.presentation_validator import (
    ACTION_PLAN_FIELDS,
    INTERPRETATION_FIELDS,
    METADATA_FIELDS,
    OVERVIEW_FIELDS,
    ROOT_FIELDS,
)
from engines.narrative_v2.summary.summary_model import OverviewSummary

ROOT_CONTRACT = (
    "status",
    "overview",
    "interpretation",
    "action_plan",
    "commercial",
    "metadata",
)


def test_p4_correct_root_contract(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
) -> None:
    overview, interpretation, action_plan = case_0001_narratives
    presentation = PresentationBuilder().build(overview, interpretation, action_plan)
    assert tuple(item.name for item in fields(presentation)) == ROOT_CONTRACT
    assert ROOT_FIELDS == ROOT_CONTRACT
    assert presentation.metadata.version == PRESENTATION_VERSION
    assert type(presentation) is NarrativeV2Presentation


def test_nested_public_fields_match_frozen_contract(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
) -> None:
    overview, interpretation, action_plan = case_0001_narratives
    presentation = PresentationBuilder().build(overview, interpretation, action_plan)
    assert presentation.overview is not None
    assert tuple(item.name for item in fields(presentation.overview)) == OVERVIEW_FIELDS
    assert presentation.interpretation is not None
    assert tuple(item.name for item in fields(presentation.interpretation)) == INTERPRETATION_FIELDS
    assert "meaning" in INTERPRETATION_FIELDS
    assert "consulting_flow" in INTERPRETATION_FIELDS
    assert "flow" not in INTERPRETATION_FIELDS
    assert presentation.action_plan is not None
    assert tuple(item.name for item in fields(presentation.action_plan)) == ACTION_PLAN_FIELDS
    assert tuple(item.name for item in fields(presentation.metadata)) == METADATA_FIELDS
