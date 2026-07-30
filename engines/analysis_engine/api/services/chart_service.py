"""Chart creation service."""

from __future__ import annotations

from typing import Any

from engines.analysis_engine.api.schemas import CreateChartRequest
from engines.analysis_engine.api.services.store import (
    ChartRecord,
    ResourceStore,
    new_id,
)


def default_luck_block() -> dict[str, Any]:
    """Deterministic default luck timeline for API chart creation."""
    return {
        "current_age": 35,
        "da_yun_sequence": [
            {
                "index": 0,
                "stem": "Bính",
                "branch": "Dần",
                "start_age": 4,
                "end_age": 13,
                "label": "dy0",
            },
            {
                "index": 1,
                "stem": "Đinh",
                "branch": "Mão",
                "start_age": 14,
                "end_age": 23,
                "label": "dy1",
            },
            {
                "index": 2,
                "stem": "Mậu",
                "branch": "Thìn",
                "start_age": 24,
                "end_age": 33,
                "label": "dy2",
            },
            {
                "index": 3,
                "stem": "Kỷ",
                "branch": "Tỵ",
                "start_age": 34,
                "end_age": 43,
                "label": "dy3",
            },
        ],
        "liu_nian": {"stem": "Giáp", "branch": "Thìn", "year": 2024, "label": "ln"},
        "liu_yue": {"stem": "Bính", "branch": "Dần", "month": 2, "label": "ly"},
        "liu_ri": {"stem": "Mậu", "branch": "Ngọ", "day": 10, "label": "lr"},
        "liu_shi": {"stem": "Nhâm", "branch": "Tý", "hour": 1, "label": "ls"},
    }


class ChartService:
    """Create and read chart snapshots."""

    def __init__(self, store: ResourceStore) -> None:
        self._store = store

    def create(self, body: CreateChartRequest) -> ChartRecord:
        """Create a chart resource from request facts."""
        chart_id = new_id("cht")
        chart: dict[str, Any] = {
            "day_master": body.day_master,
            "gender": body.gender,
            "luck": body.luck or default_luck_block(),
            "stems": {
                "year": "Canh",
                "month": "Bính",
                "day": body.day_master,
                "hour": "Mậu",
            },
        }
        calendar: dict[str, Any] = {
            "year": body.year,
            "month": body.month,
            "day": body.day,
            "hour": body.hour,
            "minute": body.minute if body.minute is not None else 0,
            "timezone": body.timezone,
        }
        metadata = {
            "full_name": body.full_name,
            **dict(body.metadata),
        }
        return self._store.put_chart(
            ChartRecord(
                chart_id=chart_id,
                chart=chart,
                calendar=calendar,
                metadata=metadata,
            )
        )

    def get(self, chart_id: str) -> ChartRecord:
        """Return a stored chart."""
        return self._store.get_chart(chart_id)
