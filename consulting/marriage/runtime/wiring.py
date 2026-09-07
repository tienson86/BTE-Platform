"""Runtime wiring for TV-01 Marriage Consulting.

Registers placeholders only. Does not start Canonical or Decision runtime.
"""

from __future__ import annotations

import logging

from consulting.marriage.adapters.placeholder import PlaceholderCanonicalRuntimeAdapter
from consulting.marriage.api.placeholder import PlaceholderMarriageApi
from consulting.marriage.decision.placeholder import PlaceholderMarriageDecisionResolver
from consulting.marriage.evidence.placeholder import PlaceholderMarriageEvidenceBuilder
from consulting.marriage.finding.placeholder import PlaceholderMarriageFindingBuilder
from consulting.marriage.orchestrator.shell import MarriageOrchestratorShell
from consulting.marriage.policy.placeholder import PlaceholderMarriagePolicyProvider
from consulting.marriage.presentation.placeholder import PlaceholderMarriagePresentationAdapter
from consulting.marriage.recommendation.placeholder import (
    PlaceholderMarriageRecommendationProvider,
)
from consulting.marriage.report.placeholder import PlaceholderMarriageReportProfile
from consulting.marriage.repository.placeholder import PlaceholderMarriageRepository
from consulting.marriage.runtime.container import MarriageContainer
from consulting.marriage.ui.placeholder import PlaceholderMarriageUILayoutProfile
from consulting.marriage.validation.placeholder import PlaceholderMarriageValidation

logger = logging.getLogger(__name__)


def wire_marriage_runtime() -> MarriageContainer:
    """Create a TV-01 container with placeholder implementations.

    Returns:
        A fully bound MarriageContainer. Orchestrator.run is not executable in TV1-B01.
    """
    validation = PlaceholderMarriageValidation()
    canonical_adapter = PlaceholderCanonicalRuntimeAdapter()
    repository = PlaceholderMarriageRepository()
    policy_provider = PlaceholderMarriagePolicyProvider()
    evidence_builder = PlaceholderMarriageEvidenceBuilder()
    finding_builder = PlaceholderMarriageFindingBuilder()
    decision_resolver = PlaceholderMarriageDecisionResolver()
    recommendation_provider = PlaceholderMarriageRecommendationProvider()
    report_profile = PlaceholderMarriageReportProfile()
    presentation_adapter = PlaceholderMarriagePresentationAdapter()
    ui_layout_profile = PlaceholderMarriageUILayoutProfile()
    api_contract = PlaceholderMarriageApi()
    orchestrator = MarriageOrchestratorShell(
        validation=validation,
        canonical_adapter=canonical_adapter,
        repository=repository,
        policy_provider=policy_provider,
        evidence_builder=evidence_builder,
        finding_builder=finding_builder,
        recommendation_provider=recommendation_provider,
        report_profile=report_profile,
        ui_layout_profile=ui_layout_profile,
    )
    logger.info(
        "marriage_runtime_wired",
        extra={"stage": "wiring", "status": "registered", "consultation_id": None},
    )
    return MarriageContainer(
        orchestrator=orchestrator,
        repository=repository,
        policy_provider=policy_provider,
        evidence_builder=evidence_builder,
        finding_builder=finding_builder,
        decision_resolver=decision_resolver,
        recommendation_provider=recommendation_provider,
        report_profile=report_profile,
        presentation_adapter=presentation_adapter,
        ui_layout_profile=ui_layout_profile,
        api_contract=api_contract,
        validation=validation,
        canonical_adapter=canonical_adapter,
    )
