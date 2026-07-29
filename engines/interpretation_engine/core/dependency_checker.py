"""
BTE Platform
Interpretation Engine

Dependency Checker

Kiểm tra quan hệ phụ thuộc giữa các module dữ liệu.
"""

from __future__ import annotations

from pathlib import Path


class DependencyError(Exception):
    """Lỗi phụ thuộc dữ liệu."""


class DependencyChecker:

    def __init__(self):

        self._dependencies: dict[str, set[str]] = {}

    def add_dependency(self, source: str, target: str):

        self._dependencies.setdefault(source, set()).add(target)

    def remove_dependency(self, source: str, target: str):

        if source in self._dependencies:
            self._dependencies[source].discard(target)

    def get_dependencies(self, source: str):

        return sorted(self._dependencies.get(source, []))

    def has_dependency(self, source: str, target: str):

        return target in self._dependencies.get(source, set())

    def validate(self):

        visited = set()
        visiting = set()

        def dfs(node):

            if node in visiting:
                raise DependencyError(
                    f"Phát hiện vòng lặp dependency tại [{node}]"
                )

            if node in visited:
                return

            visiting.add(node)

            for child in self._dependencies.get(node, set()):
                dfs(child)

            visiting.remove(node)
            visited.add(node)

        for node in self._dependencies:
            dfs(node)

        return True

    def clear(self):

        self._dependencies.clear()

    def export(self):

        return {
            key: sorted(value)
            for key, value in self._dependencies.items()
        }
