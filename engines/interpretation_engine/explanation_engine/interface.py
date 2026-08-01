"""Explanation assembly interface. No hard-coded explanations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ExplanationEngineInterface(ABC):
    """Explanation assembly interface. No hard-coded explanations."""

    @abstractmethod
    def explain(self, evidence_refs: tuple[str, ...], context: Any) -> Any:
        """Assemble explanation shell from evidence refs."""

    @abstractmethod
    def validate(self, evidence_refs: tuple[str, ...]) -> Any:
        """Validate evidence reference structure."""

