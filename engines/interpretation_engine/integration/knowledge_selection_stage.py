"""Interpretation Pipeline wrapper for IE-2 Knowledge Selection."""

from __future__ import annotations

from typing import Any, Mapping

from engines.interpretation_engine.knowledge.composition_context import (
    build_composition_context,
)
from engines.interpretation_engine.knowledge.sentence_candidate_builder import (
    SentenceCandidateBuilder,
)
from engines.interpretation_engine.pipeline.canonical_pipeline_executor import (
    InterpretationPipelineContext,
)
from engines.interpretation_engine.pipeline.diagnostics import (
    DIAG_KNOWLEDGE_MISSING,
    CanonicalInterpretationPipelineError,
    InterpretationMissingInputError,
)


def _as_dict(value: Any) -> dict[str, Any]:
    if hasattr(value, "to_dict"):
        return dict(value.to_dict())
    if isinstance(value, Mapping):
        return dict(value)
    raise InterpretationMissingInputError(DIAG_KNOWLEDGE_MISSING, "Invalid knowledge input")


class KnowledgeSelectionStage:
    """Integrate released Knowledge Selection Engine into the canonical pipeline."""

    def __init__(self) -> None:
        """Bind the released IE-2 candidate builder."""
        self._builder = SentenceCandidateBuilder()

    def execute(self, context: InterpretationPipelineContext) -> Mapping[str, Any]:
        """Run IE-2 against sealed foundation and AX snapshots."""
        if context.get_output("foundation_result") is None and context.foundation_input is None:
            raise InterpretationMissingInputError(
                DIAG_KNOWLEDGE_MISSING,
                "Missing foundation result for knowledge selection",
            )
        if context.knowledge_input is not None:
            return {"knowledge_result": _as_dict(context.knowledge_input)}
        if (
            context.analysis_input is None
            or context.decision_input is None
            or context.luck_input is None
        ):
            raise InterpretationMissingInputError(
                DIAG_KNOWLEDGE_MISSING,
                "Missing knowledge selection inputs",
            )
        foundation = context.get_output("foundation_result")
        result = self._builder.run(
            build_composition_context(
                analysis_result=context.analysis_input,
                decision_result=context.decision_input,
                luck_result=context.luck_input,
                interpretation_context=foundation,
            )
        )
        if not result.success:
            raise CanonicalInterpretationPipelineError("knowledge_execution_failed")
        return {"knowledge_result": result.to_dict()}
