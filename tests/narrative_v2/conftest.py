"""Shared fixtures for Narrative V2 evidence tests."""

from __future__ import annotations

from typing import Any

import pytest

from applications.api.services.orchestrator import OrchestratorService
from applications.production.fixtures.case_0001 import CASE_0001_REQUEST
from engines.narrative_v2.action import ActionBuilder, ActionPlanNarrative
from engines.narrative_v2.communication import CommunicationEngine, ConsultingNarrative
from engines.narrative_v2.conversation import ConversationComposer
from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.interpretation import InterpretationBuilder, InterpretationNarrative
from engines.narrative_v2.knowledge import KnowledgeResolver
from engines.narrative_v2.reasoning import ReasoningBuilder
from engines.narrative_v2.rewrite import RewriteEngine
from engines.narrative_v2.summary import OverviewSummary, SummaryBuilder


@pytest.fixture(scope="module")
def case_0001_canonical() -> dict[str, Any]:
    """Real CASE-0001 CanonicalAnalysis through luck. No hardcoded engine facts."""
    request = CASE_0001_REQUEST
    return OrchestratorService().run_stage(
        "luck",
        year=request.year,
        month=request.month,
        day=request.day,
        hour=request.hour,
        minute=request.minute,
        gender=request.gender,
        timezone=request.timezone,
    )


@pytest.fixture(scope="module")
def case_0001_bundle(
    case_0001_canonical: dict[str, Any],
) -> dict[str, Any]:
    """CASE-0001 Narrative objects used by Presentation. No Presentation rewrite."""
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    rewrite = RewriteEngine().rewrite(knowledge, reasoning, evidence)
    summary = SummaryBuilder().build(rewrite)
    interpretation = InterpretationBuilder().build(rewrite)
    conversation = ConversationComposer().compose(rewrite, interpretation)
    consulting = CommunicationEngine().style(conversation)
    action = ActionBuilder().build(rewrite, interpretation, consulting)
    return {
        "overview": summary,
        "interpretation": interpretation,
        "action": action,
        "consulting": consulting,
    }


@pytest.fixture(scope="module")
def case_0001_narratives(
    case_0001_bundle: dict[str, Any],
) -> tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative]:
    """CASE-0001 Summary, Interpretation, and Action."""
    return (
        case_0001_bundle["overview"],
        case_0001_bundle["interpretation"],
        case_0001_bundle["action"],
    )


@pytest.fixture(scope="module")
def case_0001_consulting(case_0001_bundle: dict[str, Any]) -> ConsultingNarrative:
    """CASE-0001 ConsultingNarrative. Presentation copies flow only."""
    return case_0001_bundle["consulting"]
