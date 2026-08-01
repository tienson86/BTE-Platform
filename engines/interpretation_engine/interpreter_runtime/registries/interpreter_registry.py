"""InterpreterRegistry — integrates all Pack 03 interpreter skeletons.

Features:
- auto registration
- dependency / priority / execution graphs
- validation
- health

Dependency Injection only. No singleton. No BaZi logic.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Mapping, Sequence

from engines.interpretation_engine.interpreter_runtime.dispatcher import (
    InterpreterDispatcher,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.base_skeleton import (
    InterpreterSkeletonRuntime,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.catalog import (
    INTERPRETER_SKELETON_CLASSES,
    INTERPRETER_SKELETON_IDS,
    create_all_interpreter_skeletons,
)
from engines.interpretation_engine.interpreter_runtime.registries.graphs import (
    ExecutionGraph,
    GraphNode,
)
from engines.interpretation_engine.runtime.contracts import HealthStatus
from engines.interpretation_engine.runtime.registry_base import BaseRegistry, RegistryError

logger = logging.getLogger(__name__)

# Structural dependencies only (framework ordering — not BaZi rules).
DEFAULT_INTERPRETER_DEPENDENCIES: Mapping[str, tuple[str, ...]] = {
    "strength_interpreter": (),
    "season_interpreter": (),
    "temperature_interpreter": ("season_interpreter",),
    "pattern_interpreter": ("strength_interpreter", "season_interpreter"),
    "useful_god_interpreter": ("strength_interpreter", "pattern_interpreter"),
    "combination_interpreter": ("pattern_interpreter",),
    "conflict_interpreter": ("combination_interpreter",),
    "ten_gods_interpreter": ("strength_interpreter",),
    "shensha_interpreter": ("ten_gods_interpreter",),
    "luck_interpreter": ("useful_god_interpreter", "ten_gods_interpreter"),
    "scoring_interpreter": (
        "strength_interpreter",
        "pattern_interpreter",
        "useful_god_interpreter",
    ),
    "summary_interpreter": ("scoring_interpreter", "luck_interpreter"),
}

DEFAULT_INTERPRETER_PRIORITIES: Mapping[str, int] = {
    "strength_interpreter": 10,
    "season_interpreter": 20,
    "temperature_interpreter": 30,
    "pattern_interpreter": 40,
    "useful_god_interpreter": 50,
    "combination_interpreter": 60,
    "conflict_interpreter": 70,
    "ten_gods_interpreter": 80,
    "shensha_interpreter": 90,
    "luck_interpreter": 100,
    "scoring_interpreter": 110,
    "summary_interpreter": 120,
}


@dataclass(frozen=True, slots=True)
class InterpreterRegistration:
    """Immutable registration record for an interpreter runtime."""

    interpreter_id: str
    runtime: InterpreterSkeletonRuntime
    priority: int
    dependencies: tuple[str, ...] = ()
    section_type: str = ""
    version: str = ""
    metadata: Mapping[str, object] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate registration structural integrity."""
        if not self.interpreter_id or self.runtime is None:
            return False
        return self.runtime.interpreter_id == self.interpreter_id


@dataclass(frozen=True, slots=True)
class RegistryValidationReport:
    """Immutable validation report for InterpreterRegistry."""

    success: bool
    messages: tuple[str, ...] = ()
    details: Mapping[str, object] = field(default_factory=dict)


