"""Public/private safety tests for Presentation (N-IMP-09)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from engines.narrative_v2.action.action_model import ActionPlanNarrative
from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.interpretation.interpretation_model import InterpretationNarrative
from engines.narrative_v2.presentation import PresentationBuilder, PresentationError, serialize_customer
from engines.narrative_v2.summary.summary_model import OverviewSummary

FORBIDDEN_TOKENS = (
    "evidence.strength.level",
    "NR-REL-001",
    "knowledge.pattern.chinh_an",
    "pipeline_trace",
    "source_unit_ids",
    "runtime_metrics",
    "knowledge_ids",
    "evidence_ids",
    "rewrite_ids",
    "decision_id",
    "action_id",
    "source_knowledge_ids",
)

PACK05 = Path(__file__).resolve().parents[2] / "engines" / "narrative_engine"


def test_p11_p16_no_internal_leaks(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
) -> None:
    overview, interpretation, action_plan = case_0001_narratives
    payload = serialize_customer(PresentationBuilder().build(overview, interpretation, action_plan))
    rendered = json.dumps(payload, ensure_ascii=False)
    for token in FORBIDDEN_TOKENS:
        assert token not in rendered
    assert "meaning" not in payload.get("interpretation", {})
    assert "flow" not in payload.get("interpretation", {})
    assert "references" not in rendered


def test_p25_pack05_not_modified() -> None:
    assert PACK05.exists()
    engine = (PACK05 / "engine.py").read_text(encoding="utf-8")
    assert "NarrativeEngine" in engine


def test_negative_no_new_customer_sentences(
    case_0001_narratives: tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative],
) -> None:
    overview, interpretation, action_plan = case_0001_narratives
    presentation = PresentationBuilder().build(overview, interpretation, action_plan)
    assert presentation.overview is not None
    assert presentation.overview.headline == overview.headline
    assert presentation.interpretation is not None
    assert presentation.interpretation.observation == interpretation.observation
    assert presentation.action_plan is not None
    assert presentation.action_plan.warnings[0].description == action_plan.warnings[0].description


def test_builder_rejects_evidence_object(case_0001_canonical: dict[str, Any]) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    with pytest.raises(PresentationError):
        PresentationBuilder().build(evidence, None, None, None)
