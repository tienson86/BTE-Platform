"""TV1-B04 runtime, analysis-id, and B03 preservation tests."""

from __future__ import annotations

from consulting.marriage.adapters.canonical_runtime import CanonicalOrchestratorAdapter
from consulting.marriage.models.enums import MarriageRuntimeStatus, RecommendationType
from consulting.marriage.runtime.decision_pipeline import B03_PIPELINE_STAGES, MarriageDecisionOrchestrator
from consulting.marriage.runtime.decision_wiring import wire_marriage_decision_runtime
from consulting.marriage.runtime.lifecycle import RuntimeLifecycleState
from consulting.marriage.runtime.phase import B02_PIPELINE_STAGES
from consulting.marriage.runtime.recommendation_pipeline import (
    B04_PIPELINE_STAGES,
    MarriageRecommendationOrchestrator,
)
from consulting.marriage.runtime.recommendation_wiring import wire_marriage_recommendation_runtime
from tests.consulting.runtime_fixtures import FakeCanonicalRunner, valid_request


def _recommendation_runtime() -> MarriageRecommendationOrchestrator:
    container = wire_marriage_recommendation_runtime(
        canonical_adapter=CanonicalOrchestratorAdapter(runner=FakeCanonicalRunner()),
    )
    orchestrator = container.orchestrator
    assert isinstance(orchestrator, MarriageRecommendationOrchestrator)
    return orchestrator


def test_b04_lifecycle_extends_b03_seam() -> None:
    """Recommendation runtime continues DECISION_READY → RECOMMENDATION_READY."""
    orchestrator = _recommendation_runtime()
    response = orchestrator.run(valid_request())
    assert response.status is MarriageRuntimeStatus.SUCCESS
    session = orchestrator.session
    assert session is not None
    assert session.lifecycle_state is RuntimeLifecycleState.COMPLETED
    stages = [trace.stage for trace in session.traces]
    assert stages[: len(B02_PIPELINE_STAGES)] == list(B02_PIPELINE_STAGES)
    assert stages[len(B02_PIPELINE_STAGES) : len(B02_PIPELINE_STAGES) + len(B03_PIPELINE_STAGES)] == list(
        B03_PIPELINE_STAGES
    )
    assert stages[-len(B04_PIPELINE_STAGES) :] == list(B04_PIPELINE_STAGES)
    result = session.context.decision_result
    assert result is not None
    assert session.context.recommendations is not None
    assert result.recommendations is session.context.recommendations
    assert result.overall.score is None
    assert result.overall.grade is None


def test_b03_runtime_still_stops_after_decision() -> None:
    """Frozen B03 wiring does not execute the recommendation layer."""
    container = wire_marriage_decision_runtime(
        canonical_adapter=CanonicalOrchestratorAdapter(runner=FakeCanonicalRunner()),
    )
    orchestrator = container.orchestrator
    assert isinstance(orchestrator, MarriageDecisionOrchestrator)
    assert not isinstance(orchestrator, MarriageRecommendationOrchestrator)
    orchestrator.run(valid_request())
    session = orchestrator.session
    assert session is not None
    assert session.context.decision_result is not None
    assert session.context.decision_result.recommendations == []
    assert session.context.recommendations is None


def test_canonical_analysis_id_is_tv01_envelope_identity() -> None:
    """Canonical OrchestratorService does not return analysis_id; TV-01 stamps correlation ids."""
    runner = FakeCanonicalRunner()
    orchestrator = wire_marriage_recommendation_runtime(
        canonical_adapter=CanonicalOrchestratorAdapter(runner=runner),
    ).orchestrator
    assert isinstance(orchestrator, MarriageRecommendationOrchestrator)
    orchestrator.run(valid_request())
    session = orchestrator.session
    assert session is not None
    result = session.context.decision_result
    assert result is not None
    payload_a = session.context.analysis_a
    assert payload_a is not None
    assert payload_a["analysis_id"] == f"{result.consultation_id}-A"
    inner = payload_a.get("canonical")
    assert isinstance(inner, dict)
    assert "analysis_id" not in inner
    assert result.canonical_a.source_analysis_id == f"{result.consultation_id}-A"
    assert result.canonical_b.source_analysis_id == f"{result.consultation_id}-B"
    assert result.person_a.analysis_id == result.canonical_a.source_analysis_id
    assert result.consultation_id != result.canonical_a.source_analysis_id


def test_runtime_recommendations_are_source_traceable() -> None:
    """Runtime recommendations reference Decision findings, not raw snapshots."""
    orchestrator = _recommendation_runtime()
    orchestrator.run(valid_request())
    session = orchestrator.session
    assert session is not None
    result = session.context.decision_result
    assert result is not None
    finding_ids = {item.finding_id for item in result.findings}
    for rec in result.recommendations:
        assert rec.source_decision_id == result.consultation_id
        assert set(rec.source_finding_ids) <= finding_ids
        assert rec.action_type in RecommendationType
        assert rec.narrative_key is None
