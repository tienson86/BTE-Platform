"""TV1-B03 decision pipeline. Continues from the B02 snapshot seam."""

from __future__ import annotations

from datetime import datetime, timezone

from consulting.marriage.adapters.canonical_runtime import CanonicalOrchestratorAdapter
from consulting.marriage.constants import MODULE_VERSION
from consulting.marriage.assessment.projector import project_marriage_assessment
from consulting.marriage.decision.comparison import build_marriage_comparison
from consulting.marriage.decision.context import MarriageDecisionContext
from consulting.marriage.decision.resolver import MarriageDecisionResolverV1, build_confidence
from consulting.marriage.exceptions import MarriageInternalError
from consulting.marriage.evidence.extractor import CanonicalEvidenceBuilder
from consulting.marriage.evidence.resolver import MarriageEvidenceResolver
from consulting.marriage.finding.resolver import CanonicalFindingBuilder
from consulting.marriage.models.context import MarriageRelationshipContext, RuntimeMeta
from consulting.marriage.models.decision import MarriageDomainResults, MarriageOverallDecision
from consulting.marriage.models.enums import MarriageDomain
from consulting.marriage.models.result import MarriageDecisionResult
from consulting.marriage.models.versioning import MarriageVersionBundle
from consulting.marriage.policy.context import MarriagePolicyContext
from consulting.marriage.policy.provider import MarriagePolicyV1Provider
from consulting.marriage.policy.versions import (
    EVIDENCE_CATALOG_VERSION,
    SCORE_MODEL_VERSION,
    policy_version_token,
)
from consulting.marriage.runtime.lifecycle import RuntimeLifecycleState
from consulting.marriage.runtime.phase import UNBOUND_VERSION
from consulting.marriage.runtime.pipeline import MarriageRuntimeOrchestrator
from consulting.marriage.runtime.session import MarriageRuntimeSession
from consulting.marriage.validation.decision import MarriageDecisionValidation

B03_PIPELINE_STAGES: tuple[str, ...] = (
    "evidence_builder",
    "evidence_validation",
    "domain_decision",
    "cross_domain_resolver",
    "overall_decision",
    "decision_validation",
)

BUILD_PHASE_B03 = "TV1-B03"


class MarriageDecisionOrchestrator(MarriageRuntimeOrchestrator):
    """B02 snapshots plus Marriage Decision. Stops before Recommendation."""

    def __init__(
        self,
        *,
        validation: MarriageDecisionValidation,
        canonical_adapter: CanonicalOrchestratorAdapter,
        policy_provider: MarriagePolicyV1Provider,
        evidence_builder: CanonicalEvidenceBuilder,
        evidence_resolver: MarriageEvidenceResolver,
        finding_builder: CanonicalFindingBuilder,
        decision_resolver: MarriageDecisionResolverV1,
    ) -> None:
        super().__init__(validation=validation, canonical_adapter=canonical_adapter)
        self._policy_provider = policy_provider
        self._evidence_builder = evidence_builder
        self._evidence_resolver = evidence_resolver
        self._finding_builder = finding_builder
        self._decision_resolver = decision_resolver
        self._decision_validation = validation

    def _after_snapshots(self, session: MarriageRuntimeSession) -> None:
        """Continue from SNAPSHOT_READY through DECISION_READY."""
        self._run_decision_layer(session)
        self._after_decision(session)

    def _after_decision(self, session: MarriageRuntimeSession) -> None:
        """B03 stop. Later phases continue from decision-ready through this seam."""
        session.transition(RuntimeLifecycleState.COMPLETED)

    def _run_decision_layer(self, session: MarriageRuntimeSession) -> None:
        """Execute evidence and decision stages from snapshots only."""
        consultation_id = session.context.consultation_id
        policy_context = _policy_context(session)
        self._bind_versions(session)

        def build_evidence() -> None:
            evidence = self._evidence_builder.build_from_policy_context(policy_context)
            session.context.evidence = evidence

        self._run_stage(consultation_id, session, B03_PIPELINE_STAGES[0], build_evidence)
        evidence = session.context.evidence or []
        self._run_stage(
            consultation_id,
            session,
            B03_PIPELINE_STAGES[1],
            lambda: self._decision_validation.validate_evidence(evidence),
        )
        resolved = self._evidence_resolver.resolve(evidence)
        session.context.resolved_evidence = resolved
        findings = self._finding_builder.build_from_resolved(evidence, resolved)
        session.context.findings = findings
        session.transition(RuntimeLifecycleState.EVIDENCE_READY)
        relationship = _relationship_context(session, policy_context)
        decision_context = MarriageDecisionContext(
            consultation_id=consultation_id,
            relationship=relationship,
            versions=session.context.versions,
            evidence=evidence,
            findings=findings,
        )
        self._policy_provider.provide(decision_context)
        domains: MarriageDomainResults | None = None
        overall: MarriageOverallDecision | None = None

        def resolve_domains() -> None:
            nonlocal domains
            domains = self._decision_resolver.resolve_domains(decision_context)

        self._run_stage(consultation_id, session, B03_PIPELINE_STAGES[2], resolve_domains)
        self._run_stage(consultation_id, session, B03_PIPELINE_STAGES[3], lambda: None)

        def resolve_overall() -> None:
            nonlocal overall
            overall = self._decision_resolver.resolve_overall(decision_context)

        self._run_stage(consultation_id, session, B03_PIPELINE_STAGES[4], resolve_overall)
        if domains is None or overall is None:
            raise MarriageInternalError("decision_resolution_missing")
        snapshot_a = session.context.snapshot_a
        snapshot_b = session.context.snapshot_b
        if snapshot_a is None or snapshot_b is None:
            raise MarriageInternalError("snapshots_missing_after_decision")
        confidence = build_confidence(
            data_quality=_data_quality(snapshot_a, snapshot_b),
            evidence=evidence,
            limitations=list(policy_context.limitations),
            engine_coverage=_coverage(domains),
        )
        created_at = datetime.now(timezone.utc).isoformat()
        result = MarriageDecisionResult(
            consultation_id=consultation_id,
            person_a=snapshot_a.person,
            person_b=snapshot_b.person,
            canonical_a=snapshot_a,
            canonical_b=snapshot_b,
            evidence=evidence,
            domains=domains,
            overall=overall,
            recommendations=[],
            confidence=confidence,
            versions=session.context.versions,
            created_at=created_at,
            resolved_evidence=resolved,
            findings=findings,
            limitations=list(policy_context.limitations),
        )
        result.comparison = _build_comparison(result)
        result.assessment = project_marriage_assessment(result)
        self._run_stage(
            consultation_id,
            session,
            B03_PIPELINE_STAGES[5],
            lambda: self._decision_validation.validate_decision(result),
        )
        session.context.domain_results = domains
        session.context.overall = overall
        session.context.confidence = confidence
        session.context.decision_result = result
        session.transition(RuntimeLifecycleState.DECISION_READY)

    def _bind_versions(self, session: MarriageRuntimeSession) -> None:
        """Bind policy versions. Do not silently substitute Canonical versions."""
        snapshot_a = session.context.snapshot_a
        if snapshot_a is None:
            raise MarriageInternalError("snapshot_a_missing")
        session.context.versions = MarriageVersionBundle(
            module_version=MODULE_VERSION,
            decision_profile_version=policy_version_token(),
            score_model_version=SCORE_MODEL_VERSION,
            rule_catalog_version=EVIDENCE_CATALOG_VERSION,
            canonical_versions=snapshot_a.person.canonical_version,
            narrative_version=UNBOUND_VERSION,
        )


