"""Shensha Interpreter — Pack 03 business logic module.

Infrastructure contract remains frozen.
Interprets Detected Shensha / Importance / Priority / Explanation using Pack 01
than_sat and shensha score rules.
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
from engines.interpretation_engine.interpreter_runtime.interpreters.shensha.constants import (
    SHENSHA_INTERPRETER_ID,
    SHENSHA_INTERPRETER_VERSION,
    SHENSHA_SECTION_TYPE,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.shensha.service import (
    ShenshaInterpreterService,
)
from engines.interpretation_engine.runtime.contracts import RuntimeExecuteResult

logger = logging.getLogger(__name__)


class ShenshaInterpreter(InterpreterSkeletonRuntime):
    """Complete Shensha Interpreter (Than Sat).

    Input: PackInterpretationContext.final_result (Pack 02 FinalResult)
    Output: ShenshaInterpretationSection (also exposed as SectionResult shell)

    Interprets:
    - All detected Shensha
    - Importance
    - Priority
    - Explanation

    When FinalResult has no shensha payload, falls back to empty skeleton
    section for backward-compatible infrastructure tests.
    """

    interpreter_id = SHENSHA_INTERPRETER_ID
    section_type = SHENSHA_SECTION_TYPE
    version = SHENSHA_INTERPRETER_VERSION

    def __init__(
        self,
        *,
        runtime_id: str | None = None,
        service: ShenshaInterpreterService | None = None,
    ) -> None:
        """Initialize with optional ShenshaInterpreterService (DI)."""
        super().__init__(runtime_id=runtime_id)
        self._service = service or ShenshaInterpreterService()

    def _execute_body(self, context: Any) -> RuntimeExecuteResult:
        """Execute shensha interpretation against Pack 02 FinalResult."""
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
                "shensha_interpreter_skeleton_fallback",
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
                    "shensha_interpretation_section": None,
                },
                messages=("interpreter_skeleton_ok",),
            )

        section = typed.section
        logger.info(
            "shensha_interpreter_execute",
            extra={
                "interpreter_id": self.interpreter_id,
                "context_id": context.id,
                "section_id": section.id,
                "shensha_score": typed.shensha_score,
                "detected_count": len(typed.detected),
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
                "shensha_interpretation_section": typed,
            },
            messages=("shensha_interpreter_ok",),
        )
