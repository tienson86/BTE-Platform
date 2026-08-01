"""Analysis context builder for immutable construction."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping

from engines.analysis_engine.context.interfaces import (
    ContextBuilderInterface,
    ContextInterface,
)
from engines.analysis_engine.context.runtime_context import RuntimeContext
from engines.analysis_engine.exceptions.context_error import ContextError
from engines.analysis_engine.models.analysis_context import AnalysisContext
from engines.analysis_engine.models.analysis_metadata import AnalysisMetadata, ModelTimestamps

_DEFAULT_VERSION = "1.0.0"


def utc_now() -> str:
    """Return a UTC ISO-8601 timestamp for context lifecycle events."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class ContextBuilder(ContextBuilderInterface):
    """Fluent builder for Analysis Context lifecycle creation.

    Builds immutable ``AnalysisContext`` instances without analyzer logic.
    """

    def __init__(self) -> None:
        """Initialize an empty builder."""
        self._context_id: str | None = None
        self._version: str = _DEFAULT_VERSION
        self._pipeline_id: str | None = None
        self._chart_id: str | None = None
        self._attributes: dict[str, Any] = {}
        self._trace: list[str] = []
        self._metadata_fields: dict[str, Any] = {}
        self._created_at: str | None = None

    def with_context_id(self, context_id: str) -> ContextBuilder:
        """Set the context identifier."""
        self._context_id = context_id
        return self

    def with_version(self, version: str) -> ContextBuilder:
        """Set the context schema/version label."""
        self._version = version
        return self

    def with_pipeline_id(self, pipeline_id: str) -> ContextBuilder:
        """Set the owning pipeline identifier."""
        self._pipeline_id = pipeline_id
        return self

    def with_chart_id(self, chart_id: str | None) -> ContextBuilder:
        """Set the chart identifier."""
        self._chart_id = chart_id
        return self

    def with_attribute(self, key: str, value: Any) -> ContextBuilder:
        """Assign a single opaque context attribute."""
        self._attributes[key] = value
        return self

    def with_attributes(self, attributes: Mapping[str, Any]) -> ContextBuilder:
        """Merge opaque context attributes."""
        self._attributes.update(dict(attributes))
        return self

    def with_trace(self, *trace_items: str) -> ContextBuilder:
        """Append trace identifiers."""
        self._trace.extend(trace_items)
        return self

    def with_metadata(self, metadata: Mapping[str, Any]) -> ContextBuilder:
        """Merge metadata fields."""
        self._metadata_fields.update(dict(metadata))
        return self

    def with_created_at(self, created_at: str) -> ContextBuilder:
        """Set an explicit creation timestamp."""
        self._created_at = created_at
        return self

    def build(self, context_id: str) -> ContextInterface:
        """Build a mutable runtime context for the ContextBuilderInterface."""
        self._context_id = context_id
        return RuntimeContext(
            id=context_id,
            pipeline_id=self._pipeline_id,
            chart_id=self._chart_id,
            attributes=dict(self._attributes),
            stage_outputs={},
        )

    def build_analysis_context(
        self,
        context_id: str | None = None,
    ) -> AnalysisContext:
        """Build an immutable Analysis Context contract."""
        resolved_id = context_id or self._context_id
        if not resolved_id:
            raise ContextError("context_id_required")
        if not self._pipeline_id:
            raise ContextError("pipeline_id_required")
        created_at = self._created_at or utc_now()
        timestamps = ModelTimestamps(created_at=created_at, updated_at=created_at)
        metadata = AnalysisMetadata(
            id=f"meta_{resolved_id}",
            version=self._version,
            metadata=dict(self._metadata_fields),
            trace=tuple(self._trace),
            timestamps=timestamps,
        )
        return AnalysisContext(
            id=resolved_id,
            version=self._version,
            metadata=metadata,
            trace=tuple(self._trace),
            timestamps=timestamps,
            pipeline_id=self._pipeline_id,
            chart_id=self._chart_id,
            attributes=dict(self._attributes),
        )