def _policy_context(session: MarriageRuntimeSession) -> MarriagePolicyContext:
    """Build a read-only policy context from snapshot-ready session state."""
    snapshot_a = session.context.snapshot_a
    snapshot_b = session.context.snapshot_b
    if snapshot_a is None or snapshot_b is None:
        raise MarriageInternalError("snapshots_required_for_policy_context")
    limitations = tuple(
        dict.fromkeys(
            [
                *snapshot_a.person.birth_data_quality.limitations,
                *snapshot_b.person.birth_data_quality.limitations,
            ]
        )
    )
    return MarriagePolicyContext(
        consultation_id=session.context.consultation_id,
        snapshot_a=snapshot_a,
        snapshot_b=snapshot_b,
        options=session.context.request.options,
        versions=session.context.versions,
        available_domains=(
            MarriageDomain.FIVE_ELEMENTS,
            MarriageDomain.STEM_BRANCH,
            MarriageDomain.TEN_GODS,
            MarriageDomain.INTERACTION,
            MarriageDomain.FINANCE,
            MarriageDomain.FAMILY,
            MarriageDomain.CHILDREN,
            MarriageDomain.LUCK,
        ),
        limitations=limitations,
        source_analysis_id_a=snapshot_a.source_analysis_id,
        source_analysis_id_b=snapshot_b.source_analysis_id,
    )


def _relationship_context(
    session: MarriageRuntimeSession,
    policy_context: MarriagePolicyContext,
) -> MarriageRelationshipContext:
    """Build the frozen relationship context used by Decision Context."""
    return MarriageRelationshipContext(
        person_a=policy_context.snapshot_a,
        person_b=policy_context.snapshot_b,
        options=policy_context.options,
        available_domains=list(policy_context.available_domains),
        limitations=list(policy_context.limitations),
        runtime_meta=RuntimeMeta(
            module_id="TV-01_MARRIAGE",
            build_phase=BUILD_PHASE_B03,
            pipeline_id=session.context.consultation_id,
        ),
    )


def _data_quality(snapshot_a, snapshot_b) -> float:
    """Average Canonical completeness. Missing hour is quality, not penalty."""
    return (
        snapshot_a.person.birth_data_quality.completeness_score
        + snapshot_b.person.birth_data_quality.completeness_score
    ) / 2.0


def _coverage(domains) -> float:
    """Fraction of V1 domains that have primary evidence."""
    flags = [
        domains.five_elements.availability.available,
        domains.stem_branch.availability.available,
        domains.ten_gods.availability.available,
        domains.interaction.availability.available,
        domains.finance.availability.available,
        domains.family.availability.available,
        domains.children.availability.available,
        domains.luck.availability.available,
    ]
    return sum(1 for flag in flags if flag) / len(flags)


def _build_comparison(result: MarriageDecisionResult):
    """Attach comparative decision structure without mutating evidence."""
    return build_marriage_comparison(result)
