"""Interpreter metadata model for the Pack 03 Interpreter Framework."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class InterpreterMetadata:
    """Immutable metadata attached to interpreter execution."""

    interpreter_id: str
    version: str
    category: str = ""
    description: str = ""
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate metadata structural integrity."""
        return bool(self.interpreter_id and self.version)

    def to_dict(self) -> dict[str, Any]:
        """Serialize metadata for payloads."""
        return {
            "interpreter_id": self.interpreter_id,
            "version": self.version,
            "category": self.category,
            "description": self.description,
            "attributes": dict(self.attributes),
        }
