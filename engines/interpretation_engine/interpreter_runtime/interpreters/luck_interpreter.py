"""Luck Interpreter — Pack 03 business logic module.

Infrastructure contract remains frozen.
Interprets Dayun / Liunian / Liuyue / Interaction using Pack 01 dai_van,
luck score, and interpretation rules.
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
from engines.interpretation_engine.interpreter_runtime.interpreters.luck.constants import (
    LUCK_INTERPRETER_ID,
    LUCK_INTERPRETER_VERSION,
    LUCK_SECTION_TYPE,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.luck.service import (
    LuckInterpreterService,
)
from engines.interpretation_engine.runtime.contracts import RuntimeExecuteResult

logger = logging.getLogger(__name__)


class LuckInterpreter(InterpreterSkeletonRuntime):
    """Complete Luck Interpreter (Dai Van / Luu Nien / Luu Nguyet).

    Input: PackInterpretationContext.final_result (Pack 02 FinalResult)
    Output: LuckInterpretationSection (also exposed as SectionResult shell)

    Interprets:
    - Dayun
    - Liunian
    - Liuyue
    - Interaction

    When FinalResult has no luck payload, falls back to empty skeleton
    section for backward-compatible infrastructure tests.
    """

    interpreter_id = LUCK_INTERPRETER_ID
    section_type = LUCK_SECTION_TYPE
    version = LUCK_INTERPRETER_VERSION

    def __init__(
        self,
        *,
        runtime_id: str | None = None,
        service: LuckInterpreterService | None = None,
    ) -> None:
        """Initialize with optional LuckInterpreterService (DI)."""
        super().__init__(runtime_id=runtime_id)
        self._service = service or LuckInterpreterService()

    def _execute_body(self, context: Any) -> RuntimeExecuteResult:
        """Execute luck interpretation against Pack 02 FinalResult."""
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
                "luck_interpreter_skeleton_fallback",
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
                    "luck_interpretation_section": None,
                },
                messages=("interpreter_skeleton_ok",),
            )

        section = typed.section
        logger.info(
            "luck_interpreter_execute",
            extra={
                "interpreter_id": self.interpreter_id,
                "context_id": context.id,
                "section_id": section.id,
                "luck_score": typed.luck_score,
                "dayun_count": len(typed.dayun),
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
                "luck_interpretation_section": typed,
            },
            messages=("luck_interpreter_ok",),
        )
