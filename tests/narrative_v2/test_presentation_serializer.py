"""Customer serializer tests (N-IMP-09)."""

from __future__ import annotations

import json

from engines.narrative_v2.action.action_model import ActionPlanNarrative
from engines.narrative_v2.interpretation.interpretation_model import InterpretationNarrative
from engines.narrative_v2.presentation import PresentationBuilder, serialize_customer, serialize_internal
from engines.narrative_v2.summary.summary_model import OverviewSummary


def test_p10_public_metadata_safe(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
) -> None:
    overview, interpretation, action_plan = case_0001_narratives
    payload = serialize_customer(PresentationBuilder().build(overview, interpretation, action_plan))
    assert set(payload["metadata"].keys()) == {"status", "language", "version", "created_at"}
    assert payload["metadata"]["version"] == "bte.presentation.v2.1"
    assert payload["metadata"]["language"] == "vi"


def test_p17_public_serializer_stable(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
) -> None:
    overview, interpretation, action_plan = case_0001_narratives
    first = serialize_customer(PresentationBuilder().build(overview, interpretation, action_plan))
    second = serialize_customer(PresentationBuilder().build(overview, interpretation, action_plan))
    assert first == second
    encoded = json.dumps(first, ensure_ascii=False, sort_keys=True)
    assert json.loads(encoded) == first


def test_internal_serializer_is_separate_and_still_public_shaped(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
) -> None:
    overview, interpretation, action_plan = case_0001_narratives
    presentation = PresentationBuilder().build(overview, interpretation, action_plan)
    customer = serialize_customer(presentation)
    internal = serialize_internal(presentation)
    assert customer == internal
    assert "pipeline_trace" not in json.dumps(internal)
