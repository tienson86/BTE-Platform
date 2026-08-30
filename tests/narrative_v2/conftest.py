"""Shared fixtures for Narrative V2 evidence tests."""

from __future__ import annotations

from typing import Any

import pytest

from applications.api.services.orchestrator import OrchestratorService
from applications.production.fixtures.case_0001 import CASE_0001_REQUEST
from engines.narrative_v2.action import ActionBuilder, ActionPlanNarrative
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
def case_0001_narratives(
    case_0001_canonical: dict[str, Any],
) -> tuple[OverviewSummary, InterpretationNarrative, ActionPlanNarrative]:
    """CASE-0001 Summary, Interpretation, and Action. No Presentation rewrite."""
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    rewrite = RewriteEngine().rewrite(knowledge, reasoning, evidence)
    summary = SummaryBuilder().build(rewrite)
    interpretation = InterpretationBuilder().build(rewrite)
    action = ActionBuilder().build(rewrite, interpretation)
    return summary, interpretation, action
