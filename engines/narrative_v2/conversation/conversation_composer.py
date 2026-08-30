"""Conversation Composer — InterpretationNarrative → ConversationNarrative.

Rewrites flow only. Does not rewrite Meaning.
"""

from __future__ import annotations

import logging

from engines.narrative_v2.conversation.conversation_bridge import is_duplicate, novel_sentences
from engines.narrative_v2.conversation.conversation_context import (
    STATUS_INSUFFICIENT,
    STATUS_PARTIAL,
    ConversationNarrative,
    ConversationReference,
)
from engines.narrative_v2.conversation.conversation_errors import ConversationError
from engines.narrative_v2.conversation.conversation_flow import (
    join_sentences,
    meaning_hash,
)
from engines.narrative_v2.conversation.conversation_registry import FLOW_STAGES, ConversationRegistry
from engines.narrative_v2.conversation.conversation_transition import apply_transition
from engines.narrative_v2.conversation.conversation_validator import ConversationValidator
from engines.narrative_v2.interpretation.interpretation_model import InterpretationNarrative
from engines.narrative_v2.rewrite.rewrite_context import CommercialRewriteContext

logger = logging.getLogger(__name__)

CONVERSATION_VERSION = "nimp07a.1.0"

_CONTEXT_METADATA: tuple[tuple[str, str], ...] = (
    ("shadow_mode", "true"),
    ("replaces_pack05", "false"),
    ("portal_connected", "false"),
    ("layer", "conversation"),
    ("conversation_version", CONVERSATION_VERSION),
)


class ConversationComposer:
    """Turn isolated interpretation stages into one conversation flow."""

    def __init__(
        self,
        *,
        registry: ConversationRegistry | None = None,
        validator: ConversationValidator | None = None,
    ) -> None:
        self._registry = registry or ConversationRegistry()
        self._validator = validator or ConversationValidator()

    def compose(
        self,
        rewrite_context: object,
        interpretation: object,
    ) -> ConversationNarrative:
        """Compose ConversationNarrative from rewrite + interpretation only."""
        rewrite = _require_rewrite(rewrite_context)
        source = _require_interpretation(interpretation)
        if source.status == "insufficient":
            logger.info("conversation.insufficient", extra={"reason": "no_primary_insight"})
            conversation = _insufficient(_CONTEXT_METADATA)
            self._validator.assert_valid(conversation, source, rewrite)
            return conversation
        conversation = _assemble(source, rewrite, self._registry)
        logger.info(
            "conversation.composed",
            extra={"status": conversation.status, "merged_closing": conversation.closing is None},
        )
        self._validator.assert_valid(conversation, source, rewrite)
        return conversation


def _require_rewrite(value: object) -> CommercialRewriteContext:
    if isinstance(value, CommercialRewriteContext):
        return value
    raise ConversationError("Conversation Composer accepts CommercialRewriteContext only")


def _require_interpretation(value: object) -> InterpretationNarrative:
    if isinstance(value, InterpretationNarrative):
        return value
    raise ConversationError("Conversation Composer accepts InterpretationNarrative only")


def _insufficient(base_meta: tuple[tuple[str, str], ...]) -> ConversationNarrative:
    return ConversationNarrative(
        observation=None,
        reasoning=None,
        meaning=None,
        impact=None,
        recommendation=None,
        closing=None,
        flow="",
        references=(),
        metadata=base_meta + (("status_reason", "no_primary_insight"),),
        status=STATUS_INSUFFICIENT,
    )


def _assemble(
    source: InterpretationNarrative,
    rewrite: CommercialRewriteContext,
    registry: ConversationRegistry,
) -> ConversationNarrative:
    del rewrite
    closing = None if is_duplicate(source.closing, source.observation) else source.closing
    flow, emitted_from, merged = _build_flow(source, closing, registry)
    meta = _CONTEXT_METADATA + (
        ("meaning_hash", meaning_hash(source.meaning)),
        ("merged_closing", "true" if closing is None and source.closing else "false"),
        ("flow_stages", ",".join(emitted_from)),
        ("merged_stages", ",".join(merged)),
    )
    return ConversationNarrative(
        observation=source.observation,
        reasoning=source.reasoning,
        meaning=source.meaning,
        impact=source.impact,
        recommendation=source.recommendation,
        closing=closing,
        flow=flow,
        references=_copy_references(source, closing),
        metadata=meta,
        status=STATUS_PARTIAL,
    )


def _build_flow(
    source: InterpretationNarrative,
    closing: str | None,
    registry: ConversationRegistry,
) -> tuple[str, tuple[str, ...], tuple[str, ...]]:
    spoken: list[str] = []
    chunks: list[str] = []
    emitted_from: list[str] = []
    merged: list[str] = []
    previous: str | None = None
    for stage in FLOW_STAGES:
        raw = closing if stage == "closing" else getattr(source, stage)
        if not isinstance(raw, str) or not raw.strip():
            if stage == "closing" and source.closing:
                merged.append("closing")
            continue
        novel = novel_sentences(raw, tuple(spoken))
        if not novel:
            merged.append(stage)
            continue
        chunk = join_sentences(novel)
        if previous is None:
            chunks.append(chunk)
        else:
            connector = registry.connector(previous, stage)
            chunks.append(apply_transition(connector, chunk))
        spoken.extend(novel)
        emitted_from.append(stage)
        previous = stage
    return join_sentences(tuple(chunks)), tuple(emitted_from), tuple(merged)


def _copy_references(
    source: InterpretationNarrative,
    closing: str | None,
) -> tuple[ConversationReference, ...]:
    copied: list[ConversationReference] = []
    for ref in source.references:
        if ref.field == "overview":
            continue
        if ref.field == "closing" and closing is None:
            continue
        copied.append(
            ConversationReference(
                field=ref.field,
                rewrite_ids=ref.rewrite_ids,
                knowledge_ids=ref.knowledge_ids,
                reasoning_ids=ref.reasoning_ids,
                evidence_ids=ref.evidence_ids,
            )
        )
    return tuple(copied)
