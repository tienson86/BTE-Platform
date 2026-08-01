"""Interpreter Runtime registry.

Dependency injection only. No singleton globals.
"""

from __future__ import annotations

from typing import Any

from engines.interpretation_engine.runtime.registry_base import BaseRegistry


class InterpreterRuntimeRegistry(BaseRegistry[Any]):
    """Registry for Interpreter Runtime descriptors/handlers."""

    def __init__(self) -> None:
        """Initialize empty registry."""
        super().__init__(registry_id="interpreter_runtime_registry")
