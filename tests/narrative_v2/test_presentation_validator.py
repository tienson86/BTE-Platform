"""PresentationValidator tests (N-IMP-09)."""

from __future__ import annotations

from dataclasses import replace

import pytest

from engines.narrative_v2.action.action_model import ActionPlanNarrative
from engines.narrative_v2.interpretation.interpretation_model import InterpretationNarrative
from engines.narrative_v2.presentation import (
    PresentationBuilder,
    PresentationMetadata,
    PresentationValidationError,
    PresentationValidator,
)
from engines.narrative_v2.summary.summary_model import OverviewSummary


def test_p9_status_deterministic(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
) -> None:
    overview, interpretation, action_plan = case_0001_narratives
    first = PresentationBuilder().build(overview, interpretation, action_plan)
    second = PresentationBuilder().build(overview, interpretation, action_plan)
    assert first.status == second.status
    assert first.status == "partial"
    PresentationValidator().validate(first)


def test_validator_rejects_wrong_version(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
) -> None:
    overview, interpretation, action_plan = case_0001_narratives
    presentation = PresentationBuilder().build(overview, interpretation, action_plan)
    broken = replace(
        presentation,
        metadata=replace(presentation.metadata, version="not-a-contract"),
    )
    with pytest.raises(PresentationValidationError, match="version"):
        PresentationValidator().validate(broken)


def test_validator_rejects_unknown_status(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
) -> None:
    overview, interpretation, action_plan = case_0001_narratives
    presentation = PresentationBuilder().build(overview, interpretation, action_plan)
    broken = replace(
        presentation,
        status="published",
        metadata=PresentationMetadata(
            status="published",
            language=presentation.metadata.language,
            version=presentation.metadata.version,
            created_at=presentation.metadata.created_at,
        ),
    )
    with pytest.raises(PresentationValidationError, match="status"):
        PresentationValidator().validate(broken)
