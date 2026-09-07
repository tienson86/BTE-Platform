"""TV1-B03 decision wiring. Does not replace B01 or B02 factories."""

from __future__ import annotations

import logging

from consulting.marriage.adapters.canonical_runtime import CanonicalOrchestratorAdapter
from consulting.marriage.api.placeholder import PlaceholderMarriageApi
from consulting.marriage.decision.resolver import MarriageDecisionResolverV1
from consulting.marriage.evidence.extractor import CanonicalEvidenceBuilder
from consulting.marriage.evidence.resolver import MarriageEvidenceResolver
from consulting.marriage.finding.resolver import CanonicalFindingBuilder
from consulting.marriage.policy.provider import MarriagePolicyV1Provider
from consulting.marriage.presentation.placeholder import PlaceholderMarriagePresentationAdapter
from consulting.marriage.recommendation.placeholder import (
    PlaceholderMarriageRecommendationProvider,
)
from consulting.marriage.report.placeholder import PlaceholderMarriageReportProfile
from consulting.marriage.repository.placeholder import PlaceholderMarriageRepository
from consulting.marriage.runtime.container import MarriageContainer
from consulting.marriage.runtime.decision_pipeline import MarriageDecisionOrchestrator
from consulting.marriage.ui.placeholder import PlaceholderMarriageUILayoutProfile
from consulting.marriage.validation.decision import MarriageDecisionValidation

logger = logging.getLogger(__name__)


def wire_marriage_decision_runtime(
    *,
    canonical_adapter: CanonicalOrchestratorAdapter | None = None,
) -> MarriageContainer:
    """Bind TV1-B03 decision implementations. Recommendation/report stay placeholders."""
    validation = MarriageDecisionValidation()
    adapter = canonical_adapter or CanonicalOrchestratorAdapter()
    policy_provider = MarriagePolicyV1Provider()
    evidence_builder = CanonicalEvidenceBuilder()
    finding_builder = CanonicalFindingBuilder()
    decision_resolver = MarriageDecisionResolverV1()
    orchestrator = MarriageDecisionOrchestrator(
        validation=validation,
        canonical_adapter=adapter,
        policy_provider=policy_provider,
        evidence_builder=evidence_builder,
        evidence_resolver=MarriageEvidenceResolver(),
        finding_builder=finding_builder,
        decision_resolver=decision_resolver,
    )
    logger.info(
        "marriage_decision_runtime_wired",
        extra={"stage": "wiring", "status": "registered", "consultation_id": None},
    )
    return MarriageContainer(
        orchestrator=orchestrator,
        repository=PlaceholderMarriageRepository(),
        policy_provider=policy_provider,
        evidence_builder=evidence_builder,
        finding_builder=finding_builder,
        decision_resolver=decision_resolver,
        recommendation_provider=PlaceholderMarriageRecommendationProvider(),
        report_profile=PlaceholderMarriageReportProfile(),
        presentation_adapter=PlaceholderMarriagePresentationAdapter(),
        ui_layout_profile=PlaceholderMarriageUILayoutProfile(),
        api_contract=PlaceholderMarriageApi(),
        validation=validation,
        canonical_adapter=adapter,
    )
