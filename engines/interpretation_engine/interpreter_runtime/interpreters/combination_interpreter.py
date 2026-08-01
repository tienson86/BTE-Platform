"""Combination Interpreter — Pack 03 business logic module.

Infrastructure contract remains frozen.
Interprets Stem / Branch Combinations, Transformation, and Combination Score
using Pack 01 quan_he + combination_score rules.
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
from engines.interpretation_engine.interpreter_runtime.interpreters.combination.constants import (
    COMBINATION_INTERPRETER_ID,
    COMBINATION_INTERPRETER_VERSION,
    COMBINATION_SECTION_TYPE,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.combination.service import (
    CombinationInterpreterService,
)
from engines.interpretation_engine.runtime.contracts import RuntimeExecuteResult

logger = logging.getLogger(__name__)


class CombinationInterpreter(InterpreterSkeletonRuntime):
    """Complete Combination Interpreter (Hợp Can / Hợp Chi / Hóa).

    Input: PackInterpretationContext.final_result (Pack 02 FinalResult)
    Output: CombinationInterpretationSection (also exposed as SectionResult shell)

    Interprets:
    - Stem Combination
    - Branch Combination
    - Transformation
    - Combination Score

    When FinalResult has no combination payload, falls back to empty skeleton
    section for backward-compatible infrastructure tests.
    """

    interpreter_id = COMBINATION_INTERPRETER_ID
    section_type = COMBINATION_SECTION_TYPE
    version = COMBINATION_INTERPRETER_VERSION

    def __init__(
        self,
        *,
        runtime_id: str | None = None,
        service: CombinationInterpreterService | None = None,
    ) -> None:
        """Initialize with optional CombinationInterpreterService (DI)."""
        super().__init__(runtime_id=runtime_id)
        self._service = service or CombinationInterpreterService()

    def _execute_body(self, context: Any) -> RuntimeExecuteResult:
        """Execute combination interpretation against Pack 02 FinalResult."""
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
                "combination_interpreter_skeleton_fallback",
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
                    "combination_interpretation_section": None,
                },
                messages=("interpreter_skeleton_ok",),
            )

        section = typed.section
        logger.info(
            "combination_interpreter_execute",
            extra={
                "interpreter_id": self.interpreter_id,
                "context_id": context.id,
                "section_id": section.id,
                "combination_score": typed.combination_score,
                "stem_count": len(typed.stem_combinations),
                "branch_count": len(typed.branch_combinations),
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
                "combination_interpretation_section": typed,
            },
            messages=("combination_interpreter_ok",),
        )
