"""Placeholder runtime binder shell.

Binds opaque placeholder ids only. No placeholder value interpretation.
"""

from __future__ import annotations

from typing import Any, Mapping

from engines.interpretation_engine.placeholder_runtime.registry import (
    PlaceholderRuntimeRegistry,
)


class PlaceholderRuntimeBinder:
    """Bind opaque values for registered placeholder ids."""

    def __init__(self, registry: PlaceholderRuntimeRegistry) -> None:
        """Initialize with registry dependency."""
        self._registry = registry

    def bind(self, values: Mapping[str, Any]) -> dict[str, Any]:
        """Return values scoped to registered placeholder ids."""
        bound: dict[str, Any] = {}
        for entry_id in self._registry.list():
            if entry_id in values:
                bound[entry_id] = values[entry_id]
        return bound
