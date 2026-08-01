"""Analysis Engine metadata validator interface."""

from __future__ import annotations

from typing import Any

from engines.analysis_engine.validators.validator_base import ValidatorBase


class MetadataValidator(ValidatorBase):
    """Public interface for metadata validation.

    No validation logic.
    """

    def __init__(self) -> None:
        """Initialize the metadata validator skeleton."""
        super().__init__(validator_id="metadata_validator")

    def validate(self, payload: Any) -> bool:
        """Validate metadata payload completeness."""
        raise NotImplementedError

    def errors(self) -> tuple[str, ...]:
        """Return metadata validation errors."""
        raise NotImplementedError

    def validate_required_fields(self, payload: Any, fields: tuple[str, ...]) -> bool:
        """Validate that required metadata fields are present."""
        raise NotImplementedError
