"""Timeline construction tests. No fortune calculation."""

from __future__ import annotations

from typing import Any

import pytest

from engines.luck_engine.exceptions import TimelineValidationError
from engines.luck_engine.timeline import construct_timeline


def test_construct_continuous_timeline(continuous_timeline_payload: dict[str, Any]) -> None:
    """Declared slots assemble into a valid published timeline."""
    timeline = construct_timeline(**continuous_timeline_payload)
    assert timeline.timeline_id == "TL-TEST-001"
    assert timeline.timeline_version == "1.0.0"
    assert len(timeline.major_cycles[0].periods) == 2
    assert timeline.natal_chart.day_pillar == "Mậu Thìn"
    published = timeline.to_dict()
    assert set(published) >= {
        "natal_chart",
        "major_cycles",
        "annual_cycles",
        "monthly_cycles",
        "timeline_metadata",
        "timeline_version",
    }


def test_year_gap_is_rejected(continuous_timeline_payload: dict[str, Any]) -> None:
    """Non-abutting major years must fail continuity."""
    payload = continuous_timeline_payload
    payload["major_cycles"][0]["periods"][1]["start_year"] = 2002
    with pytest.raises(TimelineValidationError, match="year_gap_or_overlap"):
        construct_timeline(**payload)


def test_duplicate_period_id_is_rejected(continuous_timeline_payload: dict[str, Any]) -> None:
    """Duplicate period identifiers are invalid."""
    payload = continuous_timeline_payload
    payload["major_cycles"][0]["periods"][1]["period_id"] = "P-MAJOR-001"
    with pytest.raises(TimelineValidationError, match="duplicate_period_id"):
        construct_timeline(**payload)
