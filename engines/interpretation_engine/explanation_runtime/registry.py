"""Explanation Runtime registry.

Dependency injection only. No singleton globals.
"""

from __future__ import annotations

from typing import Any

from engines.interpretation_engine.runtime.registry_base import BaseRegistry


class ExplanationRuntimeRegistry(BaseRegistry[Any]):
    """Registry for Explanation Runtime descriptors/handlers."""

    def __init__(self) -> None:
        """Initialize empty registry."""
        super().__init__(registry_id="explanation_runtime_registry")
