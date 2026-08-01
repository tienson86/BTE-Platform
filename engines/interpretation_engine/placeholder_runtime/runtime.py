"""Placeholder Runtime

Infrastructure only. No BaZi interpretation / NLG / rendering.
"""

from __future__ import annotations

import logging
from typing import Any

from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.runtime.base import BaseRuntime
from engines.interpretation_engine.runtime.contracts import RuntimeExecuteResult
from engines.interpretation_engine.placeholder_runtime.registry import PlaceholderRuntimeRegistry

logger = logging.getLogger(__name__)


class PlaceholderRuntime(BaseRuntime):
    """Placeholder Runtime facade implementing the Pack 03 runtime contract."""

    def __init__(
        self,
        *,
        runtime_id: str = "placeholder_runtime",
        registry: PlaceholderRuntimeRegistry | None = None,
    ) -> None:
        """Initialize with optional injected registry."""
        super().__init__(runtime_id=runtime_id)
        self._registry = registry or PlaceholderRuntimeRegistry()

    @property
    def registry(self) -> PlaceholderRuntimeRegistry:
        """Return the injected registry."""
        return self._registry

    def validate(self) -> bool:
        """Validate runtime and registry readiness."""
        if not super().validate():
            return False
        return self._registry.validate()

    def _execute_body(self, context: Any) -> RuntimeExecuteResult:
        """Execute structural stage shell using PackInterpretationContext only."""
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
        logger.info(
            "runtime_stage_execute",
            extra={
                "runtime_id": self.runtime_id,
                "context_id": context.id,
                "source_final_result_id": context.source_final_result_id,
            },
        )
        return RuntimeExecuteResult(
            runtime_id=self.runtime_id,
            success=True,
            payload={
                "context_id": context.id,
                "source_final_result_id": context.source_final_result_id,
                "registry_keys": list(self._registry.list()),
                "stage": self.runtime_id,
            },
            messages=("placeholder_runtime_ok",),
        )
