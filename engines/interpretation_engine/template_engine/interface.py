"""Template binding interface. No hard-coded templates."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class TemplateEngineInterface(ABC):
    """Template binding interface. No hard-coded templates."""

    @abstractmethod
    def bind(self, template_ref: str, values: Any) -> Any:
        """Bind values to a template reference."""

    @abstractmethod
    def validate(self, template_ref: str) -> Any:
        """Validate template reference structure."""

