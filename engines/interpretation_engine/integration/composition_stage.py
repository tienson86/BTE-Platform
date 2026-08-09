"""Interpretation Pipeline wrapper for IE-3 Composition & Assembly."""

from __future__ import annotations

from datetime import datetime
from typing import Callable, Mapping

from engines.interpretation_engine.composition.composition_engine import (
    InterpretationCompositionEngine,
)
from engines.interpretation_engine.pipeline.canonical_pipeline_executor import (
    InterpretationPipelineContext,
)
from engines.interpretation_engine.pipeline.diagnostics import (
    DIAG_COMPOSITION_MISSING,
    CanonicalInterpretationPipelineError,
    InterpretationMissingInputError,
)


class CompositionStage:
    """Integrate released Composition Engine into the canonical pipeline."""

    def __init__(self, *, clock: Callable[[], datetime] | None = None) -> None:
        """Bind a clock so nested IE-3 traces stay deterministic."""
        self._engine = InterpretationCompositionEngine(clock=clock)

    def execute(self, context: InterpretationPipelineContext) -> Mapping[str, Any]:
        """Run IE-3 against immutable foundation, knowledge, and AX snapshots."""
        knowledge = context.get_output("knowledge_result")
        foundation = context.get_output("foundation_result")
        if knowledge is None:
            raise InterpretationMissingInputError(
                DIAG_COMPOSITION_MISSING,
                "Missing knowledge result for composition",
            )
        if (
            context.analysis_input is None
            or context.decision_input is None
            or context.luck_input is None
        ):
            raise InterpretationMissingInputError(
                DIAG_COMPOSITION_MISSING,
                "Missing composition assembly inputs",
            )
        result = self._engine.run(
            analysis_result=context.analysis_input,
            decision_result=context.decision_input,
            luck_result=context.luck_input,
            interpretation_context=foundation,
            composition_result=knowledge,
        )
        if not result.success:
            raise CanonicalInterpretationPipelineError("composition_execution_failed")
        return {"composition_result": result.to_dict()}
