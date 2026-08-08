"""Recommendation Composer — Sprint D2."""

from __future__ import annotations

from engines.narrative_engine.runtime.models import ComponentType, NarrativeNode, NodeStatus

from .constants import INSUFFICIENT_EVIDENCE_NARRATIVE
from .language_rules import LanguageRuleEngine
from .models import NarrativeRecommendation, RecommendationPriority
from .source_bundle import CompositionSource, SourceFact


class RecommendationComposer:
    """Compose NarrativeRecommendation items from action/risk evidence only."""

    def __init__(self, language_rules: LanguageRuleEngine | None = None) -> None:
        self._rules = language_rules or LanguageRuleEngine()

    def compose(
        self,
        node: NarrativeNode,
        source: CompositionSource,
    ) -> tuple[NarrativeRecommendation, ...]:
        """Build recommendations for recommendation/warning nodes."""
        if node.component_type not in {
            ComponentType.RECOMMENDATION,
            ComponentType.WARNING,
        }:
            return ()
        if node.status != NodeStatus.READY:
            return (
                NarrativeRecommendation(
                    id=f"rec-{node.component_type.value}-insufficient",
                    priority=RecommendationPriority.MEDIUM,
                    action=INSUFFICIENT_EVIDENCE_NARRATIVE,
                    reason="",
                    benefit="",
                    insufficient_data=True,
                ),
            )

        facts = source.commercial_facts(node.interpretation_refs + node.evidence_refs)
        if not facts:
            return (
                NarrativeRecommendation(
                    id=f"rec-{node.component_type.value}-insufficient",
                    priority=RecommendationPriority.MEDIUM,
                    action=INSUFFICIENT_EVIDENCE_NARRATIVE,
                    insufficient_data=True,
                ),
            )

        primary = facts[0]
        action = self._rules.sanitize_or_none(
            self._rules.first_sentence(primary.display_value())
        )
        if action is None:
            return (
                NarrativeRecommendation(
                    id=f"rec-{node.component_type.value}-insufficient",
                    priority=RecommendationPriority.MEDIUM,
                    action=INSUFFICIENT_EVIDENCE_NARRATIVE,
                    insufficient_data=True,
                ),
            )
        if not action.endswith((".", "!", "?", "…")):
            if node.component_type == ComponentType.WARNING:
                action = f"Cần lưu ý: {action}."
            else:
                action = f"Ưu tiên phát huy theo nguồn phân tích: {action}."

        reason = ""
        if len(facts) > 1:
            reason_raw = self._rules.sanitize_or_none(
                self._rules.first_sentence(facts[1].display_value())
            )
            reason = reason_raw or ""

        return (
            NarrativeRecommendation(
                id=f"rec-{node.component_type.value}-1",
                priority=(
                    RecommendationPriority.HIGH
                    if node.component_type == ComponentType.RECOMMENDATION
                    else RecommendationPriority.MEDIUM
                ),
                action=action,
                reason=reason,
                benefit="",
                evidence_refs=tuple(
                    fact.id for fact in facts if fact.id in node.evidence_refs
                ),
                interpretation_refs=tuple(
                    fact.id for fact in facts if fact.id in node.interpretation_refs
                ),
                rule_refs=_union_attr(facts, "rule_refs"),
                knowledge_refs=_union_attr(facts, "knowledge_refs"),
                insufficient_data=False,
            ),
        )


def _union_attr(facts: tuple[SourceFact, ...], attr: str) -> tuple[str, ...]:
    """Union string refs from facts."""
    values: list[str] = []
    for fact in facts:
        for item in getattr(fact, attr):
            if item and item not in values:
                values.append(item)
    return tuple(values)
