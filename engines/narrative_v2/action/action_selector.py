"""Select approved Action and Warning assets for Decisions."""

from __future__ import annotations

from engines.narrative_v2.action.action_model import (
    MAX_ACTIONS,
    ActionItem,
    ActionReference,
    WarningItem,
)
from engines.narrative_v2.action.decision_model import DecisionItem
from engines.narrative_v2.language.sentence_asset import SentenceAsset
from engines.narrative_v2.language.sentence_library import SentenceLibrary
from engines.narrative_v2.rewrite.language_profile import LanguageProfile
from engines.narrative_v2.rewrite.rewrite_context import CommercialRewriteContext
from engines.narrative_v2.rewrite.rewrite_item import RewriteItem

STATUS_SELECTED = "selected"


class ActionSelector:
    """Bind approved action/warning assets to Decisions. Never generate prose."""

    def __init__(
        self,
        *,
        library: SentenceLibrary | None = None,
        profile: LanguageProfile | None = None,
    ) -> None:
        self._library = library or SentenceLibrary()
        self._profile = profile or LanguageProfile()

    def select_actions(
        self,
        decisions: tuple[DecisionItem, ...],
        rewrite: CommercialRewriteContext,
    ) -> tuple[ActionItem, ...]:
        """Return 0–6 actions in deterministic order."""
        actions: list[ActionItem] = []
        seen_text: set[str] = set()
        for decision in decisions:
            rewrite_item = _rewrite_for_decision(decision, rewrite)
            if rewrite_item is None:
                continue
            assets = self._library.select_all(
                rewrite_item.semantic_key,
                category="action",
                locale=self._profile.locale,
                audience=self._profile.audience,
                domain=rewrite_item.domain,
                meaning_key=_knowledge_id(decision),
            )
            for asset in assets:
                key = asset.text.casefold()
                if key in seen_text:
                    continue
                seen_text.add(key)
                actions.append(_to_action(decision, rewrite_item, asset))
        ordered = sorted(actions, key=lambda item: (-item.priority, item.action_id))
        return tuple(ordered[:MAX_ACTIONS])

    def select_warnings(
        self,
        decisions: tuple[DecisionItem, ...],
        rewrite: CommercialRewriteContext,
    ) -> tuple[WarningItem, ...]:
        """Return approved warnings, or empty when none exist."""
        warnings: list[WarningItem] = []
        seen: set[str] = set()
        for decision in decisions:
            rewrite_item = _rewrite_for_decision(decision, rewrite)
            if rewrite_item is None:
                continue
            assets = self._library.select_all(
                rewrite_item.semantic_key,
                category="warning",
                locale=self._profile.locale,
                audience=self._profile.audience,
                domain=rewrite_item.domain,
                meaning_key=_knowledge_id(decision),
            )
            for asset in assets:
                key = asset.text.casefold()
                if key in seen:
                    continue
                seen.add(key)
                warnings.append(_to_warning(decision, rewrite_item, asset))
        return tuple(sorted(warnings, key=lambda item: item.warning_id))


def _rewrite_for_decision(
    decision: DecisionItem,
    rewrite: CommercialRewriteContext,
) -> RewriteItem | None:
    if not decision.source_rewrite_ids:
        return None
    return rewrite.item(decision.source_rewrite_ids[0])


def _knowledge_id(decision: DecisionItem) -> str:
    if decision.source_knowledge_ids:
        return decision.source_knowledge_ids[0]
    return ""


def _to_action(
    decision: DecisionItem,
    rewrite_item: RewriteItem,
    asset: SentenceAsset,
) -> ActionItem:
    meta = dict(asset.metadata)
    title = meta.get("title") or _title_from_text(asset.text)
    knowledge_id = _knowledge_id(decision)
    return ActionItem(
        action_id=asset.sentence_id.replace("sentence.", "action.", 1),
        decision_id=decision.decision_id,
        title=title,
        description=asset.text,
        category=meta.get("action_category", "practice"),
        priority=asset.priority,
        source_knowledge_ids=(knowledge_id,) if knowledge_id else (),
        references=(
            ActionReference(
                field="actions",
                rewrite_ids=(rewrite_item.rewrite_id,),
                knowledge_ids=(knowledge_id,) if knowledge_id else (),
                reasoning_ids=rewrite_item.source_reasoning_ids,
                evidence_ids=rewrite_item.source_evidence_ids,
                decision_ids=(decision.decision_id,),
            ),
        ),
        status=STATUS_SELECTED,
        metadata=(
            ("sentence_id", asset.sentence_id),
            ("source_recommendation", meta.get("source_recommendation", "")),
        ),
    )


def _to_warning(
    decision: DecisionItem,
    rewrite_item: RewriteItem,
    asset: SentenceAsset,
) -> WarningItem:
    knowledge_id = _knowledge_id(decision)
    meta = dict(asset.metadata)
    return WarningItem(
        warning_id=asset.sentence_id.replace("sentence.", "warning.", 1),
        title=meta.get("title") or "Điều cần lưu ý",
        description=asset.text,
        severity="caution",
        source_knowledge_ids=(knowledge_id,) if knowledge_id else (),
        references=(
            ActionReference(
                field="warnings",
                rewrite_ids=(rewrite_item.rewrite_id,),
                knowledge_ids=(knowledge_id,) if knowledge_id else (),
                reasoning_ids=rewrite_item.source_reasoning_ids,
                evidence_ids=rewrite_item.source_evidence_ids,
                decision_ids=(decision.decision_id,),
            ),
        ),
        status=STATUS_SELECTED,
        metadata=(("sentence_id", asset.sentence_id),),
    )


def _title_from_text(text: str) -> str:
    body = text.strip()
    if body.startswith("Bạn "):
        body = body[4:]
    first = body.split(".")[0].strip()
    if first:
        first = first[:1].upper() + first[1:]
    return first
