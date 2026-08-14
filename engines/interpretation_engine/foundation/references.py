"""Shared reference types for interpretation foundation layers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class KnowledgeEntityReference:
    """Explicit cross-domain knowledge entity reference."""

    domain: str
    key: str

    def to_dict(self) -> dict[str, str]:
        """Serialize reference."""
        return {"domain": self.domain, "key": self.key}
