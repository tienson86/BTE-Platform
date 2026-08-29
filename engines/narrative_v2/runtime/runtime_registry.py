"""Narrative V2 runtime registry.

Builder registration only. No builder implementation.
"""

from __future__ import annotations

from dataclasses import dataclass

from engines.narrative_v2.runtime.runtime_errors import BuilderError


@dataclass(slots=True)
class BuilderRegistration:
    """Registered builder identity. Implementation may be absent."""

    builder_id: str
    builder: object | None = None


class RuntimeRegistry:
    """Register builder identities for later sprints."""

    def __init__(self) -> None:
        self._builders: dict[str, BuilderRegistration] = {}

    def register(
        self,
        builder_id: str,
        builder: object | None = None,
    ) -> None:
        """Register a builder id. ``builder`` may be None in N-IMP-01."""
        if not builder_id:
            raise BuilderError("builder_id is required")
        if builder_id in self._builders:
            raise BuilderError(f"Builder already registered: {builder_id}")
        self._builders[builder_id] = BuilderRegistration(
            builder_id=builder_id,
            builder=builder,
        )

    def get(self, builder_id: str) -> BuilderRegistration | None:
        """Return a registration, or None if missing."""
        return self._builders.get(builder_id)

    def contains(self, builder_id: str) -> bool:
        """Return True if ``builder_id`` is registered."""
        return builder_id in self._builders

    def registered_ids(self) -> tuple[str, ...]:
        """Registered builder ids in insertion order."""
        return tuple(self._builders)

    @property
    def builder_count(self) -> int:
        """Number of registered builders."""
        return len(self._builders)
