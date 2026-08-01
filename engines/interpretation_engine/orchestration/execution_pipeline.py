"""Pack 03 Runtime Execution Pipeline.

Flow:
  PackInterpretationContext
    → Registry
    → Interpreter Dispatcher
    → Interpreter Runtime
    → Section Collection
    → Explanation Runtime
    → InterpretationResult

Supports ordered execution, dependency execution, future-async design,
and per-interpreter error isolation.

Infrastructure only. No BaZi business logic.
"""

from __future__ import annotations

import logging
from typing import Any

from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.events.event_bus import LocalEventBus
from engines.interpretation_engine.events.event_model import health_changed_payload
from engines.interpretation_engine.events.event_types import InterpretationEventType
from engines.interpretation_engine.explanation_runtime.runtime import ExplanationRuntime
from engines.interpretation_engine.interpreter_runtime.dispatcher import (
    InterpreterDispatcher,
)
from engines.interpretation_engine.interpreter_runtime.registries.interpreter_registry import (
    InterpreterRegistry,
)
from engines.interpretation_engine.models.interpretation_result import InterpretationResult
from engines.interpretation_engine.models.metadata import Metadata
from engines.interpretation_engine.models.trace_information import TraceInformation
from engines.interpretation_engine.models.version_info import VersionInfo
from engines.interpretation_engine.orchestration.async_executor import (
    AsyncExecutionPlan,
    ExecutionMode,
    FutureAsyncExecutor,
)
from engines.interpretation_engine.orchestration.error_isolation import ErrorIsolator
from engines.interpretation_engine.orchestration.section_collector import (
    SectionCollectionResult,
    SectionCollector,
)
from engines.interpretation_engine.monitoring.monitor import RuntimeMonitor
from engines.interpretation_engine.runtime.base import BaseRuntime
from engines.interpretation_engine.runtime.contracts import (
    HealthStatus,
    RuntimeExecuteResult,
)

logger = logging.getLogger(__name__)


