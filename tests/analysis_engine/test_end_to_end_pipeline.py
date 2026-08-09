"""AX-2 end-to-end canonical pipeline tests. No rule evaluation."""

from __future__ import annotations

from pathlib import Path

import pytest

from engines.analysis_engine.exceptions.pipeline_error import DuplicateExecutionError
from engines.analysis_engine.pipeline.canonical_pipeline import CanonicalPipeline
from engines.analysis_engine.pipeline.diagnostics import (
    DIAG_DISABLED_STAGE,
    DIAG_EXECUTION_ORDER,
    DIAG_PIPELINE_FAIL,
    DIAG_PIPELINE_OK,
)
from engines.analysis_engine.pipeline.execution_context import AnalysisExecutionContext
from engines.analysis_engine.pipeline.package_loader import PackageLoader
from engines.analysis_engine.pipeline.stage_registry import ACTIVE_CANONICAL_STAGES

SAMPLE_CHART = {
    "datetime": "1990-06-15T08:00:00",
    "timezone": "Asia/Ho_Chi_Minh",
    "solar_term": "mang_chung",
    "month_branch": "ngo",
    "day_master": "jia",
    "day_master_element": "wood",
    "season": "summer",
    "season_phase": "wang",
    "strength_level": "strong",
    "climate_type": "hot",
    "season_score": 72,
    "strength_score": 68,
    "temperature_score": 74,
    "pattern_score": 70,
    "pattern_quality": "good",
    "pattern_confidence": "high",
    "pattern_integrity": 66,
    "pattern_stability": 64,
}


def test_normal_execution_binds_all_released_packages() -> None:
    """Calendar through Useful God should bind six released packages."""
    result = CanonicalPipeline().run(SAMPLE_CHART)
    assert result.success is True
    assert result.pipeline_version == "2.0.0"
    assert result.stage_order == ACTIVE_CANONICAL_STAGES
    assert result.seasonal is not None
    assert result.strength is not None
    assert result.temperature is not None
    assert result.pattern is not None
    assert result.pattern_evaluation is not None
    assert result.useful_god is not None
    assert result.useful_god["package_id"] == "bz_06_useful_god_foundation"
    assert result.package_versions["bz_04_pattern_core"] == "1.0.0"
    assert result.package_versions["bz_06_useful_god_foundation"] == "1.0.0"
    assert any(item.code == DIAG_PIPELINE_OK for item in result.diagnostics)
    assert any(item.code == DIAG_EXECUTION_ORDER for item in result.diagnostics)
    assert any(item.code == DIAG_DISABLED_STAGE for item in result.diagnostics)
    assert result.execution_trace.outputs_published == ACTIVE_CANONICAL_STAGES


def test_missing_package_fails(tmp_path: Path) -> None:
    """Missing Useful God root must fail with diagnostics only."""
    loader = PackageLoader(
        package_roots={
            "bz_06_useful_god_foundation": tmp_path / "missing_useful_god",
        }
    )
    result = CanonicalPipeline(loader=loader).run(SAMPLE_CHART)
    assert result.success is False
    assert any("package_not_found" in error for error in result.errors)
    assert any(item.code == DIAG_PIPELINE_FAIL for item in result.diagnostics)


def test_incompatible_version_fails() -> None:
    """Incompatible Useful God constraint must reject the run."""
    pipeline = CanonicalPipeline(
        version_constraints={"bz_06_useful_god_foundation": "^9.0.0"},
    )
    result = pipeline.run(SAMPLE_CHART)
    assert result.success is False
    assert any("version_incompatible" in error for error in result.errors)


def test_dependency_violation_without_pattern_evaluation() -> None:
    """Useful God cannot run without Pattern Evaluation."""
    result = CanonicalPipeline(active_stages=("useful_god",)).run(SAMPLE_CHART)
    assert result.success is False
    assert any("missing_prerequisite" in error for error in result.errors)


def test_duplicate_publication_prevented() -> None:
    """Reusing a published context must stop without raising to the caller."""
    context = AnalysisExecutionContext(chart=SAMPLE_CHART)
    pipeline = CanonicalPipeline()
    first = pipeline.run(SAMPLE_CHART, context=context)
    assert first.success is True
    second = pipeline.run(SAMPLE_CHART, context=context)
    assert second.success is False
    assert any("duplicate_execution" in error for error in second.errors)


def test_context_publish_still_raises_duplicate() -> None:
    """Context-level overwrite protection remains strict."""
    context = AnalysisExecutionContext(chart=SAMPLE_CHART)
    context.publish("useful_god", {"ok": True})
    with pytest.raises(DuplicateExecutionError):
        context.publish("useful_god", {"again": True})
