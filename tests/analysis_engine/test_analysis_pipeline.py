"""AX-1 analysis pipeline integration tests. No rule evaluation."""

from __future__ import annotations

from pathlib import Path

import pytest

from engines.analysis_engine.exceptions.pipeline_error import (
    DependencyViolationError,
    DuplicateExecutionError,
    IncompatiblePackageError,
    PackageLoadError,
)
from engines.analysis_engine.pipeline.analysis_pipeline import AnalysisPipeline
from engines.analysis_engine.pipeline.dependency_resolver import ACTIVE_KNOWLEDGE_STAGES
from engines.analysis_engine.pipeline.execution_context import AnalysisExecutionContext
from engines.analysis_engine.pipeline.package_loader import PackageLoader

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
}


def test_normal_execution_binds_three_packages() -> None:
    """Seasonal → Strength → Temperature should bind released packages."""
    result = AnalysisPipeline().run(SAMPLE_CHART)
    assert result.success is True
    assert result.pipeline_version == "1.0.0"
    assert result.stage_order == ACTIVE_KNOWLEDGE_STAGES
    assert result.seasonal_result is not None
    assert result.strength_result is not None
    assert result.temperature_result is not None
    assert result.seasonal_result["package_id"] == "bz_02_seasonal_core"
    assert result.strength_result["package_id"] == "bz_01_strength_core"
    assert result.temperature_result["package_id"] == "bz_03_temperature_core"
    assert result.pattern_result is None
    assert result.seasonal_result["upstream_stages"] == ("four_pillars",)
    assert result.strength_result["upstream_stages"] == ("seasonal",)
    assert result.temperature_result["upstream_stages"] == ("seasonal", "strength")


def test_missing_package_fails(tmp_path: Path) -> None:
    """Missing package roots should fail with a structured diagnostic."""
    loader = PackageLoader(
        package_roots={
            "bz_01_strength_core": tmp_path / "missing_strength",
            "bz_02_seasonal_core": tmp_path / "missing_seasonal",
            "bz_03_temperature_core": tmp_path / "missing_temperature",
        }
    )
    result = AnalysisPipeline(loader=loader).run(SAMPLE_CHART)
    assert result.success is False
    assert any("package_not_found" in error for error in result.errors)
    assert any(item.code == "PIPE-FAIL" for item in result.diagnostics)


def test_incompatible_version_fails() -> None:
    """Incompatible version constraints must reject released packages."""
    pipeline = AnalysisPipeline(
        version_constraints={"bz_02_seasonal_core": "^9.0.0"},
    )
    result = pipeline.run(SAMPLE_CHART)
    assert result.success is False
    assert any("version_incompatible" in error for error in result.errors)


def test_loader_raises_on_missing_package(tmp_path: Path) -> None:
    """Direct loader access should raise PackageLoadError."""
    loader = PackageLoader(package_roots={"bz_01_strength_core": tmp_path / "absent"})
    with pytest.raises(PackageLoadError):
        loader.load("bz_01_strength_core")


def test_loader_raises_on_incompatible_constraint() -> None:
    """Direct loader access should raise IncompatiblePackageError."""
    loader = PackageLoader()
    with pytest.raises(IncompatiblePackageError):
        loader.load("bz_03_temperature_core", version_constraint="^2.0.0")


def test_dependency_violation_without_seasonal() -> None:
    """Temperature without Seasonal/Strength must not execute."""
    result = AnalysisPipeline(active_stages=("temperature",)).run(SAMPLE_CHART)
    assert result.success is False
    assert any("missing_prerequisite" in error for error in result.errors)


def test_stage_rejects_missing_upstream() -> None:
    """A knowledge stage must not run without published upstream outputs."""
    from engines.analysis_engine.integration.temperature_stage import TemperatureStage
    from engines.analysis_engine.pipeline.package_loader import PackageLoader as Loader

    context = AnalysisExecutionContext(chart=SAMPLE_CHART)
    package = Loader().load("bz_03_temperature_core")
    with pytest.raises(DependencyViolationError):
        TemperatureStage().execute(context, package)


def test_duplicate_execution_prevented() -> None:
    """Publishing the same stage twice must fail."""
    context = AnalysisExecutionContext(chart=SAMPLE_CHART)
    pipeline = AnalysisPipeline()
    first = pipeline.run(SAMPLE_CHART, context=context)
    assert first.success is True
    second = pipeline.run(SAMPLE_CHART, context=context)
    assert second.success is False
    assert any("duplicate_execution" in error for error in second.errors)


def test_context_publish_raises_duplicate() -> None:
    """Context-level overwrite protection."""
    context = AnalysisExecutionContext(chart=SAMPLE_CHART)
    context.publish("seasonal", {"ok": True})
    with pytest.raises(DuplicateExecutionError):
        context.publish("seasonal", {"again": True})


def test_deterministic_repeated_execution() -> None:
    """Two fresh runs with the same chart must produce identical bindings."""
    pipeline = AnalysisPipeline()
    first = pipeline.run(SAMPLE_CHART)
    second = pipeline.run(SAMPLE_CHART)
    assert first.success is True
    assert second.success is True
    assert first.stage_order == second.stage_order
    assert first.seasonal_result == second.seasonal_result
    assert first.strength_result == second.strength_result
    assert first.temperature_result == second.temperature_result
