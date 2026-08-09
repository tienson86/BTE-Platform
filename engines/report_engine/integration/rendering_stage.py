"""Report Pipeline wrapper for RE-3 Rendering Engine."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Callable, Mapping

from engines.report_engine.pipeline.diagnostics import (
    DIAG_RENDERER_MISSING,
    ReportMissingInputError,
)
from engines.report_engine.pipeline.pipeline_executor import ReportPipelineContext
from engines.report_engine.rendering.rendering_engine import ReportRenderingEngine


def _as_dict(value: Any) -> dict[str, Any]:
    if hasattr(value, "to_dict"):
        return dict(value.to_dict())
    if isinstance(value, Mapping):
        return dict(value)
    raise ReportMissingInputError(DIAG_RENDERER_MISSING, "Invalid rendering input")


class RenderingStage:
    """Integrate released Rendering Engine into the canonical pipeline."""

    def __init__(self, *, clock: Callable[[], datetime] | None = None) -> None:
        """Bind a clock so nested RE-3 traces stay deterministic."""
        self._engine = ReportRenderingEngine(clock=clock)

    def execute(self, context: ReportPipelineContext) -> Mapping[str, Any]:
        """Run RE-3 against the immutable layout snapshot."""
        if context.rendering_input is not None:
            return {"rendering_result": _as_dict(context.rendering_input)}
        layout = context.get_output("layout_result")
        if layout is None:
            raise ReportMissingInputError(
                DIAG_RENDERER_MISSING,
                "Missing layout result for rendering",
            )
        if not context.renderer_id:
            raise ReportMissingInputError(DIAG_RENDERER_MISSING, "Missing renderer")
        result = self._engine.run(layout=layout, renderer=context.renderer_id)
        if not result.success:
            raise ReportMissingInputError(DIAG_RENDERER_MISSING, "Renderer missing or failed")
        return {"rendering_result": result.to_dict()}
