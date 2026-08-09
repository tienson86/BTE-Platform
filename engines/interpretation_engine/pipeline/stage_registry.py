"""Canonical stage catalog for the IX-1 Interpretation Pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from engines.interpretation_engine.pipeline.diagnostics import (
    CanonicalInterpretationPipelineError,
    InterpretationDependencyViolationError,
)

PIPELINE_ID = "canonical_interpretation_pipeline"
PIPELINE_VERSION = "1.0.0"

STAGE_FOUNDATION = "foundation"
STAGE_KNOWLEDGE = "knowledge_selection"
STAGE_COMPOSITION = "composition"
STAGE_REPORT = "report"
STAGE_AI_REWRITE = "ai_rewrite"

CANONICAL_STAGE_ORDER: tuple[str, ...] = (
    STAGE_FOUNDATION,
    STAGE_KNOWLEDGE,
    STAGE_COMPOSITION,
    STAGE_REPORT,
    STAGE_AI_REWRITE,
)

ACTIVE_INTERPRETATION_STAGES: tuple[str, ...] = (
    STAGE_FOUNDATION,
    STAGE_KNOWLEDGE,
    STAGE_COMPOSITION,
)

INACTIVE_FUTURE_STAGES: tuple[str, ...] = (
    STAGE_REPORT,
    STAGE_AI_REWRITE,
)


@dataclass(frozen=True, slots=True)
class InterpretationStageRecord:
    """Immutable catalog entry for one interpretation pipeline stage."""

    stage_id: str
    component: str
    version: str
    dependencies: tuple[str, ...]
    consumed_inputs: tuple[str, ...]
    published_outputs: tuple[str, ...]
    enabled: bool
    package_id: str | None = None

    def to_dict(self) -> dict[str, object]:
        """Serialize the catalog record."""
        return {
            "stage_id": self.stage_id,
            "component": self.component,
            "version": self.version,
            "dependencies": list(self.dependencies),
            "consumed_inputs": list(self.consumed_inputs),
            "published_outputs": list(self.published_outputs),
            "enabled": self.enabled,
            "package_id": self.package_id,
        }


def _default_records() -> tuple[InterpretationStageRecord, ...]:
    ax_inputs = (
        "canonical_analysis_result",
        "canonical_decision_result",
        "canonical_luck_result",
    )
    return (
        InterpretationStageRecord(
            stage_id=STAGE_FOUNDATION,
            component="interpretation_foundation",
            version="1.0.0",
            dependencies=(),
            consumed_inputs=ax_inputs,
            published_outputs=("foundation_result",),
            enabled=True,
        ),
        InterpretationStageRecord(
            stage_id=STAGE_KNOWLEDGE,
            component="knowledge_selection_engine",
            version="1.0.0",
            dependencies=(STAGE_FOUNDATION,),
            consumed_inputs=ax_inputs + ("foundation_result",),
            published_outputs=("knowledge_result",),
            enabled=True,
        ),
        InterpretationStageRecord(
            stage_id=STAGE_COMPOSITION,
            component="interpretation_composition_engine",
            version="1.0.0",
            dependencies=(STAGE_FOUNDATION, STAGE_KNOWLEDGE),
            consumed_inputs=ax_inputs + ("foundation_result", "knowledge_result"),
            published_outputs=("composition_result",),
            enabled=True,
        ),
        InterpretationStageRecord(
            stage_id=STAGE_REPORT,
            component="report_engine",
            version="1.0.0",
            dependencies=(STAGE_COMPOSITION,),
            consumed_inputs=("composition_result",),
            published_outputs=("report_result",),
            enabled=False,
        ),
        InterpretationStageRecord(
            stage_id=STAGE_AI_REWRITE,
            component="ai_rewrite_engine",
            version="1.0.0",
            dependencies=(STAGE_COMPOSITION,),
            consumed_inputs=("composition_result",),
            published_outputs=("rewrite_result",),
            enabled=False,
        ),
    )


class InterpretationStageRegistry:
    """Read-only registry of Canonical Interpretation Pipeline stages."""

    def __init__(self, records: Iterable[InterpretationStageRecord] | None = None) -> None:
        """Load default or injected catalog records."""
        catalog = tuple(records) if records is not None else _default_records()
        ids = [item.stage_id for item in catalog]
        if len(ids) != len(set(ids)):
            raise CanonicalInterpretationPipelineError("duplicate_stage_id")
        by_id = {item.stage_id: item for item in catalog}
        ordered = tuple(
            by_id[stage_id] for stage_id in CANONICAL_STAGE_ORDER if stage_id in by_id
        )
        extra = tuple(item for item in catalog if item.stage_id not in CANONICAL_STAGE_ORDER)
        self._records = ordered + extra
        self._by_id = {item.stage_id: item for item in self._records}

    @classmethod
    def default(cls) -> InterpretationStageRegistry:
        """Return the frozen default catalog."""
        return cls()

    def get(self, stage_id: str) -> InterpretationStageRecord:
        """Return one stage record or raise."""
        try:
            return self._by_id[stage_id]
        except KeyError as exc:
            raise InterpretationDependencyViolationError(f"unknown_stage:{stage_id}") from exc

    def disabled_stage_ids(self) -> tuple[str, ...]:
        """Return registered but inactive stage identifiers."""
        return tuple(item.stage_id for item in self._records if not item.enabled)

    def resolve_order(self, requested: Sequence[str]) -> tuple[str, ...]:
        """Return requested enabled stages in dependency order."""
        requested_set = set(requested)
        unknown = requested_set - set(self._by_id)
        if unknown:
            raise InterpretationDependencyViolationError(
                f"unknown_stages:{','.join(sorted(unknown))}"
            )
        ordered: list[str] = []
        for stage_id in CANONICAL_STAGE_ORDER:
            if stage_id not in requested_set:
                continue
            record = self.get(stage_id)
            if not record.enabled:
                continue
            missing = [dep for dep in record.dependencies if dep not in ordered]
            if missing:
                raise InterpretationDependencyViolationError(
                    f"missing_inputs:{stage_id}:{','.join(missing)}"
                )
            ordered.append(stage_id)
        return tuple(ordered)

    def to_list(self) -> list[dict[str, object]]:
        """Serialize the full registry."""
        return [item.to_dict() for item in self._records]
