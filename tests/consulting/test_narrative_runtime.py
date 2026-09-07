"""TV1-B05 runtime lifecycle, B04 preservation, and version binding tests."""

from __future__ import annotations

from consulting.marriage.adapters.canonical_runtime import CanonicalOrchestratorAdapter
from consulting.marriage.models.enums import MarriageRuntimeStatus
from consulting.marriage.report.placeholder import PlaceholderMarriageReportProfile
from consulting.marriage.report.profile import MarriageReportProfileV1
from consulting.marriage.runtime.lifecycle import RuntimeLifecycleState
from consulting.marriage.runtime.narrative_pipeline import B05_PIPELINE_STAGES, MarriageReportOrchestrator
from consulting.marriage.runtime.narrative_wiring import wire_marriage_report_runtime
from consulting.marriage.runtime.phase import B02_PIPELINE_STAGES
from consulting.marriage.runtime.decision_pipeline import B03_PIPELINE_STAGES
from consulting.marriage.runtime.recommendation_pipeline import (
    B04_PIPELINE_STAGES,
    MarriageRecommendationOrchestrator,
)
from consulting.marriage.runtime.recommendation_wiring import wire_marriage_recommendation_runtime
from consulting.marriage.ui.placeholder import PlaceholderMarriageUILayoutProfile
from tests.consulting.runtime_fixtures import FakeCanonicalRunner, valid_request


def _report_runtime() -> MarriageReportOrchestrator:
    container = wire_marriage_report_runtime(
        canonical_adapter=CanonicalOrchestratorAdapter(runner=FakeCanonicalRunner()),
    )
    orchestrator = container.orchestrator
    assert isinstance(orchestrator, MarriageReportOrchestrator)
    return orchestrator


def test_b05_lifecycle_extends_b04_seam() -> None:
    """Report runtime continues RECOMMENDATION_READY → NARRATIVE_READY → REPORT_READY."""
    orchestrator = _report_runtime()
    response = orchestrator.run(valid_request())
    assert response.status is MarriageRuntimeStatus.SUCCESS
    session = orchestrator.session
    assert session is not None
    assert session.lifecycle_state is RuntimeLifecycleState.COMPLETED
    stages = [trace.stage for trace in session.traces]
    assert stages[: len(B02_PIPELINE_STAGES)] == list(B02_PIPELINE_STAGES)
    b03_start = len(B02_PIPELINE_STAGES)
    b03_end = b03_start + len(B03_PIPELINE_STAGES)
    assert stages[b03_start:b03_end] == list(B03_PIPELINE_STAGES)
    b04_end = b03_end + len(B04_PIPELINE_STAGES)
    assert stages[b03_end:b04_end] == list(B04_PIPELINE_STAGES)
    assert stages[-len(B05_PIPELINE_STAGES) :] == list(B05_PIPELINE_STAGES)
    assert session.context.narrative is not None
    assert session.context.report_model is not None
    result = session.context.decision_result
    assert result is not None
    assert result.overall.score is None
    assert result.versions.narrative_version != "unbound"


def test_b04_runtime_still_stops_after_recommendation() -> None:
    """Frozen B04 wiring does not execute narrative or report."""
    container = wire_marriage_recommendation_runtime(
        canonical_adapter=CanonicalOrchestratorAdapter(runner=FakeCanonicalRunner()),
    )
    orchestrator = container.orchestrator
    assert isinstance(orchestrator, MarriageRecommendationOrchestrator)
    assert not isinstance(orchestrator, MarriageReportOrchestrator)
    orchestrator.run(valid_request())
    session = orchestrator.session
    assert session is not None
    result = session.context.decision_result
    assert result is not None
    assert result.recommendations
    assert session.context.narrative is None
    assert session.context.report_model is None
    assert result.versions.narrative_version == "unbound"
    assert isinstance(container.report_profile, PlaceholderMarriageReportProfile)


def test_b05_does_not_implement_ui_or_api() -> None:
    """B05 binds report profile but leaves UI and API unimplemented."""
    container = wire_marriage_report_runtime(
        canonical_adapter=CanonicalOrchestratorAdapter(runner=FakeCanonicalRunner()),
    )
    assert isinstance(container.report_profile, MarriageReportProfileV1)
    descriptor = container.report_profile.descriptor()
    assert descriptor.profile_id == "marriage.report.profile.v1"
    assert isinstance(container.ui_layout_profile, PlaceholderMarriageUILayoutProfile)
    try:
        container.ui_layout_profile.descriptor()
        raise AssertionError("ui must remain unimplemented")
    except NotImplementedError:
        pass


def test_b05_does_not_mutate_decision_or_recommendations() -> None:
    """Narrative/report stages keep Decision state and recommendation ids intact."""
    orchestrator = _report_runtime()
    orchestrator.run(valid_request())
    session = orchestrator.session
    assert session is not None
    result = session.context.decision_result
    assert result is not None
    first_state = result.overall.state
    first_recs = [item.recommendation_id for item in result.recommendations]
    first_findings = [item.finding_id for item in result.findings]
    orchestrator.run(valid_request())
    session = orchestrator.session
    assert session is not None
    result = session.context.decision_result
    assert result is not None
    assert result.overall.state == first_state
    assert [item.recommendation_id for item in result.recommendations] == first_recs
    assert [item.finding_id for item in result.findings] == first_findings
    assert result.overall.score is None
    assert result.overall.grade is None
