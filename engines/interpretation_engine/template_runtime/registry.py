"""template_runtime registry.

Dependency injection only. No singleton globals.
"""

from __future__ import annotations

from typing import Any

from engines.interpretation_engine.runtime.registry_base import BaseRegistry


class TemplateRuntimeRegistry(BaseRegistry[Any]):
    """Registry for template_runtime descriptors/handlers."""

    def __init__(self) -> None:
        """Initialize empty registry."""
        super().__init__(registry_id="template_runtime_registry")
