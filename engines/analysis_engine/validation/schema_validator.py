"""Schema validator interface.

No validation logic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from engines.analysis_engine.validation.validator_contract import ValidatorContract


class SchemaValidator(ValidatorContract, ABC):
    """Public interface for schema validation contracts."""

    @abstractmethod
    def validate_schema_id(self, schema_id: str) -> bool:
        """Validate that a schema identifier is known."""

    @abstractmethod
    def validate_against_schema(self, schema_id: str, payload: Any) -> bool:
        """Validate a payload against a named schema identifier."""

    @abstractmethod
    def list_supported_schemas(self) -> tuple[str, ...]:
        """Return supported schema identifiers."""
