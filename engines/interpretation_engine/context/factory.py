"""Interpretation context factory for lifecycle creation."""

from __future__ import annotations

from typing import Any, Mapping

from engines.analysis_engine.models.final_result import FinalResult
from engines.interpretation_engine.context.builder import ContextBuilder, utc_now
from engines.interpretation_engine.context.interpretation_context import InterpretationContext
from engines.interpretation_engine.exceptions.context_error import InterpretationContextError
from engines.interpretation_engine.utils.ids import new_id

_DEFAULT_VERSION = "0.0.0-architecture"


class ContextFactory:
    """Factory for creating Interpretation Context instances from FinalResult.

    Handles create-phase construction only. No interpretation evaluation.
    """

    def __init__(self, *, default_version: str = _DEFAULT_VERSION) -> None:
        """Initialize factory defaults."""
        self._default_version = default_version

    def create(
        self,
        *,
        final_result: FinalResult,
        context_id: str | None = None,
        pipeline_id: str | None = None,
        attributes: Mapping[str, Any] | None = None,
        version: str | None = None,
        metadata: Mapping[str, Any] | None = None,
        trace: tuple[str, ...] = (),
    ) -> InterpretationContext:
        """Create a new immutable Interpretation Context (Create phase)."""
        builder = (
            ContextBuilder()
            .with_context_id(context_id or new_id("ctx"))
            .with_pipeline_id(pipeline_id or final_result.pipeline_id)
            .with_version(version or self._default_version)
            .with_final_result(final_result)
            .with_attributes(attributes or {})
            .with_metadata(metadata or {})
            .with_trace(*trace)
            .with_created_at(utc_now())
        )
        return builder.build_context()

    def create_from_final_result(
        self,
        final_result: FinalResult,
        *,
        context_id: str | None = None,
        pipeline_id: str | None = None,
        attributes: Mapping[str, Any] | None = None,
    ) -> InterpretationContext:
        """Create InterpretationContext from Pack 02 FinalAnalysisResult only."""
        return self.create(
            final_result=final_result,
            context_id=context_id,
            pipeline_id=pipeline_id,
            attributes=attributes,
        )

    def clone_with_attributes(
        self,
        context: InterpretationContext,
        attributes: Mapping[str, Any],
        *,
        trace_item: str | None = None,
        updated_at: str | None = None,
    ) -> InterpretationContext:
        """Return a new context with merged attributes (immutable expand)."""
        if not context.validate():
            raise InterpretationContextError("context_invalid_for_clone")
        stamp = updated_at or utc_now()
        merged = dict(context.attributes)
        merged.update(dict(attributes))
        trace = context.trace + ((trace_item,) if trace_item else ())
        return InterpretationContext(
            id=context.id,
            version=context.version,
            pipeline_id=context.pipeline_id,
            source_final_result_id=context.source_final_result_id,
            final_result=context.final_result,
            attributes=merged,
            trace=trace,
            created_at=context.created_at,
            updated_at=stamp,
            completed_at=context.completed_at,
            metadata=dict(context.metadata),
        )
