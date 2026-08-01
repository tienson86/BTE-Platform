"""Analysis Engine schema validator interface."""

from __future__ import annotations

from typing import Any

from engines.analysis_engine.validators.validator_base import ValidatorBase


class SchemaValidator(ValidatorBase):
    """Public interface for schema validation.

    No validation logic.
    """

    def __init__(self) -> None:
        """Initialize the schema validator skeleton."""
        super().__init__(validator_id="schema_validator")

    def validate(self, payload: Any) -> bool:
        """Validate a payload against a schema contract."""
        raise NotImplementedError

    def errors(self) -> tuple[str, ...]:
        """Return schema validation errors."""
        raise NotImplementedError

    def validate_schema_id(self, schema_id: str, payload: Any) -> bool:
        """Validate a payload against a named schema identifier."""
        raise NotImplementedError
