"""Conflict Interpreter — Pack 03 business logic module.

Infrastructure contract remains frozen.
Interprets Clash / Punishment / Harm / Destruction using Pack 01 quan_he
and clash_score rules.
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
from engines.interpretation_engine.interpreter_runtime.interpreters.conflict.constants import (
    CONFLICT_INTERPRETER_ID,
    CONFLICT_INTERPRETER_VERSION,
    CONFLICT_SECTION_TYPE,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.conflict.service import (
    ConflictInterpreterService,
)
from engines.interpretation_engine.runtime.contracts import RuntimeExecuteResult

logger = logging.getLogger(__name__)


class ConflictInterpreter(InterpreterSkeletonRuntime):
    """Complete Conflict Interpreter (Xung / Hinh / Hai / Pha).

    Input: PackInterpretationContext.final_result (Pack 02 FinalResult)
    Output: ConflictInterpretationSection (also exposed as SectionResult shell)

    Interprets:
    - Clash
    - Punishment
    - Harm
    - Destruction

    When FinalResult has no conflict payload, falls back to empty skeleton
    section for backward-compatible infrastructure tests.
    """

    interpreter_id = CONFLICT_INTERPRETER_ID
    section_type = CONFLICT_SECTION_TYPE
    version = CONFLICT_INTERPRETER_VERSION

    def __init__(
        self,
        *,
        runtime_id: str | None = None,
        service: ConflictInterpreterService | None = None,
    ) -> None:
        """Initialize with optional ConflictInterpreterService (DI)."""
        super().__init__(runtime_id=runtime_id)
        self._service = service or ConflictInterpreterService()

    def _execute_body(self, context: Any) -> RuntimeExecuteResult:
        """Execute conflict interpretation against Pack 02 FinalResult."""
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
                "conflict_interpreter_skeleton_fallback",
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
                    "conflict_interpretation_section": None,
                },
                messages=("interpreter_skeleton_ok",),
            )

        section = typed.section
        logger.info(
            "conflict_interpreter_execute",
            extra={
                "interpreter_id": self.interpreter_id,
                "context_id": context.id,
                "section_id": section.id,
                "conflict_score": typed.conflict_score,
                "clash_count": len(typed.clashes),
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
                "conflict_interpretation_section": typed,
            },
            messages=("conflict_interpreter_ok",),
        )
