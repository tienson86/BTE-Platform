"""Assemble a LuckTimeline from declared slots. Does not calculate fortune."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from engines.luck_engine.contracts.luck_contracts import (
    LuckCycle,
    LuckEvent,
    LuckPeriod,
    LuckTimeline,
)
from engines.luck_engine.models.canonical import NatalChart
from engines.luck_engine.timeline_constants import TIMELINE_VERSION
from engines.luck_engine.timeline.validation import validate_timeline


def _period_from_mapping(data: Mapping[str, Any]) -> LuckPeriod:
    """Build one period from an explicit mapping."""
    return LuckPeriod(
        period_id=str(data["period_id"]),
        layer=str(data["layer"]),
        sequence=int(data["sequence"]),
        start_year=data.get("start_year"),
        end_year=data.get("end_year"),
        start_month=data.get("start_month"),
        end_month=data.get("end_month"),
        start_day=data.get("start_day"),
        end_day=data.get("end_day"),
        heavenly_stem=data.get("heavenly_stem"),
        earthly_branch=data.get("earthly_branch"),
        parent_period_id=data.get("parent_period_id"),
        status=str(data.get("status") or "active"),
        metadata=dict(data.get("metadata") or {}),
    )


def _cycle_from_mapping(data: Mapping[str, Any]) -> LuckCycle:
    """Build one cycle from an explicit mapping."""
    raw_periods = data.get("periods") or ()
    periods = tuple(
        item if isinstance(item, LuckPeriod) else _period_from_mapping(item)
        for item in raw_periods
    )
    return LuckCycle(
        cycle_id=str(data["cycle_id"]),
        layer=str(data["layer"]),
        periods=periods,
        parent_period_id=data.get("parent_period_id"),
        status=str(data.get("status") or "active"),
        metadata=dict(data.get("metadata") or {}),
    )


def _event_from_mapping(data: Mapping[str, Any]) -> LuckEvent:
    """Build one event from an explicit mapping."""
    return LuckEvent(
        event_id=str(data["event_id"]),
        period_id=str(data["period_id"]),
        event_type=str(data["event_type"]),
        year=data.get("year"),
        month=data.get("month"),
        day=data.get("day"),
        metadata=dict(data.get("metadata") or {}),
    )


def _natal_from_mapping(data: Mapping[str, Any] | NatalChart) -> NatalChart:
    """Build natal identity from an explicit mapping or model."""
    if isinstance(data, NatalChart):
        return data
    return NatalChart(
        chart_id=str(data["chart_id"]),
        year_pillar=str(data["year_pillar"]),
        month_pillar=str(data["month_pillar"]),
        day_pillar=str(data["day_pillar"]),
        hour_pillar=data.get("hour_pillar"),
        gender=data.get("gender"),
        birth_year=data.get("birth_year"),
        birth_month=data.get("birth_month"),
        birth_day=data.get("birth_day"),
        birth_hour=data.get("birth_hour"),
        metadata=dict(data.get("metadata") or {}),
    )


def construct_timeline(
    *,
    timeline_id: str,
    natal_chart: Mapping[str, Any] | NatalChart,
    major_cycles: Sequence[Mapping[str, Any] | LuckCycle] = (),
    annual_cycles: Sequence[Mapping[str, Any] | LuckCycle] = (),
    monthly_cycles: Sequence[Mapping[str, Any] | LuckCycle] = (),
    daily_cycles: Sequence[Mapping[str, Any] | LuckCycle] = (),
    hourly_cycles: Sequence[Mapping[str, Any] | LuckCycle] = (),
    events: Sequence[Mapping[str, Any] | LuckEvent] = (),
    timeline_metadata: Mapping[str, Any] | None = None,
    timeline_version: str = TIMELINE_VERSION,
    validate: bool = True,
) -> LuckTimeline:
    """
    Construct a canonical timeline from caller-supplied slots.

    This function does not derive Đại Vận / Lưu Niên / Lưu Nguyệt from a chart.
    """
    cycles_major = tuple(
        item if isinstance(item, LuckCycle) else _cycle_from_mapping(item)
        for item in major_cycles
    )
    cycles_annual = tuple(
        item if isinstance(item, LuckCycle) else _cycle_from_mapping(item)
        for item in annual_cycles
    )
    cycles_monthly = tuple(
        item if isinstance(item, LuckCycle) else _cycle_from_mapping(item)
        for item in monthly_cycles
    )
    cycles_daily = tuple(
        item if isinstance(item, LuckCycle) else _cycle_from_mapping(item)
        for item in daily_cycles
    )
    cycles_hourly = tuple(
        item if isinstance(item, LuckCycle) else _cycle_from_mapping(item)
        for item in hourly_cycles
    )
    timeline_events = tuple(
        item if isinstance(item, LuckEvent) else _event_from_mapping(item)
        for item in events
    )
    timeline = LuckTimeline(
        timeline_id=timeline_id,
        natal_chart=_natal_from_mapping(natal_chart),
        major_cycles=cycles_major,
        annual_cycles=cycles_annual,
        monthly_cycles=cycles_monthly,
        daily_cycles=cycles_daily,
        hourly_cycles=cycles_hourly,
        events=timeline_events,
        timeline_version=timeline_version,
        timeline_metadata=dict(timeline_metadata or {}),
    )
    if validate:
        validate_timeline(timeline)
    return timeline
