"""Interpretation Builder — CommercialRewriteContext → InterpretationNarrative.

Assembles a conversation flow from rewrite units. Does not invent meaning.
Does not generate Action.
"""

from __future__ import annotations

import logging

from engines.narrative_v2.rewrite.rewrite_context import CommercialRewriteContext
from engines.narrative_v2.rewrite.rewrite_item import RewriteItem
from engines.narrative_v2.interpretation.interpretation_errors import InterpretationError
from engines.narrative_v2.interpretation.interpretation_formula import (
    join_sentences,
    sentence_at,
    split_sentences,
)
from engines.narrative_v2.interpretation.interpretation_model import (
    FORMULA_STAGES,
    STATUS_INSUFFICIENT,
    STATUS_PARTIAL,
    CONTENT_FIELDS,
    InterpretationNarrative,
    InterpretationReference,
)
from engines.narrative_v2.interpretation.interpretation_selector import (
    InterpretationSelection,
    InterpretationSelector,
)
from engines.narrative_v2.interpretation.interpretation_validator import (
    InterpretationValidator,
)

logger = logging.getLogger(__name__)

INTERPRETATION_VERSION = "nimp07.1.0"

_CONTEXT_METADATA: tuple[tuple[str, str], ...] = (
    ("shadow_mode", "true"),
    ("replaces_pack05", "false"),
    ("portal_connected", "false"),
    ("layer", "interpretation"),
    ("interpretation_version", INTERPRETATION_VERSION),
    ("formula_stages", ",".join(FORMULA_STAGES)),
)


class InterpretationBuilder:
    """Customer interpretation assembly. Shadow mode. No Action. No Presentation."""

    def __init__(
        self,
        *,
        selector: InterpretationSelector | None = None,
        validator: InterpretationValidator | None = None,
    ) -> None:
        self._selector = selector or InterpretationSelector()
        self._validator = validator or InterpretationValidator()

    def build(self, rewrite_context: object) -> InterpretationNarrative:
        """Assemble InterpretationNarrative from rewrite units only."""
        rewrite = _require_rewrite(rewrite_context)
        selection = self._selector.select(rewrite.items)
        if selection is None:
            logger.info("interpretation.insufficient", extra={"reason": "no_primary_insight"})
            narrative = _insufficient(_CONTEXT_METADATA)
            self._validator.assert_valid(narrative, rewrite)
            return narrative
        narrative = _assemble(selection, rewrite)
        logger.info(
            "interpretation.assembled",
            extra={
                "primary": dict(narrative.metadata).get("primary_rewrite_id"),
                "status": narrative.status,
            },
        )
        self._validator.assert_valid(narrative, rewrite)
        return narrative


def _require_rewrite(value: object) -> CommercialRewriteContext:
    if isinstance(value, CommercialRewriteContext):
        return value
    raise InterpretationError("Interpretation Builder accepts CommercialRewriteContext only")


def _insufficient(base_meta: tuple[tuple[str, str], ...]) -> InterpretationNarrative:
    return InterpretationNarrative(
        overview=None,
        observation=None,
        reasoning=None,
        meaning=None,
        impact=None,
        recommendation=None,
        closing=None,
        references=(),
        metadata=base_meta + (("status_reason", "no_primary_insight"),),
        status=STATUS_INSUFFICIENT,
    )


def _assemble(
    selection: InterpretationSelection,
    rewrite: CommercialRewriteContext,
) -> InterpretationNarrative:
    primary = selection.primary
    supporting = selection.supporting
    primary_sentences = split_sentences(primary.customer_language)
    support_sentences = (
        split_sentences(supporting.customer_language) if supporting is not None else ()
    )
    observation = sentence_at(primary_sentences, 0)
    reasoning_text = sentence_at(support_sentences, 0)
    meaning = join_sentences(primary_sentences) if primary_sentences else None
    impact = sentence_at(primary_sentences, 1)
    recommendation = sentence_at(support_sentences, 1)
    closing = observation
    overview_parts = tuple(
        part for part in (observation, reasoning_text) if part is not None
    )
    overview = join_sentences(overview_parts) if overview_parts else None
    fields: dict[str, str | None] = {
        "overview": overview,
        "observation": observation,
        "reasoning": reasoning_text,
        "meaning": meaning,
        "impact": impact,
        "recommendation": recommendation,
        "closing": closing,
    }
    references: list[InterpretationReference] = []
    for field in CONTENT_FIELDS:
        text = fields[field]
        if not text:
            continue
        references.append(_reference(field, _items_for_field(field, primary, supporting)))
    rewrite_library = dict(rewrite.metadata).get("sentence_library", "runtime_gap")
    meta = _CONTEXT_METADATA + (
        ("primary_rewrite_id", primary.rewrite_id),
        ("primary_semantic_key", primary.semantic_key),
        ("primary_insight_count", "1"),
        ("sentence_library", rewrite_library),
    )
    if supporting is not None:
        meta = meta + (("supporting_rewrite_id", supporting.rewrite_id),)
    unresolved_keys = tuple(entry.semantic_key for entry in rewrite.unresolved)
    if unresolved_keys:
        meta = meta + (("rewrite_unresolved", ",".join(unresolved_keys)),)
    omitted = tuple(field for field in FORMULA_STAGES if not fields[field])
    if omitted:
        meta = meta + (("omitted_stages", ",".join(omitted)),)
    return InterpretationNarrative(
        overview=overview,
        observation=observation,
        reasoning=reasoning_text,
        meaning=meaning,
        impact=impact,
        recommendation=recommendation,
        closing=closing,
        references=tuple(references),
        metadata=meta,
        status=STATUS_PARTIAL,
    )


def _items_for_field(
    field: str,
    primary: RewriteItem,
    supporting: RewriteItem | None,
) -> tuple[RewriteItem, ...]:
    if field in {"reasoning", "recommendation"} and supporting is not None:
        return (supporting,)
    if field == "overview" and supporting is not None:
        return (primary, supporting)
    return (primary,)


def _reference(field: str, items: tuple[RewriteItem, ...]) -> InterpretationReference:
    rewrite_ids: list[str] = []
    knowledge_ids: list[str] = []
    reasoning_ids: list[str] = []
    evidence_ids: list[str] = []
    for item in items:
        rewrite_ids.append(item.rewrite_id)
        knowledge_ids.extend(item.source_knowledge_ids)
        reasoning_ids.extend(item.source_reasoning_ids)
        evidence_ids.extend(item.source_evidence_ids)
        for ref in item.references:
            knowledge_ids.append(ref.knowledge_id)
            reasoning_ids.extend(ref.reasoning_ids)
            evidence_ids.extend(ref.evidence_ids)
    return InterpretationReference(
        field=field,
        rewrite_ids=tuple(_unique(rewrite_ids)),
        knowledge_ids=tuple(_unique(knowledge_ids)),
        reasoning_ids=tuple(_unique(reasoning_ids)),
        evidence_ids=tuple(_unique(evidence_ids)),
    )


def _unique(values: list[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return tuple(ordered)
