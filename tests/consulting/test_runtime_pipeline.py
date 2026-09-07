"""Runtime pipeline tests with a fake Canonical runner. No business assertions."""

from __future__ import annotations

import pytest

from consulting.marriage.adapters.canonical_runtime import CanonicalOrchestratorAdapter
from consulting.marriage.dto.request import MarriageConsultationRequest, MarriagePersonInput
from consulting.marriage.models.enums import CanonicalGender, MarriageRuntimeStatus
from consulting.marriage.runtime.canonical_wiring import wire_marriage_canonical_runtime
from consulting.marriage.runtime.pipeline import MarriageRuntimeOrchestrator
from consulting.marriage.runtime.wiring import wire_marriage_runtime
from tests.consulting.runtime_fixtures import FakeCanonicalRunner, valid_request


def _runtime() -> tuple[MarriageRuntimeOrchestrator, FakeCanonicalRunner]:
    runner = FakeCanonicalRunner()
    container = wire_marriage_canonical_runtime(
        canonical_adapter=CanonicalOrchestratorAdapter(runner=runner),
    )
    orchestrator = container.orchestrator
    assert isinstance(orchestrator, MarriageRuntimeOrchestrator)
    return orchestrator, runner


def test_canonical_invocation_runs_person_a_and_person_b() -> None:
    """Canonical runtime is invoked once per person."""
    orchestrator, runner = _runtime()
    orchestrator.run(valid_request())
    assert len(runner.calls) == 2
    assert runner.calls[0]["year"] == 1987
    assert runner.calls[0]["month"] == 1
    assert runner.calls[0]["day"] == 21
    assert runner.calls[0]["hour"] == 4
    assert runner.calls[0]["minute"] == 30
    assert runner.calls[0]["gender"] == "male"
    assert runner.calls[1]["year"] == 1990
    assert runner.calls[1]["gender"] == "female"


def test_snapshot_builder_binds_canonical_fields_without_hour_invention() -> None:
    """Snapshots copy Canonical pillars and drop hour when birth time is unknown."""
    orchestrator, runner = _runtime()
    response = orchestrator.run(valid_request(time_a=None))
    assert response.status is MarriageRuntimeStatus.SUCCESS
    session = orchestrator.session
    assert session is not None
    snapshot_a = session.context.snapshot_a
    snapshot_b = session.context.snapshot_b
    assert snapshot_a is not None
    assert snapshot_b is not None
    assert snapshot_a.pillars.year.stem == "Bính"
    assert snapshot_a.pillars.hour is None
    assert snapshot_b.pillars.hour is not None
    assert snapshot_a.person.birth_data_quality.birth_time_known is False
    assert any(warning.code == "BIRTH_TIME_UNKNOWN" for warning in response.warnings)
    assert runner.calls[0]["hour"] == 0


def test_missing_gender_fails_request_validation() -> None:
    """Gender is required. TV-01 does not default it."""
    orchestrator, runner = _runtime()
    request = MarriageConsultationRequest(
        person_a=MarriagePersonInput(gender=CanonicalGender.MALE, birth_date="1987-01-21"),
        person_b=MarriagePersonInput(gender=CanonicalGender.MALE, birth_date="1990-05-15"),
    )
    request.person_a.gender = None  # type: ignore[assignment]
    response = orchestrator.run(request)
    assert response.status is MarriageRuntimeStatus.FAILED
    assert response.error is not None
    assert response.error.code == "VALIDATION_ERROR"
    assert runner.calls == []


def test_invalid_birth_date_fails_request_validation() -> None:
    """Invalid dates stop the pipeline before Canonical invocation."""
    orchestrator, runner = _runtime()
    request = valid_request()
    request.person_a.birth_date = "21/01/1987"
    response = orchestrator.run(request)
    assert response.status is MarriageRuntimeStatus.FAILED
    assert response.error is not None
    assert response.error.code == "VALIDATION_ERROR"
    assert runner.calls == []


def test_later_phases_remain_unimplemented() -> None:
    """Evidence, decision, recommendation, report, UI, and API stay placeholders."""
    container = wire_marriage_canonical_runtime(
        canonical_adapter=CanonicalOrchestratorAdapter(runner=FakeCanonicalRunner()),
    )
    with pytest.raises(NotImplementedError):
        container.evidence_builder.build(None)  # type: ignore[arg-type]
    with pytest.raises(NotImplementedError):
        container.finding_builder.build([])
    with pytest.raises(NotImplementedError):
        container.decision_resolver.resolve_overall(None)  # type: ignore[arg-type]
    with pytest.raises(NotImplementedError):
        container.recommendation_provider.provide(None)  # type: ignore[arg-type]
    with pytest.raises(NotImplementedError):
        container.policy_provider.descriptor()
    with pytest.raises(NotImplementedError):
        container.report_profile.descriptor()
    with pytest.raises(NotImplementedError):
        container.ui_layout_profile.descriptor()
    with pytest.raises(NotImplementedError):
        container.validation.validate_evidence([])
    with pytest.raises(NotImplementedError):
        container.validation.validate_decision(None)  # type: ignore[arg-type]


def test_b01_placeholder_wiring_is_unchanged() -> None:
    """TV1-B01 placeholder factory still refuses orchestrator execution."""
    container = wire_marriage_runtime()
    with pytest.raises(NotImplementedError):
        container.orchestrator.run(valid_request())
