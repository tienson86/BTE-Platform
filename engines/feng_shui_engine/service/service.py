"""Feng Shui Engine service — Cung Phi / Đông-Tây Tứ Trạch only."""

from __future__ import annotations

from typing import Any

from engines.feng_shui_engine.calculator.east_west_group import group_for_gua_number
from engines.feng_shui_engine.calculator.gua_calculator import (
    calculate_gua_number,
    gua_name_for_number,
)
from engines.feng_shui_engine.exceptions import FengShuiEngineError, FengShuiValidationError
from engines.feng_shui_engine.models.gua import GuaResult


class FengShuiService:
    """
    Public service for Feng Shui Engine V1.

    Responsibility: compute Cung Phi (Mệnh Quái) and Đông/Tây Tứ Trạch group.
    Does not implement any other Dương Trạch features.
    """

    def calculate(
        self,
        *,
        year: int,
        gender: str | None,
        metadata: dict[str, Any] | None = None,
    ) -> GuaResult:
        """
        Calculate Cung Phi from birth year and gender.

        ``metadata`` is reserved for future profile fields and is ignored in V1.
        """
        del metadata  # reserved for future extension
        try:
            gua_number = calculate_gua_number(year=year, gender=gender)
            gua_name = gua_name_for_number(gua_number)
            group = group_for_gua_number(gua_number)
            return GuaResult(gua_number=gua_number, gua_name=gua_name, group=group)
        except FengShuiEngineError:
            raise
        except Exception as exc:  # noqa: BLE001 — wrap unexpected failures
            raise FengShuiEngineError(f"Feng Shui calculation failed: {exc}") from exc


class FengShuiEngine:
    """Thin engine facade (orchestrator-friendly Public API)."""

    def __init__(self, service: FengShuiService | None = None) -> None:
        self._service = service or FengShuiService()

    def calculate(
        self,
        *,
        year: int,
        gender: str | None,
        metadata: dict[str, Any] | None = None,
    ) -> GuaResult:
        """Delegate to ``FengShuiService.calculate``."""
        return self._service.calculate(year=year, gender=gender, metadata=metadata)
