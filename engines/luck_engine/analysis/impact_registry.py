"""Deterministic Luck Analysis impact stage registry."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from engines.luck_engine.analysis_constants import (
    ANALYSIS_VERSION,
    CANONICAL_IMPACT_ORDER,
    STAGE_PATTERN,
    STAGE_PATTERN_EVALUATION,
    STAGE_SEASONAL,
    STAGE_STRENGTH,
    STAGE_TEMPERATURE,
    STAGE_USEFUL_GOD,
)
from engines.luck_engine.exceptions import ImpactRegistryError


@dataclass(frozen=True, slots=True)
class ImpactStageRecord:
    """Immutable catalog entry for one impact stage."""

    stage_id: str
    dependencies: tuple[str, ...]
    consumed_inputs: tuple[str, ...]
    published_outputs: tuple[str, ...]
    version: str
    enabled: bool

    def to_dict(self) -> dict[str, Any]:
        """Serialize a registry record."""
        return {
            "stage_id": self.stage_id,
            "dependencies": list(self.dependencies),
            "consumed_inputs": list(self.consumed_inputs),
            "published_outputs": list(self.published_outputs),
            "version": self.version,
            "enabled": self.enabled,
        }


def _default_records() -> tuple[ImpactStageRecord, ...]:
    version = ANALYSIS_VERSION
    return (
        ImpactStageRecord(
            stage_id=STAGE_SEASONAL,
            dependencies=(),
            consumed_inputs=(
                "timeline",
                "natal_chart.month_pillar",
                "analysis.seasonal",
            ),
            published_outputs=(STAGE_SEASONAL,),
            version=version,
            enabled=True,
        ),
        ImpactStageRecord(
            stage_id=STAGE_STRENGTH,
            dependencies=(STAGE_SEASONAL,),
            consumed_inputs=(
                "timeline",
                "natal_chart.day_pillar",
                "analysis.strength",
                STAGE_SEASONAL,
            ),
            published_outputs=(STAGE_STRENGTH,),
            version=version,
            enabled=True,
        ),
        ImpactStageRecord(
            stage_id=STAGE_TEMPERATURE,
            dependencies=(STAGE_SEASONAL, STAGE_STRENGTH),
            consumed_inputs=(
                "timeline",
                "natal_chart.month_pillar",
                "natal_chart.day_pillar",
                "analysis.temperature",
                STAGE_STRENGTH,
            ),
            published_outputs=(STAGE_TEMPERATURE,),
            version=version,
            enabled=True,
        ),
        ImpactStageRecord(
            stage_id=STAGE_PATTERN,
            dependencies=(STAGE_TEMPERATURE,),
            consumed_inputs=(
                "timeline",
                "analysis.pattern",
                STAGE_TEMPERATURE,
            ),
            published_outputs=(STAGE_PATTERN,),
            version=version,
            enabled=True,
        ),
        ImpactStageRecord(
            stage_id=STAGE_PATTERN_EVALUATION,
            dependencies=(STAGE_PATTERN,),
            consumed_inputs=(
                "timeline",
                "analysis.pattern_evaluation",
                STAGE_PATTERN,
            ),
            published_outputs=(STAGE_PATTERN_EVALUATION,),
            version=version,
            enabled=True,
        ),
        ImpactStageRecord(
            stage_id=STAGE_USEFUL_GOD,
            dependencies=(STAGE_PATTERN_EVALUATION,),
            consumed_inputs=(
                "timeline",
                "analysis.useful_god",
                "decision.final_useful_god",
                STAGE_PATTERN_EVALUATION,
            ),
            published_outputs=(STAGE_USEFUL_GOD,),
            version=version,
            enabled=True,
        ),
    )


class ImpactRegistry:
    """Read-only registry of Luck Analysis impact stages."""

    def __init__(self, records: Iterable[ImpactStageRecord] | None = None) -> None:
        """Load default or injected catalog records."""
        catalog = tuple(records) if records is not None else _default_records()
        ids = [item.stage_id for item in catalog]
        if len(ids) != len(set(ids)):
            raise ImpactRegistryError("duplicate_stage_id")
        by_id = {item.stage_id: item for item in catalog}
        ordered = tuple(by_id[stage_id] for stage_id in CANONICAL_IMPACT_ORDER if stage_id in by_id)
        extra = tuple(item for item in catalog if item.stage_id not in CANONICAL_IMPACT_ORDER)
        self._records = ordered + extra
        self._by_id = {item.stage_id: item for item in self._records}

    def get(self, stage_id: str) -> ImpactStageRecord:
        """Return one stage record or raise."""
        try:
            return self._by_id[stage_id]
        except KeyError as exc:
            raise ImpactRegistryError(f"unknown_stage:{stage_id}") from exc

    def active_stages(self) -> tuple[ImpactStageRecord, ...]:
        """Return enabled stages in canonical order."""
        return tuple(item for item in self._records if item.enabled)

    def canonical_order(self) -> tuple[str, ...]:
        """Return enabled stage ids in dependency order."""
        return tuple(item.stage_id for item in self.active_stages())

    def to_list(self) -> list[dict[str, Any]]:
        """Serialize the full registry."""
        return [item.to_dict() for item in self._records]
