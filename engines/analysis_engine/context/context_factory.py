"""Analysis context factory for lifecycle creation."""

from __future__ import annotations

from typing import Any, Mapping
from uuid import uuid4

from engines.analysis_engine.context.context_builder import ContextBuilder, utc_now
from engines.analysis_engine.context.runtime_context import RuntimeContext
from engines.analysis_engine.exceptions.context_error import ContextError
from engines.analysis_engine.models.analysis_context import AnalysisContext
from engines.analysis_engine.models.analysis_metadata import AnalysisMetadata, ModelTimestamps

_DEFAULT_VERSION = "1.0.0"


class ContextFactory:
    """Factory for creating Analysis Context instances.

    Handles create-phase construction only. No analyzer evaluation.
    """

    def __init__(self, *, default_version: str = _DEFAULT_VERSION) -> None:
        """Initialize factory defaults."""
        self._default_version = default_version

    def create(
        self,
        *,
        pipeline_id: str,
        context_id: str | None = None,
        chart_id: str | None = None,
        attributes: Mapping[str, Any] | None = None,
        version: str | None = None,
        metadata: Mapping[str, Any] | None = None,
        trace: tuple[str, ...] = (),
    ) -> AnalysisContext:
        """Create a new immutable Analysis Context (Create phase)."""
        builder = (
            ContextBuilder()
            .with_context_id(context_id or str(uuid4()))
            .with_pipeline_id(pipeline_id)
            .with_chart_id(chart_id)
            .with_version(version or self._default_version)
            .with_attributes(attributes or {})
            .with_metadata(metadata or {})
            .with_trace(*trace)
            .with_created_at(utc_now())
        )
        return builder.build_analysis_context()

    def create_from_runtime(self, runtime: RuntimeContext) -> AnalysisContext:
        """Create an Analysis Context from a runtime context view."""
        if not runtime.id:
            raise ContextError("runtime_context_id_required")
        if not runtime.pipeline_id:
            raise ContextError("runtime_pipeline_id_required")
        attributes = dict(runtime.attributes)
        if runtime.stage_outputs:
            attributes = {
                **attributes,
                "stage_outputs": dict(runtime.stage_outputs),
            }
        return self.create(
            pipeline_id=runtime.pipeline_id,
            context_id=runtime.id,
            chart_id=runtime.chart_id,
            attributes=attributes,
        )

    def create_runtime(
        self,
        *,
        pipeline_id: str,
        context_id: str | None = None,
        chart_id: str | None = None,
        attributes: Mapping[str, Any] | None = None,
    ) -> RuntimeContext:
        """Create a mutable runtime context shell for pipeline execution."""
        return RuntimeContext(
            id=context_id or str(uuid4()),
            pipeline_id=pipeline_id,
            chart_id=chart_id,
            attributes=dict(attributes or {}),
            stage_outputs={},
        )

    def clone_with_attributes(
        self,
        context: AnalysisContext,
        attributes: Mapping[str, Any],
        *,
        trace_item: str | None = None,
        updated_at: str | None = None,
    ) -> AnalysisContext:
        """Return a new context with merged attributes (immutable expand)."""
        stamp = updated_at or utc_now()
        merged = dict(context.attributes)
        merged.update(dict(attributes))
        trace = context.trace + ((trace_item,) if trace_item else ())
        timestamps = ModelTimestamps(
            created_at=context.timestamps.created_at,
            updated_at=stamp,
            completed_at=context.timestamps.completed_at,
        )
        metadata = AnalysisMetadata(
            id=context.metadata.id,
            version=context.metadata.version,
            metadata=dict(context.metadata.metadata),
            trace=trace,
            timestamps=timestamps,
        )
        return AnalysisContext(
            id=context.id,
            version=context.version,
            metadata=metadata,
            trace=trace,
            timestamps=timestamps,
            pipeline_id=context.pipeline_id,
            chart_id=context.chart_id,
            attributes=merged,
        )
