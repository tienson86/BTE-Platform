"""Execution manager for ordered stage runs within one request."""

from __future__ import annotations

import logging
import time
from typing import Mapping

from engines.analysis_engine.runtime.cache_manager import CacheManager
from engines.analysis_engine.runtime.constants import RUNTIME_VERSION
from engines.analysis_engine.runtime.dependency_resolver import DependencyResolver
from engines.analysis_engine.runtime.error_handler import ErrorHandler
from engines.analysis_engine.runtime.exceptions import StateError
from engines.analysis_engine.runtime.models import (
    AnalysisContext,
    AnalysisResult,
    ExecutionMetadata,
    ExecutionTrace,
    PerformanceMetrics,
    StageMetrics,
)
from engines.analysis_engine.runtime.module_executor import ModuleExecutor
from engines.analysis_engine.runtime.protocols import ModuleDescriptor
from engines.analysis_engine.runtime.validation_manager import ValidationManager

logger = logging.getLogger(__name__)


class ExecutionManager:
    """Drive sequential stage execution and assemble AnalysisResult."""

    def __init__(
        self,
        *,
        module_executor: ModuleExecutor,
        validation_manager: ValidationManager,
        dependency_resolver: DependencyResolver,
        error_handler: ErrorHandler,
        cache_manager: CacheManager,
        runtime_version: str = RUNTIME_VERSION,
    ) -> None:
        self._executor = module_executor
        self._validation = validation_manager
        self._dependencies = dependency_resolver
        self._errors = error_handler
        self._cache = cache_manager
        self._runtime_version = runtime_version

    def run_pipeline(
        self,
        context: AnalysisContext,
        *,
        registry: Mapping[str, ModuleDescriptor],
        order: tuple[str, ...],
    ) -> AnalysisResult:
        """Execute all stages in order and publish AnalysisResult."""
        self._cache.begin_request()
        request_started = time.perf_counter()
        trace = ExecutionTrace(request_id=context.request_id)
        metrics = PerformanceMetrics()
        stage_metrics: list[StageMetrics] = []

        try:
            self._validation.validate_admission(context)

            for stage_id in order:
                descriptor = registry.get(stage_id)
                if descriptor is None:
                    raise StateError(
                        f"Stage '{stage_id}' is not registered",
                        stage_id=stage_id,
                    )
                result, stage_metric, span = self._executor.execute(
                    descriptor.module,
                    context,
                    dependencies=descriptor.dependencies,
                )
                context.publish_stage_result(result)
                stage_metrics.append(stage_metric)
                trace.add_span(span)
                if stage_metric.cache_hit:
                    metrics.cache_hits += 1
                else:
                    metrics.cache_misses += 1

            self._validation.validate_final(
                context,
                required_stages=order,
            )

            finished = time.perf_counter()
            duration_ms = (finished - request_started) * 1000.0
            metrics.total_duration_ms = duration_ms
            metrics.stage_metrics = list(stage_metrics)
            cache_stats = self._cache.snapshot_stats()
            metrics.cache_hits = cache_stats["hits"]
            metrics.cache_misses = cache_stats["misses"]

            execution_metadata = ExecutionMetadata(
                request_id=context.request_id,
                runtime_version=self._runtime_version,
                correlation_id=context.request_id,
                started_at=request_started,
                finished_at=finished,
                duration_ms=duration_ms,
                knowledge_version=context.knowledge_version,
                status="completed",
            )
            analysis_result = AnalysisResult.from_context(
                context,
                execution_metadata=execution_metadata,
                performance_metrics=metrics,
                execution_trace=trace,
            )
            self._validation.validate_analysis_result(
                analysis_result,
                required_stages=order,
            )
            logger.info(
                "pipeline_completed",
                extra={
                    "request_id": context.request_id,
                    "duration_ms": duration_ms,
                    "stages": list(order),
                },
            )
            return analysis_result

        except Exception as exc:
            metrics.validation_failure_count += 1
            self._errors.raise_handled(
                exc,
                request_id=context.request_id,
            )
            raise  # pragma: no cover
        finally:
            self._cache.end_request()
