"""Validate Luck Timeline structure. No fortune scoring."""

from __future__ import annotations

from typing import Any, Iterable, Mapping

from engines.luck_engine.contracts.luck_contracts import LuckCycle, LuckPeriod, LuckTimeline
from engines.luck_engine.exceptions import TimelineValidationError
from engines.luck_engine.timeline_constants import (
    FORBIDDEN_TIMELINE_FIELDS,
    LAYER_ANNUAL,
    LAYER_DAILY,
    LAYER_HOURLY,
    LAYER_MAJOR,
    LAYER_MONTHLY,
    LAYER_STATUS_RESERVED,
    PUBLISHED_OUTPUTS,
    REQUIRED_SCHEMA_VERSION,
    TIMELINE_VERSION,
)
from engines.luck_engine.timeline.registry import TimelineRegistry


def _flatten_periods(cycles: Iterable[LuckCycle]) -> list[LuckPeriod]:
    """Return all periods from cycles."""
    periods: list[LuckPeriod] = []
    for cycle in cycles:
        periods.extend(cycle.periods)
    return periods


def _contains_forbidden(payload: Any, path: str = "") -> str | None:
    """Return the first forbidden field path when present."""
    if isinstance(payload, Mapping):
        for key, value in payload.items():
            lowered = str(key).lower()
            next_path = f"{path}.{key}" if path else str(key)
            if lowered in FORBIDDEN_TIMELINE_FIELDS:
                return next_path
            nested = _contains_forbidden(value, next_path)
            if nested:
                return nested
    elif isinstance(payload, (list, tuple)):
        for index, item in enumerate(payload):
            nested = _contains_forbidden(item, f"{path}[{index}]")
            if nested:
                return nested
    return None


def validate_metadata(metadata: Mapping[str, Any], *, path: str) -> None:
    """Reject judgment fields inside metadata."""
    forbidden = _contains_forbidden(dict(metadata), path)
    if forbidden:
        raise TimelineValidationError(f"forbidden_field:{forbidden}")


def validate_schema(timeline: LuckTimeline) -> None:
    """Require canonical identity fields."""
    if not timeline.timeline_id:
        raise TimelineValidationError("missing_timeline_id")
    if not timeline.natal_chart.chart_id:
        raise TimelineValidationError("missing_chart_id")
    for field_name in ("year_pillar", "month_pillar", "day_pillar"):
        if not getattr(timeline.natal_chart, field_name):
            raise TimelineValidationError(f"missing_natal_field:{field_name}")
    published = timeline.to_dict()
    missing = [name for name in PUBLISHED_OUTPUTS if name not in published]
    if missing:
        raise TimelineValidationError(f"missing_published_outputs:{','.join(missing)}")


def validate_version_compatibility(
    *,
    timeline_version: str,
    schema_version: str = REQUIRED_SCHEMA_VERSION,
) -> None:
    """Admit only Foundation-era timeline and schema versions."""
    if timeline_version != TIMELINE_VERSION:
        raise TimelineValidationError(f"incompatible_timeline_version:{timeline_version}")
    if schema_version != REQUIRED_SCHEMA_VERSION:
        raise TimelineValidationError(f"incompatible_schema_version:{schema_version}")


def validate_duplicate_ids(timeline: LuckTimeline) -> None:
    """Reject duplicate cycle, period, or event identifiers."""
    cycle_ids = [
        cycle.cycle_id
        for group in (
            timeline.major_cycles,
            timeline.annual_cycles,
            timeline.monthly_cycles,
            timeline.daily_cycles,
            timeline.hourly_cycles,
        )
        for cycle in group
    ]
    period_ids = [
        period.period_id
        for group in (
            timeline.major_cycles,
            timeline.annual_cycles,
            timeline.monthly_cycles,
            timeline.daily_cycles,
            timeline.hourly_cycles,
        )
        for period in _flatten_periods(group)
    ]
    event_ids = [event.event_id for event in timeline.events]
    for label, values in (
        ("cycle_id", cycle_ids),
        ("period_id", period_ids),
        ("event_id", event_ids),
    ):
        if len(values) != len(set(values)):
            raise TimelineValidationError(f"duplicate_{label}")


def _month_key(year: int | None, month: int | None) -> tuple[int, int] | None:
    if year is None or month is None:
        return None
    return (int(year), int(month))


