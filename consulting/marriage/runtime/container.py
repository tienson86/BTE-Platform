"""Marriage consulting service container. Constructor injection. No global singleton."""

from __future__ import annotations

from dataclasses import dataclass

from consulting.marriage.adapters.contract import CanonicalRuntimeAdapter
from consulting.marriage.api.contract import MarriageApiContract
from consulting.marriage.decision.contract import MarriageDecisionResolver
from consulting.marriage.evidence.contract import MarriageEvidenceBuilder
from consulting.marriage.finding.contract import MarriageFindingBuilder
from consulting.marriage.orchestrator.contract import MarriageOrchestrator
from consulting.marriage.policy.contract import MarriagePolicyProvider
from consulting.marriage.presentation.contract import MarriagePresentationAdapter
from consulting.marriage.recommendation.contract import MarriageRecommendationProvider
from consulting.marriage.report.contract import MarriageReportProfile
from consulting.marriage.repository.contract import MarriageRepository
from consulting.marriage.ui.contract import MarriageUILayoutProfile
from consulting.marriage.validation.contract import MarriageValidationContract


@dataclass(slots=True)
class MarriageContainer:
    """Bound TV-01 contracts. Implementations are injected, never constructed inline by callers."""

    orchestrator: MarriageOrchestrator
    repository: MarriageRepository
    policy_provider: MarriagePolicyProvider
    evidence_builder: MarriageEvidenceBuilder
    finding_builder: MarriageFindingBuilder
    decision_resolver: MarriageDecisionResolver
    recommendation_provider: MarriageRecommendationProvider
    report_profile: MarriageReportProfile
    presentation_adapter: MarriagePresentationAdapter
    ui_layout_profile: MarriageUILayoutProfile
    api_contract: MarriageApiContract
    validation: MarriageValidationContract
    canonical_adapter: CanonicalRuntimeAdapter
