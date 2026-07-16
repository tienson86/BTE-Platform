"""
BTE Platform - Engine Dependency Manager.

Quản lý quan hệ phụ thuộc giữa các Engine.
"""

from __future__ import annotations

from collections import defaultdict
from graphlib import TopologicalSorter, CycleError


class DependencyError(Exception):
    """Lỗi phụ thuộc Engine."""
    pass


class EngineDependency:
    """
    Quản lý Dependency giữa các Engine.
    """

    def __init__(self):

        self._graph: dict[str, set[str]] = defaultdict(set)

    # =====================================================
    # Register
    # =====================================================

    def add(
        self,
        engine: str,
        depends_on: str,
    ) -> None:
        """
        engine phụ thuộc depends_on
        """

        self._graph[engine].add(depends_on)

        if depends_on not in self._graph:
            self._graph[depends_on] = set()

    def remove(
        self,
        engine: str,
        depends_on: str,
    ) -> None:

        self._graph[engine].discard(depends_on)

    # =====================================================
    # Query
    # =====================================================

    def dependencies(
        self,
        engine: str,
    ) -> list[str]:

        return sorted(
            self._graph.get(engine, set())
        )

    def dependents(
        self,
        engine: str,
    ) -> list[str]:
        """
        Các Engine phụ thuộc vào engine.
        """

        result = []

        for node, deps in self._graph.items():

            if engine in deps:

                result.append(node)

        return sorted(result)

    def exists(
        self,
        engine: str,
    ) -> bool:

        return engine in self._graph

    def has_dependency(
        self,
        engine: str,
        depends_on: str,
    ) -> bool:

        return depends_on in self._graph.get(
            engine,
            set(),
        )

    # =====================================================
    # Validation
    # =====================================================

    def validate(self) -> bool:
        """
        Kiểm tra Circular Dependency.
        """

        try:

            TopologicalSorter(
                self._graph
            ).prepare()

            return True

        except CycleError as exc:

            raise DependencyError(

                f"Circular dependency detected: {exc}"

            ) from exc

    # =====================================================
    # Execution Order
    # =====================================================

    def execution_order(self) -> list[str]:
        """
        Thứ tự thực thi.
        """

        self.validate()

        sorter = TopologicalSorter(
            self._graph
        )

        return list(
            sorter.static_order()
        )

    # =====================================================
    # Utility
    # =====================================================

    def engines(self) -> list[str]:

        return sorted(self._graph.keys())

    def count(self) -> int:

        return len(self._graph)

    def clear(self):

        self._graph.clear()

    def export(self) -> dict:

        return {

            engine: sorted(deps)

            for engine, deps

            in self._graph.items()

        }

    def import_graph(
        self,
        graph: dict[str, list[str]],
    ) -> None:

        self.clear()

        for engine, deps in graph.items():

            self._graph[engine] = set(deps)

    # =====================================================
    # Debug
    # =====================================================

    def print_graph(self):

        for engine in sorted(self._graph):

            print(

                f"{engine:20} <- "

                f"{sorted(self._graph[engine])}"

            )


# =========================================================
# Singleton
# =========================================================

dependency = EngineDependency()

# =========================================================
# Default BTE Pipeline
# =========================================================

dependency.add(
    "bazi",
    "calendar",
)

dependency.add(
    "score",
    "bazi",
)

dependency.add(
    "pattern",
    "score",
)

dependency.add(
    "interpretation",
    "pattern",
)

dependency.add(
    "report",
    "interpretation",
)
