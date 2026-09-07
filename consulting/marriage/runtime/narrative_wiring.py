"""TV1-B05 narrative/report wiring. Does not replace B01–B04 factories."""

from __future__ import annotations

import logging

from consulting.marriage.adapters.canonical_runtime import CanonicalOrchestratorAdapter
from consulting.marriage.api.placeholder import PlaceholderMarriageApi
from consulting.marriage.decision.resolver import MarriageDecisionResolverV1
from consulting.marriage.evidence.extractor import CanonicalEvidenceBuilder
from consulting.marriage.evidence.resolver import MarriageEvidenceResolver
from consulting.marriage.finding.resolver import CanonicalFindingBuilder
from consulting.marriage.narrative.composer import CanonicalNarrativeComposer
from consulting.marriage.policy.provider import MarriagePolicyV1Provider
from consulting.marriage.presentation.placeholder import PlaceholderMarriagePresentationAdapter
from consulting.marriage.recommendation.builder import CanonicalRecommendationProvider
from consulting.marriage.report.profile import MarriageReportProfileV1
from consulting.marriage.repository.placeholder import PlaceholderMarriageRepository
from consulting.marriage.runtime.container import MarriageContainer
from consulting.marriage.runtime.narrative_pipeline import MarriageReportOrchestrator
from consulting.marriage.ui.placeholder import PlaceholderMarriageUILayoutProfile
from consulting.marriage.validation.narrative import MarriageReportValidation

logger = logging.getLogger(__name__)


def wire_marriage_report_runtime(
    *,
    canonical_adapter: CanonicalOrchestratorAdapter | None = None,
) -> MarriageContainer:
    """Bind TV1-B05 narrative and report implementations. UI/API stay placeholders."""
    validation = MarriageReportValidation()
    adapter = canonical_adapter or CanonicalOrchestratorAdapter()
    policy_provider = MarriagePolicyV1Provider()
    evidence_builder = CanonicalEvidenceBuilder()
    finding_builder = CanonicalFindingBuilder()
    decision_resolver = MarriageDecisionResolverV1()
    recommendation_provider = CanonicalRecommendationProvider()
    narrative_composer = CanonicalNarrativeComposer()
    report_profile = MarriageReportProfileV1()
    orchestrator = MarriageReportOrchestrator(
        validation=validation,
        canonical_adapter=adapter,
        policy_provider=policy_provider,
        evidence_builder=evidence_builder,
        evidence_resolver=MarriageEvidenceResolver(),
        finding_builder=finding_builder,
        decision_resolver=decision_resolver,
        recommendation_provider=recommendation_provider,
        narrative_composer=narrative_composer,
        report_profile=report_profile,
    )
    logger.info(
        "marriage_report_runtime_wired",
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
        report_profile=report_profile,
        presentation_adapter=PlaceholderMarriagePresentationAdapter(),
        ui_layout_profile=PlaceholderMarriageUILayoutProfile(),
        api_contract=PlaceholderMarriageApi(),
        validation=validation,
        canonical_adapter=adapter,
    )
