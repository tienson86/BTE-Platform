"""Abstract BaseInterpreter for Pack 03 business interpreters.

Extends frozen InterpreterSkeletonRuntime. Adds framework lifecycle hooks,
standard result shaping, and capability metadata — no BaZi logic.
"""

from __future__ import annotations

import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any

from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.interpreter_framework.interpreter_builder import (
    InterpretationSectionBuilder,
)
from engines.interpretation_engine.interpreter_framework.interpreter_capability import (
    InterpreterCapability,
)
from engines.interpretation_engine.interpreter_framework.interpreter_exception import (
    ExecutionError,
    ValidationError,
)
from engines.interpretation_engine.interpreter_framework.interpreter_metadata import (
    InterpreterMetadata,
)
from engines.interpretation_engine.interpreter_framework.interpreter_result import (
    ExecutionStatistics,
    FrameworkInterpreterResult,
)
from engines.interpretation_engine.interpreter_framework.interpreter_trace import (
    InterpreterTrace,
)
from engines.interpretation_engine.interpreter_framework.interpreter_validator import (
    InterpreterValidator,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.base_skeleton import (
    InterpreterSkeletonRuntime,
)
from engines.interpretation_engine.runtime.contracts import (
    HealthStatus,
    RuntimeExecuteResult,
)

logger = logging.getLogger(__name__)


def _utc_now() -> str:
    """Return UTC ISO-8601 timestamp."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class BaseInterpreter(InterpreterSkeletonRuntime, ABC):
    """Abstract framework base for Pack 03 interpreters.

    Standard lifecycle (inherited + hooks):
    initialize / validate / before_execute / execute / after_execute /
    shutdown / health / metrics

    Subclasses implement ``interpret`` only (no BaZi logic in this base).
    """

    category: str = "framework"
    description: str = ""
    dependencies: tuple[str, ...] = ()
    optional_dependencies: tuple[str, ...] = ()
    supported_inputs: tuple[str, ...] = ("PackInterpretationContext", "FinalResult")
    supported_outputs: tuple[str, ...] = ("InterpretationSection",)
    default_priority: int = 100

    def __init__(
        self,
        *,
        runtime_id: str | None = None,
        validator: InterpreterValidator | None = None,
        builder: InterpretationSectionBuilder | None = None,
        priority: int | None = None,
    ) -> None:
        """Initialize framework interpreter with DI hooks."""
        super().__init__(runtime_id=runtime_id)
        self.validator = validator or InterpreterValidator()
        self._builder_seed = builder
        self.priority = self.default_priority if priority is None else priority
        self._last_trace = InterpreterTrace()
        self._before_called = False
        self._after_called = False

    def capability(self) -> InterpreterCapability:
        """Return capability declaration for this interpreter."""
        return InterpreterCapability(
            interpreter_id=self.interpreter_id,
            category=self.category,
            priority=self.priority,
            dependencies=self.dependencies,
            optional_dependencies=self.optional_dependencies,
            supported_inputs=self.supported_inputs,
            supported_outputs=self.supported_outputs,
            version=self.version,
            description=self.description,
        )

    def metadata(self) -> InterpreterMetadata:
        """Return runtime metadata for this interpreter."""
        return InterpreterMetadata(
            interpreter_id=self.interpreter_id,
            version=self.version,
            category=self.category,
            description=self.description,
        )

    def new_builder(self) -> InterpretationSectionBuilder:
        """Create a fresh InterpretationSectionBuilder."""
        if self._builder_seed is not None:
            # Seed is a template instance; always start a new builder.
            return InterpretationSectionBuilder()
        return InterpretationSectionBuilder()

    def before_execute(self, context: PackInterpretationContext) -> None:
        """Hook invoked before ``interpret`` (override as needed)."""
        self._before_called = True
        self._last_trace = self._last_trace.with_event(
            "before_execute",
            detail=context.id,
        )

    def after_execute(
        self,
        context: PackInterpretationContext,
        result: FrameworkInterpreterResult | None,
        *,
        error: BaseException | None = None,
    ) -> None:
        """Hook invoked after ``interpret`` (override as needed)."""
        self._after_called = True
        detail = "error" if error is not None else "ok"
        self._last_trace = self._last_trace.with_event(
            "after_execute",
            detail=detail,
            attributes={"context_id": context.id},
        )

    def health(self) -> HealthStatus:
        """Return runtime health (frozen BaseRuntime behavior)."""
        return super().health()

    def metrics(self):
        """Return runtime metrics snapshot."""
        return super().metrics()

    @abstractmethod
    def interpret(
        self, context: PackInterpretationContext
    ) -> FrameworkInterpreterResult:
        """Execute interpreter business orchestration (no BaZi in base).

        Subclasses must build InterpretationSection via InterpretationSectionBuilder.
        """

    def _execute_body(self, context: Any) -> RuntimeExecuteResult:
        """Framework execute body with validation and lifecycle hooks."""
        self._before_called = False
        self._after_called = False
        self._last_trace = InterpreterTrace().with_event("execute_start")

        try:
            pack_context = self.validator.require_input(context)
        except ValidationError as exc:
            return RuntimeExecuteResult(
                runtime_id=self.runtime_id,
                success=False,
                messages=(exc.code, str(exc)),
            )

        self.validator.require_capability(self.capability())
        started = time.perf_counter()
        started_at = _utc_now()
        framework_result: FrameworkInterpreterResult | None = None
        error: BaseException | None = None

        try:
            self.before_execute(pack_context)
            framework_result = self.interpret(pack_context)
            self.validator.require_result(framework_result)
        except ValidationError as exc:
            error = exc
            return RuntimeExecuteResult(
                runtime_id=self.runtime_id,
                success=False,
                messages=(exc.code, str(exc)),
            )
        except ExecutionError as exc:
            error = exc
            return RuntimeExecuteResult(
                runtime_id=self.runtime_id,
                success=False,
                messages=(exc.code, str(exc)),
            )
        except Exception as exc:  # noqa: BLE001 - framework boundary
            error = exc
            logger.exception(
                "base_interpreter_interpret_failed",
                extra={
                    "interpreter_id": self.interpreter_id,
                    "error": type(exc).__name__,
                },
            )
            return RuntimeExecuteResult(
                runtime_id=self.runtime_id,
                success=False,
                messages=(
                    "execution_error",
                    f"interpret failed: {type(exc).__name__}: {exc}",
                ),
            )
        finally:
            finished_at = _utc_now()
            duration_ms = (time.perf_counter() - started) * 1000.0
            self.after_execute(pack_context, framework_result, error=error)
            if framework_result is not None and error is None:
                # Attach framework statistics/trace when subclass omitted them.
                stats = framework_result.statistics
                if not stats.started_at:
                    framework_result = FrameworkInterpreterResult(
                        section=framework_result.section,
                        metadata=framework_result.metadata,
                        trace=framework_result.trace
                        if framework_result.trace.events
                        else self._last_trace,
                        confidence=framework_result.confidence,
                        warnings=framework_result.warnings,
                        statistics=ExecutionStatistics(
                            started_at=started_at,
                            finished_at=finished_at,
                            duration_ms=duration_ms,
                            attributes=dict(stats.attributes),
                        ),
                        success=framework_result.success,
                        messages=framework_result.messages,
                        attributes=dict(framework_result.attributes),
                    )

        assert framework_result is not None
        payload = framework_result.to_payload()
        payload["context_id"] = pack_context.id
        payload["trace"] = self._last_trace.to_dict()
        logger.info(
            "base_interpreter_execute",
            extra={
                "interpreter_id": self.interpreter_id,
                "context_id": pack_context.id,
                "success": framework_result.success,
            },
        )
        return RuntimeExecuteResult(
            runtime_id=self.runtime_id,
            success=framework_result.success,
            payload=payload,
            messages=framework_result.messages
            or (f"{self.interpreter_id}_ok",),
        )


class EmptyFrameworkInterpreter(BaseInterpreter):
    """Concrete framework interpreter that returns an empty section.

    Useful for factory/lifecycle tests. No BaZi logic.
    """

    interpreter_id = "empty_framework_interpreter"
    section_type = "framework"
    version = "1.0.0"
    category = "framework"
    description = "Empty framework interpreter"
    default_priority = 1000

    def interpret(
        self, context: PackInterpretationContext
    ) -> FrameworkInterpreterResult:
        """Build an empty InterpretationSection via the standard builder."""
        section = (
            self.new_builder()
            .for_interpreter(
                interpreter_id=self.interpreter_id,
                section_type=self.section_type,
                context_id=context.id,
            )
            .with_title_ref("framework.empty")
            .with_messages(("empty_framework_interpreter_ok",))
            .with_attributes({"skeleton": False, "framework": True})
            .build()
        )
        return FrameworkInterpreterResult(
            section=section,
            metadata=self.metadata(),
            trace=InterpreterTrace().with_event("interpret"),
            confidence=1.0,
            warnings=(),
            success=True,
            messages=("empty_framework_interpreter_ok",),
        )
