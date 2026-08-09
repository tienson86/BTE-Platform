"""AX-1 stage output contract tests."""

from __future__ import annotations

from engines.analysis_engine.pipeline.analysis_pipeline import AnalysisPipeline
from engines.analysis_engine.pipeline.execution_context import AnalysisExecutionContext
from engines.analysis_engine.validation.pipeline_validation import PipelineValidation

CHART = {
    "month_branch": "zi",
    "day_master_element": "water",
    "season": "winter",
    "strength_level": "weak",
    "climate_type": "cold",
}


def test_context_exposes_required_fields() -> None:
    """Shared context exposes chart, stage results, and diagnostics."""
    context = AnalysisExecutionContext(chart=CHART)
    assert context.chart["season"] == "winter"
    assert context.seasonal_result is None
    assert context.strength_result is None
    assert context.temperature_result is None
    assert context.diagnostics == []
    assert context.pattern_result is None


def test_stage_outputs_include_package_bindings() -> None:
    """Each knowledge stage publishes package identity and signal contracts."""
    result = AnalysisPipeline().run(CHART)
    assert result.success is True
    seasonal = result.seasonal_result
    strength = result.strength_result
    temperature = result.temperature_result
    assert seasonal is not None and strength is not None and temperature is not None
    assert seasonal["produced_signals"] == ("season", "season_phase", "season_score")
    assert strength["produced_signals"] == ("strength_score", "strength_level")
    assert "temperature_score" in temperature["produced_signals"]
    assert seasonal["chart_facts"]["season"] == "winter"
    assert strength["chart_facts"]["strength_level"] == "weak"
    assert temperature["chart_facts"]["climate_type"] == "cold"
    assert seasonal["rule_count"] >= 80
    assert strength["rule_count"] >= 80
    assert temperature["rule_count"] >= 80


def test_validation_report_after_successful_run() -> None:
    """Pipeline validation should pass after a complete run."""
    pipeline = AnalysisPipeline()
    context = AnalysisExecutionContext(chart=CHART)
    result = pipeline.run(CHART, context=context)
    assert result.success is True
    report = PipelineValidation().validate_run(
        context=context,
        packages=pipeline.load_packages(),
        stage_order=result.stage_order,
    )
    assert report.success is True
    assert report.errors == ()
    assert any(item.code == "PIPE-OK" for item in report.diagnostics)
    assert any(item.code == "PKG-LOADED" for item in report.diagnostics)
