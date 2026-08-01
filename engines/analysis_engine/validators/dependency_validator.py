"""Analysis Engine dependency validator interface."""

from __future__ import annotations

from typing import Any

from engines.analysis_engine.validators.validator_base import ValidatorBase


class DependencyValidator(ValidatorBase):
    """Public interface for dependency validation.

    No validation logic.
    """

    def __init__(self) -> None:
        """Initialize the dependency validator skeleton."""
        super().__init__(validator_id="dependency_validator")

    def validate(self, payload: Any) -> bool:
        """Validate dependency declarations in a payload."""
        raise NotImplementedError

    def errors(self) -> tuple[str, ...]:
        """Return dependency validation errors."""
        raise NotImplementedError

    def validate_acyclic(self, dependencies: tuple[tuple[str, str], ...]) -> bool:
        """Validate that dependency edges do not form a cycle."""
        raise NotImplementedError

    def validate_resolved(
        self,
        required: tuple[str, ...],
        available: tuple[str, ...],
    ) -> bool:
        """Validate that required dependencies are available."""
        raise NotImplementedError
