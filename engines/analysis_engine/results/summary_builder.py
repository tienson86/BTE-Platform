"""Summary builder for structural result summaries."""

from __future__ import annotations

from dataclasses import dataclass

from engines.analysis_engine.models.analysis_result import AnalysisResult
from engines.analysis_engine.models.final_result import FinalResult
from engines.analysis_engine.models.module_result import ModuleResult


@dataclass(frozen=True, slots=True)
class ResultSummary:
    """Structural summary of an analysis result.

    Contains identifiers and status codes only.
    Does not contain interpretive narrative or report prose.
    """

    result_id: str
    pipeline_id: str
    success: bool
    module_ids: tuple[str, ...]
    stage_ids: tuple[str, ...]
    score_dimensions: tuple[str, ...]
    decision_ids: tuple[str, ...]
    summary_codes: tuple[str, ...]


class SummaryBuilder:
    """Build opaque structural summary codes from result collections.

    No interpretation and no report generation.
    """

    def build_from_analysis_result(self, result: AnalysisResult) -> ResultSummary:
        """Build a structural summary from an analysis result."""
        module_ids = tuple(sorted({module.module_id for module in result.module_results}))
        stage_ids = tuple(sorted({stage.stage_id for stage in result.stage_results}))
        score_dimensions = tuple(sorted({score.dimension for score in result.scores}))
        decision_ids = tuple(sorted(decision.id for decision in result.decisions))
        codes = self._codes_for_modules(result.module_results)
        codes += self._codes_for_stages(result)
        codes += (
            f"analysis:{result.id}:{'ok' if result.success else 'fail'}",
            f"pipeline:{result.pipeline_id}",
        )
        return ResultSummary(
            result_id=result.id,
            pipeline_id=result.pipeline_id,
            success=result.success,
            module_ids=module_ids,
            stage_ids=stage_ids,
            score_dimensions=score_dimensions,
            decision_ids=decision_ids,
            summary_codes=codes,
        )

    def build_from_final_result(self, result: FinalResult) -> ResultSummary:
        """Build a structural summary from a final result."""
        if result.analysis_result is not None:
            base = self.build_from_analysis_result(result.analysis_result)
            codes = base.summary_codes + result.summary_codes + (
                f"final:{result.id}:{'ok' if result.success else 'fail'}",
            )
            return ResultSummary(
                result_id=result.id,
                pipeline_id=result.pipeline_id,
                success=result.success,
                module_ids=base.module_ids,
                stage_ids=base.stage_ids,
                score_dimensions=base.score_dimensions,
                decision_ids=base.decision_ids,
                summary_codes=tuple(dict.fromkeys(codes)),
            )
        module_ids = tuple(sorted({module.module_id for module in result.module_results}))
        codes = self._codes_for_modules(result.module_results) + result.summary_codes + (
            f"final:{result.id}:{'ok' if result.success else 'fail'}",
        )
        return ResultSummary(
            result_id=result.id,
            pipeline_id=result.pipeline_id,
            success=result.success,
            module_ids=module_ids,
            stage_ids=(),
            score_dimensions=tuple(sorted({score.dimension for score in result.scores})),
            decision_ids=tuple(sorted(decision.id for decision in result.decisions)),
            summary_codes=tuple(dict.fromkeys(codes)),
        )

    def _codes_for_modules(self, modules: tuple[ModuleResult, ...]) -> tuple[str, ...]:
        """Create opaque module status codes."""
        return tuple(
            f"module:{module.module_id}:{'ok' if module.success else 'fail'}"
            for module in sorted(modules, key=lambda item: item.module_id)
        )

    def _codes_for_stages(self, result: AnalysisResult) -> tuple[str, ...]:
        """Create opaque stage status codes."""
        return tuple(
            f"stage:{stage.stage_id}:{'ok' if stage.success else 'fail'}"
            for stage in sorted(result.stage_results, key=lambda item: item.stage_id)
        )
