"""Deterministic Luck Timeline layer registry. No calculations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from engines.luck_engine.exceptions import TimelineRegistryError
from engines.luck_engine.timeline_constants import (
    LAYER_ANNUAL,
    LAYER_DAILY,
    LAYER_HOURLY,
    LAYER_MAJOR,
    LAYER_MONTHLY,
    LAYER_NATAL,
    LAYER_STATUS_ACTIVE,
    LAYER_STATUS_RESERVED,
    TIMELINE_VERSION,
)


@dataclass(frozen=True, slots=True)
class TimelineLayerRecord:
    """Immutable catalog entry for one timeline layer."""

    layer_id: str
    display_name: str
    vietnamese_name: str
    status: str
    parent_layer_id: str | None
    sequence: int
    published_output: str | None
    version: str = TIMELINE_VERSION

    def to_dict(self) -> dict[str, Any]:
        """Serialize a registry record."""
        return {
            "layer_id": self.layer_id,
            "display_name": self.display_name,
            "vietnamese_name": self.vietnamese_name,
            "status": self.status,
            "parent_layer_id": self.parent_layer_id,
            "sequence": self.sequence,
            "published_output": self.published_output,
            "version": self.version,
        }


CANONICAL_LAYER_ORDER: tuple[str, ...] = (
    LAYER_NATAL,
    LAYER_MAJOR,
    LAYER_ANNUAL,
    LAYER_MONTHLY,
    LAYER_DAILY,
    LAYER_HOURLY,
)

ACTIVE_TIMELINE_LAYERS: tuple[str, ...] = (
    LAYER_NATAL,
    LAYER_MAJOR,
    LAYER_ANNUAL,
    LAYER_MONTHLY,
)

RESERVED_TIMELINE_LAYERS: tuple[str, ...] = (
    LAYER_DAILY,
    LAYER_HOURLY,
)


def _default_records() -> tuple[TimelineLayerRecord, ...]:
    return (
        TimelineLayerRecord(
            layer_id=LAYER_NATAL,
            display_name="Natal Chart",
            vietnamese_name="Lá số gốc",
            status=LAYER_STATUS_ACTIVE,
            parent_layer_id=None,
            sequence=0,
            published_output="natal_chart",
        ),
        TimelineLayerRecord(
            layer_id=LAYER_MAJOR,
            display_name="Major Luck Cycle",
            vietnamese_name="Đại Vận",
            status=LAYER_STATUS_ACTIVE,
            parent_layer_id=LAYER_NATAL,
            sequence=1,
            published_output="major_cycles",
        ),
        TimelineLayerRecord(
            layer_id=LAYER_ANNUAL,
            display_name="Annual Luck",
            vietnamese_name="Lưu Niên",
            status=LAYER_STATUS_ACTIVE,
            parent_layer_id=LAYER_MAJOR,
            sequence=2,
            published_output="annual_cycles",
        ),
        TimelineLayerRecord(
            layer_id=LAYER_MONTHLY,
            display_name="Monthly Luck",
            vietnamese_name="Lưu Nguyệt",
            status=LAYER_STATUS_ACTIVE,
            parent_layer_id=LAYER_ANNUAL,
            sequence=3,
            published_output="monthly_cycles",
        ),
        TimelineLayerRecord(
            layer_id=LAYER_DAILY,
            display_name="Daily Luck",
            vietnamese_name="Lưu Nhật",
            status=LAYER_STATUS_RESERVED,
            parent_layer_id=LAYER_MONTHLY,
            sequence=4,
            published_output=None,
        ),
        TimelineLayerRecord(
            layer_id=LAYER_HOURLY,
            display_name="Hourly Luck",
            vietnamese_name="Lưu Thời",
            status=LAYER_STATUS_RESERVED,
            parent_layer_id=LAYER_DAILY,
            sequence=5,
            published_output=None,
        ),
    )


class TimelineRegistry:
    """Read-only registry of canonical luck timeline layers."""

    def __init__(self, records: Iterable[TimelineLayerRecord] | None = None) -> None:
        """Load default or injected catalog records."""
        catalog = tuple(records) if records is not None else _default_records()
        ids = [item.layer_id for item in catalog]
        if len(ids) != len(set(ids)):
            raise TimelineRegistryError("duplicate_layer_id")
        ordered = tuple(sorted(catalog, key=lambda item: (item.sequence, item.layer_id)))
        self._records = ordered
        self._by_id = {item.layer_id: item for item in ordered}

    def get(self, layer_id: str) -> TimelineLayerRecord:
        """Return one layer record or raise."""
        try:
            return self._by_id[layer_id]
        except KeyError as exc:
            raise TimelineRegistryError(f"unknown_layer:{layer_id}") from exc

    def is_active(self, layer_id: str) -> bool:
        """Return True when the layer is active in LE-1."""
        return self.get(layer_id).status == LAYER_STATUS_ACTIVE

    def is_reserved(self, layer_id: str) -> bool:
        """Return True when the layer is reserved."""
        return self.get(layer_id).status == LAYER_STATUS_RESERVED

    def active_layers(self) -> tuple[TimelineLayerRecord, ...]:
        """Return active layers in canonical order."""
        return tuple(item for item in self._records if item.status == LAYER_STATUS_ACTIVE)

    def reserved_layers(self) -> tuple[TimelineLayerRecord, ...]:
        """Return reserved layers in canonical order."""
        return tuple(item for item in self._records if item.status == LAYER_STATUS_RESERVED)

    def parent_of(self, layer_id: str) -> TimelineLayerRecord | None:
        """Return the parent layer record when declared."""
        parent_id = self.get(layer_id).parent_layer_id
        if parent_id is None:
            return None
        return self.get(parent_id)

    def to_list(self) -> list[dict[str, Any]]:
        """Serialize the full registry."""
        return [item.to_dict() for item in self._records]
