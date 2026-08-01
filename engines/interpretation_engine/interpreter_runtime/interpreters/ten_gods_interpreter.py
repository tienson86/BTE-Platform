"""Ten Gods Interpreter — Pack 03 business logic module.

Infrastructure contract remains frozen.
Interprets Ten Gods / Distribution / Strength / Interaction using Pack 01
thap_than, score, and interpretation rules.
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
from engines.interpretation_engine.interpreter_runtime.interpreters.ten_gods.constants import (
    TEN_GODS_INTERPRETER_ID,
    TEN_GODS_INTERPRETER_VERSION,
    TEN_GODS_SECTION_TYPE,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.ten_gods.service import (
    TenGodsInterpreterService,
)
from engines.interpretation_engine.runtime.contracts import RuntimeExecuteResult

logger = logging.getLogger(__name__)


class TenGodsInterpreter(InterpreterSkeletonRuntime):
    """Complete Ten Gods Interpreter (Thap Than).

    Input: PackInterpretationContext.final_result (Pack 02 FinalResult)
    Output: TenGodsInterpretationSection (also exposed as SectionResult shell)

    Interprets:
    - Ten Gods
    - Distribution
    - Strength
    - Interaction

    When FinalResult has no ten-gods payload, falls back to empty skeleton
    section for backward-compatible infrastructure tests.
    """

    interpreter_id = TEN_GODS_INTERPRETER_ID
    section_type = TEN_GODS_SECTION_TYPE
    version = TEN_GODS_INTERPRETER_VERSION

    def __init__(
        self,
        *,
        runtime_id: str | None = None,
        service: TenGodsInterpreterService | None = None,
    ) -> None:
        """Initialize with optional TenGodsInterpreterService (DI)."""
        super().__init__(runtime_id=runtime_id)
        self._service = service or TenGodsInterpreterService()

    def _execute_body(self, context: Any) -> RuntimeExecuteResult:
        """Execute ten-gods interpretation against Pack 02 FinalResult."""
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
                "ten_gods_interpreter_skeleton_fallback",
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
                    "ten_gods_interpretation_section": None,
                },
                messages=("interpreter_skeleton_ok",),
            )

        section = typed.section
        logger.info(
            "ten_gods_interpreter_execute",
            extra={
                "interpreter_id": self.interpreter_id,
                "context_id": context.id,
                "section_id": section.id,
                "ten_gods_score": typed.ten_gods_score,
                "ten_gods_count": len(typed.ten_gods),
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
                "ten_gods_interpretation_section": typed,
            },
            messages=("ten_gods_interpreter_ok",),
        )
