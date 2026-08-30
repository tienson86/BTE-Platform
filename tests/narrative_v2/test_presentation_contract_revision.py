"""Presentation contract revision tests (N-IMP-09A)."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, fields
from pathlib import Path
from typing import Any

import pytest

from engines.narrative_v2.action.action_model import ActionPlanNarrative
from engines.narrative_v2.communication.communication_context import ConsultingNarrative
from engines.narrative_v2.interpretation.interpretation_model import InterpretationNarrative
from engines.narrative_v2.presentation import (
    PRESENTATION_VERSION,
    PREVIOUS_PRESENTATION_VERSION,
    PresentationBuilder,
    serialize_customer,
)
from engines.narrative_v2.runtime import SHADOW_MODE, NarrativeRuntime
from engines.narrative_v2.summary.summary_model import OverviewSummary

PACK05 = Path(__file__).resolve().parents[2] / "engines" / "narrative_engine"
PORTAL_ADAPTER = (
    Path(__file__).resolve().parents[2]
    / "applications"
    / "customer_portal"
    / "src"
    / "adapters"
    / "narrativeResultAdapter.ts"
)


def _build(
    narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
    consulting: ConsultingNarrative | None = None,
):
    overview, interpretation, action_plan = narratives
    return PresentationBuilder().build(
        overview,
        interpretation,
        action_plan,
        None,
        consulting=consulting,
    )


def test_pa1_consulting_flow_exists_in_revised_contract(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
    case_0001_consulting: ConsultingNarrative,
) -> None:
    presentation = _build(case_0001_narratives, case_0001_consulting)
    names = tuple(item.name for item in fields(presentation.interpretation))
    assert "consulting_flow" in names
    assert presentation.interpretation is not None
    assert presentation.interpretation.consulting_flow


def test_pa2_consulting_flow_copied_exactly(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
    case_0001_consulting: ConsultingNarrative,
) -> None:
    presentation = _build(case_0001_narratives, case_0001_consulting)
    assert presentation.interpretation is not None
    assert presentation.interpretation.consulting_flow == case_0001_consulting.flow


def test_pa3_meaning_restored_when_available(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
    case_0001_consulting: ConsultingNarrative,
) -> None:
    _, interpretation, _ = case_0001_narratives
    presentation = _build(case_0001_narratives, case_0001_consulting)
    assert interpretation.meaning
    assert presentation.interpretation is not None
    assert presentation.interpretation.meaning == interpretation.meaning


def test_pa4_structured_fields_unchanged(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
    case_0001_consulting: ConsultingNarrative,
) -> None:
    _, interpretation, _ = case_0001_narratives
    presentation = _build(case_0001_narratives, case_0001_consulting)
    view = presentation.interpretation
    assert view is not None
    assert view.overview == interpretation.overview
    assert view.observation == interpretation.observation
    assert view.reasoning == interpretation.reasoning
    assert view.impact == interpretation.impact
    assert view.recommendation == interpretation.recommendation
    assert view.closing == interpretation.closing


def test_pa5_no_rewrite_in_presentation(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
    case_0001_consulting: ConsultingNarrative,
) -> None:
    overview, interpretation, action_plan = case_0001_narratives
    presentation = _build(case_0001_narratives, case_0001_consulting)
    assert presentation.overview is not None
    assert presentation.overview.headline == overview.headline
    assert presentation.interpretation is not None
    assert presentation.interpretation.recommendation == interpretation.recommendation
    assert presentation.action_plan is not None
    assert presentation.action_plan.actions[0].description == action_plan.actions[0].description


def test_pa6_no_flow_recomposition(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
    case_0001_consulting: ConsultingNarrative,
) -> None:
    _, interpretation, _ = case_0001_narratives
    presentation = _build(case_0001_narratives, case_0001_consulting)
    view = presentation.interpretation
    assert view is not None
    joined = " ".join(
        part.strip()
        for part in (
            interpretation.observation,
            interpretation.reasoning,
            interpretation.meaning,
            interpretation.impact,
            interpretation.recommendation,
            interpretation.closing,
        )
        if part and part.strip()
    )
    assert view.consulting_flow != joined
    assert view.consulting_flow == case_0001_consulting.flow


def test_pa7_no_internal_ids_exposed(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
    case_0001_consulting: ConsultingNarrative,
) -> None:
    payload = serialize_customer(_build(case_0001_narratives, case_0001_consulting))
    rendered = __import__("json").dumps(payload, ensure_ascii=False)
    for token in (
        "evidence.strength.level",
        "NR-REL-001",
        "knowledge.pattern.chinh_an",
        "pipeline_trace",
        "source_unit_ids",
        "rewrite_ids",
        "decision_id",
        "source_conversation_ids",
        "frame_id",
    ):
        assert token not in rendered
    assert "flow" not in payload["interpretation"]


def test_pa8_serializer_deterministic(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
    case_0001_consulting: ConsultingNarrative,
) -> None:
    first = serialize_customer(_build(case_0001_narratives, case_0001_consulting))
    second = serialize_customer(_build(case_0001_narratives, case_0001_consulting))
    assert first == second


def test_pa9_freeze_remains_immutable(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
    case_0001_consulting: ConsultingNarrative,
) -> None:
    presentation = _build(case_0001_narratives, case_0001_consulting)
    with pytest.raises(FrozenInstanceError):
        presentation.interpretation.consulting_flow = "new flow"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        presentation.interpretation.meaning = "new meaning"  # type: ignore[misc]


def test_pa10_commercial_remains_null(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
    case_0001_consulting: ConsultingNarrative,
) -> None:
    presentation = _build(case_0001_narratives, case_0001_consulting)
    assert presentation.commercial is None


def test_pa11_summary_gaps_remain_untouched(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
    case_0001_consulting: ConsultingNarrative,
) -> None:
    overview, _, _ = case_0001_narratives
    presentation = _build(case_0001_narratives, case_0001_consulting)
    assert overview.identity is None
    assert overview.balance is None
    assert overview.conclusion is None
    assert presentation.overview is not None
    assert presentation.overview.identity is None
    assert presentation.overview.balance is None
    assert presentation.overview.conclusion is None


def test_pa12_portal_remains_disconnected(case_0001_canonical: dict[str, Any]) -> None:
    runtime = NarrativeRuntime()
    result = runtime.run(case_0001_canonical)
    assert runtime.portal_connected is False
    assert result.runtime_metadata["portal_connected"] is False
    adapter = PORTAL_ADAPTER.read_text(encoding="utf-8")
    assert "pack05_narrative_result_v1" in adapter
    assert "narrative_v2" not in adapter


def test_pa13_pack05_remains_unchanged() -> None:
    assert PACK05.exists()
    engine = (PACK05 / "engine.py").read_text(encoding="utf-8")
    assert "NarrativeEngine" in engine


def test_pa14_schema_version_migration_is_explicit() -> None:
    assert PREVIOUS_PRESENTATION_VERSION == "bte.presentation.v2"
    assert PRESENTATION_VERSION == "bte.presentation.v2.1"
    assert PRESENTATION_VERSION != PREVIOUS_PRESENTATION_VERSION


def test_pa15_same_case_0001_same_presentation(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
    case_0001_consulting: ConsultingNarrative,
) -> None:
    first = serialize_customer(_build(case_0001_narratives, case_0001_consulting))
    second = serialize_customer(_build(case_0001_narratives, case_0001_consulting))
    assert first == second
    assert first["metadata"]["version"] == "bte.presentation.v2.1"
    assert first["interpretation"]["consulting_flow"] == case_0001_consulting.flow


def test_runtime_publish_includes_consulting_flow(case_0001_canonical: dict[str, Any]) -> None:
    runtime = NarrativeRuntime()
    result = runtime.run(case_0001_canonical)
    assert SHADOW_MODE is True
    assert result.presentation is not None
    assert result.presentation.interpretation.consulting_flow
    assert result.presentation.interpretation.meaning
    assert result.presentation.commercial is None
