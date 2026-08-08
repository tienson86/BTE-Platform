"""Sentence Composer — build sentences only from source facts."""

from __future__ import annotations

import logging

from engines.narrative_engine.runtime.models import ComponentType, NodeStatus

from .constants import INSUFFICIENT_EVIDENCE_NARRATIVE
from .language_rules import LanguageRuleEngine
from .models import NarrativeParagraph, ParagraphRole
from .source_bundle import CompositionSource, SourceFact

logger = logging.getLogger(__name__)

_ROLE_BY_COMPONENT: dict[ComponentType, ParagraphRole] = {
    ComponentType.EXECUTIVE_SUMMARY: ParagraphRole.SUMMARY,
    ComponentType.OBSERVATION: ParagraphRole.OBSERVATION,
    ComponentType.REASONING: ParagraphRole.EXPLANATION,
    ComponentType.IMPACT: ParagraphRole.IMPACT,
    ComponentType.RECOMMENDATION: ParagraphRole.SUGGESTION,
    ComponentType.WARNING: ParagraphRole.OBSERVATION,
    ComponentType.CONCLUSION: ParagraphRole.SUMMARY,
}


class SentenceComposer:
    """
    Compose sentence text exclusively from Interpretation/Evidence facts.

    Never invents analytical conclusions.
    """

    def __init__(self, language_rules: LanguageRuleEngine | None = None) -> None:
        self._rules = language_rules or LanguageRuleEngine()

    def compose_paragraph(
        self,
        *,
        paragraph_id: str,
        component_type: ComponentType,
        status: NodeStatus,
        source: CompositionSource,
        evidence_refs: tuple[str, ...],
        interpretation_refs: tuple[str, ...],
        confidence: float,
    ) -> NarrativeParagraph:
        """Compose one paragraph for a tree node."""
        role = _ROLE_BY_COMPONENT.get(component_type, ParagraphRole.OTHER)
        if status != NodeStatus.READY:
            return self._insufficient(paragraph_id, role)

        facts = source.commercial_facts(interpretation_refs + evidence_refs)
        if not facts:
            return self._insufficient(paragraph_id, role)

        selected = self._pick_facts(component_type, facts)
        text = self._render_from_facts(component_type, selected)
        allowed = self._rules.sanitize_or_none(text)
        if allowed is None:
            logger.info(
                "sentence_composer.blocked_by_language_rules component=%s",
                component_type.value,
            )
            return self._insufficient(paragraph_id, role)

        return NarrativeParagraph(
            id=paragraph_id,
            role=role,
            text=allowed,
            evidence_refs=tuple(fact.id for fact in selected if fact.id in evidence_refs),
            interpretation_refs=tuple(
                fact.id for fact in selected if fact.id in interpretation_refs
            ),
            rule_refs=_merge_refs(selected, "rule_refs"),
            knowledge_refs=_merge_refs(selected, "knowledge_refs"),
            confidence=confidence if confidence > 0 else _avg_confidence(selected),
            insufficient_data=False,
        )

    def _insufficient(self, paragraph_id: str, role: ParagraphRole) -> NarrativeParagraph:
        """Emit approved insufficient-evidence narrative."""
        return NarrativeParagraph(
            id=paragraph_id,
            role=role,
            text=INSUFFICIENT_EVIDENCE_NARRATIVE,
            evidence_refs=(),
            interpretation_refs=(),
            rule_refs=(),
            knowledge_refs=(),
            confidence=0.0,
            insufficient_data=True,
        )

    def _pick_facts(
        self,
        component_type: ComponentType,
        facts: tuple[SourceFact, ...],
    ) -> tuple[SourceFact, ...]:
        """Prefer interpretation prose facts, then evidence facts (max 2)."""
        interp_like = [fact for fact in facts if fact.raw_text.strip()]
        if interp_like:
            return tuple(interp_like[:2])
        return tuple(facts[:2])

    def _render_from_facts(
        self,
        component_type: ComponentType,
        facts: tuple[SourceFact, ...],
    ) -> str:
        """
        Render consultant sentence(s) from source display values only.

        Framing prefixes are structural (writing system), not new analytical claims.
        """
        chunks: list[str] = []
        for fact in facts:
            display = self._rules.first_sentence(fact.display_value())
            cleaned = self._rules.sanitize_or_none(display)
            if cleaned is None:
                continue
            chunks.append(cleaned)
        if not chunks:
            return ""
        if len(chunks) == 1:
            return _frame(component_type, chunks[0])
        return _frame(component_type, chunks[0]) + " " + chunks[1]


def _frame(component_type: ComponentType, body: str) -> str:
    """Apply minimal role framing without adding facts."""
    body = body.strip()
    if not body:
        return ""
    # If source already looks like a full sentence, keep it.
    if body.endswith((".", "!", "?", "…")):
        return body
    prefixes = {
        ComponentType.OBSERVATION: "Quan sát từ dữ liệu phân tích: ",
        ComponentType.REASONING: "Lý giải dựa trên nguồn đã kiểm chứng: ",
        ComponentType.IMPACT: "Ý nghĩa thực tế từ nguồn phân tích: ",
        ComponentType.RECOMMENDATION: "Ưu tiên theo nguồn phân tích: ",
        ComponentType.WARNING: "Cần lưu ý theo nguồn phân tích: ",
        ComponentType.CONCLUSION: "Điểm then chốt từ các nguồn đã nêu: ",
        ComponentType.EXECUTIVE_SUMMARY: "",
    }
    prefix = prefixes.get(component_type, "")
    return f"{prefix}{body}."


def _merge_refs(facts: tuple[SourceFact, ...], attr: str) -> tuple[str, ...]:
    """Union rule/knowledge refs from selected facts."""
    values: list[str] = []
    for fact in facts:
        for item in getattr(fact, attr):
            if item and item not in values:
                values.append(item)
    return tuple(values)


def _avg_confidence(facts: tuple[SourceFact, ...]) -> float:
    """Average confidence of selected facts."""
    if not facts:
        return 0.0
    return round(sum(fact.confidence for fact in facts) / len(facts), 4)
