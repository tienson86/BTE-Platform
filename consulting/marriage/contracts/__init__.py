"""Public TV-01 contracts. Re-exports only. No logic."""

from __future__ import annotations

from consulting.marriage.adapters.contract import CanonicalRuntimeAdapter
from consulting.marriage.api.contract import MarriageApiContract
from consulting.marriage.decision.context import MarriageDecisionContext
from consulting.marriage.decision.contract import MarriageDecisionResolver
from consulting.marriage.evidence.contract import MarriageEvidenceBuilder
from consulting.marriage.finding.contract import MarriageFindingBuilder
from consulting.marriage.orchestrator.contract import MarriageOrchestrator
from consulting.marriage.policy.contract import MarriagePolicyDescriptor, MarriagePolicyProvider
from consulting.marriage.presentation.contract import MarriagePresentationAdapter
from consulting.marriage.recommendation.contract import MarriageRecommendationProvider
from consulting.marriage.report.contract import MarriageReportProfile, MarriageReportProfileDescriptor
from consulting.marriage.repository.contract import MarriageRepository
from consulting.marriage.runtime.context import MarriageRuntimeContext
from consulting.marriage.ui.contract import MarriageUILayoutProfile, MarriageUILayoutProfileDescriptor
from consulting.marriage.validation.contract import MarriageValidationContract

__all__ = [
    "CanonicalRuntimeAdapter",
    "MarriageApiContract",
    "MarriageDecisionContext",
    "MarriageDecisionResolver",
    "MarriageEvidenceBuilder",
    "MarriageFindingBuilder",
    "MarriageOrchestrator",
    "MarriagePolicyDescriptor",
    "MarriagePolicyProvider",
    "MarriagePresentationAdapter",
    "MarriageRecommendationProvider",
    "MarriageReportProfile",
    "MarriageReportProfileDescriptor",
    "MarriageRepository",
    "MarriageRuntimeContext",
    "MarriageUILayoutProfile",
    "MarriageUILayoutProfileDescriptor",
    "MarriageValidationContract",
]
