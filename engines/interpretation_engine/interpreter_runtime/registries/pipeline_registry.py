"""PipelineRegistry — DI registry for Pack 03 orchestration components.

Registers RuntimePipeline / ExecutionManager and related collaborators.
Dependency Injection only. No singleton. No BaZi logic.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Mapping

from engines.interpretation_engine.interpreter_runtime.registries.graphs import (
    ExecutionGraph,
    GraphNode,
)
from engines.interpretation_engine.interpreter_runtime.registries.interpreter_registry import (
    InterpreterRegistry,
)
from engines.interpretation_engine.interpreter_runtime.registries.runtime_registry import (
    RuntimeRegistry,
)
from engines.interpretation_engine.runtime.contracts import HealthStatus
from engines.interpretation_engine.runtime.registry_base import BaseRegistry, RegistryError

logger = logging.getLogger(__name__)

DEFAULT_PIPELINE_PRIORITIES: Mapping[str, int] = {
    "interpreter_registry": 10,
    "runtime_registry": 20,
    "runtime_pipeline": 30,
    "execution_manager": 40,
}

DEFAULT_PIPELINE_DEPENDENCIES: Mapping[str, tuple[str, ...]] = {
    "interpreter_registry": (),
    "runtime_registry": (),
    "runtime_pipeline": ("runtime_registry",),
    "execution_manager": ("runtime_pipeline",),
}


@dataclass(frozen=True, slots=True)
class PipelineRegistration:
    """Immutable registration for a pipeline/orchestration component."""

    component_id: str
    component: object
    priority: int
    dependencies: tuple[str, ...] = ()
    metadata: Mapping[str, object] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate pipeline registration structural integrity."""
        return bool(self.component_id) and self.component is not None


