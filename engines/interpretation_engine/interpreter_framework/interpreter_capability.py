"""Interpreter capability declaration model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.interpretation_engine.interpreter_framework.interpreter_exception import (
    ConfigurationError,
)


@dataclass(frozen=True, slots=True)
class InterpreterCapability:
    """Declares what an interpreter can do and how it fits the graph."""

    interpreter_id: str
    category: str
    priority: int
    dependencies: tuple[str, ...] = ()
    optional_dependencies: tuple[str, ...] = ()
    supported_inputs: tuple[str, ...] = ("PackInterpretationContext", "FinalResult")
    supported_outputs: tuple[str, ...] = ("InterpretationSection",)
    version: str = "1.0.0"
    description: str = ""
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate capability declaration."""
        if not self.interpreter_id:
            return False
        if not self.category:
            return False
        if not self.version:
            return False
        if not isinstance(self.priority, int):
            return False
        overlap = set(self.dependencies) & set(self.optional_dependencies)
        if overlap:
            return False
        return True

    def require_valid(self) -> None:
        """Raise ConfigurationError when capability is invalid."""
        if not self.validate():
            raise ConfigurationError(
                f"invalid capability for interpreter_id={self.interpreter_id!r}"
            )

    def to_dict(self) -> dict[str, Any]:
        """Serialize capability for registry metadata."""
        return {
            "interpreter_id": self.interpreter_id,
            "category": self.category,
            "priority": self.priority,
            "dependencies": list(self.dependencies),
            "optional_dependencies": list(self.optional_dependencies),
            "supported_inputs": list(self.supported_inputs),
            "supported_outputs": list(self.supported_outputs),
            "version": self.version,
            "description": self.description,
            "attributes": dict(self.attributes),
        }
