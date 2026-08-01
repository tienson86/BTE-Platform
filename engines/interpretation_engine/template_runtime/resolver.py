"""Template runtime resolver shell.

Resolves template-ref ids from registry. No template bodies.
"""

from __future__ import annotations

from engines.interpretation_engine.runtime.registry_base import RegistryError
from engines.interpretation_engine.template_runtime.registry import TemplateRuntimeRegistry


class TemplateRuntimeResolver:
    """Resolve template descriptors from the injected registry."""

    def __init__(self, registry: TemplateRuntimeRegistry) -> None:
        """Initialize with registry dependency."""
        self._registry = registry

    def resolve(self, template_ref_id: str) -> object:
        """Resolve a template reference descriptor."""
        entry = self._registry.lookup(template_ref_id)
        if entry is None:
            raise RegistryError(f"template_ref_not_found:{template_ref_id}")
        return entry
