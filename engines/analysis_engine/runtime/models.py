"""Analysis Runtime shared models."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping
from uuid import uuid4

from engines.analysis_engine.runtime.constants import (
    CANONICAL_STAGES,
    STAGE_RESULT_ATTR,
)
from engines.analysis_engine.runtime.exceptions import StateError


@dataclass(slots=True)
class RuleEvidence:
    """Explainability evidence attached to a stage result."""

    rule_id: str
    version: str = "1.0.0"
    category: str = ""
    priority: int = 0
    reference: str = ""
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class DiagnosticInfo:
    """Non-semantic diagnostic message."""

    code: str
    message: str
    level: str = "info"
    stage_id: str | None = None
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ConfidenceEvaluation:
    """Optional confidence aggregate for a stage or full analysis."""

    score: float | None = None
    level: str | None = None
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ExecutionMetadata:
    """Shared execution metadata for request or stage spans."""

    request_id: str
    runtime_version: str = "1.0.0"
    correlation_id: str = ""
    started_at: float | None = None
    finished_at: float | None = None
    duration_ms: float | None = None
    stage_id: str | None = None
    module_version: str | None = None
    knowledge_version: str | None = None
    status: str = "pending"
    extras: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class StageMetrics:
    """Per-stage performance metrics."""

    stage_id: str
    duration_ms: float
    status: str
    cache_hit: bool = False


@dataclass(slots=True)
class PerformanceMetrics:
    """Request-level performance metrics."""

    total_duration_ms: float = 0.0
    knowledge_bind_ms: float = 0.0
    validation_failure_count: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    stage_metrics: list[StageMetrics] = field(default_factory=list)


@dataclass(slots=True)
class TraceSpan:
    """Single execution trace span."""

    name: str
    started_at: float
    finished_at: float | None = None
    duration_ms: float | None = None
    status: str = "running"
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ExecutionTrace:
    """Ordered execution trace for one request."""

    request_id: str
    spans: list[TraceSpan] = field(default_factory=list)

    def add_span(self, span: TraceSpan) -> None:
        """Append a completed or open span."""
        self.spans.append(span)


@dataclass(slots=True)
class StageResult:
    """Immutable stage publication contract (framework-level)."""

    stage_id: str
    status: str = "success"
    module_version: str = "1.0.0"
    payload: dict[str, Any] = field(default_factory=dict)
    confidence: ConfidenceEvaluation | None = None
    evidence: list[RuleEvidence] = field(default_factory=list)
    diagnostics: list[DiagnosticInfo] = field(default_factory=list)
    execution_metadata: ExecutionMetadata | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize stage result for diagnostics and tests."""
        return {
            "stage_id": self.stage_id,
            "status": self.status,
            "module_version": self.module_version,
            "payload": dict(self.payload),
            "confidence": None
            if self.confidence is None
            else {
                "score": self.confidence.score,
                "level": self.confidence.level,
                "details": dict(self.confidence.details),
            },
            "evidence": [
                {
                    "rule_id": item.rule_id,
                    "version": item.version,
                    "category": item.category,
                    "priority": item.priority,
                    "reference": item.reference,
                    "details": dict(item.details),
                }
                for item in self.evidence
            ],
            "diagnostics": [
                {
                    "code": item.code,
                    "message": item.message,
                    "level": item.level,
                    "stage_id": item.stage_id,
                    "details": dict(item.details),
                }
                for item in self.diagnostics
            ],
        }


