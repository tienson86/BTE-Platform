"""Result aggregator for structural Final Analysis Result assembly."""

from __future__ import annotations

from engines.analysis_engine.exceptions.result_error import ResultError
from engines.analysis_engine.models.analysis_result import AnalysisResult
from engines.analysis_engine.models.final_result import FinalResult
from engines.analysis_engine.models.module_result import ModuleResult
from engines.analysis_engine.models.stage_result import StageResult
from engines.analysis_engine.results.result_builder import ResultBuilder
from engines.analysis_engine.results.result_merger import ResultMerger
from engines.analysis_engine.results.summary_builder import SummaryBuilder


class ResultAggregator:
    """Aggregate module/stage results into AnalysisResult and FinalResult.

    Structural integration only. No conflict interpretation or report generation.
    """

    def __init__(
        self,
        *,
        merger: ResultMerger | None = None,
        summary_builder: SummaryBuilder | None = None,
    ) -> None:
        """Initialize aggregation collaborators."""
        self._merger = merger or ResultMerger()
        self._summary_builder = summary_builder or SummaryBuilder()

    def aggregate_stages_to_module(
        self,
        *,
        module_id: str,
        stage_results: tuple[StageResult, ...],
        pipeline_id: str,
        result_id: str | None = None,
        version: str = "1.0.0",
    ) -> ModuleResult:
        """Aggregate stage results into a module result."""
        if not module_id:
            raise ResultError("module_id_required")
        stages = self._merger.merge_stage_results(stage_results)
        scores = self._merger.merge_scores(*(stage.scores for stage in stages))
        decisions = self._merger.merge_decisions(*(stage.decisions for stage in stages))
        success = all(stage.success for stage in stages) if stages else True
        trace = tuple(item for stage in stages for item in stage.trace) + (
            f"aggregate_module:{module_id}",
        )
        return (
            ResultBuilder()
            .with_id(result_id or f"module_result_{module_id}")
            .with_version(version)
            .with_pipeline_id(pipeline_id)
            .with_module_id(module_id)
            .with_success(success)
            .with_trace(*trace)
            .with_stage_results(*stages)
            .with_scores(*scores)
            .with_decisions(*decisions)
            .build_module_result()
        )

    def aggregate_modules_to_analysis(
        self,
        *,
        pipeline_id: str,
        module_results: tuple[ModuleResult, ...],
        stage_results: tuple[StageResult, ...] = (),
        result_id: str | None = None,
        version: str = "1.0.0",
    ) -> AnalysisResult:
        """Aggregate module results into an analysis result."""
        if not pipeline_id:
            raise ResultError("pipeline_id_required")
        modules = self._merger.merge_module_results(module_results)
        stages = self._merger.merge_stage_results(
            stage_results,
            *(module.stage_results for module in modules),
        )
        scores = self._merger.merge_scores(
            *(module.scores for module in modules),
            *(stage.scores for stage in stages),
        )
        decisions = self._merger.merge_decisions(
            *(module.decisions for module in modules),
            *(stage.decisions for stage in stages),
        )
        success = all(module.success for module in modules) if modules else True
        if stages and not all(stage.success for stage in stages):
            success = False
        trace = tuple(item for module in modules for item in module.trace) + (
            "aggregate_analysis",
        )
        return (
            ResultBuilder()
            .with_id(result_id or f"analysis_result_{pipeline_id}")
            .with_version(version)
            .with_pipeline_id(pipeline_id)
            .with_success(success)
            .with_trace(*trace)
            .with_stage_results(*stages)
            .with_module_results(*modules)
            .with_scores(*scores)
            .with_decisions(*decisions)
            .build_analysis_result()
        )

    def aggregate_to_final(
        self,
        analysis_result: AnalysisResult,
        *,
        result_id: str | None = None,
    ) -> FinalResult:
        """Aggregate an analysis result into a final result with summary codes."""
        summary = self._summary_builder.build_from_analysis_result(analysis_result)
        return (
            ResultBuilder()
            .with_id(result_id or f"final_{analysis_result.id}")
            .with_version(analysis_result.version)
            .with_pipeline_id(analysis_result.pipeline_id)
            .with_success(analysis_result.success and summary.success)
            .with_trace(*analysis_result.trace, "aggregate_final")
            .with_module_results(*analysis_result.module_results)
            .with_scores(*analysis_result.scores)
            .with_decisions(*analysis_result.decisions)
            .with_summary_codes(*summary.summary_codes)
            .with_created_at(analysis_result.timestamps.created_at)
            .build_final_result(analysis_result=analysis_result)
        )
