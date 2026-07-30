"""Dependency resolution for analysis modules."""

from __future__ import annotations

import logging
from collections import defaultdict
from graphlib import CycleError, TopologicalSorter
from typing import Iterable, Mapping, Sequence

from engines.analysis_engine.runtime.constants import (
    CANONICAL_STAGES,
    DEFAULT_DEPENDENCIES,
)
from engines.analysis_engine.runtime.exceptions import (
    CompatibilityError,
    RegistrationError,
    StateError,
)

logger = logging.getLogger(__name__)


class DependencyResolver:
    """Resolve module dependencies and enforce canonical execution order."""

    def __init__(
        self,
        *,
        canonical_order: Sequence[str] | None = None,
        default_dependencies: Mapping[str, Sequence[str]] | None = None,
    ) -> None:
        self._canonical_order = tuple(canonical_order or CANONICAL_STAGES)
        self._default_dependencies = {
            key: tuple(value)
            for key, value in (
                default_dependencies or DEFAULT_DEPENDENCIES
            ).items()
        }
        self._graph: dict[str, set[str]] = defaultdict(set)
        for stage_id, deps in self._default_dependencies.items():
            self._graph[stage_id] = set(deps)

    def register(
        self,
        stage_id: str,
        dependencies: Sequence[str] | None = None,
    ) -> None:
        """Register or update dependencies for a stage."""
        if stage_id not in self._canonical_order:
            raise RegistrationError(
                f"Unknown stage_id outside canonical pipeline: {stage_id}",
                stage_id=stage_id,
            )
        deps = (
            tuple(dependencies)
            if dependencies is not None
            else self._default_dependencies.get(stage_id, ())
        )
        self._validate_dependency_set(stage_id, deps)
        self._graph[stage_id] = set(deps)
        logger.debug(
            "dependency_registered",
            extra={"stage_id": stage_id, "dependencies": list(deps)},
        )

    def dependencies_of(self, stage_id: str) -> tuple[str, ...]:
        """Return declared dependencies for a stage."""
        return tuple(sorted(self._graph.get(stage_id, set())))

    def resolve_order(
        self,
        registered_stages: Iterable[str],
    ) -> tuple[str, ...]:
        """Return deterministic execution order for registered stages.

        Canonical pipeline order is preferred. Topological validation ensures
        no cycles. Unregistered canonical stages are omitted.
        """
        registered = set(registered_stages)
        if not registered:
            return ()

        unknown = registered - set(self._canonical_order)
        if unknown:
            raise RegistrationError(
                f"Registered unknown stages: {sorted(unknown)}",
                details={"unknown": sorted(unknown)},
            )

        subgraph = {
            stage_id: set(self._graph.get(stage_id, set())) & registered
            for stage_id in registered
        }
        try:
            TopologicalSorter(subgraph).prepare()
        except CycleError as exc:
            raise CompatibilityError(
                f"Circular module dependency detected: {exc}",
                details={"registered": sorted(registered)},
            ) from exc

        # Preserve canonical sequential order (V1.0: no reordering for speed).
        order = tuple(
            stage_id
            for stage_id in self._canonical_order
            if stage_id in registered
        )
        self._assert_prerequisites_precede(order)
        return order

    def assert_ready(
        self,
        stage_id: str,
        published_stages: Iterable[str],
    ) -> None:
        """Fail if dependencies are not published."""
        published = set(published_stages)
        missing = [
            dep
            for dep in self.dependencies_of(stage_id)
            if dep not in published
        ]
        if missing:
            raise StateError(
                f"Stage '{stage_id}' is not ready; missing {missing}",
                stage_id=stage_id,
                details={"missing": missing},
            )

    def _validate_dependency_set(
        self,
        stage_id: str,
        dependencies: Sequence[str],
    ) -> None:
        stage_index = {
            name: index for index, name in enumerate(self._canonical_order)
        }
        for dep in dependencies:
            if dep not in stage_index:
                raise RegistrationError(
                    f"Dependency '{dep}' is not a canonical stage",
                    stage_id=stage_id,
                )
            if stage_index[dep] >= stage_index[stage_id]:
                raise RegistrationError(
                    f"Dependency '{dep}' must precede stage '{stage_id}'",
                    stage_id=stage_id,
                )

    def _assert_prerequisites_precede(self, order: Sequence[str]) -> None:
        positions = {stage_id: index for index, stage_id in enumerate(order)}
        for stage_id in order:
            for dep in self.dependencies_of(stage_id):
                if dep not in positions:
                    continue
                if positions[dep] >= positions[stage_id]:
                    raise CompatibilityError(
                        f"Dependency order violation: {dep} before {stage_id}",
                        stage_id=stage_id,
                    )
