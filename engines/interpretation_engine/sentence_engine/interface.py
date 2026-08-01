"""Sentence assembly interface. No hard-coded sentences."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class SentenceEngineInterface(ABC):
    """Sentence assembly interface. No hard-coded sentences."""

    @abstractmethod
    def assemble(self, refs: tuple[str, ...], context: Any) -> Any:
        """Assemble sentence refs into an output shell."""

    @abstractmethod
    def validate(self, refs: tuple[str, ...]) -> Any:
        """Validate sentence reference structure."""

