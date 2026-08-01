"""Analysis Engine registry validator interface."""

from __future__ import annotations

from typing import Any

from engines.analysis_engine.registry.registry import Registry
from engines.analysis_engine.registry.registry_models import RegistryEntry, RegistrySnapshot
from engines.analysis_engine.validators.validator_base import ValidatorBase


class RegistryValidator(ValidatorBase):
    """Public interface for registry validation within the validators layer.

    No validation logic.
    """

    def __init__(self) -> None:
        """Initialize the registry validator skeleton."""
        super().__init__(validator_id="registry_validator")

    def validate(self, payload: Any) -> bool:
        """Validate a registry-related payload."""
        raise NotImplementedError

    def errors(self) -> tuple[str, ...]:
        """Return registry validation errors."""
        raise NotImplementedError

    def validate_entry(self, entry: RegistryEntry) -> bool:
        """Validate a registry entry contract."""
        raise NotImplementedError

    def validate_registry(self, registry: Registry) -> bool:
        """Validate a registry instance."""
        raise NotImplementedError

    def validate_snapshot(self, snapshot: RegistrySnapshot) -> bool:
        """Validate a registry snapshot."""
        raise NotImplementedError
