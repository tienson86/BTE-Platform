"""RuntimeRegistry — DI registry for Pack 03 stage runtimes.

Registers Interpreter / Sentence / Template / Placeholder / Explanation runtimes.
Dependency Injection only. No singleton. No BaZi logic.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Mapping

from engines.interpretation_engine.explanation_runtime.runtime import ExplanationRuntime
from engines.interpretation_engine.interpreter_runtime.registries.graphs import (
    ExecutionGraph,
    GraphNode,
)
from engines.interpretation_engine.interpreter_runtime.runtime import InterpreterRuntime
from engines.interpretation_engine.placeholder_runtime.runtime import PlaceholderRuntime
from engines.interpretation_engine.runtime.base import BaseRuntime
from engines.interpretation_engine.runtime.contracts import HealthStatus
from engines.interpretation_engine.runtime.registry_base import BaseRegistry, RegistryError
from engines.interpretation_engine.sentence_runtime.runtime import SentenceRuntime
from engines.interpretation_engine.template_runtime.runtime import TemplateRuntime

logger = logging.getLogger(__name__)

DEFAULT_RUNTIME_DEPENDENCIES: Mapping[str, tuple[str, ...]] = {
    "interpreter_runtime": (),
    "sentence_runtime": ("interpreter_runtime",),
    "template_runtime": ("sentence_runtime",),
    "placeholder_runtime": ("template_runtime",),
    "explanation_runtime": ("placeholder_runtime",),
}

DEFAULT_RUNTIME_PRIORITIES: Mapping[str, int] = {
    "interpreter_runtime": 10,
    "sentence_runtime": 20,
    "template_runtime": 30,
    "placeholder_runtime": 40,
    "explanation_runtime": 50,
}


@dataclass(frozen=True, slots=True)
class RuntimeRegistration:
    """Immutable registration for a stage runtime."""

    runtime_id: str
    runtime: BaseRuntime
    priority: int
    dependencies: tuple[str, ...] = ()
    metadata: Mapping[str, object] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate runtime registration structural integrity."""
        if not self.runtime_id or self.runtime is None:
            return False
        return self.runtime.runtime_id == self.runtime_id


class RuntimeRegistry(BaseRegistry[RuntimeRegistration]):
    """DI registry for Pack 03 pipeline stage runtimes."""

    def __init__(
        self,
        *,
        execution_graph: ExecutionGraph | None = None,
        dependencies: Mapping[str, tuple[str, ...]] | None = None,
        priorities: Mapping[str, int] | None = None,
    ) -> None:
        """Initialize empty runtime registry."""
        super().__init__(registry_id="runtime_registry")
        self._execution_graph = execution_graph or ExecutionGraph()
        self._dependencies = dict(dependencies or DEFAULT_RUNTIME_DEPENDENCIES)
        self._priorities = dict(priorities or DEFAULT_RUNTIME_PRIORITIES)
        self._auto_registered = False

    @property
    def execution_graph(self) -> ExecutionGraph:
        """Return execution graph collaborator."""
        return self._execution_graph

    @property
    def auto_registered(self) -> bool:
        """Return whether auto_register has been applied."""
        return self._auto_registered

    def register_runtime(self, registration: RuntimeRegistration) -> None:
        """Register a stage runtime and rebuild graphs."""
        if not registration.validate():
            raise RegistryError("runtime_registration_invalid")
        self.register(registration.runtime_id, registration)
        self._rebuild_graphs()
        logger.info(
            "runtime_registered",
            extra={"runtime_id": registration.runtime_id},
        )

    def auto_register(
        self,
        *,
        interpreter_runtime: InterpreterRuntime | None = None,
        sentence_runtime: SentenceRuntime | None = None,
        template_runtime: TemplateRuntime | None = None,
        placeholder_runtime: PlaceholderRuntime | None = None,
        explanation_runtime: ExplanationRuntime | None = None,
        initialize: bool = True,
    ) -> tuple[RuntimeRegistration, ...]:
        """Auto-register the five Pack 03 stage runtimes."""
        stages: tuple[BaseRuntime, ...] = (
            interpreter_runtime or InterpreterRuntime(),
            sentence_runtime or SentenceRuntime(),
            template_runtime or TemplateRuntime(),
            placeholder_runtime or PlaceholderRuntime(),
            explanation_runtime or ExplanationRuntime(),
        )
        registrations: list[RuntimeRegistration] = []
        for stage in stages:
            if initialize:
                stage.initialize()
            registration = RuntimeRegistration(
                runtime_id=stage.runtime_id,
                runtime=stage,
                priority=self._priorities.get(stage.runtime_id, 100),
                dependencies=tuple(self._dependencies.get(stage.runtime_id, ())),
                metadata={"auto_registered": True},
            )
            self.register_runtime(registration)
            registrations.append(registration)
        self._auto_registered = True
        return tuple(registrations)

    def execution_order(self) -> tuple[str, ...]:
        """Return stage runtime execution order."""
        return self._execution_graph.execution_order()

    def priority_order(self) -> tuple[str, ...]:
        """Return stage runtime priority order."""
        return self._execution_graph.priority_order()

    def validate_registry(self) -> bool:
        """Validate registrations and execution graph."""
        if not self.validate():
            return False
        return self._execution_graph.validate()

    def health(self) -> HealthStatus:
        """Aggregate health of registered stage runtimes."""
        statuses = [
            registration.runtime.health()
            for registration in self._ordered_registrations()
        ]
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

    def health_map(self) -> dict[str, HealthStatus]:
        """Return per-runtime health map."""
        return {
            item.runtime_id: item.runtime.health()
            for item in self._ordered_registrations()
        }

    def shutdown_all(self) -> None:
        """Shutdown all registered runtimes in reverse execution order."""
        for registration in reversed(self._ordered_registrations()):
            registration.runtime.shutdown()

    def _ordered_registrations(self) -> tuple[RuntimeRegistration, ...]:
        """Return registrations in execution order when possible."""
        try:
            order = self.execution_order()
        except RegistryError:
            order = self.list()
        result: list[RuntimeRegistration] = []
        for runtime_id in order:
            entry = self.lookup(runtime_id)
            if entry is not None:
                result.append(entry)
        return tuple(result)

    def _rebuild_graphs(self) -> None:
        """Rebuild graphs from current runtime registrations."""
        nodes = []
        for runtime_id in self.list():
            entry = self.lookup(runtime_id)
            if entry is None:
                continue
            nodes.append(
                GraphNode(
                    node_id=entry.runtime_id,
                    priority=entry.priority,
                    dependencies=entry.dependencies,
                    metadata=dict(entry.metadata),
                )
            )
        self._execution_graph.rebuild_from_nodes(tuple(nodes))
