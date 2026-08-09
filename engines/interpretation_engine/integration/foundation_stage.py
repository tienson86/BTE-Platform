"""Interpretation Pipeline wrapper for IE-1 Foundation."""

from __future__ import annotations

from typing import Any, Mapping

from engines.interpretation_engine.context.canonical_interpretation_context import (
    build_interpretation_context,
)
from engines.interpretation_engine.pipeline.canonical_pipeline_executor import (
    InterpretationPipelineContext,
)
from engines.interpretation_engine.pipeline.diagnostics import (
    DIAG_FOUNDATION_MISSING,
    InterpretationMissingInputError,
)


def _as_dict(value: Any) -> dict[str, Any]:
    if hasattr(value, "to_dict"):
        return dict(value.to_dict())
    if isinstance(value, Mapping):
        return dict(value)
    raise InterpretationMissingInputError(DIAG_FOUNDATION_MISSING, "Invalid foundation input")


class FoundationStage:
    """Integrate released Interpretation Foundation into the canonical pipeline."""

    def execute(self, context: InterpretationPipelineContext) -> Mapping[str, Any]:
        """Build or admit an IE-1 Interpretation Context snapshot."""
        if context.foundation_input is not None:
            return {"foundation_result": _as_dict(context.foundation_input)}
        if (
            context.analysis_input is None
            or context.decision_input is None
            or context.luck_input is None
        ):
            raise InterpretationMissingInputError(
                DIAG_FOUNDATION_MISSING,
                "Missing Interpretation Foundation inputs",
            )
        built = build_interpretation_context(
            analysis_result=context.analysis_input,
            decision_result=context.decision_input,
            luck_result=context.luck_input,
        )
        return {"foundation_result": built.to_dict()}
