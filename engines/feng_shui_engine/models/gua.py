"""Feng Shui Engine models — Cung Phi / Mệnh Quái only (V1)."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True)
class GuaResult:
    """Result of Cung Phi (Mệnh Quái) calculation."""

    gua_number: int
    gua_name: str
    group: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize for API / presentation layers."""
        data = asdict(self)
        # Portal-friendly aliases (display only; same values).
        data["cung_phi"] = self.gua_name
        data["menh_quai"] = self.gua_name
        data["nhom_trach"] = self.group
        return data
