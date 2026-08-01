"""Interpreter dependency model and ordering helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from engines.interpretation_engine.interpreter_framework.interpreter_exception import (
    DependencyError,
)


@dataclass(frozen=True, slots=True)
class InterpreterDependency:
    """One dependency edge for an interpreter."""

    interpreter_id: str
    depends_on: str
    required: bool = True

    def validate(self) -> bool:
        """Validate dependency edge."""
        if not self.interpreter_id or not self.depends_on:
            return False
        if self.interpreter_id == self.depends_on:
            return False
        return True


@dataclass(frozen=True, slots=True)
class DependencyResolution:
    """Resolved dependency plan for a set of interpreters."""

    order: tuple[str, ...]
    missing_required: tuple[str, ...] = ()
    missing_optional: tuple[str, ...] = ()

    def validate(self) -> bool:
        """True when no required dependencies are missing."""
        return not self.missing_required


class DependencyResolver:
    """Resolve required/optional dependencies into an execution order."""

    def resolve(
        self,
        *,
        interpreter_ids: Sequence[str],
        required: Mapping[str, Sequence[str]],
        optional: Mapping[str, Sequence[str]] | None = None,
    ) -> DependencyResolution:
        """Topologically order interpreters; report missing deps."""
        optional = optional or {}
        available = set(interpreter_ids)
        missing_required: list[str] = []
        missing_optional: list[str] = []

        for interpreter_id in interpreter_ids:
            for dep in required.get(interpreter_id, ()):
                if dep not in available:
                    missing_required.append(f"{interpreter_id}->{dep}")
            for dep in optional.get(interpreter_id, ()):
                if dep not in available:
                    missing_optional.append(f"{interpreter_id}->{dep}")

        if missing_required:
            raise DependencyError(
                "missing required dependencies: "
                + ", ".join(sorted(missing_required))
            )

        # Kahn topological sort using required edges only.
        incoming: dict[str, int] = {item: 0 for item in interpreter_ids}
        edges: dict[str, list[str]] = {item: [] for item in interpreter_ids}
        for interpreter_id in interpreter_ids:
            for dep in required.get(interpreter_id, ()):
                # Required deps were validated above to exist in ``available``.
                edges[dep].append(interpreter_id)
                incoming[interpreter_id] += 1

        queue = sorted(
            [item for item, count in incoming.items() if count == 0]
        )
        order: list[str] = []
        while queue:
            node = queue.pop(0)
            order.append(node)
            for child in sorted(edges[node]):
                incoming[child] -= 1
                if incoming[child] == 0:
                    queue.append(child)
                    queue.sort()

        if len(order) != len(interpreter_ids):
            raise DependencyError("cyclic interpreter dependency detected")

        return DependencyResolution(
            order=tuple(order),
            missing_required=(),
            missing_optional=tuple(sorted(missing_optional)),
        )
