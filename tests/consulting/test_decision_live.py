"""Live Canonical → Decision verification. No narrative or recommendation."""

from __future__ import annotations

from consulting.marriage.models.enums import MarriageRuntimeStatus
from consulting.marriage.runtime.decision_pipeline import MarriageDecisionOrchestrator
from consulting.marriage.runtime.decision_wiring import wire_marriage_decision_runtime
from consulting.marriage.runtime.lifecycle import RuntimeLifecycleState
from tests.consulting.runtime_fixtures import valid_request


def test_live_canonical_pair_reaches_decision() -> None:
    """Real Canonical A/B snapshots feed evidence, findings, and decision."""
    container = wire_marriage_decision_runtime()
    orchestrator = container.orchestrator
    assert isinstance(orchestrator, MarriageDecisionOrchestrator)
    response = orchestrator.run(valid_request())
    assert response.status is MarriageRuntimeStatus.SUCCESS
    session = orchestrator.session
    assert session is not None
    assert session.lifecycle_state is RuntimeLifecycleState.COMPLETED
    snapshot_a = session.context.snapshot_a
    snapshot_b = session.context.snapshot_b
    result = session.context.decision_result
    assert snapshot_a is not None and snapshot_b is not None
    assert result is not None
    assert result.consultation_id == session.context.consultation_id
    assert result.canonical_a.source_analysis_id.endswith("-A")
    assert result.canonical_b.source_analysis_id.endswith("-B")
    assert result.canonical_a.source_analysis_id != result.consultation_id
    assert result.evidence is session.context.evidence
    for atom in result.evidence:
        assert atom.source_refs
        assert all(
            ref.analysis_id in {snapshot_a.source_analysis_id, snapshot_b.source_analysis_id}
            for ref in atom.source_refs
        )
    assert result.findings is not None
    assert result.overall.state is not None
    assert result.overall.score is None
    assert result.recommendations == []
    assert session.context.recommendations is None
    assert session.context.analysis_a is not None
    assert session.context.analysis_b is not None
    assert snapshot_a.day_master.stem
    assert snapshot_b.day_master.stem
    assert result.versions.decision_profile_version == "marriage.policy.v1@1.0.0"
    assert result.versions.score_model_version == "unavailable"
    assert result.versions.narrative_version == "unbound"
