"""Report Pipeline wrapper for RE-2 Layout Engine."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Callable, Mapping

from engines.report_engine.layout.layout_engine import ReportLayoutEngine
from engines.report_engine.pipeline.diagnostics import (
    DIAG_LAYOUT_MISSING,
    CanonicalReportPipelineError,
    ReportMissingInputError,
)
from engines.report_engine.pipeline.pipeline_executor import ReportPipelineContext


def _as_dict(value: Any) -> dict[str, Any]:
    if hasattr(value, "to_dict"):
        return dict(value.to_dict())
    if isinstance(value, Mapping):
        return dict(value)
    raise ReportMissingInputError(DIAG_LAYOUT_MISSING, "Invalid layout input")


class LayoutStage:
    """Integrate released Layout Engine into the canonical pipeline."""

    def __init__(self, *, clock: Callable[[], datetime] | None = None) -> None:
        """Bind a clock so nested RE-2 traces stay deterministic."""
        self._engine = ReportLayoutEngine(clock=clock)

    def execute(self, context: ReportPipelineContext) -> Mapping[str, Any]:
        """Run RE-2 against immutable foundation and interpretation snapshots."""
        if context.get_output("foundation_result") is None and context.foundation_input is None:
            raise ReportMissingInputError(DIAG_LAYOUT_MISSING, "Missing foundation result for layout")
        if context.layout_input is not None:
            return {"layout_result": _as_dict(context.layout_input)}
        if context.interpretation_input is None and context.analysis_input is None:
            raise ReportMissingInputError(DIAG_LAYOUT_MISSING, "Missing layout inputs")
        foundation = context.get_output("foundation_result")
        interpretation = context.interpretation_input
        if interpretation is None and isinstance(foundation, Mapping):
            interpretation = foundation.get("interpretation_snapshot")
        result = self._engine.run(
            report_context=foundation,
            interpretation_result=interpretation,
        )
        if not result.success:
            raise CanonicalReportPipelineError("layout_execution_failed")
        return {"layout_result": result.to_dict()}
