"""Explanation Runtime — Pack 03 infrastructure facade."""

from __future__ import annotations

import logging
from typing import Any

from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.explanation_runtime.assembler import ExplanationAssembler
from engines.interpretation_engine.explanation_runtime.publisher import ExplanationPublisher
from engines.interpretation_engine.explanation_runtime.registry import (
    ExplanationRuntimeRegistry,
)
from engines.interpretation_engine.runtime.base import BaseRuntime
from engines.interpretation_engine.runtime.contracts import RuntimeExecuteResult

logger = logging.getLogger(__name__)


class ExplanationRuntime(BaseRuntime):
    """Explanation runtime with assembler/publisher infrastructure."""

    def __init__(
        self,
        *,
        runtime_id: str = "explanation_runtime",
        registry: ExplanationRuntimeRegistry | None = None,
        assembler: ExplanationAssembler | None = None,
        publisher: ExplanationPublisher | None = None,
    ) -> None:
        """Initialize explanation runtime dependencies."""
        super().__init__(runtime_id=runtime_id)
        self._registry = registry or ExplanationRuntimeRegistry()
        self._assembler = assembler or ExplanationAssembler(self._registry)
        self._publisher = publisher or ExplanationPublisher()

    @property
    def registry(self) -> ExplanationRuntimeRegistry:
        """Return explanation registry."""
        return self._registry

    def validate(self) -> bool:
        """Validate runtime and registry readiness."""
        if not super().validate():
            return False
        return self._registry.validate()

    def _execute_body(self, context: Any) -> RuntimeExecuteResult:
        """Assemble/publish explanation refs only."""
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
        refs = self._assembler.assemble()
        published = self._publisher.publish(refs)
        logger.info(
            "explanation_runtime_execute",
            extra={"context_id": context.id, "ref_count": len(refs)},
        )
        return RuntimeExecuteResult(
            runtime_id=self.runtime_id,
            success=True,
            payload={
                "context_id": context.id,
                "explanation_refs": list(refs),
                "published": published,
            },
            messages=("explanation_runtime_ok",),
        )
