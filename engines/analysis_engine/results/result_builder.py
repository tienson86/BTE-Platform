"""Result builder for immutable result construction."""

from __future__ import annotations

from typing import Any, Mapping
from uuid import uuid4

from engines.analysis_engine.exceptions.result_error import ResultError
from engines.analysis_engine.models.analysis_decision import AnalysisDecision
from engines.analysis_engine.models.analysis_metadata import AnalysisMetadata, ModelTimestamps
from engines.analysis_engine.models.analysis_result import AnalysisResult
from engines.analysis_engine.models.analysis_score import AnalysisScore
from engines.analysis_engine.models.final_result import FinalResult
from engines.analysis_engine.models.module_result import ModuleResult
from engines.analysis_engine.models.stage_result import StageResult
from engines.analysis_engine.results._time import utc_now

_DEFAULT_VERSION = "1.0.0"


class ResultBuilder:
    """Fluent builder for immutable analysis result contracts.

    Infrastructure only: constructs result objects without interpretation.
    """

    def __init__(self, *, default_version: str = _DEFAULT_VERSION) -> None:
        """Initialize builder defaults."""
        self._default_version = default_version
        self._result_id: str | None = None
        self._version: str = default_version
        self._pipeline_id: str | None = None
        self._success: bool = True
        self._trace: list[str] = []
        self._metadata_fields: dict[str, Any] = {}
        self._stage_results: list[StageResult] = []
        self._module_results: list[ModuleResult] = []
        self._scores: list[AnalysisScore] = []
        self._decisions: list[AnalysisDecision] = []
        self._summary_codes: list[str] = []
        self._payload: dict[str, Any] = {}
        self._module_id: str | None = None
        self._stage_id: str | None = None
        self._created_at: str | None = None

    def with_id(self, result_id: str) -> ResultBuilder:
        """Set the result identifier."""
        self._result_id = result_id
        return self

    def with_version(self, version: str) -> ResultBuilder:
        """Set the result version."""
        self._version = version
        return self

    def with_pipeline_id(self, pipeline_id: str) -> ResultBuilder:
        """Set the pipeline identifier."""
        self._pipeline_id = pipeline_id
        return self

    def with_success(self, success: bool) -> ResultBuilder:
        """Set the success flag."""
        self._success = success
        return self

    def with_trace(self, *trace_items: str) -> ResultBuilder:
        """Append trace identifiers."""
        self._trace.extend(trace_items)
        return self

    def with_metadata(self, metadata: Mapping[str, Any]) -> ResultBuilder:
        """Merge metadata fields."""
        self._metadata_fields.update(dict(metadata))
        return self

    def with_stage_results(self, *stage_results: StageResult) -> ResultBuilder:
        """Append stage results."""
        self._stage_results.extend(stage_results)
        return self

    def with_module_results(self, *module_results: ModuleResult) -> ResultBuilder:
        """Append module results."""
        self._module_results.extend(module_results)
        return self

    def with_scores(self, *scores: AnalysisScore) -> ResultBuilder:
        """Append scores."""
        self._scores.extend(scores)
        return self

    def with_decisions(self, *decisions: AnalysisDecision) -> ResultBuilder:
        """Append decisions."""
        self._decisions.extend(decisions)
        return self

    def with_summary_codes(self, *codes: str) -> ResultBuilder:
        """Append opaque summary codes (no interpretation text)."""
        self._summary_codes.extend(codes)
        return self

    def with_payload(self, payload: Mapping[str, Any]) -> ResultBuilder:
        """Merge opaque payload fields."""
        self._payload.update(dict(payload))
        return self

    def with_module_id(self, module_id: str) -> ResultBuilder:
        """Set module identifier for module result construction."""
        self._module_id = module_id
        return self

    def with_stage_id(self, stage_id: str) -> ResultBuilder:
        """Set stage identifier for stage result construction."""
        self._stage_id = stage_id
        return self

    def with_created_at(self, created_at: str) -> ResultBuilder:
        """Set an explicit creation timestamp."""
        self._created_at = created_at
        return self

    def build_stage_result(self) -> StageResult:
        """Build an immutable stage result."""
        if not self._stage_id:
            raise ResultError("stage_id_required")
        result_id, metadata, timestamps, trace = self._identity(prefix="stage")
        return StageResult(
            id=result_id,
            version=self._version,
            metadata=metadata,
            trace=trace,
            timestamps=timestamps,
            stage_id=self._stage_id,
            success=self._success,
            scores=tuple(self._scores),
            decisions=tuple(self._decisions),
            payload=dict(self._payload),
        )

    def build_module_result(self) -> ModuleResult:
        """Build an immutable module result."""
        if not self._module_id:
            raise ResultError("module_id_required")
        result_id, metadata, timestamps, trace = self._identity(prefix="module")
        return ModuleResult(
            id=result_id,
            version=self._version,
            metadata=metadata,
            trace=trace,
            timestamps=timestamps,
            module_id=self._module_id,
            success=self._success,
            stage_results=tuple(self._stage_results),
            scores=tuple(self._scores),
            decisions=tuple(self._decisions),
            payload=dict(self._payload),
        )

    def build_analysis_result(self) -> AnalysisResult:
        """Build an immutable analysis result."""
        if not self._pipeline_id:
            raise ResultError("pipeline_id_required")
        result_id, metadata, timestamps, trace = self._identity(prefix="analysis")
        return AnalysisResult(
            id=result_id,
            version=self._version,
            metadata=metadata,
            trace=trace,
            timestamps=timestamps,
            pipeline_id=self._pipeline_id,
            success=self._success,
            stage_results=tuple(self._stage_results),
            module_results=tuple(self._module_results),
            scores=tuple(self._scores),
            decisions=tuple(self._decisions),
        )

    def build_final_result(
        self,
        *,
        analysis_result: AnalysisResult | None = None,
    ) -> FinalResult:
        """Build an immutable final result."""
        if not self._pipeline_id:
            raise ResultError("pipeline_id_required")
        result_id, metadata, timestamps, trace = self._identity(prefix="final")
        return FinalResult(
            id=result_id,
            version=self._version,
            metadata=metadata,
            trace=trace,
            timestamps=timestamps,
            pipeline_id=self._pipeline_id,
            success=self._success,
            analysis_result=analysis_result,
            module_results=tuple(self._module_results),
            scores=tuple(self._scores),
            decisions=tuple(self._decisions),
            summary_codes=tuple(self._summary_codes),
        )

    def _identity(
        self,
        *,
        prefix: str,
    ) -> tuple[str, AnalysisMetadata, ModelTimestamps, tuple[str, ...]]:
        """Build shared identity fields for a result object."""
        result_id = self._result_id or f"{prefix}_{uuid4()}"
        created_at = self._created_at or utc_now()
        timestamps = ModelTimestamps(created_at=created_at, updated_at=created_at)
        trace = tuple(self._trace)
        metadata = AnalysisMetadata(
            id=f"meta_{result_id}",
            version=self._version,
            metadata=dict(self._metadata_fields),
            trace=trace,
            timestamps=timestamps,
        )
        return result_id, metadata, timestamps, trace
