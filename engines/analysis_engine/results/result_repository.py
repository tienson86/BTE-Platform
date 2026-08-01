"""Result repository for in-memory result persistence."""

from __future__ import annotations

from engines.analysis_engine.exceptions.result_error import ResultError
from engines.analysis_engine.interfaces.result_provider import ResultProviderInterface
from engines.analysis_engine.models.analysis_result import AnalysisResult
from engines.analysis_engine.models.final_result import FinalResult
from engines.analysis_engine.models.module_result import ModuleResult
from engines.analysis_engine.models.stage_result import StageResult


class ResultRepository(ResultProviderInterface):
    """In-memory repository for immutable analysis results.

    Stores finalized result objects for pipeline/audit retrieval.
    Does not mutate stored results after insertion.
    """

    def __init__(self) -> None:
        """Initialize empty result stores."""
        self._analysis: dict[str, AnalysisResult] = {}
        self._stages: dict[str, StageResult] = {}
        self._modules: dict[str, ModuleResult] = {}
        self._finals: dict[str, FinalResult] = {}

    def put_analysis_result(self, result: AnalysisResult) -> None:
        """Store an analysis result by identifier."""
        if result.id in self._analysis:
            raise ResultError(f"analysis_result_already_stored:{result.id}")
        self._analysis[result.id] = result
        for stage in result.stage_results:
            self._stages.setdefault(stage.id, stage)
        for module in result.module_results:
            self._modules.setdefault(module.id, module)

    def put_stage_result(self, result: StageResult) -> None:
        """Store a stage result by identifier."""
        if result.id in self._stages:
            raise ResultError(f"stage_result_already_stored:{result.id}")
        self._stages[result.id] = result

    def put_module_result(self, result: ModuleResult) -> None:
        """Store a module result by identifier."""
        if result.id in self._modules:
            raise ResultError(f"module_result_already_stored:{result.id}")
        self._modules[result.id] = result
        for stage in result.stage_results:
            self._stages.setdefault(stage.id, stage)

    def put_final_result(self, result: FinalResult) -> None:
        """Store a final result by identifier."""
        if result.id in self._finals:
            raise ResultError(f"final_result_already_stored:{result.id}")
        self._finals[result.id] = result
        if result.analysis_result is not None:
            self._analysis.setdefault(result.analysis_result.id, result.analysis_result)

    def get_analysis_result(self, result_id: str) -> AnalysisResult:
        """Return an analysis result by identifier."""
        result = self._analysis.get(result_id)
        if result is None:
            raise ResultError(f"analysis_result_not_found:{result_id}")
        return result

    def get_stage_result(self, result_id: str) -> StageResult:
        """Return a stage result by identifier."""
        result = self._stages.get(result_id)
        if result is None:
            raise ResultError(f"stage_result_not_found:{result_id}")
        return result

    def get_module_result(self, result_id: str) -> ModuleResult:
        """Return a module result by identifier."""
        result = self._modules.get(result_id)
        if result is None:
            raise ResultError(f"module_result_not_found:{result_id}")
        return result

    def get_final_result(self, result_id: str) -> FinalResult:
        """Return a final result by identifier."""
        result = self._finals.get(result_id)
        if result is None:
            raise ResultError(f"final_result_not_found:{result_id}")
        return result

    def list_analysis_result_ids(self) -> tuple[str, ...]:
        """Return stored analysis result identifiers."""
        return tuple(sorted(self._analysis.keys()))

    def list_final_result_ids(self) -> tuple[str, ...]:
        """Return stored final result identifiers."""
        return tuple(sorted(self._finals.keys()))

    def clear(self) -> None:
        """Clear all stored results."""
        self._analysis.clear()
        self._stages.clear()
        self._modules.clear()
        self._finals.clear()
