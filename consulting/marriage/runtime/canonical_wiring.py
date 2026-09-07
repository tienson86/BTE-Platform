"""TV1-B02 Canonical runtime wiring. Does not replace TV1-B01 placeholder wiring."""

from __future__ import annotations

import logging

from consulting.marriage.adapters.canonical_runtime import CanonicalOrchestratorAdapter
from consulting.marriage.api.placeholder import PlaceholderMarriageApi
from consulting.marriage.decision.placeholder import PlaceholderMarriageDecisionResolver
from consulting.marriage.evidence.placeholder import PlaceholderMarriageEvidenceBuilder
from consulting.marriage.finding.placeholder import PlaceholderMarriageFindingBuilder
from consulting.marriage.policy.placeholder import PlaceholderMarriagePolicyProvider
from consulting.marriage.presentation.placeholder import PlaceholderMarriagePresentationAdapter
from consulting.marriage.recommendation.placeholder import (
    PlaceholderMarriageRecommendationProvider,
)
from consulting.marriage.report.placeholder import PlaceholderMarriageReportProfile
from consulting.marriage.repository.placeholder import PlaceholderMarriageRepository
from consulting.marriage.runtime.container import MarriageContainer
from consulting.marriage.runtime.pipeline import MarriageRuntimeOrchestrator
from consulting.marriage.ui.placeholder import PlaceholderMarriageUILayoutProfile
from consulting.marriage.validation.runtime import MarriageRuntimeValidation

logger = logging.getLogger(__name__)


def wire_marriage_canonical_runtime(
    *,
    canonical_adapter: CanonicalOrchestratorAdapter | None = None,
) -> MarriageContainer:
    """Bind TV1-B02 runtime implementations. Later-phase contracts stay placeholders."""
    validation = MarriageRuntimeValidation()
    adapter = canonical_adapter or CanonicalOrchestratorAdapter()
    orchestrator = MarriageRuntimeOrchestrator(
        validation=validation,
        canonical_adapter=adapter,
    )
    logger.info(
        "marriage_canonical_runtime_wired",
        extra={"stage": "wiring", "status": "registered", "consultation_id": None},
    )
    return MarriageContainer(
        orchestrator=orchestrator,
        repository=PlaceholderMarriageRepository(),
        policy_provider=PlaceholderMarriagePolicyProvider(),
        evidence_builder=PlaceholderMarriageEvidenceBuilder(),
        finding_builder=PlaceholderMarriageFindingBuilder(),
        decision_resolver=PlaceholderMarriageDecisionResolver(),
        recommendation_provider=PlaceholderMarriageRecommendationProvider(),
        report_profile=PlaceholderMarriageReportProfile(),
        presentation_adapter=PlaceholderMarriagePresentationAdapter(),
        ui_layout_profile=PlaceholderMarriageUILayoutProfile(),
        api_contract=PlaceholderMarriageApi(),
        validation=validation,
        canonical_adapter=adapter,
    )
