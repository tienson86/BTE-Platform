"""AX-3 Decision Pipeline integration tests. No rule evaluation."""

from __future__ import annotations

from pathlib import Path

from engines.decision_engine.pipeline.canonical_decision_pipeline import (
    CanonicalDecisionPipeline,
)
from engines.decision_engine.pipeline.decision_context import DecisionExecutionContext
from engines.decision_engine.pipeline.diagnostics import (
    DIAG_DISABLED_STAGE,
    DIAG_EXECUTION_FAILURE,
    DIAG_EXECUTION_SUCCESS,
)
from engines.decision_engine.pipeline.package_loader import DecisionPackageLoader
from engines.decision_engine.pipeline.stage_registry import ACTIVE_DECISION_STAGES

SAMPLE = {
    "season_score": 62,
    "strength_score": 78,
    "temperature_score": 48,
    "pattern_score": 82,
    "pattern_quality": "excellent",
    "pattern_confidence": "high",
    "pattern_integrity": 80,
    "pattern_stability": 76,
    "useful_god": "Chính Quan",
    "favorable_gods": ["Chính Quan", "Chính Ấn"],
    "unfavorable_gods": ["Thất Sát"],
    "decision_confidence": "high",
    "decision_score": 84,
    "decision_reasoning": "Foundation published Chính Quan.",
    "decision_diagnostics": [],
}


def test_normal_execution_binds_three_decision_packages() -> None:
    """Foundation → Priority → Override should bind released packages."""
    result = CanonicalDecisionPipeline().run(SAMPLE)
    assert result.success is True
    assert result.decision_pipeline_version == "1.0.0"
    assert result.stage_order == ACTIVE_DECISION_STAGES
    assert result.foundation is not None
    assert result.priority is not None
    assert result.override is not None
    assert result.foundation["package_id"] == "bz_06_useful_god_foundation"
    assert result.priority["package_id"] == "bz_07_useful_god_priority"
    assert result.override["package_id"] == "bz_08_useful_god_override"
    assert result.final_useful_god == "Chính Quan"
    assert result.package_versions["bz_08_useful_god_override"] == "1.0.0"
    assert any(item.code == DIAG_EXECUTION_SUCCESS for item in result.diagnostics)
    assert any(item.code == DIAG_DISABLED_STAGE for item in result.diagnostics)
    step_ids = [step.step_id for step in (result.decision_trace.steps if result.decision_trace else ())]
    assert step_ids == [
        "candidate_generation",
        "priority_ordering",
        "conflict_resolution",
        "override_decision",
        "final_publication",
    ]


def test_missing_package_fails(tmp_path: Path) -> None:
    """Missing Override root must fail with diagnostics only."""
    loader = DecisionPackageLoader(
        package_roots={"bz_08_useful_god_override": tmp_path / "missing_override"},
    )
    result = CanonicalDecisionPipeline(loader=loader).run(SAMPLE)
    assert result.success is False
    assert any("package_not_found" in error for error in result.errors)
    assert any(item.code == DIAG_EXECUTION_FAILURE for item in result.diagnostics)


def test_incompatible_version_fails() -> None:
    """Incompatible Override constraint must reject the run."""
    pipeline = CanonicalDecisionPipeline(
        version_constraints={"bz_08_useful_god_override": "^9.0.0"},
    )
    result = pipeline.run(SAMPLE)
    assert result.success is False
    assert any("version_incompatible" in error for error in result.errors)


def test_dependency_violation_without_priority() -> None:
    """Override cannot run without Priority."""
    result = CanonicalDecisionPipeline(
        active_stages=("useful_god_override",),
    ).run(SAMPLE)
    assert result.success is False
    assert any("missing_prerequisite" in error for error in result.errors)


def test_priority_conflict_passthrough() -> None:
    """Multiple-candidate diagnostics must surface as applied conflict resolution."""
    snapshot = dict(SAMPLE)
    snapshot["decision_diagnostics"] = ["multiple_candidates"]
    result = CanonicalDecisionPipeline().run(snapshot)
    assert result.success is True
    assert result.priority is not None
    assert result.priority["conflict_resolution"] == "applied"


def test_override_conflict_passthrough() -> None:
    """Contradiction diagnostics must apply override and withhold the final god."""
    snapshot = dict(SAMPLE)
    snapshot["resolution_diagnostics"] = ["contradiction"]
    result = CanonicalDecisionPipeline().run(snapshot)
    assert result.success is True
    assert result.override is not None
    assert result.override["override_applied"] is True
    assert result.final_useful_god == "withheld"
    assert result.decision_audit is not None
    assert result.decision_audit.upstream_preserved is True
    assert result.decision_audit.new_outputs_only is True


def test_duplicate_publication_prevented() -> None:
    """Reusing a published context must stop without raising to the caller."""
    context = DecisionExecutionContext(snapshot=SAMPLE)
    pipeline = CanonicalDecisionPipeline()
    first = pipeline.run(SAMPLE, context=context)
    assert first.success is True
    second = pipeline.run(SAMPLE, context=context)
    assert second.success is False
    assert any("duplicate_execution" in error for error in second.errors)
