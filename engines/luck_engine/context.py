"""
LuckContext — immutable runtime model (Sprint 4 foundation).

No business calculations. Fields may remain NULL until Sprint 4.1+ providers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping


def _freeze_mapping(data: Mapping[str, Any] | None) -> Mapping[str, Any]:
    """Return a read-only mapping view."""
    if data is None:
        return MappingProxyType({})
    if isinstance(data, MappingProxyType):
        return data
    return MappingProxyType(dict(data))


@dataclass(frozen=True, slots=True)
class LuckContext:
    """
    Authoritative Luck Engine output for the production pipeline.

    Consumes upstream contexts; never mutates RuleContext.
    """

    current_dayun: Any | None = None
    current_liunian: Any | None = None
    current_liuyue: Any | None = None
    current_liuri: Any | None = None
    current_liushi: Any | None = None
    support_elements: tuple[str, ...] = ()
    attack_elements: tuple[str, ...] = ()
    support_level: str | None = None
    attack_level: str | None = None
    luck_stage: str | None = None
    luck_strength: float | None = None
    luck_summary: str | None = None
    confidence: float | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)
    available: bool = False
    reason: str | None = "luck_engine_foundation_no_calculation"

    def __post_init__(self) -> None:
        """Freeze metadata mapping after init."""
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))
        object.__setattr__(
            self,
            "support_elements",
            tuple(self.support_elements or ()),
        )
        object.__setattr__(
            self,
            "attack_elements",
            tuple(self.attack_elements or ()),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize LuckContext for pipeline payload (nulls preserved)."""
        return {
            "current_dayun": _serialize_period(self.current_dayun),
            "current_liunian": _serialize_period(self.current_liunian),
            "current_liuyue": _serialize_period(self.current_liuyue),
            "current_liuri": _serialize_period(self.current_liuri),
            "current_liushi": _serialize_period(self.current_liushi),
            "support_elements": list(self.support_elements),
            "attack_elements": list(self.attack_elements),
            "support_level": self.support_level,
            "attack_level": self.attack_level,
            "luck_stage": self.luck_stage,
            "luck_strength": self.luck_strength,
            "luck_summary": self.luck_summary,
            "confidence": self.confidence,
            "metadata": dict(self.metadata),
            "available": self.available,
            "reason": self.reason,
        }


def _serialize_period(value: Any) -> Any:
    """Serialize a period object via ``to_dict`` when available."""
    if value is None:
        return None
    to_dict = getattr(value, "to_dict", None)
    if callable(to_dict):
        return to_dict()
    return value
