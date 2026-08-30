"""Build DecisionItems from approved decision language assets."""

from __future__ import annotations

from engines.narrative_v2.action.action_context import DecisionContext
from engines.narrative_v2.action.decision_model import DecisionItem, DecisionReference
from engines.narrative_v2.action.decision_selector import DecisionSelector
from engines.narrative_v2.interpretation.interpretation_model import InterpretationNarrative
from engines.narrative_v2.language.sentence_asset import SentenceAsset
from engines.narrative_v2.language.sentence_library import SentenceLibrary
from engines.narrative_v2.rewrite.language_profile import LanguageProfile
from engines.narrative_v2.rewrite.rewrite_context import CommercialRewriteContext
from engines.narrative_v2.rewrite.rewrite_item import RewriteItem

STATUS_SELECTED = "selected"


class DecisionBuilder:
    """Create Decisions from approved assets. Does not invent astrology."""

    def __init__(
        self,
        *,
        selector: DecisionSelector | None = None,
        library: SentenceLibrary | None = None,
        profile: LanguageProfile | None = None,
    ) -> None:
        self._selector = selector or DecisionSelector()
        self._library = library or SentenceLibrary()
        self._profile = profile or LanguageProfile()

    def build(
        self,
        rewrite: CommercialRewriteContext,
        interpretation: InterpretationNarrative,
    ) -> DecisionContext:
        """Return selected Decisions, or an empty insufficient context."""
        eligible = self._selector.select(rewrite, interpretation)
        items: list[DecisionItem] = []
        for rewrite_item in eligible:
            asset = self._library.select(
                rewrite_item.semantic_key,
                category="decision",
                locale=self._profile.locale,
                audience=self._profile.audience,
                domain=rewrite_item.domain,
                meaning_key=_meaning_key(rewrite_item),
            )
            if asset is None:
                continue
            items.append(_to_decision(rewrite_item, asset))
        ordered = tuple(sorted(items, key=lambda item: (-item.priority, item.decision_id)))
        status = "selected" if ordered else "insufficient"
        return DecisionContext(items=ordered, status=status)


def _meaning_key(item: RewriteItem) -> str:
    if item.source_knowledge_ids:
        return item.source_knowledge_ids[0]
    return dict(item.metadata).get("knowledge_id", "")


def _to_decision(item: RewriteItem, asset: SentenceAsset) -> DecisionItem:
    meta = dict(asset.metadata)
    title = meta.get("title") or _title_from_text(asset.text)
    knowledge_id = _meaning_key(item)
    ref = item.references[0] if item.references else None
    source_path = ref.source_path if ref is not None else ""
    return DecisionItem(
        decision_id=f"decision.{item.domain}.{_slug(knowledge_id)}.001",
        semantic_key=item.semantic_key,
        title=title,
        description=asset.text,
        priority=asset.priority,
        source_rewrite_ids=(item.rewrite_id,),
        source_knowledge_ids=(knowledge_id,) if knowledge_id else (),
        source_reasoning_ids=item.source_reasoning_ids,
        source_evidence_ids=item.source_evidence_ids,
        status=STATUS_SELECTED,
        references=(
            DecisionReference(
                rewrite_id=item.rewrite_id,
                knowledge_id=knowledge_id,
                source_path=source_path,
                reasoning_ids=item.source_reasoning_ids,
                evidence_ids=item.source_evidence_ids,
            ),
        ),
        metadata=(
            ("sentence_id", asset.sentence_id),
            ("source_recommendation", meta.get("source_recommendation", "")),
        ),
    )


def _slug(knowledge_id: str) -> str:
    return knowledge_id.removeprefix("knowledge.").replace(".", "_") or "unknown"


def _title_from_text(text: str) -> str:
    body = text.strip()
    if body.startswith("Bạn "):
        body = body[4:]
    if body.endswith("."):
        body = body[:-1]
    if body:
        body = body[:1].upper() + body[1:]
    return body
