"""Registry infrastructure exceptions."""

from __future__ import annotations


class RegistryError(Exception):
    """Base error for Registry infrastructure failures."""


class RegistryLoadError(RegistryError):
    """Raised when a registry catalog cannot be loaded."""


class RegistryValidationError(RegistryError):
    """Raised when registry validation fails fatally."""


class RegistrySchemaError(RegistryValidationError):
    """Raised when JSON Schema validation fails."""


class RegistryDuplicateError(RegistryValidationError):
    """Raised when duplicate identities are detected."""


class RegistryQueryError(RegistryError):
    """Raised when a query cannot be executed."""


class RegistryIOError(RegistryError):
    """Raised when import/export IO fails."""


class RegistrySyncError(RegistryError):
    """Raised when registry synchronization fails."""