class InterpreterRegistry(BaseRegistry[InterpreterRegistration]):
    """DI registry integrating every Pack 03 interpreter skeleton."""

    def __init__(
        self,
        *,
        execution_graph: ExecutionGraph | None = None,
        dispatcher: InterpreterDispatcher | None = None,
        dependencies: Mapping[str, tuple[str, ...]] | None = None,
        priorities: Mapping[str, int] | None = None,
    ) -> None:
        """Initialize empty interpreter registry with injected collaborators."""
        super().__init__(registry_id="interpreter_registry")
        self._execution_graph = execution_graph or ExecutionGraph()
        self._dispatcher = dispatcher
        self._dependencies = dict(dependencies or DEFAULT_INTERPRETER_DEPENDENCIES)
        self._priorities = dict(priorities or DEFAULT_INTERPRETER_PRIORITIES)
        self._auto_registered = False

    @property
    def execution_graph(self) -> ExecutionGraph:
        """Return execution graph collaborator."""
        return self._execution_graph

    @property
    def dispatcher(self) -> InterpreterDispatcher | None:
        """Return optional injected dispatcher."""
        return self._dispatcher

    @property
    def auto_registered(self) -> bool:
        """Return whether auto_register has been applied."""
        return self._auto_registered

    def register_interpreter(self, registration: InterpreterRegistration) -> None:
        """Register an interpreter registration record and rebuild graphs."""
        if not registration.validate():
            raise RegistryError("interpreter_registration_invalid")
        self.register(registration.interpreter_id, registration)
        self._rebuild_graphs()
        self._sync_dispatcher(registration)
        logger.info(
            "interpreter_registered",
            extra={
                "interpreter_id": registration.interpreter_id,
                "priority": registration.priority,
            },
        )

    def unregister_interpreter(self, interpreter_id: str) -> None:
        """Unregister an interpreter and rebuild graphs."""
        self.unregister(interpreter_id)
        if self._dispatcher is not None:
            self._dispatcher.unregister(interpreter_id)
        self._rebuild_graphs()

    def auto_register(
        self,
        *,
        skeletons: Sequence[InterpreterSkeletonRuntime] | None = None,
        initialize: bool = True,
    ) -> tuple[InterpreterRegistration, ...]:
        """Auto-register all standard interpreter skeletons.

        Creates instances via DI factory when skeletons are not injected.
        """
        instances = (
            tuple(skeletons)
            if skeletons is not None
            else create_all_interpreter_skeletons()
        )
        registrations: list[InterpreterRegistration] = []
        for skeleton in instances:
            if initialize:
                skeleton.initialize()
            registration = InterpreterRegistration(
                interpreter_id=skeleton.interpreter_id,
                runtime=skeleton,
                priority=self._priorities.get(skeleton.interpreter_id, 100),
                dependencies=tuple(
                    self._dependencies.get(skeleton.interpreter_id, ())
                ),
                section_type=skeleton.section_type,
                version=skeleton.version,
                metadata={"skeleton": True, "auto_registered": True},
            )
            self.register_interpreter(registration)
            registrations.append(registration)
        self._auto_registered = True
        logger.info(
            "interpreter_auto_register_complete",
            extra={"count": len(registrations)},
        )
        return tuple(registrations)

    def dependency_graph_order(self) -> tuple[str, ...]:
        """Return dependency topological order."""
        return self._execution_graph.dependency_graph.topological_order()

    def priority_graph_order(self) -> tuple[str, ...]:
        """Return priority order."""
        return self._execution_graph.priority_order()

    def execution_graph_order(self) -> tuple[str, ...]:
        """Return execution graph order."""
        return self._execution_graph.execution_order()

    def validate_registry(self) -> RegistryValidationReport:
        """Validate registrations, graphs, and expected interpreter set."""
        messages: list[str] = []
        if not self.validate():
            return RegistryValidationReport(
                success=False,
                messages=("registry_base_invalid",),
            )

        registered = set(self.list())
        expected = set(INTERPRETER_SKELETON_IDS)
        missing = tuple(sorted(expected - registered))
        unexpected = tuple(sorted(registered - expected))
        if missing and self._auto_registered:
            messages.append("interpreters_missing")
        if unexpected:
            messages.append("interpreters_unexpected")

        if not self._execution_graph.validate():
            messages.append("execution_graph_invalid")
        missing_deps = self._execution_graph.dependency_graph.missing_dependencies()
        if missing_deps:
            messages.append("dependencies_missing")

        for entry_id in self.list():
            entry = self.lookup(entry_id)
            if entry is None or not entry.validate():
                messages.append(f"registration_invalid:{entry_id}")

        success = not messages
        if success:
            messages.append("interpreter_registry_ok")

        execution_order: list[str] = []
        if not missing_deps and not self._execution_graph.dependency_graph.has_cycle():
            execution_order = list(self.execution_graph_order())

        return RegistryValidationReport(
            success=success,
            messages=tuple(messages),
            details={
                "registered": list(self.list()),
                "missing": list(missing),
                "unexpected": list(unexpected),
                "missing_dependencies": list(missing_deps),
                "execution_order": execution_order,
            },
        )

    def health(self) -> HealthStatus:
        """Aggregate health across registered interpreter runtimes."""
        statuses = [item.runtime.health() for item in self._registrations()]
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
        """Return per-interpreter health map."""
        return {
            entry.interpreter_id: entry.runtime.health()
            for entry in self._registrations()
        }

    def initialize_all(self) -> None:
        """Initialize all registered interpreter runtimes."""
        for entry in self._registrations():
            entry.runtime.initialize()

    def shutdown_all(self) -> None:
        """Shutdown all registered interpreter runtimes."""
        for entry in reversed(self._registrations()):
            entry.runtime.shutdown()

    def _registrations(self) -> tuple[InterpreterRegistration, ...]:
        """Return registrations in execution order when possible."""
        try:
            order = self.execution_graph_order()
        except RegistryError:
            order = self.list()
        result: list[InterpreterRegistration] = []
        for entry_id in order:
            entry = self.lookup(entry_id)
            if entry is not None:
                result.append(entry)
        return tuple(result)

    def _rebuild_graphs(self) -> None:
        """Rebuild execution graphs from current registrations."""
        nodes: list[GraphNode] = []
        for entry_id in self.list():
            entry = self.lookup(entry_id)
            if entry is None:
                continue
            nodes.append(
                GraphNode(
                    node_id=entry.interpreter_id,
                    priority=entry.priority,
                    dependencies=entry.dependencies,
                    metadata={
                        "section_type": entry.section_type,
                        "version": entry.version,
                    },
                )
            )
        self._execution_graph.rebuild_from_nodes(tuple(nodes))

    def _sync_dispatcher(self, registration: InterpreterRegistration) -> None:
        """Optionally sync a registration into the injected dispatcher."""
        if self._dispatcher is None:
            return

        def _handler(
            context: object,
            *,
            _runtime: InterpreterSkeletonRuntime = registration.runtime,
        ) -> object:
            return _runtime.execute(context)

        self._dispatcher.register(
            registration.interpreter_id,
            _handler,
            priority=registration.priority,
            dependencies=registration.dependencies,
            metadata={
                "section_type": registration.section_type,
                "version": registration.version,
            },
        )


# Keep class catalog import reachable for audits.
_SKELETON_CLASS_COUNT = len(INTERPRETER_SKELETON_CLASSES)
