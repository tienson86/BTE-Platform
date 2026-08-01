"""Strength Interpreter — first Pack 03 business logic module.

Infrastructure contract remains frozen.
Business logic reads Pack 02 FinalResult and Pack 01 strength rules only.
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
from engines.interpretation_engine.interpreter_runtime.interpreters.strength.constants import (
    STRENGTH_INTERPRETER_ID,
    STRENGTH_INTERPRETER_VERSION,
    STRENGTH_SECTION_TYPE,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.strength.service import (
    StrengthInterpreterService,
)
from engines.interpretation_engine.runtime.contracts import RuntimeExecuteResult

logger = logging.getLogger(__name__)


class StrengthInterpreter(InterpreterSkeletonRuntime):
    """Complete Strength Interpreter (Thân vượng / Thân nhược).

    Input: PackInterpretationContext.final_result (Pack 02 FinalResult)
    Output: StrengthInterpretationSection (also exposed as SectionResult shell)

    When FinalResult has no strength payload, falls back to empty skeleton
    section for backward-compatible infrastructure tests.
    """

    interpreter_id = STRENGTH_INTERPRETER_ID
    section_type = STRENGTH_SECTION_TYPE
    version = STRENGTH_INTERPRETER_VERSION

    def __init__(
        self,
        *,
        runtime_id: str | None = None,
        service: StrengthInterpreterService | None = None,
    ) -> None:
        """Initialize with optional StrengthInterpreterService (DI)."""
        super().__init__(runtime_id=runtime_id)
        self._service = service or StrengthInterpreterService()

    def _execute_body(self, context: Any) -> RuntimeExecuteResult:
        """Execute strength interpretation against Pack 02 FinalResult."""
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
            # No Pack 02 strength payload → preserve frozen skeleton contract.
            section = self.build_empty_section(context)
            logger.info(
                "strength_interpreter_skeleton_fallback",
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
                    "strength_interpretation_section": None,
                },
                messages=("interpreter_skeleton_ok",),
            )

        section = typed.section
        logger.info(
            "strength_interpreter_execute",
            extra={
                "interpreter_id": self.interpreter_id,
                "context_id": context.id,
                "section_id": section.id,
                "final_strength": typed.final_strength,
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
                "strength_interpretation_section": typed,
            },
            messages=("strength_interpreter_ok",),
        )
