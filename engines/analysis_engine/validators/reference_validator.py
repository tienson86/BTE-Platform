"""Analysis Engine reference validator interface."""

from __future__ import annotations

from typing import Any

from engines.analysis_engine.validators.validator_base import ValidatorBase


class ReferenceValidator(ValidatorBase):
    """Public interface for reference validation.

    No validation logic.
    """

    def __init__(self) -> None:
        """Initialize the reference validator skeleton."""
        super().__init__(validator_id="reference_validator")

    def validate(self, payload: Any) -> bool:
        """Validate references contained in a payload."""
        raise NotImplementedError

    def errors(self) -> tuple[str, ...]:
        """Return reference validation errors."""
        raise NotImplementedError

    def validate_reference(self, reference_id: str) -> bool:
        """Validate that a single reference identifier resolves."""
        raise NotImplementedError

    def validate_references(self, reference_ids: tuple[str, ...]) -> bool:
        """Validate that all reference identifiers resolve."""
        raise NotImplementedError
