"""TV1-B04 recommendation pipeline. Continues from the B03 decision seam."""

from __future__ import annotations

from consulting.marriage.adapters.canonical_runtime import CanonicalOrchestratorAdapter
from consulting.marriage.decision.resolver import MarriageDecisionResolverV1
from consulting.marriage.exceptions import MarriageInternalError
from consulting.marriage.evidence.extractor import CanonicalEvidenceBuilder
from consulting.marriage.evidence.resolver import MarriageEvidenceResolver
from consulting.marriage.finding.resolver import CanonicalFindingBuilder
from consulting.marriage.policy.provider import MarriagePolicyV1Provider
from consulting.marriage.recommendation.builder import CanonicalRecommendationProvider
from consulting.marriage.runtime.decision_pipeline import MarriageDecisionOrchestrator
from consulting.marriage.runtime.lifecycle import RuntimeLifecycleState
from consulting.marriage.runtime.session import MarriageRuntimeSession
from consulting.marriage.validation.recommendation import MarriageRecommendationValidation

B04_PIPELINE_STAGES: tuple[str, ...] = (
    "recommendation_builder",
    "recommendation_validation",
)

BUILD_PHASE_B04 = "TV1-B04"


class MarriageRecommendationOrchestrator(MarriageDecisionOrchestrator):
    """B03 decision plus structured Recommendation. Stops before Narrative."""

    def __init__(
        self,
        *,
        validation: MarriageRecommendationValidation,
        canonical_adapter: CanonicalOrchestratorAdapter,
        policy_provider: MarriagePolicyV1Provider,
        evidence_builder: CanonicalEvidenceBuilder,
        evidence_resolver: MarriageEvidenceResolver,
        finding_builder: CanonicalFindingBuilder,
        decision_resolver: MarriageDecisionResolverV1,
        recommendation_provider: CanonicalRecommendationProvider,
    ) -> None:
        super().__init__(
            validation=validation,
            canonical_adapter=canonical_adapter,
            policy_provider=policy_provider,
            evidence_builder=evidence_builder,
            evidence_resolver=evidence_resolver,
            finding_builder=finding_builder,
            decision_resolver=decision_resolver,
        )
        self._recommendation_provider = recommendation_provider
        self._recommendation_validation = validation

    def _after_decision(self, session: MarriageRuntimeSession) -> None:
        """Continue from DECISION_READY through RECOMMENDATION_READY."""
        self._run_recommendation_layer(session)
        self._after_recommendation(session)

    def _after_recommendation(self, session: MarriageRuntimeSession) -> None:
        """B04 stop. Later phases continue from recommendation-ready through this seam."""
        session.transition(RuntimeLifecycleState.COMPLETED)

    def _run_recommendation_layer(self, session: MarriageRuntimeSession) -> None:
        """Build and validate actions from the already-validated Decision Result."""
        consultation_id = session.context.consultation_id
        result = session.context.decision_result
        if result is None:
            raise MarriageInternalError("decision_result_missing")
        overall_state = result.overall.state
        overall_score = result.overall.score
        finding_ids = [item.finding_id for item in result.findings]

        def build() -> None:
            recommendations = self._recommendation_provider.provide(result)
            result.recommendations = recommendations
            session.context.recommendations = recommendations

        self._run_stage(consultation_id, session, B04_PIPELINE_STAGES[0], build)
        recommendations = result.recommendations

        def validate() -> None:
            self._recommendation_validation.validate_recommendations(result, recommendations)

        self._run_stage(consultation_id, session, B04_PIPELINE_STAGES[1], validate)
        if result.overall.state != overall_state or result.overall.score != overall_score:
            raise MarriageInternalError("decision_mutated_by_recommendation")
        if [item.finding_id for item in result.findings] != finding_ids:
            raise MarriageInternalError("findings_mutated_by_recommendation")
        session.transition(RuntimeLifecycleState.RECOMMENDATION_READY)
