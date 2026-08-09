"""Deterministic IE-3 composition stage registry."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from engines.interpretation_engine.composition.composition_context import (
    ASSEMBLY_VERSION,
    AssemblyError,
)

STAGE_SECTION = "section_builder"
STAGE_CHAPTER = "chapter_builder"
STAGE_FLOW = "flow_optimizer"
STAGE_CROSS_REFERENCE = "cross_reference_builder"
STAGE_ASSEMBLY = "assembly"

CANONICAL_STAGE_ORDER: tuple[str, ...] = (
    STAGE_SECTION,
    STAGE_CHAPTER,
    STAGE_FLOW,
    STAGE_CROSS_REFERENCE,
    STAGE_ASSEMBLY,
)


@dataclass(frozen=True, slots=True)
class CompositionStageRecord:
    """Immutable catalog entry for one assembly stage."""

    stage_id: str
    component: str
    version: str
    dependencies: tuple[str, ...]
    consumed_inputs: tuple[str, ...]
    published_outputs: tuple[str, ...]
    enabled: bool
    deterministic: bool

    def to_dict(self) -> dict[str, object]:
        """Serialize the stage catalog record."""
        return {
            "stage_id": self.stage_id,
            "component": self.component,
            "version": self.version,
            "dependencies": list(self.dependencies),
            "consumed_inputs": list(self.consumed_inputs),
            "published_outputs": list(self.published_outputs),
            "enabled": self.enabled,
            "deterministic": self.deterministic,
        }


def _record(
    stage_id: str,
    *,
    dependencies: tuple[str, ...],
    consumed_inputs: tuple[str, ...],
    published_outputs: tuple[str, ...],
) -> CompositionStageRecord:
    return CompositionStageRecord(
        stage_id=stage_id,
        component=stage_id,
        version=ASSEMBLY_VERSION,
        dependencies=dependencies,
        consumed_inputs=consumed_inputs,
        published_outputs=published_outputs,
        enabled=True,
        deterministic=True,
    )


def _default_records() -> tuple[CompositionStageRecord, ...]:
    upstream = (
        "interpretation_context",
        "composition_result",
        "sentence_candidates",
        "canonical_analysis_result",
        "canonical_decision_result",
        "canonical_luck_result",
    )
    return (
        _record(
            STAGE_SECTION,
            dependencies=(),
            consumed_inputs=upstream,
            published_outputs=("sections",),
        ),
        _record(
            STAGE_CHAPTER,
            dependencies=(STAGE_SECTION,),
            consumed_inputs=("sections",),
            published_outputs=("chapters",),
        ),
        _record(
            STAGE_FLOW,
            dependencies=(STAGE_SECTION, STAGE_CHAPTER),
            consumed_inputs=("sections", "chapters"),
            published_outputs=("flow_plan",),
        ),
        _record(
            STAGE_CROSS_REFERENCE,
            dependencies=(STAGE_SECTION, STAGE_CHAPTER),
            consumed_inputs=("sections", "chapters", "composition_result"),
            published_outputs=("cross_references",),
        ),
        _record(
            STAGE_ASSEMBLY,
            dependencies=(STAGE_SECTION, STAGE_CHAPTER, STAGE_FLOW, STAGE_CROSS_REFERENCE),
            consumed_inputs=("sections", "chapters", "flow_plan", "cross_references"),
            published_outputs=("canonical_interpretation_result",),
        ),
    )


class CompositionRegistry:
    """Read-only catalog of IE-3 assembly stages."""

    def __init__(self, records: Iterable[CompositionStageRecord] | None = None) -> None:
        """Load default or injected stage records."""
        catalog = tuple(records) if records is not None else _default_records()
        ids = [item.stage_id for item in catalog]
        if len(ids) != len(set(ids)):
            raise AssemblyError("duplicate_stage_id")
        by_id = {item.stage_id: item for item in catalog}
        ordered = tuple(
            by_id[stage_id] for stage_id in CANONICAL_STAGE_ORDER if stage_id in by_id
        )
        extra = tuple(item for item in catalog if item.stage_id not in CANONICAL_STAGE_ORDER)
        self._records = ordered + extra
        self._by_id = {item.stage_id: item for item in self._records}

    @classmethod
    def default(cls) -> CompositionRegistry:
        """Return the frozen default assembly catalog."""
        return cls()

    def get(self, stage_id: str) -> CompositionStageRecord:
        """Return one stage record or raise."""
        try:
            return self._by_id[stage_id]
        except KeyError as exc:
            raise AssemblyError(f"unknown_stage:{stage_id}") from exc

    def registered_ids(self) -> tuple[str, ...]:
        """Return stage identifiers in canonical order."""
        return tuple(item.stage_id for item in self._records)

    def resolve_order(self, requested: Sequence[str] | None = None) -> tuple[str, ...]:
        """Return requested stages in dependency order."""
        requested_ids = tuple(requested) if requested is not None else self.registered_ids()
        requested_set = set(requested_ids)
        unknown = requested_set - set(self._by_id)
        if unknown:
            raise AssemblyError(f"unknown_stages:{','.join(sorted(unknown))}")
        ordered: list[str] = []
        for stage_id in CANONICAL_STAGE_ORDER:
            if stage_id not in requested_set:
                continue
            record = self.get(stage_id)
            missing = [dep for dep in record.dependencies if dep not in requested_set]
            if missing:
                raise AssemblyError(f"missing_dependencies:{stage_id}:{','.join(missing)}")
            if any(dep not in ordered for dep in record.dependencies):
                raise AssemblyError(f"dependency_order:{stage_id}")
            ordered.append(stage_id)
        return tuple(ordered)

    def to_list(self) -> list[dict[str, object]]:
        """Serialize the full composition registry."""
        return [item.to_dict() for item in self._records]
