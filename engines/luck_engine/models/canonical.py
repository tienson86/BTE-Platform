"""LE-1 canonical timeline models. Definitions only — no fortune analysis."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from engines.luck_engine.timeline.constants import (
    LAYER_ANNUAL,
    LAYER_DAILY,
    LAYER_HOURLY,
    LAYER_MAJOR,
    LAYER_MONTHLY,
    LAYER_STATUS_ACTIVE,
    LAYER_STATUS_RESERVED,
    TIMELINE_VERSION,
)


def _freeze_mapping(data: Mapping[str, Any] | None) -> Mapping[str, Any]:
    """Return a read-only mapping view."""
    if data is None:
        return MappingProxyType({})
    if isinstance(data, MappingProxyType):
        return data
    return MappingProxyType(dict(data))


@dataclass(frozen=True, slots=True)
class NatalChart:
    """Natal Four Pillars identity used as the timeline origin. No judgments."""

    chart_id: str
    year_pillar: str
    month_pillar: str
    day_pillar: str
    hour_pillar: str | None = None
    gender: str | None = None
    birth_year: int | None = None
    birth_month: int | None = None
    birth_day: int | None = None
    birth_hour: int | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Freeze metadata after init."""
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Serialize natal identity."""
        return {
            "chart_id": self.chart_id,
            "year_pillar": self.year_pillar,
            "month_pillar": self.month_pillar,
            "day_pillar": self.day_pillar,
            "hour_pillar": self.hour_pillar,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "birth_month": self.birth_month,
            "birth_day": self.birth_day,
            "birth_hour": self.birth_hour,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class MajorLuckCycle:
    """Đại Vận cycle container. Periods are timeline slots only."""

    cycle_id: str
    periods: tuple[str, ...] = ()
    status: str = LAYER_STATUS_ACTIVE
    layer: str = LAYER_MAJOR
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Freeze nested collections."""
        object.__setattr__(self, "periods", tuple(self.periods or ()))
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))
        object.__setattr__(self, "layer", LAYER_MAJOR)

    def to_dict(self) -> dict[str, Any]:
        """Serialize major-cycle identity."""
        return {
            "cycle_id": self.cycle_id,
            "layer": self.layer,
            "status": self.status,
            "periods": list(self.periods),
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class AnnualLuck:
    """Lưu Niên cycle container. Nested under a major period when declared."""

    cycle_id: str
    parent_period_id: str | None = None
    periods: tuple[str, ...] = ()
    status: str = LAYER_STATUS_ACTIVE
    layer: str = LAYER_ANNUAL
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Freeze nested collections."""
        object.__setattr__(self, "periods", tuple(self.periods or ()))
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))
        object.__setattr__(self, "layer", LAYER_ANNUAL)

    def to_dict(self) -> dict[str, Any]:
        """Serialize annual-cycle identity."""
        return {
            "cycle_id": self.cycle_id,
            "layer": self.layer,
            "status": self.status,
            "parent_period_id": self.parent_period_id,
            "periods": list(self.periods),
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class MonthlyLuck:
    """Lưu Nguyệt cycle container. Nested under an annual period when declared."""

    cycle_id: str
    parent_period_id: str | None = None
    periods: tuple[str, ...] = ()
    status: str = LAYER_STATUS_ACTIVE
    layer: str = LAYER_MONTHLY
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Freeze nested collections."""
        object.__setattr__(self, "periods", tuple(self.periods or ()))
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))
        object.__setattr__(self, "layer", LAYER_MONTHLY)

    def to_dict(self) -> dict[str, Any]:
        """Serialize monthly-cycle identity."""
        return {
            "cycle_id": self.cycle_id,
            "layer": self.layer,
            "status": self.status,
            "parent_period_id": self.parent_period_id,
            "periods": list(self.periods),
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class DailyLuck:
    """Lưu Nhật layer. Reserved in Foundation 1.0.0 / LE-1."""

    cycle_id: str
    parent_period_id: str | None = None
    periods: tuple[str, ...] = ()
    status: str = LAYER_STATUS_RESERVED
    layer: str = LAYER_DAILY
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Force reserved daily layer."""
        object.__setattr__(self, "periods", tuple(self.periods or ()))
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))
        object.__setattr__(self, "layer", LAYER_DAILY)
        object.__setattr__(self, "status", LAYER_STATUS_RESERVED)

    def to_dict(self) -> dict[str, Any]:
        """Serialize reserved daily-cycle identity."""
        return {
            "cycle_id": self.cycle_id,
            "layer": self.layer,
            "status": self.status,
            "parent_period_id": self.parent_period_id,
            "periods": list(self.periods),
            "metadata": dict(self.metadata),
            "timeline_version": TIMELINE_VERSION,
        }


@dataclass(frozen=True, slots=True)
class HourlyLuck:
    """Lưu Thời layer. Reserved in Foundation 1.0.0 / LE-1."""

    cycle_id: str
    parent_period_id: str | None = None
    periods: tuple[str, ...] = ()
    status: str = LAYER_STATUS_RESERVED
    layer: str = LAYER_HOURLY
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Force reserved hourly layer."""
        object.__setattr__(self, "periods", tuple(self.periods or ()))
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))
        object.__setattr__(self, "layer", LAYER_HOURLY)
        object.__setattr__(self, "status", LAYER_STATUS_RESERVED)

    def to_dict(self) -> dict[str, Any]:
        """Serialize reserved hourly-cycle identity."""
        return {
            "cycle_id": self.cycle_id,
            "layer": self.layer,
            "status": self.status,
            "parent_period_id": self.parent_period_id,
            "periods": list(self.periods),
            "metadata": dict(self.metadata),
            "timeline_version": TIMELINE_VERSION,
        }
