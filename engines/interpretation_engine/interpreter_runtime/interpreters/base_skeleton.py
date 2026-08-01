"""Base interpreter skeleton runtime.

Implements the Pack 03 runtime contract.
Returns empty InterpretationSection shells only — no BaZi logic.
"""

from __future__ import annotations

import logging
from typing import Any

from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.models.section_result import SectionResult
from engines.interpretation_engine.runtime.base import BaseRuntime
from engines.interpretation_engine.runtime.contracts import RuntimeExecuteResult

logger = logging.getLogger(__name__)

# Public alias: empty InterpretationSection == SectionResult shell.
InterpretationSection = SectionResult


def empty_interpretation_section(
    *,
    interpreter_id: str,
    section_type: str,
    context_id: str | None = None,
) -> InterpretationSection:
    """Build an empty InterpretationSection (no paragraphs / no content)."""
    section_id = f"section_{interpreter_id}"
    if context_id:
        section_id = f"section_{interpreter_id}_{context_id}"
    return InterpretationSection(
        id=section_id,
        section_type=section_type,
        title_ref=None,
        interpreter_id=interpreter_id,
        paragraphs=(),
        success=True,
        messages=("interpreter_skeleton_empty_section",),
        attributes={"skeleton": True},
    )


class InterpreterSkeletonRuntime(BaseRuntime):
    """Shared skeleton for Pack 03 domain interpreter runtimes.

    Public contract:
    initialize / validate / execute / shutdown / health / metrics
    """

    interpreter_id: str = "interpreter_skeleton"
    section_type: str = "skeleton"
    version: str = "0.0.0-skeleton"

    def __init__(self, *, runtime_id: str | None = None) -> None:
        """Initialize skeleton runtime identity."""
        resolved_id = runtime_id or self.interpreter_id
        super().__init__(runtime_id=resolved_id)

    def build_empty_section(
        self, context: PackInterpretationContext
    ) -> InterpretationSection:
        """Return an empty InterpretationSection for the given context."""
        return empty_interpretation_section(
            interpreter_id=self.interpreter_id,
            section_type=self.section_type,
            context_id=context.id,
        )

    def _execute_body(self, context: Any) -> RuntimeExecuteResult:
        """Execute skeleton: validate Pack context, return empty section."""
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

        section = self.build_empty_section(context)
        logger.info(
            "interpreter_skeleton_execute",
            extra={
                "interpreter_id": self.interpreter_id,
                "context_id": context.id,
                "section_id": section.id,
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
            },
            messages=("interpreter_skeleton_ok",),
        )
