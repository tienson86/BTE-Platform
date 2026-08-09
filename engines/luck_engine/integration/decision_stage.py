"""Luck Pipeline wrapper for LE-3 Luck Decision."""

from __future__ import annotations

from datetime import datetime
from typing import Callable, Mapping

from engines.luck_engine.decision.luck_decision_engine import LuckDecisionEngine
from engines.luck_engine.exceptions import (
    LuckDependencyViolationError,
    LuckMissingInputError,
    LuckPipelineError,
)
from engines.luck_engine.pipeline.diagnostics import DIAG_ANALYSIS_MISSING, DIAG_DECISION_MISSING
from engines.luck_engine.pipeline.pipeline_executor import LuckPipelineContext


class DecisionStage:
    """Integrate released Luck Decision Engine into the canonical pipeline."""

    def __init__(self, *, clock: Callable[[], datetime] | None = None) -> None:
        """Bind a clock so nested decision traces stay deterministic."""
        self._engine = LuckDecisionEngine(clock=clock)

    def execute(self, context: LuckPipelineContext) -> Mapping[str, Any]:
        """Run LE-3 against immutable timeline, luck analysis, and AX snapshots."""
        timeline_result = context.get_output("timeline_result")
        analysis_result = context.get_output("analysis_result")
        if timeline_result is None or analysis_result is None:
            missing = []
            if timeline_result is None:
                missing.append("timeline")
            if analysis_result is None:
                missing.append("analysis")
            raise LuckDependencyViolationError(
                f"missing_inputs:decision:{','.join(missing)}"
            )
        if context.analysis_input is None:
            raise LuckMissingInputError(DIAG_ANALYSIS_MISSING, "Missing canonical analysis input")
        if context.decision_input is None:
            raise LuckMissingInputError(DIAG_DECISION_MISSING, "Missing canonical decision input")
        result = self._engine.run(
            timeline_result=timeline_result,
            luck_analysis_result=analysis_result,
            analysis_result=context.analysis_input,
            decision_result=context.decision_input,
        )
        payload = result.to_dict()
        if not result.success:
            raise LuckPipelineError("decision_execution_failed")
        return {"decision_result": payload}
