"""
Interpretation interface for future feng_shui consumption.

V1 prepares a typed view of ``payload["feng_shui"]`` only.
No business rules / sentence generation here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class FengShuiInterpretationInput:
    """
    Read-only snapshot of Feng Shui Engine output for Interpretation Engine.

    Interpretation may later consume this to generate sentences.
    This module does not invent content.
    """

    gua_number: int | None = None
    gua_name: str | None = None
    group: str | None = None

    @classmethod
    def from_analyze_payload(cls, payload: dict[str, Any] | None) -> FengShuiInterpretationInput:
        """Extract ``feng_shui`` (or legacy ``fengshui``) from an analyze payload."""
        data = payload if isinstance(payload, dict) else {}
        raw = data.get("feng_shui")
        if not isinstance(raw, dict):
            raw = data.get("fengshui")
        if not isinstance(raw, dict):
            return cls()
        gua_number = raw.get("gua_number")
        try:
            gua_number_int = int(gua_number) if gua_number is not None else None
        except (TypeError, ValueError):
            gua_number_int = None
        gua_name = raw.get("gua_name") or raw.get("cung_phi") or raw.get("menh_quai")
        group = raw.get("group") or raw.get("nhom_trach")
        return cls(
            gua_number=gua_number_int,
            gua_name=str(gua_name) if gua_name is not None else None,
            group=str(group) if group is not None else None,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize for future rule-context injection."""
        return {
            "gua_number": self.gua_number,
            "gua_name": self.gua_name,
            "group": self.group,
        }

    @property
    def available(self) -> bool:
        """True when enough data exists for a future interpretation section."""
        return self.gua_name is not None and self.group is not None
