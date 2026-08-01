"""Season Interpreter — Pack 03 business logic module.

Infrastructure contract remains frozen.
Business logic reads Pack 02 FinalResult and Pack 01 temperature season/climate rules.
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
from engines.interpretation_engine.interpreter_runtime.interpreters.season.constants import (
    SEASON_INTERPRETER_ID,
    SEASON_INTERPRETER_VERSION,
    SEASON_SECTION_TYPE,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.season.service import (
    SeasonInterpreterService,
)
from engines.interpretation_engine.runtime.contracts import RuntimeExecuteResult

logger = logging.getLogger(__name__)


class SeasonInterpreter(InterpreterSkeletonRuntime):
    """Complete Season Interpreter (tháng lệnh / mùa / khí hậu).

    Input: PackInterpretationContext.final_result (Pack 02 FinalResult)
    Output: SeasonInterpretationSection (also exposed as SectionResult shell)

    Interprets:
    - Season Rules
    - Temperature Rules
    - Month Branch
    - Qi Stage (season_phase)
    - Climate

    When FinalResult has no season/climate payload, falls back to empty skeleton
    section for backward-compatible infrastructure tests.
    """

    interpreter_id = SEASON_INTERPRETER_ID
    section_type = SEASON_SECTION_TYPE
    version = SEASON_INTERPRETER_VERSION

    def __init__(
        self,
        *,
        runtime_id: str | None = None,
        service: SeasonInterpreterService | None = None,
    ) -> None:
        """Initialize with optional SeasonInterpreterService (DI)."""
        super().__init__(runtime_id=runtime_id)
        self._service = service or SeasonInterpreterService()

    def _execute_body(self, context: Any) -> RuntimeExecuteResult:
        """Execute season interpretation against Pack 02 FinalResult."""
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
                "season_interpreter_skeleton_fallback",
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
                    "season_interpretation_section": None,
                },
                messages=("interpreter_skeleton_ok",),
            )

        section = typed.section
        logger.info(
            "season_interpreter_execute",
            extra={
                "interpreter_id": self.interpreter_id,
                "context_id": context.id,
                "section_id": section.id,
                "season": typed.season,
                "month_branch": typed.month_branch,
                "qi_stage": typed.qi_stage,
                "climate": typed.climate,
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
                "season_interpretation_section": typed,
            },
            messages=("season_interpreter_ok",),
        )
