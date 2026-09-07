"""Live Canonical → Decision → Recommendation → Narrative → Report verification."""

from __future__ import annotations

from consulting.marriage.models.enums import MarriageRuntimeStatus
from consulting.marriage.presentation.placeholder import PlaceholderMarriagePresentationAdapter
from consulting.marriage.report.access import customer_visible_text
from consulting.marriage.report.profile import MarriageReportProfileV1
from consulting.marriage.runtime.lifecycle import RuntimeLifecycleState
from consulting.marriage.runtime.narrative_pipeline import MarriageReportOrchestrator
from consulting.marriage.runtime.narrative_wiring import wire_marriage_report_runtime
from tests.consulting.runtime_fixtures import valid_request


def test_live_canonical_pair_reaches_report_model() -> None:
    """Real Canonical pair flows through Narrative to a semantic Report Model."""
    container = wire_marriage_report_runtime()
    orchestrator = container.orchestrator
    assert isinstance(orchestrator, MarriageReportOrchestrator)
    response = orchestrator.run(valid_request())
    assert response.status is MarriageRuntimeStatus.SUCCESS
    session = orchestrator.session
    assert session is not None
    assert session.lifecycle_state is RuntimeLifecycleState.COMPLETED
    result = session.context.decision_result
    narrative = session.context.narrative
    report = session.context.report_model
    assert result is not None
    assert narrative is not None
    assert report is not None
    assert result.overall.score is None
    assert result.overall.grade is None
    assert result.versions.narrative_version != "unbound"
    assert result.versions.score_model_version == "unavailable"
    finding_ids = [item.finding_id for item in result.findings]
    rec_ids = [item.recommendation_id for item in result.recommendations]
    assert report.metadata.consultation_id == result.consultation_id
    assert [item.finding_id for item in result.findings] == finding_ids
    assert [item.recommendation_id for item in result.recommendations] == rec_ids
    text = customer_visible_text(report)
    assert "/100" not in text
    assert "Grade" not in text
    assert "EV-" not in text
    assert "F-" not in text
    ids = [item.section_id for item in report.sections]
    assert ids[0] == "identity"
    assert "compatibility_hero" in ids
    assert "action_plan" in ids
    assert isinstance(container.report_profile, MarriageReportProfileV1)
    assert isinstance(container.presentation_adapter, PlaceholderMarriagePresentationAdapter)
    try:
        container.ui_layout_profile.descriptor()
        raise AssertionError("ui must remain unimplemented")
    except NotImplementedError:
        pass
    try:
        container.api_contract.create_consultation(valid_request())
        raise AssertionError("api must remain unimplemented")
    except NotImplementedError:
        pass
    try:
        container.presentation_adapter.adapt(result)
        raise AssertionError("presentation must remain unimplemented")
    except NotImplementedError:
        pass
