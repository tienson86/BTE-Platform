"""Temperature Interpreter — Pack 03 business logic module.

Infrastructure contract remains frozen.
Business logic reads Pack 02 FinalResult and Pack 01 temperature rules only.
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
from engines.interpretation_engine.interpreter_runtime.interpreters.temperature.constants import (
    TEMPERATURE_INTERPRETER_ID,
    TEMPERATURE_INTERPRETER_VERSION,
    TEMPERATURE_SECTION_TYPE,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.temperature.service import (
    TemperatureInterpreterService,
)
from engines.interpretation_engine.runtime.contracts import RuntimeExecuteResult

logger = logging.getLogger(__name__)


class TemperatureInterpreter(InterpreterSkeletonRuntime):
    """Complete Temperature Interpreter (Hàn / Nhiệt / Táo / Thấp / Cân bằng).

    Input: PackInterpretationContext.final_result (Pack 02 FinalResult)
    Output: TemperatureInterpretationSection (also exposed as SectionResult shell)

    Evaluates:
    - Cold
    - Hot
    - Dry
    - Wet
    - Balance

    Pack 01 rule database only (``database/11_temperature``).

    When FinalResult has no temperature payload, falls back to empty skeleton
    section for backward-compatible infrastructure tests.
    """

    interpreter_id = TEMPERATURE_INTERPRETER_ID
    section_type = TEMPERATURE_SECTION_TYPE
    version = TEMPERATURE_INTERPRETER_VERSION

    def __init__(
        self,
        *,
        runtime_id: str | None = None,
        service: TemperatureInterpreterService | None = None,
    ) -> None:
        """Initialize with optional TemperatureInterpreterService (DI)."""
        super().__init__(runtime_id=runtime_id)
        self._service = service or TemperatureInterpreterService()

    def _execute_body(self, context: Any) -> RuntimeExecuteResult:
        """Execute temperature interpretation against Pack 02 FinalResult."""
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
                "temperature_interpreter_skeleton_fallback",
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
                    "temperature_interpretation_section": None,
                },
                messages=("interpreter_skeleton_ok",),
            )

        section = typed.section
        logger.info(
            "temperature_interpreter_execute",
            extra={
                "interpreter_id": self.interpreter_id,
                "context_id": context.id,
                "section_id": section.id,
                "temperature_level": typed.temperature_level,
                "cold": typed.cold,
                "hot": typed.hot,
                "dry": typed.dry,
                "wet": typed.wet,
                "balance": typed.balance,
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
                "temperature_interpretation_section": typed,
            },
            messages=("temperature_interpreter_ok",),
        )
