"""Single-stage module invocation."""

from __future__ import annotations

import logging
import time
from typing import Sequence

from engines.analysis_engine.runtime.cache_manager import CacheManager
from engines.analysis_engine.runtime.error_handler import ErrorHandler
from engines.analysis_engine.runtime.exceptions import AnalysisRuntimeError
from engines.analysis_engine.runtime.models import (
    AnalysisContext,
    ExecutionMetadata,
    StageMetrics,
    StageResult,
    TraceSpan,
)
from engines.analysis_engine.runtime.protocols import AnalysisModule
from engines.analysis_engine.runtime.validation_manager import ValidationManager

logger = logging.getLogger(__name__)


class ModuleExecutor:
    """Invoke one AnalysisModule with pre/post validation and tracing."""

    def __init__(
        self,
        *,
        validation_manager: ValidationManager,
        error_handler: ErrorHandler,
        cache_manager: CacheManager | None = None,
        runtime_version: str = "1.0.0",
    ) -> None:
        self._validation = validation_manager
        self._errors = error_handler
        self._cache = cache_manager
        self._runtime_version = runtime_version

    def execute(
        self,
        module: AnalysisModule,
        context: AnalysisContext,
        *,
        dependencies: Sequence[str] | None = None,
    ) -> tuple[StageResult, StageMetrics, TraceSpan]:
        """Run module.evaluate once and return result, metrics, and span."""
        stage_id = module.stage_id
        resolved_deps = (
            tuple(dependencies)
            if dependencies is not None
            else tuple(module.dependencies)
        )
        started = time.perf_counter()
        span = TraceSpan(
            name=f"stage:{stage_id}",
            started_at=started,
            attributes={
                "module_version": module.version,
                "request_id": context.request_id,
            },
        )
        cache_hit = False

        try:
            self._validation.validate_preconditions(
                context,
                stage_id=stage_id,
                dependencies=resolved_deps,
            )

            cached = self._try_cache_get(module, context)
            if cached is not None:
                result = cached
                cache_hit = True
            else:
                result = module.evaluate(context)
                self._try_cache_set(module, context, result)

            self._validation.validate_stage_result(
                result,
                expected_stage_id=stage_id,
            )
            finished = time.perf_counter()
            duration_ms = (finished - started) * 1000.0
            metadata = ExecutionMetadata(
                request_id=context.request_id,
                runtime_version=self._runtime_version,
                correlation_id=context.request_id,
                started_at=started,
                finished_at=finished,
                duration_ms=duration_ms,
                stage_id=stage_id,
                module_version=module.version,
                knowledge_version=context.knowledge_version,
                status="success",
            )
            if result.execution_metadata is None:
                result.execution_metadata = metadata

            span.finished_at = finished
            span.duration_ms = duration_ms
            span.status = "success"

            metrics = StageMetrics(
                stage_id=stage_id,
                duration_ms=duration_ms,
                status="success",
                cache_hit=cache_hit,
            )
            logger.info(
                "stage_executed",
                extra={
                    "request_id": context.request_id,
                    "stage_id": stage_id,
                    "duration_ms": duration_ms,
                    "cache_hit": cache_hit,
                    "module_version": module.version,
                },
            )
            return result, metrics, span

        except AnalysisRuntimeError:
            self._finalize_failed_span(span, started, "failed")
            raise
        except Exception as exc:
            self._finalize_failed_span(span, started, "failed")
            self._errors.raise_handled(
                exc,
                stage_id=stage_id,
                request_id=context.request_id,
            )
            raise  # pragma: no cover - raise_handled always raises

    def _try_cache_get(
        self,
        module: AnalysisModule,
        context: AnalysisContext,
    ) -> StageResult | None:
        if self._cache is None:
            return None
        key = self._cache_key(module, context)
        value = self._cache.get(key, scope="request")
        if isinstance(value, StageResult):
            return value
        return None

    def _try_cache_set(
        self,
        module: AnalysisModule,
        context: AnalysisContext,
        result: StageResult,
    ) -> None:
        if self._cache is None:
            return
        key = self._cache_key(module, context)
        self._cache.set(key, result, scope="request")

    @staticmethod
    def _cache_key(
        module: AnalysisModule,
        context: AnalysisContext,
    ) -> tuple[str, str, str | None, tuple[str, ...]]:
        return (
            module.stage_id,
            module.version,
            context.knowledge_version,
            context.published_stage_ids(),
        )

    @staticmethod
    def _finalize_failed_span(
        span: TraceSpan,
        started: float,
        status: str,
    ) -> None:
        finished = time.perf_counter()
        span.finished_at = finished
        span.duration_ms = (finished - started) * 1000.0
        span.status = status
