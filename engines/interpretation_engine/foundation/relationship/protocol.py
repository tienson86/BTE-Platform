"""Protocol for relationship explainers."""

from __future__ import annotations

from typing import Any, Protocol

from engines.interpretation_engine.foundation.relationship.models import (
    RelationshipAssessment,
)


class RelationshipExplainer(Protocol):
    """Common interface for relationship reasoning over upstream analytical truth."""

    def explain(self, facts: Any) -> RelationshipAssessment:
        """Transform upstream relationship records into a structured assessment."""
        ...
