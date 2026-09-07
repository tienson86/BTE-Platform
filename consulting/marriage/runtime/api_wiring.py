"""TV1-B06 public API wiring. Does not replace B01–B05 factories."""

from __future__ import annotations

import logging

from consulting.marriage.adapters.canonical_runtime import CanonicalOrchestratorAdapter
from consulting.marriage.api.service import MarriageConsultationApi
from consulting.marriage.decision.resolver import MarriageDecisionResolverV1
from consulting.marriage.evidence.extractor import CanonicalEvidenceBuilder
from consulting.marriage.evidence.resolver import MarriageEvidenceResolver
from consulting.marriage.finding.resolver import CanonicalFindingBuilder
from consulting.marriage.narrative.composer import CanonicalNarrativeComposer
from consulting.marriage.policy.provider import MarriagePolicyV1Provider
from consulting.marriage.presentation.placeholder import PlaceholderMarriagePresentationAdapter
from consulting.marriage.recommendation.builder import CanonicalRecommendationProvider
from consulting.marriage.report.profile import MarriageReportProfileV1
from consulting.marriage.repository.memory import InMemoryMarriageRepository
from consulting.marriage.runtime.container import MarriageContainer
from consulting.marriage.runtime.narrative_pipeline import MarriageReportOrchestrator
from consulting.marriage.ui.placeholder import PlaceholderMarriageUILayoutProfile
from consulting.marriage.validation.narrative import MarriageReportValidation

logger = logging.getLogger(__name__)


def wire_marriage_api_runtime(
    *,
    canonical_adapter: CanonicalOrchestratorAdapter | None = None,
    repository: InMemoryMarriageRepository | None = None,
) -> MarriageContainer:
    """Bind TV1-B06 API and in-memory repository. UI stays unimplemented."""
    validation = MarriageReportValidation()
    adapter = canonical_adapter or CanonicalOrchestratorAdapter()
    policy_provider = MarriagePolicyV1Provider()
    evidence_builder = CanonicalEvidenceBuilder()
    finding_builder = CanonicalFindingBuilder()
    decision_resolver = MarriageDecisionResolverV1()
    recommendation_provider = CanonicalRecommendationProvider()
    narrative_composer = CanonicalNarrativeComposer()
    report_profile = MarriageReportProfileV1()
    store = repository or InMemoryMarriageRepository()
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
    api_contract = MarriageConsultationApi(
        orchestrator=orchestrator,
        repository=store,
        validation=validation,
    )
    logger.info(
        "marriage_api_runtime_wired",
        extra={"stage": "wiring", "status": "registered", "consultation_id": None},
    )
    return MarriageContainer(
        orchestrator=orchestrator,
        repository=store,
        policy_provider=policy_provider,
        evidence_builder=evidence_builder,
        finding_builder=finding_builder,
        decision_resolver=decision_resolver,
        recommendation_provider=recommendation_provider,
        report_profile=report_profile,
        presentation_adapter=PlaceholderMarriagePresentationAdapter(),
        ui_layout_profile=PlaceholderMarriageUILayoutProfile(),
        api_contract=api_contract,
        validation=validation,
        canonical_adapter=adapter,
    )
