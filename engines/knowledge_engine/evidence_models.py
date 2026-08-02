"""Evidence package models for RuleContext → explainable evidence."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


EVIDENCE_CATEGORIES: tuple[str, ...] = (
    "bazi",
    "five_elements",
    "ten_gods",
    "useful_god",
    "pattern",
    "strength",
    "temperature",
    "shensha",
)

CATEGORY_LABELS: dict[str, str] = {
    "bazi": "BaZi",
    "five_elements": "Five Elements",
    "ten_gods": "Ten Gods",
    "useful_god": "Useful God",
    "pattern": "Pattern",
    "strength": "Strength",
    "temperature": "Temperature",
    "shensha": "ShenSha",
}


@dataclass(slots=True)
class EvidenceItem:
    """One evidence fact extracted from RuleContext."""

    rule: str
    reason: str
    confidence: float
    source: str
    category: str

    @property
    def dedupe_key(self) -> str:
        """Stable key used to prevent duplicated evidence."""
        return "|".join(
            [
                self.category.strip().lower(),
                self.rule.strip().lower(),
                self.source.strip().lower(),
            ]
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize evidence item."""
        return {
            "category": self.category,
            "category_label": CATEGORY_LABELS.get(self.category, self.category),
            "rule": self.rule,
            "reason": self.reason,
            "confidence": self.confidence,
            "source": self.source,
        }


@dataclass(slots=True)
class EvidencePackage:
    """Categorized evidence package built from RuleContext."""

    items: list[EvidenceItem]
    categories: dict[str, list[EvidenceItem]] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def for_category(self, category: str) -> list[EvidenceItem]:
        """Return items for one category key."""
        key = str(category or "").strip().lower()
        if key in self.categories:
            return list(self.categories[key])
        return [item for item in self.items if item.category == key]

    @property
    def trace(self) -> list[dict[str, Any]]:
        """Return metadata.trace entries."""
        raw = self.metadata.get("trace") if self.metadata else None
        return list(raw) if isinstance(raw, list) else []

    def to_dict(self) -> dict[str, Any]:
        """Serialize package for validation reports / prompt builders."""
        return {
            "categories": {
                key: [item.to_dict() for item in rows]
                for key, rows in self.categories.items()
            },
            "items": [item.to_dict() for item in self.items],
            "metadata": dict(self.metadata),
        }