def _validate_layer_continuity(periods: list[LuckPeriod], *, layer: str) -> None:
    """Require monotonic sequence and abutting bounds inside one cycle."""
    ordered = sorted(periods, key=lambda item: item.sequence)
    sequences = [item.sequence for item in ordered]
    if len(sequences) != len(set(sequences)):
        raise TimelineValidationError(f"duplicate_sequence:{layer}")
    for index, period in enumerate(ordered):
        if period.layer != layer:
            raise TimelineValidationError(f"layer_mismatch:{period.period_id}")
        if index == 0:
            continue
        previous = ordered[index - 1]
        if period.sequence <= previous.sequence:
            raise TimelineValidationError(f"sequence_not_increasing:{period.period_id}")
        if layer in {LAYER_MAJOR, LAYER_ANNUAL}:
            if previous.end_year is None or period.start_year is None:
                raise TimelineValidationError(f"missing_year_bounds:{period.period_id}")
            if int(period.start_year) != int(previous.end_year) + 1:
                raise TimelineValidationError(f"year_gap_or_overlap:{period.period_id}")
        if layer == LAYER_MONTHLY:
            prev_key = _month_key(previous.end_year, previous.end_month)
            next_key = _month_key(period.start_year, period.start_month)
            if prev_key is None or next_key is None:
                raise TimelineValidationError(f"missing_month_bounds:{period.period_id}")
            prev_year, prev_month = prev_key
            expected_month = prev_month + 1
            expected_year = prev_year
            if expected_month > 12:
                expected_month = 1
                expected_year += 1
            if next_key != (expected_year, expected_month):
                raise TimelineValidationError(f"month_gap_or_overlap:{period.period_id}")


def validate_continuity(timeline: LuckTimeline) -> None:
    """Validate per-cycle continuity and parent nesting."""
    major_ids = {period.period_id for period in _flatten_periods(timeline.major_cycles)}
    annual_ids = {period.period_id for period in _flatten_periods(timeline.annual_cycles)}
    for cycle in timeline.major_cycles:
        _validate_layer_continuity(list(cycle.periods), layer=LAYER_MAJOR)
    for cycle in timeline.annual_cycles:
        _validate_layer_continuity(list(cycle.periods), layer=LAYER_ANNUAL)
        if cycle.parent_period_id and cycle.parent_period_id not in major_ids:
            raise TimelineValidationError(f"annual_parent_missing:{cycle.cycle_id}")
        for period in cycle.periods:
            if period.parent_period_id and period.parent_period_id not in major_ids:
                raise TimelineValidationError(f"annual_parent_missing:{period.period_id}")
    for cycle in timeline.monthly_cycles:
        _validate_layer_continuity(list(cycle.periods), layer=LAYER_MONTHLY)
        if cycle.parent_period_id and cycle.parent_period_id not in annual_ids:
            raise TimelineValidationError(f"monthly_parent_missing:{cycle.cycle_id}")
        for period in cycle.periods:
            if period.parent_period_id and period.parent_period_id not in annual_ids:
                raise TimelineValidationError(f"monthly_parent_missing:{period.period_id}")


def validate_reserved_layers(timeline: LuckTimeline) -> None:
    """Daily and hourly layers stay reserved and empty in LE-1."""
    registry = TimelineRegistry()
    for cycle in (*timeline.daily_cycles, *timeline.hourly_cycles):
        record = registry.get(cycle.layer)
        if record.status != LAYER_STATUS_RESERVED:
            raise TimelineValidationError(f"layer_not_reserved:{cycle.layer}")
        if cycle.periods:
            raise TimelineValidationError(f"reserved_layer_not_empty:{cycle.layer}")
        if cycle.status != LAYER_STATUS_RESERVED:
            raise TimelineValidationError(f"reserved_status_required:{cycle.cycle_id}")


def validate_contract_integrity(payload: Mapping[str, Any]) -> None:
    """Ensure published output names exist and judgment fields are absent."""
    missing = [name for name in PUBLISHED_OUTPUTS if name not in payload]
    if missing:
        raise TimelineValidationError(f"contract_missing:{','.join(missing)}")
    forbidden = _contains_forbidden(payload)
    if forbidden:
        raise TimelineValidationError(f"forbidden_field:{forbidden}")


def validate_timeline(timeline: LuckTimeline) -> None:
    """Run the full LE-1 timeline validation suite."""
    validate_schema(timeline)
    validate_metadata(timeline.timeline_metadata, path="timeline_metadata")
    validate_metadata(timeline.natal_chart.metadata, path="natal_chart.metadata")
    validate_version_compatibility(timeline_version=timeline.timeline_version)
    validate_duplicate_ids(timeline)
    validate_continuity(timeline)
    validate_reserved_layers(timeline)
    validate_contract_integrity(timeline.to_dict())
