"""Runtime lifecycle and trace tests. No business assertions."""

from __future__ import annotations

from consulting.marriage.adapters.canonical_runtime import CanonicalOrchestratorAdapter
from consulting.marriage.models.enums import MarriageRuntimeStatus
from consulting.marriage.runtime.canonical_wiring import wire_marriage_canonical_runtime
from consulting.marriage.runtime.lifecycle import RuntimeLifecycleState
from consulting.marriage.runtime.phase import B02_PIPELINE_STAGES
from consulting.marriage.runtime.pipeline import MarriageRuntimeOrchestrator
from tests.consulting.runtime_fixtures import FakeCanonicalRunner, valid_request


def _orchestrator() -> tuple[MarriageRuntimeOrchestrator, FakeCanonicalRunner]:
    runner = FakeCanonicalRunner()
    container = wire_marriage_canonical_runtime(
        canonical_adapter=CanonicalOrchestratorAdapter(runner=runner),
    )
    orchestrator = container.orchestrator
    assert isinstance(orchestrator, MarriageRuntimeOrchestrator)
    return orchestrator, runner


def test_runtime_lifecycle_reaches_completed_after_snapshots() -> None:
    """B02 lifecycle ends at COMPLETED once snapshots exist."""
    orchestrator, _runner = _orchestrator()
    response = orchestrator.run(valid_request())
    assert response.status is MarriageRuntimeStatus.SUCCESS
    session = orchestrator.session
    assert session is not None
    assert session.lifecycle_state is RuntimeLifecycleState.COMPLETED
    assert session.context.snapshot_a is not None
    assert session.context.snapshot_b is not None
    assert session.context.evidence is None
    assert session.context.overall is None
    assert session.context.recommendations is None


def test_runtime_trace_records_b02_stages() -> None:
    """Every B02 stage is traced with start, end, duration, and status."""
    orchestrator, _runner = _orchestrator()
    orchestrator.run(valid_request())
    session = orchestrator.session
    assert session is not None
    stages = [trace.stage for trace in session.traces]
    assert stages == list(B02_PIPELINE_STAGES)
    for trace in session.traces:
        assert trace.status == "SUCCESS"
        assert trace.start_time
        assert trace.end_time
        assert trace.duration_ms >= 0


def test_consultation_id_is_stable_for_the_run() -> None:
    """The same consultation id is used on the response, context, and analysis ids."""
    orchestrator, _runner = _orchestrator()
    response = orchestrator.run(valid_request())
    session = orchestrator.session
    assert session is not None
    consultation_id = response.consultation_id
    assert consultation_id
    assert session.context.consultation_id == consultation_id
    assert session.context.snapshot_a is not None
    assert session.context.snapshot_b is not None
    assert session.context.snapshot_a.source_analysis_id == f"{consultation_id}-A"
    assert session.context.snapshot_b.source_analysis_id == f"{consultation_id}-B"
