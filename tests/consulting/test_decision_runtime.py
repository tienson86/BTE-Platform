"""TV1-B03 runtime lifecycle, determinism, trace, and no-narrative tests."""

from __future__ import annotations

from consulting.marriage.adapters.canonical_runtime import CanonicalOrchestratorAdapter
from consulting.marriage.models.enums import MarriageRuntimeStatus
from consulting.marriage.recommendation.placeholder import PlaceholderMarriageRecommendationProvider
from consulting.marriage.runtime.canonical_wiring import wire_marriage_canonical_runtime
from consulting.marriage.runtime.decision_pipeline import B03_PIPELINE_STAGES, MarriageDecisionOrchestrator
from consulting.marriage.runtime.decision_wiring import wire_marriage_decision_runtime
from consulting.marriage.runtime.lifecycle import RuntimeLifecycleState
from consulting.marriage.runtime.phase import B02_PIPELINE_STAGES
from consulting.marriage.runtime.pipeline import MarriageRuntimeOrchestrator
from tests.consulting.runtime_fixtures import FakeCanonicalRunner, valid_request


def _decision_runtime() -> MarriageDecisionOrchestrator:
    container = wire_marriage_decision_runtime(
        canonical_adapter=CanonicalOrchestratorAdapter(runner=FakeCanonicalRunner()),
    )
    orchestrator = container.orchestrator
    assert isinstance(orchestrator, MarriageDecisionOrchestrator)
    return orchestrator


def test_b03_lifecycle_extends_b02_seam() -> None:
    """Decision runtime continues SNAPSHOT_READY → EVIDENCE_READY → DECISION_READY."""
    orchestrator = _decision_runtime()
    response = orchestrator.run(valid_request())
    assert response.status is MarriageRuntimeStatus.SUCCESS
    session = orchestrator.session
    assert session is not None
    assert session.lifecycle_state is RuntimeLifecycleState.COMPLETED
    stages = [trace.stage for trace in session.traces]
    assert stages[: len(B02_PIPELINE_STAGES)] == list(B02_PIPELINE_STAGES)
    assert stages[len(B02_PIPELINE_STAGES) :] == list(B03_PIPELINE_STAGES)
    assert session.context.evidence is not None
    assert session.context.resolved_evidence is not None
    assert session.context.findings is not None
    assert session.context.decision_result is not None
    assert session.context.overall is not None
    assert session.context.recommendations is None


def test_b02_runtime_still_stops_after_snapshots() -> None:
    """Frozen B02 wiring does not execute the decision layer."""
    container = wire_marriage_canonical_runtime(
        canonical_adapter=CanonicalOrchestratorAdapter(runner=FakeCanonicalRunner()),
    )
    orchestrator = container.orchestrator
    assert isinstance(orchestrator, MarriageRuntimeOrchestrator)
    assert not isinstance(orchestrator, MarriageDecisionOrchestrator)
    orchestrator.run(valid_request())
    session = orchestrator.session
    assert session is not None
    assert session.context.evidence is None
    assert session.context.overall is None


def test_decision_determinism() -> None:
    """Same snapshots and policy produce identical decision semantics."""
    first = _decision_runtime().run(valid_request())
    second = _decision_runtime().run(valid_request())
    session_a = _decision_runtime()
    session_a.run(valid_request())
    session_b = _decision_runtime()
    session_b.run(valid_request())
    result_a = session_a.session.context.decision_result
    result_b = session_b.session.context.decision_result
    assert result_a is not None and result_b is not None
    assert [item.predicate for item in result_a.evidence] == [
        item.predicate for item in result_b.evidence
    ]
    assert [item.evidence_type for item in result_a.evidence] == [
        item.evidence_type for item in result_b.evidence
    ]
    assert [item.finding_id for item in result_a.findings] == [
        item.finding_id for item in result_b.findings
    ]
    assert result_a.overall.state == result_b.overall.state
    assert result_a.confidence.overall == result_b.confidence.overall
    assert result_a.overall.score is None
    assert first.status is MarriageRuntimeStatus.SUCCESS
    assert second.status is MarriageRuntimeStatus.SUCCESS


def test_decision_trace_chain() -> None:
    """Decision → domain → finding → evidence → canonical analysis_id."""
    orchestrator = _decision_runtime()
    orchestrator.run(valid_request())
    session = orchestrator.session
    assert session is not None
    result = session.context.decision_result
    assert result is not None
    assert result.consultation_id == session.context.consultation_id
    assert result.canonical_a.source_analysis_id == f"{result.consultation_id}-A"
    assert result.canonical_b.source_analysis_id == f"{result.consultation_id}-B"
    assert result.person_a.analysis_id == result.canonical_a.source_analysis_id
    evidence_by_id = {item.evidence_id: item for item in result.evidence}
    for domain in (
        result.domains.five_elements,
        result.domains.stem_branch,
        result.domains.ten_gods,
        result.domains.luck,
    ):
        for finding in domain.findings:
            assert finding.evidence_ids
            for evidence_id in finding.evidence_ids:
                atom = evidence_by_id[evidence_id]
                assert atom.source_refs
                for ref in atom.source_refs:
                    assert ref.analysis_id in {
                        result.canonical_a.source_analysis_id,
                        result.canonical_b.source_analysis_id,
                    }


def test_no_customer_narrative_or_recommendation() -> None:
    """B03 produces factual decision only."""
    orchestrator = _decision_runtime()
    orchestrator.run(valid_request())
    session = orchestrator.session
    assert session is not None
    result = session.context.decision_result
    assert result is not None
    assert result.recommendations == []
    assert session.context.recommendations is None
    for item in result.evidence:
        assert item.description is None
    for finding in result.findings:
        assert finding.title_key is None
        assert finding.summary_key is None
        assert finding.recommendation_ids == []
    provider = PlaceholderMarriageRecommendationProvider()
    try:
        provider.provide(None)  # type: ignore[arg-type]
        raise AssertionError("recommendation provider must remain unimplemented")
    except NotImplementedError:
        pass
    forbidden = (
        "must marry",
        "must not marry",
        "certain divorce",
        "certain infidelity",
        "infertile",
        "spouse will die",
        "marriage guarantees wealth",
    )
    blob = " ".join(
        filter(
            None,
            [
                *(item.predicate or "" for item in result.evidence),
                *(item.technical_summary or "" for item in result.findings),
                result.overall.state.value if result.overall.state else "",
            ],
        )
    ).lower()
    for phrase in forbidden:
        assert phrase not in blob
