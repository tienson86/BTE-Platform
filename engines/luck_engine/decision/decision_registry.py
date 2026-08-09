"""Deterministic Luck Decision stage registry."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from engines.luck_engine.decision_constants import (
    CANONICAL_DECISION_ORDER,
    DECISION_VERSION,
    OUTPUT_AUDIT,
    OUTPUT_CONFIDENCE,
    OUTPUT_OPPORTUNITY,
    OUTPUT_OVERALL,
    OUTPUT_PRIORITY,
    OUTPUT_REASONING,
    OUTPUT_RISK,
    OUTPUT_TRACE,
    OUTPUT_VERSION,
    STAGE_CONFIDENCE,
    STAGE_OPPORTUNITY,
    STAGE_PRIORITY,
    STAGE_PUBLICATION,
    STAGE_RISK,
)
from engines.luck_engine.exceptions import LuckDecisionRegistryError


@dataclass(frozen=True, slots=True)
class LuckDecisionStageRecord:
    """Immutable catalog entry for one luck decision stage."""

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


def _default_records() -> tuple[LuckDecisionStageRecord, ...]:
    version = DECISION_VERSION
    return (
        LuckDecisionStageRecord(
            stage_id=STAGE_OPPORTUNITY,
            dependencies=(),
            consumed_inputs=("luck_analysis.impacts", "timeline"),
            published_outputs=(OUTPUT_OPPORTUNITY,),
            version=version,
            enabled=True,
        ),
        LuckDecisionStageRecord(
            stage_id=STAGE_RISK,
            dependencies=(OUTPUT_OPPORTUNITY,),
            consumed_inputs=("luck_analysis.impacts", OUTPUT_OPPORTUNITY),
            published_outputs=(OUTPUT_RISK,),
            version=version,
            enabled=True,
        ),
        LuckDecisionStageRecord(
            stage_id=STAGE_CONFIDENCE,
            dependencies=(OUTPUT_OPPORTUNITY, OUTPUT_RISK),
            consumed_inputs=(
                "luck_analysis.impacts.confidence",
                "analysis.success",
                "decision.success",
                OUTPUT_OPPORTUNITY,
                OUTPUT_RISK,
            ),
            published_outputs=(OUTPUT_CONFIDENCE,),
            version=version,
            enabled=True,
        ),
        LuckDecisionStageRecord(
            stage_id=STAGE_PRIORITY,
            dependencies=(OUTPUT_OPPORTUNITY, OUTPUT_RISK, OUTPUT_CONFIDENCE),
            consumed_inputs=(OUTPUT_OPPORTUNITY, OUTPUT_RISK, OUTPUT_CONFIDENCE),
            published_outputs=(OUTPUT_PRIORITY,),
            version=version,
            enabled=True,
        ),
        LuckDecisionStageRecord(
            stage_id=STAGE_PUBLICATION,
            dependencies=(OUTPUT_PRIORITY,),
            consumed_inputs=(
                OUTPUT_OPPORTUNITY,
                OUTPUT_RISK,
                OUTPUT_CONFIDENCE,
                OUTPUT_PRIORITY,
            ),
            published_outputs=(
                OUTPUT_REASONING,
                OUTPUT_TRACE,
                OUTPUT_AUDIT,
                OUTPUT_OVERALL,
                OUTPUT_VERSION,
            ),
            version=version,
            enabled=True,
        ),
    )


class LuckDecisionRegistry:
    """Read-only registry of Luck Decision stages."""

    def __init__(self, records: Iterable[LuckDecisionStageRecord] | None = None) -> None:
        """Load default or injected catalog records."""
        catalog = tuple(records) if records is not None else _default_records()
        ids = [item.stage_id for item in catalog]
        if len(ids) != len(set(ids)):
            raise LuckDecisionRegistryError("duplicate_stage_id")
        by_id = {item.stage_id: item for item in catalog}
        ordered = tuple(
            by_id[stage_id] for stage_id in CANONICAL_DECISION_ORDER if stage_id in by_id
        )
        extra = tuple(item for item in catalog if item.stage_id not in CANONICAL_DECISION_ORDER)
        self._records = ordered + extra
        self._by_id = {item.stage_id: item for item in self._records}

    def get(self, stage_id: str) -> LuckDecisionStageRecord:
        """Return one stage record or raise."""
        try:
            return self._by_id[stage_id]
        except KeyError as exc:
            raise LuckDecisionRegistryError(f"unknown_stage:{stage_id}") from exc

    def active_stages(self) -> tuple[LuckDecisionStageRecord, ...]:
        """Return enabled stages in canonical order."""
        return tuple(item for item in self._records if item.enabled)

    def canonical_order(self) -> tuple[str, ...]:
        """Return enabled stage ids in dependency order."""
        return tuple(item.stage_id for item in self.active_stages())

    def to_list(self) -> list[dict[str, Any]]:
        """Serialize the full registry."""
        return [item.to_dict() for item in self._records]
