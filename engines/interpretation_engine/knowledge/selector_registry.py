"""Deterministic IE-2 selector registry."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from engines.interpretation_engine.knowledge.composition_context import (
    COMPOSITION_VERSION,
    CompositionError,
)

SELECTOR_KNOWLEDGE = "knowledge"
SELECTOR_EVIDENCE = "evidence"
SELECTOR_REASONING = "reasoning"
SELECTOR_TEMPLATE = "template"
SELECTOR_PLACEHOLDER = "placeholder"
SELECTOR_SENTENCE_CANDIDATE = "sentence_candidate"

CANONICAL_SELECTOR_ORDER: tuple[str, ...] = (
    SELECTOR_KNOWLEDGE,
    SELECTOR_EVIDENCE,
    SELECTOR_REASONING,
    SELECTOR_TEMPLATE,
    SELECTOR_PLACEHOLDER,
    SELECTOR_SENTENCE_CANDIDATE,
)


@dataclass(frozen=True, slots=True)
class SelectorRecord:
    """Immutable catalog entry for one knowledge-selection stage."""

    selector_id: str
    component: str
    version: str
    dependencies: tuple[str, ...]
    consumed_inputs: tuple[str, ...]
    published_outputs: tuple[str, ...]
    enabled: bool
    deterministic: bool

    def to_dict(self) -> dict[str, object]:
        """Serialize the selector catalog record."""
        return {
            "selector_id": self.selector_id,
            "component": self.component,
            "version": self.version,
            "dependencies": list(self.dependencies),
            "consumed_inputs": list(self.consumed_inputs),
            "published_outputs": list(self.published_outputs),
            "enabled": self.enabled,
            "deterministic": self.deterministic,
        }


def _record(
    selector_id: str,
    *,
    dependencies: tuple[str, ...],
    consumed_inputs: tuple[str, ...],
    published_outputs: tuple[str, ...],
) -> SelectorRecord:
    return SelectorRecord(
        selector_id=selector_id,
        component=f"{selector_id}_selector",
        version=COMPOSITION_VERSION,
        dependencies=dependencies,
        consumed_inputs=consumed_inputs,
        published_outputs=published_outputs,
        enabled=True,
        deterministic=True,
    )


def _default_records() -> tuple[SelectorRecord, ...]:
    upstream = (
        "canonical_analysis_result",
        "canonical_decision_result",
        "canonical_luck_result",
        "interpretation_context",
    )
    return (
        _record(
            SELECTOR_KNOWLEDGE,
            dependencies=(),
            consumed_inputs=upstream,
            published_outputs=("knowledge_selection",),
        ),
        _record(
            SELECTOR_EVIDENCE,
            dependencies=(SELECTOR_KNOWLEDGE,),
            consumed_inputs=upstream + ("knowledge_selection",),
            published_outputs=("evidence_selection",),
        ),
        _record(
            SELECTOR_REASONING,
            dependencies=(SELECTOR_KNOWLEDGE,),
            consumed_inputs=upstream + ("knowledge_selection",),
            published_outputs=("reasoning_selection",),
        ),
        _record(
            SELECTOR_TEMPLATE,
            dependencies=(SELECTOR_KNOWLEDGE,),
            consumed_inputs=upstream + ("knowledge_selection",),
            published_outputs=("template_selection",),
        ),
        _record(
            SELECTOR_PLACEHOLDER,
            dependencies=(SELECTOR_KNOWLEDGE, SELECTOR_TEMPLATE),
            consumed_inputs=upstream + ("knowledge_selection", "template_selection"),
            published_outputs=("placeholder_bindings",),
        ),
        _record(
            SELECTOR_SENTENCE_CANDIDATE,
            dependencies=(
                SELECTOR_KNOWLEDGE,
                SELECTOR_EVIDENCE,
                SELECTOR_REASONING,
                SELECTOR_TEMPLATE,
                SELECTOR_PLACEHOLDER,
            ),
            consumed_inputs=(
                "knowledge_selection",
                "evidence_selection",
                "reasoning_selection",
                "template_selection",
                "placeholder_bindings",
            ),
            published_outputs=("sentence_candidates",),
        ),
    )


class SelectorRegistry:
    """Read-only catalog of IE-2 selectors. All stages are deterministic."""

    def __init__(self, records: Iterable[SelectorRecord] | None = None) -> None:
        """Load default or injected selector records."""
        catalog = tuple(records) if records is not None else _default_records()
        ids = [item.selector_id for item in catalog]
        if len(ids) != len(set(ids)):
            raise CompositionError("duplicate_selector_id")
        by_id = {item.selector_id: item for item in catalog}
        ordered = tuple(
            by_id[selector_id]
            for selector_id in CANONICAL_SELECTOR_ORDER
            if selector_id in by_id
        )
        extra = tuple(item for item in catalog if item.selector_id not in CANONICAL_SELECTOR_ORDER)
        self._records = ordered + extra
        self._by_id = {item.selector_id: item for item in self._records}

    @classmethod
    def default(cls) -> SelectorRegistry:
        """Return the frozen default selector catalog."""
        return cls()

    def get(self, selector_id: str) -> SelectorRecord:
        """Return one selector record or raise."""
        try:
            return self._by_id[selector_id]
        except KeyError as exc:
            raise CompositionError(f"unknown_selector:{selector_id}") from exc

    def registered_ids(self) -> tuple[str, ...]:
        """Return selector identifiers in canonical order."""
        return tuple(item.selector_id for item in self._records)

    def resolve_order(self, requested: Sequence[str] | None = None) -> tuple[str, ...]:
        """Return requested selectors in dependency order."""
        requested_ids = tuple(requested) if requested is not None else self.registered_ids()
        requested_set = set(requested_ids)
        unknown = requested_set - set(self._by_id)
        if unknown:
            raise CompositionError(f"unknown_selectors:{','.join(sorted(unknown))}")
        ordered: list[str] = []
        for selector_id in CANONICAL_SELECTOR_ORDER:
            if selector_id not in requested_set:
                continue
            record = self.get(selector_id)
            missing = [dep for dep in record.dependencies if dep not in requested_set]
            if missing:
                raise CompositionError(f"missing_dependencies:{selector_id}:{','.join(missing)}")
            if any(dep not in ordered for dep in record.dependencies):
                raise CompositionError(f"dependency_order:{selector_id}")
            ordered.append(selector_id)
        return tuple(ordered)

    def to_list(self) -> list[dict[str, object]]:
        """Serialize the full selector registry."""
        return [item.to_dict() for item in self._records]
