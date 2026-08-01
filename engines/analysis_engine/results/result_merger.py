"""Result merger for structural combination of result collections."""

from __future__ import annotations

from typing import TypeVar

from engines.analysis_engine.exceptions.result_error import ResultError
from engines.analysis_engine.models.analysis_decision import AnalysisDecision
from engines.analysis_engine.models.analysis_metadata import AnalysisMetadata, ModelTimestamps
from engines.analysis_engine.models.analysis_result import AnalysisResult
from engines.analysis_engine.models.analysis_score import AnalysisScore
from engines.analysis_engine.models.module_result import ModuleResult
from engines.analysis_engine.models.stage_result import StageResult
from engines.analysis_engine.results._time import utc_now
from engines.analysis_engine.results.result_builder import ResultBuilder

T = TypeVar("T")


class ResultMerger:
    """Merge analysis result collections without interpretation.

    Preserves all stage/module/score/decision/evidence identifiers.
    Does not resolve conflicts semantically or generate report text.
    """

    def merge_by_id(self, items: tuple[T, ...]) -> tuple[T, ...]:
        """Deduplicate items by ``id``, keeping the last occurrence, sorted by id."""
        keyed: dict[str, T] = {}
        for item in items:
            item_id = getattr(item, "id", None)
            if not isinstance(item_id, str) or not item_id:
                raise ResultError("merge_item_missing_id")
            keyed[item_id] = item
        return tuple(keyed[key] for key in sorted(keyed.keys()))

    def merge_stage_results(
        self,
        *groups: tuple[StageResult, ...],
    ) -> tuple[StageResult, ...]:
        """Merge stage result tuples without dropping entries by identity."""
        combined: list[StageResult] = []
        for group in groups:
            combined.extend(group)
        return self.merge_by_id(tuple(combined))

    def merge_module_results(
        self,
        *groups: tuple[ModuleResult, ...],
    ) -> tuple[ModuleResult, ...]:
        """Merge module result tuples without dropping entries by identity."""
        combined: list[ModuleResult] = []
        for group in groups:
            combined.extend(group)
        return self.merge_by_id(tuple(combined))

    def merge_scores(
        self,
        *groups: tuple[AnalysisScore, ...],
    ) -> tuple[AnalysisScore, ...]:
        """Merge score tuples without dropping entries by identity."""
        combined: list[AnalysisScore] = []
        for group in groups:
            combined.extend(group)
        return self.merge_by_id(tuple(combined))

    def merge_decisions(
        self,
        *groups: tuple[AnalysisDecision, ...],
    ) -> tuple[AnalysisDecision, ...]:
        """Merge decision tuples without dropping entries by identity."""
        combined: list[AnalysisDecision] = []
        for group in groups:
            combined.extend(group)
        return self.merge_by_id(tuple(combined))

    def merge_analysis_results(
        self,
        *results: AnalysisResult,
        result_id: str | None = None,
    ) -> AnalysisResult:
        """Merge multiple analysis results into one structural aggregate."""
        if not results:
            raise ResultError("merge_analysis_results_empty")
        pipeline_ids = {result.pipeline_id for result in results}
        if len(pipeline_ids) != 1:
            raise ResultError(f"merge_pipeline_mismatch:{','.join(sorted(pipeline_ids))}")
        pipeline_id = next(iter(pipeline_ids))
        stamp = utc_now()
        success = all(result.success for result in results)
        stage_results = self.merge_stage_results(*(result.stage_results for result in results))
        module_results = self.merge_module_results(
            *(result.module_results for result in results)
        )
        scores = self.merge_scores(*(result.scores for result in results))
        decisions = self.merge_decisions(*(result.decisions for result in results))
        trace = tuple(
            item for result in results for item in result.trace
        ) + ("result_merged",)
        version = results[0].version
        meta = AnalysisMetadata(
            id=f"meta_{result_id or results[0].id}_merged",
            version=version,
            metadata={"merged_from": [result.id for result in results]},
            trace=trace,
            timestamps=ModelTimestamps(
                created_at=results[0].timestamps.created_at,
                updated_at=stamp,
            ),
        )
        builder = (
            ResultBuilder()
            .with_id(result_id or f"merged_{results[0].id}")
            .with_version(version)
            .with_pipeline_id(pipeline_id)
            .with_success(success)
            .with_trace(*trace)
            .with_metadata(dict(meta.metadata))
            .with_created_at(results[0].timestamps.created_at)
            .with_stage_results(*stage_results)
            .with_module_results(*module_results)
            .with_scores(*scores)
            .with_decisions(*decisions)
        )
        merged = builder.build_analysis_result()
        return AnalysisResult(
            id=merged.id,
            version=merged.version,
            metadata=meta,
            trace=trace,
            timestamps=ModelTimestamps(
                created_at=results[0].timestamps.created_at,
                updated_at=stamp,
            ),
            pipeline_id=pipeline_id,
            success=success,
            stage_results=stage_results,
            module_results=module_results,
            scores=scores,
            decisions=decisions,
        )
