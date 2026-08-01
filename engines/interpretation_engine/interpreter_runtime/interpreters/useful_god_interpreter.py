"""Useful God Interpreter — Pack 03 business logic module.

Infrastructure contract remains frozen.
Interprets Useful / Favorable / Unfavorable Gods and Supporting Elements
using Pack 01 ``database/13_useful_god`` rules.
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
from engines.interpretation_engine.interpreter_runtime.interpreters.useful_god.constants import (
    USEFUL_GOD_INTERPRETER_ID,
    USEFUL_GOD_INTERPRETER_VERSION,
    USEFUL_GOD_SECTION_TYPE,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.useful_god.service import (
    UsefulGodInterpreterService,
)
from engines.interpretation_engine.runtime.contracts import RuntimeExecuteResult

logger = logging.getLogger(__name__)


class UsefulGodInterpreter(InterpreterSkeletonRuntime):
    """Complete Useful God Interpreter (Dụng / Hỷ / Kỵ thần).

    Input: PackInterpretationContext.final_result (Pack 02 FinalResult)
    Output: UsefulGodInterpretationSection (also exposed as SectionResult shell)

    Interprets:
    - Useful God
    - Favorable God
    - Unfavorable God
    - Supporting Elements

    When FinalResult has no useful-god payload, falls back to empty skeleton
    section for backward-compatible infrastructure tests.
    """

    interpreter_id = USEFUL_GOD_INTERPRETER_ID
    section_type = USEFUL_GOD_SECTION_TYPE
    version = USEFUL_GOD_INTERPRETER_VERSION

    def __init__(
        self,
        *,
        runtime_id: str | None = None,
        service: UsefulGodInterpreterService | None = None,
    ) -> None:
        """Initialize with optional UsefulGodInterpreterService (DI)."""
        super().__init__(runtime_id=runtime_id)
        self._service = service or UsefulGodInterpreterService()

    def _execute_body(self, context: Any) -> RuntimeExecuteResult:
        """Execute useful-god interpretation against Pack 02 FinalResult."""
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
                "useful_god_interpreter_skeleton_fallback",
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
                    "useful_god_interpretation_section": None,
                },
                messages=("interpreter_skeleton_ok",),
            )

        section = typed.section
        logger.info(
            "useful_god_interpreter_execute",
            extra={
                "interpreter_id": self.interpreter_id,
                "context_id": context.id,
                "section_id": section.id,
                "useful_god": typed.useful_god,
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
                "useful_god_interpretation_section": typed,
            },
            messages=("useful_god_interpreter_ok",),
        )
