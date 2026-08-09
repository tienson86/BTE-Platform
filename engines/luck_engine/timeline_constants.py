"""Deterministic constants for the Luck Timeline Foundation."""

from __future__ import annotations

TIMELINE_VERSION = "1.0.0"
TIMELINE_CONTRACT_ID = "bte.luck.timeline.v1"
PACKAGE_ID = "bz_09_luck_foundation"
PACKAGE_VERSION_CONSTRAINT = "^1.0.0"
REQUIRED_SCHEMA_VERSION = "2.0.0"
FOUNDATION_VERSION = "1.0.0"

LAYER_NATAL = "natal_chart"
LAYER_MAJOR = "major_luck"
LAYER_ANNUAL = "annual_luck"
LAYER_MONTHLY = "monthly_luck"
LAYER_DAILY = "daily_luck"
LAYER_HOURLY = "hourly_luck"

LAYER_STATUS_ACTIVE = "active"
LAYER_STATUS_RESERVED = "reserved"

EVENT_BOUNDARY = "boundary"
EVENT_START = "start"
EVENT_END = "end"

PUBLISHED_OUTPUTS: tuple[str, ...] = (
    "natal_chart",
    "major_cycles",
    "annual_cycles",
    "monthly_cycles",
    "timeline_metadata",
    "timeline_version",
)

PUBLISHED_INPUTS: tuple[str, ...] = (
    "year_pillar",
    "month_pillar",
    "day_pillar",
    "hour_pillar",
    "gender",
    "birth_year",
    "birth_month",
    "birth_day",
    "birth_hour",
)

FORBIDDEN_TIMELINE_FIELDS: tuple[str, ...] = (
    "score",
    "luck_score",
    "quality",
    "favorable",
    "unfavorable",
    "useful_god",
    "judgment",
    "interpretation",
    "fortune",
)

RESERVED_RESULT_STATUS = "reserved"