@dataclass(slots=True)
class AnalysisContext:
    """Shared analytical context for one Execution Unit.

    Input facts are treated as an immutable snapshot. Stage results are
    append-only via :meth:`publish_stage_result`.
    """

    request_id: str = field(default_factory=lambda: str(uuid4()))
    chart: Mapping[str, Any] = field(default_factory=dict)
    calendar: Mapping[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    knowledge_session: Any | None = None
    knowledge_version: str | None = None
    _stage_results: dict[str, StageResult] = field(
        default_factory=dict,
        repr=False,
    )
    _diagnostics: list[DiagnosticInfo] = field(
        default_factory=list,
        repr=False,
    )

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "chart",
            MappingProxyType(dict(self.chart)),
        )
        object.__setattr__(
            self,
            "calendar",
            MappingProxyType(dict(self.calendar)),
        )

    def get_stage_result(self, stage_id: str) -> StageResult | None:
        """Return a published stage result, if present."""
        return self._stage_results.get(stage_id)

    def publish_stage_result(self, result: StageResult) -> None:
        """Append an immutable stage result. Re-publish is forbidden."""
        if result.stage_id in self._stage_results:
            raise StateError(
                f"Stage result already published: {result.stage_id}",
                stage_id=result.stage_id,
            )
        self._stage_results[result.stage_id] = result

    def has_stage_result(self, stage_id: str) -> bool:
        """Return True when stage_id has been published."""
        return stage_id in self._stage_results

    def published_stage_ids(self) -> tuple[str, ...]:
        """Return published stage ids in canonical order where possible."""
        published = set(self._stage_results)
        ordered = [stage for stage in CANONICAL_STAGES if stage in published]
        extras = sorted(published - set(CANONICAL_STAGES))
        return tuple(ordered + extras)

    def add_diagnostic(self, diagnostic: DiagnosticInfo) -> None:
        """Record a non-semantic diagnostic on the shared context."""
        self._diagnostics.append(diagnostic)

    def diagnostics(self) -> tuple[DiagnosticInfo, ...]:
        """Return a snapshot of diagnostics."""
        return tuple(self._diagnostics)

    def stage_results_map(self) -> Mapping[str, StageResult]:
        """Return a read-only view of published stage results."""
        return MappingProxyType(dict(self._stage_results))

    @property
    def strength_result(self) -> StageResult | None:
        return self._stage_results.get("strength")

    @property
    def temperature_result(self) -> StageResult | None:
        return self._stage_results.get("temperature")

    @property
    def pattern_result(self) -> StageResult | None:
        return self._stage_results.get("pattern")

    @property
    def useful_god_result(self) -> StageResult | None:
        return self._stage_results.get("useful_god")

    @property
    def ten_gods_result(self) -> StageResult | None:
        return self._stage_results.get("ten_gods")

    @property
    def combination_result(self) -> StageResult | None:
        return self._stage_results.get("combination")

    @property
    def shensha_result(self) -> StageResult | None:
        return self._stage_results.get("shensha")

    @property
    def luck_result(self) -> StageResult | None:
        return self._stage_results.get("luck")

    @property
    def summary_result(self) -> StageResult | None:
        return self._stage_results.get("summary")


@dataclass(slots=True)
class AnalysisResult:
    """Immutable successful publication for downstream consumers."""

    request_id: str
    stage_results: Mapping[str, StageResult]
    execution_metadata: ExecutionMetadata
    performance_metrics: PerformanceMetrics
    execution_trace: ExecutionTrace
    diagnostics: tuple[DiagnosticInfo, ...] = ()
    confidence: ConfidenceEvaluation | None = None
    knowledge_version: str | None = None
    runtime_version: str = "1.0.0"
    strength_result: StageResult | None = None
    temperature_result: StageResult | None = None
    pattern_result: StageResult | None = None
    useful_god_result: StageResult | None = None
    ten_gods_result: StageResult | None = None
    combination_result: StageResult | None = None
    shensha_result: StageResult | None = None
    luck_result: StageResult | None = None
    summary_result: StageResult | None = None

    @classmethod
    def from_context(
        cls,
        context: AnalysisContext,
        *,
        execution_metadata: ExecutionMetadata,
        performance_metrics: PerformanceMetrics,
        execution_trace: ExecutionTrace,
        confidence: ConfidenceEvaluation | None = None,
    ) -> AnalysisResult:
        """Assemble AnalysisResult from a completed shared context."""
        results = dict(context.stage_results_map())
        attrs: dict[str, StageResult | None] = {
            STAGE_RESULT_ATTR[stage_id]: results.get(stage_id)
            for stage_id in CANONICAL_STAGES
        }
        return cls(
            request_id=context.request_id,
            stage_results=MappingProxyType(results),
            execution_metadata=execution_metadata,
            performance_metrics=performance_metrics,
            execution_trace=execution_trace,
            diagnostics=context.diagnostics(),
            confidence=confidence,
            knowledge_version=context.knowledge_version,
            **attrs,
        )

    def get_stage_result(self, stage_id: str) -> StageResult | None:
        """Return a stage result by id."""
        return self.stage_results.get(stage_id)
