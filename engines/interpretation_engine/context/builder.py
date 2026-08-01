"""Interpretation context builder for immutable construction."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping

from engines.analysis_engine.models.final_result import FinalResult
from engines.interpretation_engine.context.context_builder_interface import (
    InterpretationContextBuilderInterface,
)
from engines.interpretation_engine.context.interpretation_context import InterpretationContext
from engines.interpretation_engine.exceptions.context_error import InterpretationContextError
from engines.interpretation_engine.models.final_analysis_input import FinalAnalysisInput
from engines.interpretation_engine.models.interpretation_context_model import (
    InterpretationContextModel,
)
from engines.interpretation_engine.utils.ids import new_id

_DEFAULT_VERSION = "0.0.0-architecture"


def utc_now() -> str:
    """Return a UTC ISO-8601 timestamp for context lifecycle events."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class ContextBuilder(InterpretationContextBuilderInterface):
    """Fluent builder for Interpretation Context from Pack 02 FinalAnalysisResult.

    Builds immutable contexts without interpretation business logic.
    """

    def __init__(self) -> None:
        """Initialize an empty builder."""
        self._context_id: str | None = None
        self._version: str = _DEFAULT_VERSION
        self._pipeline_id: str | None = None
        self._final_result: FinalResult | None = None
        self._attributes: dict[str, Any] = {}
        self._trace: list[str] = []
        self._metadata: dict[str, Any] = {}
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

    def with_final_result(self, final_result: FinalResult) -> ContextBuilder:
        """Set the Pack 02 FinalAnalysisResult / FinalResult input."""
        self._final_result = final_result
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
        self._metadata.update(dict(metadata))
        return self

    def with_created_at(self, created_at: str) -> ContextBuilder:
        """Set an explicit creation timestamp."""
        self._created_at = created_at
        return self

    def validate(self, final_input: FinalAnalysisInput) -> bool:
        """Validate Pack 02 input before context construction."""
        return final_input.validate() and final_input.final_result.validate()

    def build(self, final_input: FinalAnalysisInput) -> InterpretationContextModel:
        """Build an architecture model from FinalAnalysisInput (interface contract)."""
        context = self.build_from_final_result(
            final_input.final_result,
            context_id=final_input.id if final_input.id else None,
            version=final_input.version or self._version,
            attributes=final_input.metadata,
        )
        return InterpretationContextModel(
            id=context.id,
            version=context.version,
            pipeline_id=context.pipeline_id,
            input=final_input,
            attributes=dict(context.attributes),
            trace=context.trace,
        )

    def build_context(
        self,
        context_id: str | None = None,
    ) -> InterpretationContext:
        """Build an immutable Pack 03 InterpretationContext from builder state."""
        if self._final_result is None:
            raise InterpretationContextError("final_result_required")
        return self.build_from_final_result(
            self._final_result,
            context_id=context_id or self._context_id,
            version=self._version,
            pipeline_id=self._pipeline_id,
            attributes=self._attributes,
            trace=tuple(self._trace),
            metadata=self._metadata,
            created_at=self._created_at,
        )

    def build_from_final_result(
        self,
        final_result: FinalResult,
        *,
        context_id: str | None = None,
        version: str | None = None,
        pipeline_id: str | None = None,
        attributes: Mapping[str, Any] | None = None,
        trace: tuple[str, ...] = (),
        metadata: Mapping[str, Any] | None = None,
        created_at: str | None = None,
    ) -> InterpretationContext:
        """Build InterpretationContext from Pack 02 FinalResult (sole input)."""
        if final_result is None:
            raise InterpretationContextError("final_result_required")
        if not final_result.validate():
            raise InterpretationContextError("final_result_invalid")

        resolved_id = context_id or self._context_id or new_id("ctx")
        resolved_pipeline = (
            pipeline_id
            or self._pipeline_id
            or final_result.pipeline_id
            or "interpretation_pipeline"
        )
        stamp = created_at or self._created_at or utc_now()
        merged_attributes = dict(self._attributes)
        if attributes:
            merged_attributes.update(dict(attributes))
        merged_trace = tuple(self._trace) + tuple(trace)
        merged_metadata = dict(self._metadata)
        if metadata:
            merged_metadata.update(dict(metadata))

        return InterpretationContext(
            id=resolved_id,
            version=version or self._version,
            pipeline_id=resolved_pipeline,
            source_final_result_id=final_result.id,
            final_result=final_result,
            attributes=merged_attributes,
            trace=merged_trace + ("context_built_from_final_result",),
            created_at=stamp,
            updated_at=stamp,
            completed_at=None,
            metadata=merged_metadata,
        )
