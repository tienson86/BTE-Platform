"""Summary Builder — CommercialRewriteContext → OverviewSummary.

Assembles rewrite units. Does not invent meaning. Does not concatenate domains.
"""

from __future__ import annotations

import logging

from engines.narrative_v2.rewrite.rewrite_context import CommercialRewriteContext
from engines.narrative_v2.rewrite.rewrite_item import RewriteItem
from engines.narrative_v2.summary.summary_errors import SummaryError
from engines.narrative_v2.summary.summary_formula import (
    headline_from_insight,
    join_sentences,
    split_sentences,
)
from engines.narrative_v2.summary.summary_model import (
    STATUS_INSUFFICIENT,
    STATUS_PARTIAL,
    OverviewSummary,
    SummaryReference,
)
from engines.narrative_v2.summary.summary_selector import InsightSelection, SummarySelector
from engines.narrative_v2.summary.summary_validator import SummaryValidator

logger = logging.getLogger(__name__)

SUMMARY_VERSION = "nimp06.1.0"

_CONTEXT_METADATA: tuple[tuple[str, str], ...] = (
    ("shadow_mode", "true"),
    ("replaces_pack05", "false"),
    ("portal_connected", "false"),
    ("layer", "summary"),
    ("summary_version", SUMMARY_VERSION),
    ("sentence_library", "runtime_gap"),
)


class SummaryBuilder:
    """Executive summary assembly. Shadow mode. No Presentation."""

    def __init__(
        self,
        *,
        selector: SummarySelector | None = None,
        validator: SummaryValidator | None = None,
    ) -> None:
        self._selector = selector or SummarySelector()
        self._validator = validator or SummaryValidator()

    def build(self, rewrite_context: object) -> OverviewSummary:
        """Assemble OverviewSummary from rewrite units only."""
        rewrite = _require_rewrite(rewrite_context)
        selection = self._selector.select(rewrite.items)
        if selection is None:
            logger.info("summary.insufficient", extra={"reason": "no_primary_insight"})
            summary = _insufficient(_CONTEXT_METADATA)
            self._validator.assert_valid(summary, rewrite)
            return summary
        summary = _assemble(selection, rewrite)
        logger.info(
            "summary.assembled",
            extra={
                "primary": dict(summary.metadata).get("primary_rewrite_id"),
                "status": summary.status,
            },
        )
        self._validator.assert_valid(summary, rewrite)
        return summary


def _require_rewrite(value: object) -> CommercialRewriteContext:
    if isinstance(value, CommercialRewriteContext):
        return value
    raise SummaryError("Summary Builder accepts CommercialRewriteContext only")


def _insufficient(base_meta: tuple[tuple[str, str], ...]) -> OverviewSummary:
    return OverviewSummary(
        headline=None,
        summary=None,
        identity=None,
        balance=None,
        conclusion=None,
        references=(),
        metadata=base_meta + (("status_reason", "no_primary_insight"),),
        status=STATUS_INSUFFICIENT,
    )


def _assemble(
    selection: InsightSelection,
    rewrite: CommercialRewriteContext,
) -> OverviewSummary:
    primary = selection.primary
    supporting = selection.supporting
    headline = headline_from_insight(primary.customer_language)
    summary_text = _summary_body(primary, supporting, headline)
    references: list[SummaryReference] = []
    if headline:
        references.append(_reference("headline", (primary,)))
    used_for_summary = [primary]
    if supporting is not None and summary_text:
        used_for_summary.append(supporting)
    if summary_text:
        references.append(_reference("summary", tuple(used_for_summary)))
    meta = _CONTEXT_METADATA + (
        ("primary_rewrite_id", primary.rewrite_id),
        ("primary_semantic_key", primary.semantic_key),
        ("primary_insight_count", "1"),
        ("identity_status", "unresolved"),
        ("balance_status", "unresolved"),
        ("conclusion_status", "omitted"),
    )
    if supporting is not None:
        meta = meta + (("supporting_rewrite_id", supporting.rewrite_id),)
    unresolved_keys = tuple(entry.semantic_key for entry in rewrite.unresolved)
    if unresolved_keys:
        meta = meta + (("rewrite_unresolved", ",".join(unresolved_keys)),)
    return OverviewSummary(
        headline=headline,
        summary=summary_text,
        identity=None,
        balance=None,
        conclusion=None,
        references=tuple(references),
        metadata=meta,
        status=STATUS_PARTIAL,
    )


def _summary_body(
    primary: RewriteItem,
    supporting: RewriteItem | None,
    headline: str | None,
) -> str | None:
    sentences: list[str] = []
    for sentence in split_sentences(primary.customer_language):
        if headline and sentence == headline:
            continue
        sentences.append(sentence)
    if supporting is not None:
        support_sentences = split_sentences(supporting.customer_language)
        if support_sentences:
            first = support_sentences[0]
            if first != headline and first not in sentences:
                sentences.append(first)
    trimmed = tuple(sentences[:4])
    if not trimmed:
        return None
    return join_sentences(trimmed)


def _reference(field: str, items: tuple[RewriteItem, ...]) -> SummaryReference:
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
            knowledge_ids.extend((ref.knowledge_id,))
            reasoning_ids.extend(ref.reasoning_ids)
            evidence_ids.extend(ref.evidence_ids)
    return SummaryReference(
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