class ExecutionPipeline(BaseRuntime):
    """Interpreter-focused runtime execution pipeline."""

    def __init__(
        self,
        *,
        runtime_id: str = "execution_pipeline",
        interpreter_registry: InterpreterRegistry | None = None,
        dispatcher: InterpreterDispatcher | None = None,
        explanation_runtime: ExplanationRuntime | None = None,
        section_collector: SectionCollector | None = None,
        error_isolator: ErrorIsolator | None = None,
        async_executor: FutureAsyncExecutor | None = None,
        event_bus: LocalEventBus | None = None,
        monitor: RuntimeMonitor | None = None,
        execution_mode: ExecutionMode = ExecutionMode.DEPENDENCY,
        auto_register: bool = True,
    ) -> None:
        """Initialize pipeline with injected DI collaborators."""
        super().__init__(runtime_id=runtime_id)
        self._dispatcher = dispatcher or InterpreterDispatcher()
        self._registry = interpreter_registry or InterpreterRegistry(
            dispatcher=self._dispatcher
        )
        self._explanation = explanation_runtime or ExplanationRuntime()
        self._collector = section_collector or SectionCollector()
        self._isolator = error_isolator or ErrorIsolator()
        self._async_executor = async_executor or FutureAsyncExecutor(
            isolator=self._isolator
        )
        self._event_bus = event_bus or LocalEventBus(bus_id=f"bus_{runtime_id}")
        self._monitor = monitor or RuntimeMonitor(monitor_id=f"monitor_{runtime_id}")
        self._execution_mode = execution_mode
        self._auto_register = auto_register
        self._last_emitted_health: HealthStatus | None = None

    @property
    def registry(self) -> InterpreterRegistry:
        """Return interpreter registry collaborator."""
        return self._registry

    @property
    def dispatcher(self) -> InterpreterDispatcher:
        """Return interpreter dispatcher collaborator."""
        return self._dispatcher

    @property
    def execution_mode(self) -> ExecutionMode:
        """Return configured execution mode."""
        return self._execution_mode

    @property
    def event_bus(self) -> LocalEventBus:
        """Return local event bus collaborator."""
        return self._event_bus

    @property
    def monitor(self) -> RuntimeMonitor:
        """Return runtime monitor collaborator."""
        return self._monitor

    def initialize(self) -> None:
        """Initialize registry, interpreters, and explanation runtime."""
        previous = self.health()
        if self._auto_register and not self._registry.auto_registered:
            self._registry.auto_register(initialize=True)
        else:
            self._registry.initialize_all()
        self._explanation.initialize()
        super().initialize()
        self._emit_health_changed(previous=previous, current=self.health())

    def shutdown(self) -> None:
        """Shutdown explanation runtime and registered interpreters."""
        previous = self.health()
        self._explanation.shutdown()
        self._registry.shutdown_all()
        super().shutdown()
        self._emit_health_changed(previous=previous, current=self.health())

    def validate(self) -> bool:
        """Validate pipeline, registry, and explanation readiness."""
        if not super().validate():
            return False
        report = self._registry.validate_registry()
        if self._auto_register and not report.success:
            return False
        if not self._explanation.validate():
            return False
        try:
            self._resolve_execution_order()
        except Exception:
            return False
        return True

    def _execute_body(self, context: Any) -> RuntimeExecuteResult:
        """Execute the full interpretation runtime pipeline."""
        if not isinstance(context, PackInterpretationContext):
            self._emit_runtime_error(
                error_code="pack_interpretation_context_required",
                detail="invalid_context_type",
                correlation_id=None,
            )
            return RuntimeExecuteResult(
                runtime_id=self.runtime_id,
                success=False,
                messages=("pack_interpretation_context_required",),
            )
        if not context.validate():
            self._emit_runtime_error(
                error_code="pack_interpretation_context_invalid",
                detail="context_validation_failed",
                correlation_id=context.id,
            )
            return RuntimeExecuteResult(
                runtime_id=self.runtime_id,
                success=False,
                messages=("pack_interpretation_context_invalid",),
            )

        previous_health = self.health()
        self._monitor.start_pipeline()
        self._event_bus.emit(
            InterpretationEventType.PIPELINE_STARTED,
            source=self.runtime_id,
            payload={
                "context_id": context.id,
                "pipeline_id": context.pipeline_id,
                "execution_mode": self._execution_mode.value,
            },
            correlation_id=context.id,
        )
        self._emit_health_changed(previous=previous_health, current=HealthStatus.RUNNING)

        # 1) Registry readiness
        registry_report = self._registry.validate_registry()
        if self._auto_register and not registry_report.success:
            self._emit_runtime_error(
                error_code="registry_invalid",
                detail=",".join(registry_report.messages),
                correlation_id=context.id,
            )
            self._event_bus.emit(
                InterpretationEventType.PIPELINE_FINISHED,
                source=self.runtime_id,
                payload={
                    "context_id": context.id,
                    "success": False,
                    "reason": "registry_invalid",
                },
                correlation_id=context.id,
            )
            self._monitor.finish_pipeline(success=False)
            return RuntimeExecuteResult(
                runtime_id=self.runtime_id,
                success=False,
                messages=("registry_invalid",) + registry_report.messages,
                payload={
                    "registry": dict(registry_report.details),
                    "monitoring": self._monitor.snapshot(),
                },
            )

        # 2) Resolve ordered / dependency execution order
        order = self._resolve_execution_order()

        # 3) Interpreter Dispatcher + Interpreter Runtime (error-isolated)
        dispatch_results = self._dispatch_interpreters(context=context, order=order)

        # 4) Section Collection
        collection = self._collector.collect_from_dispatch(dispatch_results)

        # 5) Explanation Runtime (isolated from interpreter failures)
        explanation_result = self._explanation.execute(context)
        explanation_refs: tuple[str, ...] = ()
        explanation_ok = explanation_result.success
        if explanation_ok:
            explanation_refs = tuple(
                explanation_result.payload.get("explanation_refs", ())
            )
        else:
            self._emit_runtime_error(
                error_code="explanation_runtime_failed",
                detail=",".join(explanation_result.messages),
                correlation_id=context.id,
            )

        # 6) Interpretation Result
        interpretation = self._build_result(
            context=context,
            order=order,
            collection=collection,
            explanation_refs=explanation_refs,
            explanation_ok=explanation_ok,
        )

        messages = (
            ("execution_pipeline_ok",)
            + collection.messages
            + explanation_result.messages
        )
        # Pipeline succeeds when context/registry ok; interpreter failures are isolated.
        success = explanation_ok
        if collection.failed_interpreter_ids:
            self._monitor.record_warning(
                "interpreters_failed",
                f"failed={','.join(collection.failed_interpreter_ids)}",
                source=self.runtime_id,
            )
        self._event_bus.emit(
            InterpretationEventType.PIPELINE_FINISHED,
            source=self.runtime_id,
            payload={
                "context_id": context.id,
                "success": success,
                "section_count": len(collection.sections),
                "failed_interpreter_ids": list(collection.failed_interpreter_ids),
            },
            correlation_id=context.id,
        )
        latency = self._monitor.finish_pipeline(success=success)
        logger.info(
            "execution_pipeline_complete",
            extra={
                "context_id": context.id,
                "section_count": len(collection.sections),
                "failed_interpreters": list(collection.failed_interpreter_ids),
                "mode": self._execution_mode.value,
                "pipeline_latency": latency,
            },
        )
        self._emit_health_changed(
            previous=HealthStatus.RUNNING,
            current=HealthStatus.READY,
        )
        return RuntimeExecuteResult(
            runtime_id=self.runtime_id,
            success=success,
            payload={
                "context_id": context.id,
                "execution_order": list(order),
                "execution_mode": self._execution_mode.value,
                "sections": list(collection.sections),
                "failed_interpreter_ids": list(collection.failed_interpreter_ids),
                "explanation_refs": list(explanation_refs),
                "interpretation_result": interpretation,
                "registry_health": self._registry.health().value,
                "event_bus_id": self._event_bus.bus_id,
                "pipeline_latency": latency,
                "monitoring": self._monitor.snapshot(),
            },
            messages=messages,
        )

    def _resolve_execution_order(self) -> tuple[str, ...]:
        """Resolve execution order from registry graphs / dispatcher."""
        if self._execution_mode is ExecutionMode.ORDERED:
            return self._registry.priority_graph_order() or self._dispatcher.list()
        if self._execution_mode is ExecutionMode.FUTURE_ASYNC:
            # Future async still uses dependency order as the plan backbone.
            return self._registry.execution_graph_order() or self._dispatcher.execution_order()
        # DEPENDENCY (default)
        if self._registry.list():
            return self._registry.execution_graph_order()
        return self._dispatcher.execution_order()

    def _dispatch_interpreters(
        self,
        *,
        context: PackInterpretationContext,
        order: tuple[str, ...],
    ) -> tuple[tuple[str, Any], ...]:
        """Dispatch interpreters using async-ready executor + error isolation."""
        callbacks: dict[str, Any] = {}
        for entry_id in order:
            registration = self._registry.lookup(entry_id)
            if registration is None:
                continue

            def _callback(
                *,
                _runtime=registration.runtime,
                _context=context,
                _entry_id=entry_id,
            ) -> Any:
                self._event_bus.emit(
                    InterpretationEventType.BEFORE_INTERPRETER,
                    source=self.runtime_id,
                    payload={
                        "interpreter_id": _entry_id,
                        "context_id": _context.id,
                    },
                    correlation_id=_context.id,
                )
                result = _runtime.execute(_context)
                success = bool(getattr(result, "success", False))
                self._event_bus.emit(
                    InterpretationEventType.AFTER_INTERPRETER,
                    source=self.runtime_id,
                    payload={
                        "interpreter_id": _entry_id,
                        "context_id": _context.id,
                        "success": success,
                    },
                    correlation_id=_context.id,
                )
                if not success:
                    messages = getattr(result, "messages", ())
                    self._emit_runtime_error(
                        error_code="interpreter_execute_failed",
                        detail=f"{_entry_id}:{','.join(messages)}",
                        correlation_id=_context.id,
                        interpreter_id=_entry_id,
                    )
                return result

            callbacks[entry_id] = _callback

        plan = AsyncExecutionPlan(
            mode=self._execution_mode,
            entry_ids=order,
            allow_parallel=self._execution_mode is ExecutionMode.FUTURE_ASYNC,
            attributes={"pipeline_id": self.runtime_id},
        )
        isolated = self._async_executor.execute(plan, callbacks)
        results: list[tuple[str, Any]] = []
        for item in isolated:
            if item.success:
                results.append((item.entry_id, item.value))
            else:
                self._emit_runtime_error(
                    error_code="interpreter_isolated_error",
                    detail=f"{item.entry_id}:{item.error_type}:{item.error_message}",
                    correlation_id=context.id,
                    interpreter_id=item.entry_id,
                )
                results.append(
                    (
                        item.entry_id,
                        {
                            "success": False,
                            "messages": (
                                f"isolated_error:{item.error_type}:{item.error_message}",
                            ),
                        },
                    )
                )
        return tuple(results)

    def _emit_runtime_error(
        self,
        *,
        error_code: str,
        detail: str,
        correlation_id: str | None,
        interpreter_id: str | None = None,
    ) -> None:
        """Publish a runtime_error event and record monitoring error."""
        payload: dict[str, Any] = {
            "error_code": error_code,
            "detail": detail,
            "runtime_id": self.runtime_id,
        }
        if interpreter_id is not None:
            payload["interpreter_id"] = interpreter_id
        self._monitor.record_error(
            error_code,
            detail,
            source=self.runtime_id,
            attributes=payload,
        )
        self._event_bus.emit(
            InterpretationEventType.RUNTIME_ERROR,
            source=self.runtime_id,
            payload=payload,
            correlation_id=correlation_id,
        )

    def _emit_health_changed(
        self,
        *,
        previous: HealthStatus | None,
        current: HealthStatus,
    ) -> None:
        """Publish health_changed when status transitions."""
        if previous is current:
            return
        self._event_bus.emit(
            InterpretationEventType.HEALTH_CHANGED,
            source=self.runtime_id,
            payload=health_changed_payload(
                previous=previous,
                current=current,
                runtime_id=self.runtime_id,
            ),
            correlation_id=self.runtime_id,
        )
        self._last_emitted_health = current

    def _build_result(
        self,
        *,
        context: PackInterpretationContext,
        order: tuple[str, ...],
        collection: SectionCollectionResult,
        explanation_refs: tuple[str, ...],
        explanation_ok: bool,
    ) -> InterpretationResult:
        """Build InterpretationResult from collected sections."""
        metadata = Metadata(
            id=f"meta_{context.id}",
            version_info=VersionInfo(schema_version=context.version or "1.0.0"),
            created_at=context.created_at,
            updated_at=context.updated_at,
            completed_at=context.completed_at,
            attributes={"source": "execution_pipeline"},
        )
        trace = TraceInformation(
            trace_id=f"trace_{context.id}",
            pipeline_id=context.pipeline_id,
            source_final_result_id=context.source_final_result_id,
            stage_ids=(
                "registry",
                "interpreter_dispatcher",
                "interpreter_runtime",
                "section_collection",
                "explanation_runtime",
            ),
            interpreter_ids=order,
            events=tuple(context.trace)
            + (
                "execution_pipeline_complete",
                f"sections:{len(collection.sections)}",
                f"failed:{len(collection.failed_interpreter_ids)}",
            ),
        )
        overall_success = explanation_ok and not collection.failed_interpreter_ids
        messages = collection.messages + (
            ("explanation_ok",) if explanation_ok else ("explanation_failed",)
        )
        return InterpretationResult(
            id=f"ir_{context.id}",
            metadata=metadata,
            trace=trace,
            source_final_result_id=context.source_final_result_id,
            pipeline_id=context.pipeline_id,
            success=overall_success,
            sections=collection.sections,
            explanation_refs=explanation_refs,
            messages=messages,
            attributes={
                "runtime_id": self.runtime_id,
                "execution_mode": self._execution_mode.value,
                "failed_interpreter_ids": list(collection.failed_interpreter_ids),
                "registry_health": self._registry.health().value
                if self._registry.health()
                else HealthStatus.UNKNOWN.value,
            },
        )
