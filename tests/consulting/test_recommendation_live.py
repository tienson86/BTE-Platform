"""Live Canonical → Decision → Recommendation verification. No Narrative or Report."""

from __future__ import annotations

from consulting.marriage.models.enums import MarriageRuntimeStatus
from consulting.marriage.report.placeholder import PlaceholderMarriageReportProfile
from consulting.marriage.runtime.lifecycle import RuntimeLifecycleState
from consulting.marriage.runtime.recommendation_pipeline import MarriageRecommendationOrchestrator
from consulting.marriage.runtime.recommendation_wiring import wire_marriage_recommendation_runtime
from tests.consulting.runtime_fixtures import valid_request


def test_live_canonical_pair_reaches_recommendation() -> None:
    """Real Canonical A/B snapshots feed Decision then structured Recommendations."""
    container = wire_marriage_recommendation_runtime()
    orchestrator = container.orchestrator
    assert isinstance(orchestrator, MarriageRecommendationOrchestrator)
    response = orchestrator.run(valid_request())
    assert response.status is MarriageRuntimeStatus.SUCCESS
    session = orchestrator.session
    assert session is not None
    assert session.lifecycle_state is RuntimeLifecycleState.COMPLETED
    result = session.context.decision_result
    assert result is not None
    assert result.overall.score is None
    assert result.overall.grade is None
    assert result.overall.state is not None
    finding_ids = {item.finding_id for item in result.findings}
    for rec in result.recommendations:
        assert rec.source_decision_id == result.consultation_id
        assert rec.source_finding_ids
        assert set(rec.source_finding_ids) <= finding_ids
        assert rec.narrative_key is None
        assert rec.objective
        assert rec.version
    assert result.versions.narrative_version == "unbound"
    assert result.canonical_a.source_analysis_id.endswith("-A")
    assert result.canonical_b.source_analysis_id.endswith("-B")
    try:
        container.report_profile.descriptor()
        raise AssertionError("report must remain unimplemented")
    except NotImplementedError:
        pass
    assert isinstance(container.report_profile, PlaceholderMarriageReportProfile)
    assert container.ui_layout_profile.descriptor
    try:
        container.ui_layout_profile.descriptor()
        raise AssertionError("ui must remain unimplemented")
    except NotImplementedError:
        pass
