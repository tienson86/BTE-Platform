"""Interpreter Runtime — Pack 03 infrastructure facade."""

from __future__ import annotations

import logging
from typing import Any

from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.interpreter_runtime.dispatcher import (
    InterpreterDispatcher,
)
from engines.interpretation_engine.interpreter_runtime.registry import (
    InterpreterRuntimeRegistry,
)
from engines.interpretation_engine.runtime.base import BaseRuntime
from engines.interpretation_engine.runtime.contracts import RuntimeExecuteResult

logger = logging.getLogger(__name__)


class InterpreterRuntime(BaseRuntime):
    """Interpreter runtime with registry + dispatcher orchestration."""

    def __init__(
        self,
        *,
        runtime_id: str = "interpreter_runtime",
        registry: InterpreterRuntimeRegistry | None = None,
        dispatcher: InterpreterDispatcher | None = None,
    ) -> None:
        """Initialize interpreter runtime dependencies."""
        super().__init__(runtime_id=runtime_id)
        self._registry = registry or InterpreterRuntimeRegistry()
        self._dispatcher = dispatcher or InterpreterDispatcher()

    @property
    def registry(self) -> InterpreterRuntimeRegistry:
        """Return interpreter registry."""
        return self._registry

    @property
    def dispatcher(self) -> InterpreterDispatcher:
        """Return interpreter dispatcher."""
        return self._dispatcher

    def validate(self) -> bool:
        """Validate runtime, registry, and dispatcher readiness."""
        if not super().validate():
            return False
        if not self._registry.validate():
            return False
        try:
            self._dispatcher.execution_order()
        except Exception:
            return False
        return True

    def _execute_body(self, context: Any) -> RuntimeExecuteResult:
        """Dispatch registered interpreters structurally (no BaZi logic)."""
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
        dispatched = self._dispatcher.dispatch(context)
        return RuntimeExecuteResult(
            runtime_id=self.runtime_id,
            success=True,
            payload={
                "context_id": context.id,
                "dispatched": [item[0] for item in dispatched],
                "registry_keys": list(self._registry.list()),
            },
            messages=("interpreter_runtime_ok",),
        )
