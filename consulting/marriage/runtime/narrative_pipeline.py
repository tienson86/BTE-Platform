"""TV1-B05 narrative and report pipeline. Continues from the B04 recommendation seam."""

from __future__ import annotations

from consulting.marriage.adapters.canonical_runtime import CanonicalOrchestratorAdapter
from consulting.marriage.decision.resolver import MarriageDecisionResolverV1
from consulting.marriage.exceptions import MarriageInternalError
from consulting.marriage.evidence.extractor import CanonicalEvidenceBuilder
from consulting.marriage.evidence.resolver import MarriageEvidenceResolver
from consulting.marriage.finding.resolver import CanonicalFindingBuilder
from consulting.marriage.narrative.composer import CanonicalNarrativeComposer
from consulting.marriage.narrative.input import narrative_input_from_decision
from consulting.marriage.narrative.versions import AUDIENCE_CUSTOMER, LANGUAGE_VI, NARRATIVE_VERSION
from consulting.marriage.policy.provider import MarriagePolicyV1Provider
from consulting.marriage.recommendation.builder import CanonicalRecommendationProvider
from consulting.marriage.report.profile import MarriageReportProfileV1
from consulting.marriage.runtime.lifecycle import RuntimeLifecycleState
from consulting.marriage.runtime.recommendation_pipeline import MarriageRecommendationOrchestrator
from consulting.marriage.runtime.session import MarriageRuntimeSession
from consulting.marriage.validation.narrative import MarriageReportValidation

B05_PIPELINE_STAGES: tuple[str, ...] = (
    "narrative_composer",
    "narrative_validation",
    "report_builder",
    "report_validation",
)

BUILD_PHASE_B05 = "TV1-B05"


class MarriageReportOrchestrator(MarriageRecommendationOrchestrator):
    """B04 recommendations plus Narrative and semantic Report. Stops before API/UI."""

    def __init__(
        self,
        *,
        validation: MarriageReportValidation,
        canonical_adapter: CanonicalOrchestratorAdapter,
        policy_provider: MarriagePolicyV1Provider,
        evidence_builder: CanonicalEvidenceBuilder,
        evidence_resolver: MarriageEvidenceResolver,
        finding_builder: CanonicalFindingBuilder,
        decision_resolver: MarriageDecisionResolverV1,
        recommendation_provider: CanonicalRecommendationProvider,
        narrative_composer: CanonicalNarrativeComposer,
        report_profile: MarriageReportProfileV1,
    ) -> None:
        super().__init__(
            validation=validation,
            canonical_adapter=canonical_adapter,
            policy_provider=policy_provider,
            evidence_builder=evidence_builder,
            evidence_resolver=evidence_resolver,
            finding_builder=finding_builder,
            decision_resolver=decision_resolver,
            recommendation_provider=recommendation_provider,
        )
        self._narrative_composer = narrative_composer
        self._report_profile = report_profile
        self._report_validation = validation

    def _after_recommendation(self, session: MarriageRuntimeSession) -> None:
        """Continue from RECOMMENDATION_READY through REPORT_READY."""
        self._run_narrative_layer(session)
        self._run_report_layer(session)
        self._after_report(session)

    def _after_report(self, session: MarriageRuntimeSession) -> None:
        """B05 stop. Later phases continue from report-ready through this seam."""
        session.transition(RuntimeLifecycleState.COMPLETED)

    def _run_narrative_layer(self, session: MarriageRuntimeSession) -> None:
        """Compose and validate narrative from Decision/Recommendation only."""
        consultation_id = session.context.consultation_id
        result = session.context.decision_result
        if result is None:
            raise MarriageInternalError("decision_result_missing")
        overall_state = result.overall.state
        overall_score = result.overall.score
        finding_ids = [item.finding_id for item in result.findings]
        rec_ids = [item.recommendation_id for item in result.recommendations]

        def compose() -> None:
            payload = narrative_input_from_decision(
                result,
                language=LANGUAGE_VI,
                audience=AUDIENCE_CUSTOMER,
            )
            narrative = self._narrative_composer.compose(payload)
            session.context.narrative = narrative
            result.versions.narrative_version = NARRATIVE_VERSION

        self._run_stage(consultation_id, session, B05_PIPELINE_STAGES[0], compose)
        narrative = session.context.narrative
        if narrative is None:
            raise MarriageInternalError("narrative_missing")

        def validate_narrative() -> None:
            self._report_validation.validate_narrative(result, narrative)

        self._run_stage(consultation_id, session, B05_PIPELINE_STAGES[1], validate_narrative)
        if result.overall.state != overall_state or result.overall.score != overall_score:
            raise MarriageInternalError("decision_mutated_by_narrative")
        if [item.finding_id for item in result.findings] != finding_ids:
            raise MarriageInternalError("findings_mutated_by_narrative")
        if [item.recommendation_id for item in result.recommendations] != rec_ids:
            raise MarriageInternalError("recommendations_mutated_by_narrative")
        session.transition(RuntimeLifecycleState.NARRATIVE_READY)

    def _run_report_layer(self, session: MarriageRuntimeSession) -> None:
        """Build and validate the semantic report model."""
        consultation_id = session.context.consultation_id
        result = session.context.decision_result
        narrative = session.context.narrative
        if result is None or narrative is None:
            raise MarriageInternalError("narrative_required_for_report")
        overall_state = result.overall.state
        rec_ids = [item.recommendation_id for item in result.recommendations]

        def build() -> None:
            payload = narrative_input_from_decision(
                result,
                language=LANGUAGE_VI,
                audience=AUDIENCE_CUSTOMER,
            )
            report = self._report_profile.compose(payload, narrative)
            session.context.report_model = report

        self._run_stage(consultation_id, session, B05_PIPELINE_STAGES[2], build)
        report = session.context.report_model
        if report is None:
            raise MarriageInternalError("report_model_missing")

        def validate_report() -> None:
            self._report_validation.validate_report(result, narrative, report)

        self._run_stage(consultation_id, session, B05_PIPELINE_STAGES[3], validate_report)
        if result.overall.state != overall_state:
            raise MarriageInternalError("decision_mutated_by_report")
        if [item.recommendation_id for item in result.recommendations] != rec_ids:
            raise MarriageInternalError("recommendations_mutated_by_report")
        session.transition(RuntimeLifecycleState.REPORT_READY)
