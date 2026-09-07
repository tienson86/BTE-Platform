"""Marriage orchestrator shell. TV1-B01: wiring only, no runtime execution."""

from __future__ import annotations

from consulting.marriage.adapters.contract import CanonicalRuntimeAdapter
from consulting.marriage.dto.request import MarriageConsultationRequest
from consulting.marriage.dto.response import MarriageRuntimeResponse
from consulting.marriage.evidence.contract import MarriageEvidenceBuilder
from consulting.marriage.finding.contract import MarriageFindingBuilder
from consulting.marriage.orchestrator.contract import MarriageOrchestrator
from consulting.marriage.policy.contract import MarriagePolicyProvider
from consulting.marriage.recommendation.contract import MarriageRecommendationProvider
from consulting.marriage.report.contract import MarriageReportProfile
from consulting.marriage.repository.contract import MarriageRepository
from consulting.marriage.ui.contract import MarriageUILayoutProfile
from consulting.marriage.validation.contract import MarriageValidationContract


class MarriageOrchestratorShell(MarriageOrchestrator):
    """Dependency-injected orchestrator shell. Pipeline is not executed in TV1-B01."""

    def __init__(
        self,
        *,
        validation: MarriageValidationContract,
        canonical_adapter: CanonicalRuntimeAdapter,
        repository: MarriageRepository,
        policy_provider: MarriagePolicyProvider,
        evidence_builder: MarriageEvidenceBuilder,
        finding_builder: MarriageFindingBuilder,
        recommendation_provider: MarriageRecommendationProvider,
        report_profile: MarriageReportProfile,
        ui_layout_profile: MarriageUILayoutProfile,
    ) -> None:
        self._validation = validation
        self._canonical_adapter = canonical_adapter
        self._repository = repository
        self._policy_provider = policy_provider
        self._evidence_builder = evidence_builder
        self._finding_builder = finding_builder
        self._recommendation_provider = recommendation_provider
        self._report_profile = report_profile
        self._ui_layout_profile = ui_layout_profile

    def run(self, request: MarriageConsultationRequest) -> MarriageRuntimeResponse:
        """Refuse execution. Runtime integration belongs to TV1-B02."""
        raise NotImplementedError("TV1-B01: Marriage runtime is not implemented")
