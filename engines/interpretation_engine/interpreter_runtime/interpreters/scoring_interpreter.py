"""Scoring Interpreter — Pack 03 business logic module.

Infrastructure contract remains frozen.
Interprets Overall Score / Dimension Scores / Confidence / Quality using
Pack 01 ``09_final_score`` rules.
"""

from __future__ import annotations

import logging
from typing import Any

from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.base_skeleton import (
    InterpreterSkeletonRuntime,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.scoring.constants import (
    SCORING_INTERPRETER_ID,
    SCORING_INTERPRETER_VERSION,
    SCORING_SECTION_TYPE,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.scoring.service import (
    ScoringInterpreterService,
)
from engines.interpretation_engine.runtime.contracts import RuntimeExecuteResult

logger = logging.getLogger(__name__)


class ScoringInterpreter(InterpreterSkeletonRuntime):
    """Complete Scoring Interpreter (Final Score).

    Input: PackInterpretationContext.final_result (Pack 02 FinalResult)
    Output: ScoringInterpretationSection (also exposed as SectionResult shell)

    Interprets:
    - Overall Score
    - Dimension Scores
    - Confidence
    - Quality

    When FinalResult has no scoring payload/scores, falls back to empty skeleton
    section for backward-compatible infrastructure tests.
    """

    interpreter_id = SCORING_INTERPRETER_ID
    section_type = SCORING_SECTION_TYPE
    version = SCORING_INTERPRETER_VERSION

    def __init__(
        self,
        *,
        runtime_id: str | None = None,
        service: ScoringInterpreterService | None = None,
    ) -> None:
        """Initialize with optional ScoringInterpreterService (DI)."""
        super().__init__(runtime_id=runtime_id)
        self._service = service or ScoringInterpreterService()

    def _execute_body(self, context: Any) -> RuntimeExecuteResult:
        """Execute scoring interpretation against Pack 02 FinalResult."""
        if not isinstance(context, PackInterpretationContext):
            return RuntimeExecuteResult(
                runtime_id=self.runtime_id,
                success=False,
                messages=("pack_interpretation_context_required",),
            )
        if not context.validate():
            return RuntimeExecuteResult(
                runtime_id=self.runtime_id,
                success=False,
                messages=("pack_interpretation_context_invalid",),
            )

        typed = self._service.interpret(context)
        if typed is None:
            section = self.build_empty_section(context)
            logger.info(
                "scoring_interpreter_skeleton_fallback",
                extra={"context_id": context.id, "section_id": section.id},
            )
            return RuntimeExecuteResult(
                runtime_id=self.runtime_id,
                success=True,
                payload={
                    "interpreter_id": self.interpreter_id,
                    "version": self.version,
                    "context_id": context.id,
                    "section": section,
                    "interpretation_section": section,
                    "scoring_interpretation_section": None,
                },
                messages=("interpreter_skeleton_ok",),
            )

        section = typed.section
        logger.info(
            "scoring_interpreter_execute",
            extra={
                "interpreter_id": self.interpreter_id,
                "context_id": context.id,
                "section_id": section.id,
                "overall_score": typed.overall_score,
                "grade": typed.grade,
            },
        )
        return RuntimeExecuteResult(
            runtime_id=self.runtime_id,
            success=True,
            payload={
                "interpreter_id": self.interpreter_id,
                "version": self.version,
                "context_id": context.id,
                "section": section,
                "interpretation_section": section,
                "scoring_interpretation_section": typed,
            },
            messages=("scoring_interpreter_ok",),
        )
