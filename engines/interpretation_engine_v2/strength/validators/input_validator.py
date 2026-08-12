"""Input validation for Strength runtime."""

from __future__ import annotations

from engines.interpretation_engine_v2.strength.contracts.models import (
    InvalidInputError,
    PublishedStrengthFacts,
)


class InputValidator:
    """Validate published Strength facts before reasoning."""

    def validate_published(self, published: PublishedStrengthFacts) -> None:
        """Validate minimum required fields."""
        if not published.case_id:
            raise InvalidInputError("case_id is required")
        if not published.class_id:
            raise InvalidInputError("classification.class_id is required")
        if "classification" not in published.facts:
            raise InvalidInputError("classification fact must be published")
