"""Report Pipeline wrapper for RE-1 Foundation."""

from __future__ import annotations

from typing import Any, Mapping

from engines.report_engine.context.canonical_report_context import build_report_context
from engines.report_engine.pipeline.diagnostics import (
    DIAG_FOUNDATION_MISSING,
    ReportMissingInputError,
)
from engines.report_engine.pipeline.pipeline_executor import ReportPipelineContext


def _as_dict(value: Any) -> dict[str, Any]:
    if hasattr(value, "to_dict"):
        return dict(value.to_dict())
    if isinstance(value, Mapping):
        return dict(value)
    raise ReportMissingInputError(DIAG_FOUNDATION_MISSING, "Invalid foundation input")


class FoundationStage:
    """Integrate released Report Foundation into the canonical pipeline."""

    def execute(self, context: ReportPipelineContext) -> Mapping[str, Any]:
        """Build or admit an RE-1 Report Context snapshot."""
        if context.foundation_input is not None:
            return {"foundation_result": _as_dict(context.foundation_input)}
        if (
            context.analysis_input is None
            or context.decision_input is None
            or context.luck_input is None
            or context.interpretation_input is None
        ):
            raise ReportMissingInputError(
                DIAG_FOUNDATION_MISSING,
                "Missing Report Foundation inputs",
            )
        built = build_report_context(
            analysis_result=context.analysis_input,
            decision_result=context.decision_input,
            luck_result=context.luck_input,
            interpretation_result=context.interpretation_input,
        )
        return {"foundation_result": built.to_dict()}