class PipelineRegistry(BaseRegistry[PipelineRegistration]):
    """DI registry for Pack 03 pipeline orchestration components."""

    def __init__(
        self,
        *,
        execution_graph: ExecutionGraph | None = None,
        interpreter_registry: InterpreterRegistry | None = None,
        runtime_registry: RuntimeRegistry | None = None,
        dependencies: Mapping[str, tuple[str, ...]] | None = None,
        priorities: Mapping[str, int] | None = None,
    ) -> None:
        """Initialize empty pipeline registry with optional injected registries."""
        super().__init__(registry_id="pipeline_registry")
        self._execution_graph = execution_graph or ExecutionGraph()
        self._interpreter_registry = interpreter_registry
        self._runtime_registry = runtime_registry
        self._dependencies = dict(dependencies or DEFAULT_PIPELINE_DEPENDENCIES)
        self._priorities = dict(priorities or DEFAULT_PIPELINE_PRIORITIES)
        self._auto_registered = False

    @property
    def execution_graph(self) -> ExecutionGraph:
        """Return execution graph collaborator."""
        return self._execution_graph

    @property
    def interpreter_registry(self) -> InterpreterRegistry | None:
        """Return injected interpreter registry if present."""
        return self._interpreter_registry

    @property
    def runtime_registry(self) -> RuntimeRegistry | None:
        """Return injected runtime registry if present."""
        return self._runtime_registry

    @property
    def auto_registered(self) -> bool:
        """Return whether auto_register has been applied."""
        return self._auto_registered

    def register_component(self, registration: PipelineRegistration) -> None:
        """Register a pipeline component and rebuild graphs."""
        if not registration.validate():
            raise RegistryError("pipeline_registration_invalid")
        self.register(registration.component_id, registration)
        self._rebuild_graphs()
        logger.info(
            "pipeline_component_registered",
            extra={"component_id": registration.component_id},
        )

    def auto_register(
        self,
        *,
        interpreter_registry: InterpreterRegistry | None = None,
        runtime_registry: RuntimeRegistry | None = None,
        pipeline: object | None = None,
        execution_manager: object | None = None,
        initialize_pipeline: bool = True,
    ) -> tuple[PipelineRegistration, ...]:
        """Auto-register pipeline orchestration components via DI."""
        # Lazy imports avoid circular dependency with orchestration package.
        from engines.interpretation_engine.orchestration.execution_manager import (
            ExecutionManager,
        )
        from engines.interpretation_engine.orchestration.runtime_pipeline import (
            RuntimePipeline,
        )

        interp = interpreter_registry or self._interpreter_registry or InterpreterRegistry()
        runtime = runtime_registry or self._runtime_registry or RuntimeRegistry()
        if not interp.auto_registered:
            interp.auto_register()
        if not runtime.auto_registered:
            runtime.auto_register()

        resolved_pipeline = pipeline if pipeline is not None else RuntimePipeline()
        if not isinstance(resolved_pipeline, RuntimePipeline):
            raise RegistryError("pipeline_component_invalid")
        resolved_manager = (
            execution_manager
            if execution_manager is not None
            else ExecutionManager(resolved_pipeline)
        )
        if not isinstance(resolved_manager, ExecutionManager):
            raise RegistryError("execution_manager_component_invalid")
        if initialize_pipeline:
            resolved_manager.initialize()

        self._interpreter_registry = interp
        self._runtime_registry = runtime

        components: list[tuple[str, object]] = [
            ("interpreter_registry", interp),
            ("runtime_registry", runtime),
            ("runtime_pipeline", resolved_pipeline),
            ("execution_manager", resolved_manager),
        ]
        registrations: list[PipelineRegistration] = []
        for component_id, component in components:
            registration = PipelineRegistration(
                component_id=component_id,
                component=component,
                priority=self._priorities.get(component_id, 100),
                dependencies=tuple(self._dependencies.get(component_id, ())),
                metadata={"auto_registered": True},
            )
            self.register_component(registration)
            registrations.append(registration)

        self._auto_registered = True
        return tuple(registrations)

    def execution_order(self) -> tuple[str, ...]:
        """Return pipeline component execution/bootstrap order."""
        return self._execution_graph.execution_order()

    def priority_order(self) -> tuple[str, ...]:
        """Return pipeline component priority order."""
        return self._execution_graph.priority_order()

    def validate_registry(self) -> bool:
        """Validate pipeline registrations and nested registries."""
        if not self.validate():
            return False
        if not self._execution_graph.validate():
            return False
        if self._interpreter_registry is not None:
            report = self._interpreter_registry.validate_registry()
            if not report.success:
                return False
        if self._runtime_registry is not None and not self._runtime_registry.validate_registry():
            return False
        return True

    def health(self) -> HealthStatus:
        """Aggregate health from nested registries and execution manager."""
        statuses: list[HealthStatus] = []
        if self._interpreter_registry is not None:
            statuses.append(self._interpreter_registry.health())
        if self._runtime_registry is not None:
            statuses.append(self._runtime_registry.health())
        manager_entry = self.lookup("execution_manager")
        if manager_entry is not None and hasattr(manager_entry.component, "health"):
            statuses.append(manager_entry.component.health())
        if not statuses:
            return HealthStatus.UNKNOWN
        if any(status is HealthStatus.FAILED for status in statuses):
            return HealthStatus.FAILED
        if any(status is HealthStatus.RUNNING for status in statuses):
            return HealthStatus.RUNNING
        if all(status is HealthStatus.DISABLED for status in statuses):
            return HealthStatus.DISABLED
        if all(status is HealthStatus.READY for status in statuses):
            return HealthStatus.READY
        if any(status is HealthStatus.UNKNOWN for status in statuses):
            return HealthStatus.UNKNOWN
        return HealthStatus.READY

    def health_map(self) -> dict[str, str]:
        """Return nested health snapshot as strings."""
        data: dict[str, str] = {"pipeline_registry": self.health().value}
        if self._interpreter_registry is not None:
            data["interpreter_registry"] = self._interpreter_registry.health().value
            for key, value in self._interpreter_registry.health_map().items():
                data[f"interpreter:{key}"] = value.value
        if self._runtime_registry is not None:
            data["runtime_registry"] = self._runtime_registry.health().value
            for key, value in self._runtime_registry.health_map().items():
                data[f"runtime:{key}"] = value.value
        return data

    def _rebuild_graphs(self) -> None:
        """Rebuild graphs from current pipeline registrations."""
        nodes = []
        for component_id in self.list():
            entry = self.lookup(component_id)
            if entry is None:
                continue
            nodes.append(
                GraphNode(
                    node_id=entry.component_id,
                    priority=entry.priority,
                    dependencies=entry.dependencies,
                    metadata=dict(entry.metadata),
                )
            )
        self._execution_graph.rebuild_from_nodes(tuple(nodes))
