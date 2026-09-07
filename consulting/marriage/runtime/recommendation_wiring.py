"""TV1-B04 recommendation wiring. Does not replace B01–B03 factories."""

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
from consulting.marriage.recommendation.builder import CanonicalRecommendationProvider
from consulting.marriage.report.placeholder import PlaceholderMarriageReportProfile
from consulting.marriage.repository.placeholder import PlaceholderMarriageRepository
from consulting.marriage.runtime.container import MarriageContainer
from consulting.marriage.runtime.recommendation_pipeline import MarriageRecommendationOrchestrator
from consulting.marriage.ui.placeholder import PlaceholderMarriageUILayoutProfile
from consulting.marriage.validation.recommendation import MarriageRecommendationValidation

logger = logging.getLogger(__name__)


def wire_marriage_recommendation_runtime(
    *,
    canonical_adapter: CanonicalOrchestratorAdapter | None = None,
) -> MarriageContainer:
    """Bind TV1-B04 recommendation implementations. Report/UI/API stay placeholders."""
    validation = MarriageRecommendationValidation()
    adapter = canonical_adapter or CanonicalOrchestratorAdapter()
    policy_provider = MarriagePolicyV1Provider()
    evidence_builder = CanonicalEvidenceBuilder()
    finding_builder = CanonicalFindingBuilder()
    decision_resolver = MarriageDecisionResolverV1()
    recommendation_provider = CanonicalRecommendationProvider()
    orchestrator = MarriageRecommendationOrchestrator(
        validation=validation,
        canonical_adapter=adapter,
        policy_provider=policy_provider,
        evidence_builder=evidence_builder,
        evidence_resolver=MarriageEvidenceResolver(),
        finding_builder=finding_builder,
        decision_resolver=decision_resolver,
        recommendation_provider=recommendation_provider,
    )
    logger.info(
        "marriage_recommendation_runtime_wired",
        extra={"stage": "wiring", "status": "registered", "consultation_id": None},
    )
    return MarriageContainer(
        orchestrator=orchestrator,
        repository=PlaceholderMarriageRepository(),
        policy_provider=policy_provider,
        evidence_builder=evidence_builder,
        finding_builder=finding_builder,
        decision_resolver=decision_resolver,
        recommendation_provider=recommendation_provider,
        report_profile=PlaceholderMarriageReportProfile(),
        presentation_adapter=PlaceholderMarriagePresentationAdapter(),
        ui_layout_profile=PlaceholderMarriageUILayoutProfile(),
        api_contract=PlaceholderMarriageApi(),
        validation=validation,
        canonical_adapter=adapter,
    )
