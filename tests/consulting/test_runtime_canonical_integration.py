"""Canonical Runtime integration test. No marriage business assertions."""

from __future__ import annotations

from consulting.marriage.models.enums import MarriageRuntimeStatus
from consulting.marriage.runtime.canonical_wiring import wire_marriage_canonical_runtime
from consulting.marriage.runtime.lifecycle import RuntimeLifecycleState
from consulting.marriage.runtime.pipeline import MarriageRuntimeOrchestrator
from tests.consulting.runtime_fixtures import valid_request


def test_canonical_runtime_builds_snapshots_for_both_persons() -> None:
    """Live Canonical OrchestratorService produces snapshots for Person A and B."""
    container = wire_marriage_canonical_runtime()
    orchestrator = container.orchestrator
    assert isinstance(orchestrator, MarriageRuntimeOrchestrator)
    response = orchestrator.run(valid_request())
    assert response.status is MarriageRuntimeStatus.SUCCESS
    session = orchestrator.session
    assert session is not None
    assert session.lifecycle_state is RuntimeLifecycleState.COMPLETED
    snapshot_a = session.context.snapshot_a
    snapshot_b = session.context.snapshot_b
    assert snapshot_a is not None
    assert snapshot_b is not None
    assert snapshot_a.day_master.stem
    assert snapshot_b.day_master.stem
    assert snapshot_a.pillars.year.stem
    assert snapshot_b.pillars.year.stem
    assert snapshot_a.source_analysis_id.endswith("-A")
    assert snapshot_b.source_analysis_id.endswith("-B")
    assert snapshot_a.strength.classification
    assert snapshot_b.strength.classification
    assert session.context.evidence is None
    assert session.context.overall is None
    assert session.context.recommendations is None
