"""Pattern Interpreter — Pack 03 business logic module.

Infrastructure contract remains frozen.
Uses Pattern Engine Matching / Priority / Resolution with Pack 01 rules.
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
from engines.interpretation_engine.interpreter_runtime.interpreters.pattern.constants import (
    PATTERN_INTERPRETER_ID,
    PATTERN_INTERPRETER_VERSION,
    PATTERN_SECTION_TYPE,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.pattern.service import (
    PatternInterpreterService,
)
from engines.interpretation_engine.runtime.contracts import RuntimeExecuteResult

logger = logging.getLogger(__name__)


class PatternInterpreter(InterpreterSkeletonRuntime):
    """Complete Pattern Interpreter (Cách cục).

    Input: PackInterpretationContext.final_result (Pack 02 FinalResult)
    Output: PatternInterpretationSection (also exposed as SectionResult shell)

    Uses:
    - Pattern Engine (Pack 01 loader/rules)
    - Pattern Matching
    - Pattern Priority
    - Pattern Resolution

    When FinalResult has no pattern payload, falls back to empty skeleton
    section for backward-compatible infrastructure tests.
    """

    interpreter_id = PATTERN_INTERPRETER_ID
    section_type = PATTERN_SECTION_TYPE
    version = PATTERN_INTERPRETER_VERSION

    def __init__(
        self,
        *,
        runtime_id: str | None = None,
        service: PatternInterpreterService | None = None,
    ) -> None:
        """Initialize with optional PatternInterpreterService (DI)."""
        super().__init__(runtime_id=runtime_id)
        self._service = service or PatternInterpreterService()

    def _execute_body(self, context: Any) -> RuntimeExecuteResult:
        """Execute pattern interpretation against Pack 02 FinalResult."""
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
                "pattern_interpreter_skeleton_fallback",
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
                    "pattern_interpretation_section": None,
                },
                messages=("interpreter_skeleton_ok",),
            )

        section = typed.section
        logger.info(
            "pattern_interpreter_execute",
            extra={
                "interpreter_id": self.interpreter_id,
                "context_id": context.id,
                "section_id": section.id,
                "final_pattern": typed.final_pattern,
                "status": typed.status,
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
                "pattern_interpretation_section": typed,
            },
            messages=("pattern_interpreter_ok",),
        )
