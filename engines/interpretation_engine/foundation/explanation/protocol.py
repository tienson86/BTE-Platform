"""Protocol for domain decision explainers."""

from __future__ import annotations

from typing import Any, Protocol

from engines.interpretation_engine.foundation.explanation.models import DecisionExplanationResult


class DecisionExplainer(Protocol):
    """Common interface for domain interpreters using the explanation framework."""

    def explain(self, facts: Any) -> DecisionExplanationResult:
        """Transform domain facts into a structured decision explanation."""
        ...
