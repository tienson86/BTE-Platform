"""Canonical Luck Engine timeline contracts (LE-1). No scoring or interpretation."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from engines.luck_engine.models.canonical import NatalChart
from engines.luck_engine.timeline.constants import (
    RESERVED_RESULT_STATUS,
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
class LuckPeriod:
    """One contiguous timeline slot. Identity and bounds only."""

    period_id: str
    layer: str
    sequence: int
    start_year: int | None = None
    end_year: int | None = None
    start_month: int | None = None
    end_month: int | None = None
    start_day: int | None = None
    end_day: int | None = None
    heavenly_stem: str | None = None
    earthly_branch: str | None = None
    parent_period_id: str | None = None
    status: str = "active"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Freeze metadata after init."""
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))

    @property
    def ganzhi(self) -> str | None:
        """Stem-branch label when both parts exist."""
        if self.heavenly_stem and self.earthly_branch:
            return f"{self.heavenly_stem}{self.earthly_branch}"
        return None

    def to_dict(self) -> dict[str, Any]:
        """Serialize a timeline period."""
        return {
            "period_id": self.period_id,
            "layer": self.layer,
            "sequence": self.sequence,
            "start_year": self.start_year,
            "end_year": self.end_year,
            "start_month": self.start_month,
            "end_month": self.end_month,
            "start_day": self.start_day,
            "end_day": self.end_day,
            "heavenly_stem": self.heavenly_stem,
            "earthly_branch": self.earthly_branch,
            "ganzhi": self.ganzhi,
            "parent_period_id": self.parent_period_id,
            "status": self.status,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class LuckCycle:
    """Ordered collection of periods on one timeline layer."""

    cycle_id: str
    layer: str
    periods: tuple[LuckPeriod, ...] = ()
    parent_period_id: str | None = None
    status: str = "active"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Freeze nested collections."""
        object.__setattr__(self, "periods", tuple(self.periods or ()))
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Serialize a timeline cycle."""
        return {
            "cycle_id": self.cycle_id,
            "layer": self.layer,
            "status": self.status,
            "parent_period_id": self.parent_period_id,
            "periods": [period.to_dict() for period in self.periods],
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class LuckEvent:
    """Timeline boundary marker. Not a fortune event."""

    event_id: str
    period_id: str
    event_type: str
    year: int | None = None
    month: int | None = None
    day: int | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Freeze metadata after init."""
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Serialize a timeline event."""
        return {
            "event_id": self.event_id,
            "period_id": self.period_id,
            "event_type": self.event_type,
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class LuckTimeline:
    """Canonical published timeline. No scores and no interpretation."""

    timeline_id: str
    natal_chart: NatalChart
    major_cycles: tuple[LuckCycle, ...] = ()
    annual_cycles: tuple[LuckCycle, ...] = ()
    monthly_cycles: tuple[LuckCycle, ...] = ()
    daily_cycles: tuple[LuckCycle, ...] = ()
    hourly_cycles: tuple[LuckCycle, ...] = ()
    events: tuple[LuckEvent, ...] = ()
    timeline_version: str = TIMELINE_VERSION
    timeline_metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Freeze nested collections."""
        object.__setattr__(self, "major_cycles", tuple(self.major_cycles or ()))
        object.__setattr__(self, "annual_cycles", tuple(self.annual_cycles or ()))
        object.__setattr__(self, "monthly_cycles", tuple(self.monthly_cycles or ()))
        object.__setattr__(self, "daily_cycles", tuple(self.daily_cycles or ()))
        object.__setattr__(self, "hourly_cycles", tuple(self.hourly_cycles or ()))
        object.__setattr__(self, "events", tuple(self.events or ()))
        object.__setattr__(self, "timeline_metadata", _freeze_mapping(self.timeline_metadata))

    def to_dict(self) -> dict[str, Any]:
        """Serialize the published timeline contract."""
        return {
            "natal_chart": self.natal_chart.to_dict(),
            "major_cycles": [cycle.to_dict() for cycle in self.major_cycles],
            "annual_cycles": [cycle.to_dict() for cycle in self.annual_cycles],
            "monthly_cycles": [cycle.to_dict() for cycle in self.monthly_cycles],
            "timeline_metadata": {
                **dict(self.timeline_metadata),
                "timeline_id": self.timeline_id,
                "daily_reserved": True,
                "hourly_reserved": True,
                "daily_cycles": [cycle.to_dict() for cycle in self.daily_cycles],
                "hourly_cycles": [cycle.to_dict() for cycle in self.hourly_cycles],
                "events": [event.to_dict() for event in self.events],
            },
            "timeline_version": self.timeline_version,
        }


@dataclass(frozen=True, slots=True)
class LuckContext:
    """
    LE-1 timeline context contract.

    Distinct from ``engines.luck_engine.context.LuckContext`` (runtime evaluation).
    This type carries natal + timeline identity for future Luck Analysis packages.
    """

    natal_chart: NatalChart | None = None
    timeline: LuckTimeline | None = None
    timeline_version: str = TIMELINE_VERSION
    analysis_published: Mapping[str, Any] | None = None
    decision_published: Mapping[str, Any] | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Freeze mappings after init."""
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))
        if self.analysis_published is not None:
            object.__setattr__(
                self,
                "analysis_published",
                _freeze_mapping(self.analysis_published),
            )
        if self.decision_published is not None:
            object.__setattr__(
                self,
                "decision_published",
                _freeze_mapping(self.decision_published),
            )

    def to_dict(self) -> dict[str, Any]:
        """Serialize the timeline context contract."""
        return {
            "natal_chart": None if self.natal_chart is None else self.natal_chart.to_dict(),
            "timeline": None if self.timeline is None else self.timeline.to_dict(),
            "timeline_version": self.timeline_version,
            "analysis_published": (
                None if self.analysis_published is None else dict(self.analysis_published)
            ),
            "decision_published": (
                None if self.decision_published is None else dict(self.decision_published)
            ),
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class LuckResult:
    """Reserved analytical result. LE-1 does not populate fortune fields."""

    result_id: str | None = None
    status: str = RESERVED_RESULT_STATUS
    timeline: LuckTimeline | None = None
    timeline_version: str = TIMELINE_VERSION
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Force reserved status and freeze metadata."""
        object.__setattr__(self, "status", RESERVED_RESULT_STATUS)
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Serialize the reserved result placeholder."""
        return {
            "result_id": self.result_id,
            "status": self.status,
            "timeline": None if self.timeline is None else self.timeline.to_dict(),
            "timeline_version": self.timeline_version,
            "metadata": dict(self.metadata),
        }
