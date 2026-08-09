"""Build structured sentence candidates. No paragraph composition."""

from __future__ import annotations

from typing import Sequence

from engines.interpretation_engine.knowledge.composition_context import CompositionContext
from engines.interpretation_engine.knowledge.composition_result import (
    CompositionResult,
    SentenceCandidate,
    build_composition_result,
)
from engines.interpretation_engine.knowledge.evidence_selector import EvidenceBundle, EvidenceSelector
from engines.interpretation_engine.knowledge.knowledge_selector import (
    KnowledgeSelection,
    KnowledgeSelector,
)
from engines.interpretation_engine.knowledge.placeholder_binder import (
    PlaceholderBinder,
    PlaceholderBinding,
)
from engines.interpretation_engine.knowledge.reasoning_selector import (
    ReasoningSelection,
    ReasoningSelector,
)
from engines.interpretation_engine.knowledge.selector_registry import (
    SELECTOR_EVIDENCE,
    SELECTOR_KNOWLEDGE,
    SELECTOR_PLACEHOLDER,
    SELECTOR_REASONING,
    SELECTOR_SENTENCE_CANDIDATE,
    SELECTOR_TEMPLATE,
    SelectorRegistry,
)
from engines.interpretation_engine.knowledge.template_selector import (
    TemplateSelection,
    TemplateSelector,
)
from engines.interpretation_engine.knowledge.validation import validate_composition


class SentenceCandidateBuilder:
    """Produce deterministic sentence candidates from selected knowledge."""

    def __init__(
        self,
        *,
        knowledge_selector: KnowledgeSelector | None = None,
        evidence_selector: EvidenceSelector | None = None,
        reasoning_selector: ReasoningSelector | None = None,
        template_selector: TemplateSelector | None = None,
        placeholder_binder: PlaceholderBinder | None = None,
        registry: SelectorRegistry | None = None,
    ) -> None:
        """Inject selectors. Defaults are the released IE-2 catalog."""
        self._knowledge = knowledge_selector or KnowledgeSelector()
        self._evidence = evidence_selector or EvidenceSelector()
        self._reasoning = reasoning_selector or ReasoningSelector()
        self._templates = template_selector or TemplateSelector()
        self._placeholders = placeholder_binder or PlaceholderBinder()
        self._registry = registry or SelectorRegistry.default()

    def build_candidates(
        self,
        *,
        knowledge: Sequence[KnowledgeSelection],
        evidence: Sequence[EvidenceBundle],
        reasoning: Sequence[ReasoningSelection],
        templates: Sequence[TemplateSelection],
        placeholders: Sequence[PlaceholderBinding],
    ) -> tuple[SentenceCandidate, ...]:
        """Compose structured candidates. One candidate per selected knowledge id."""
        evidence_by_kn = {item.knowledge_id: item for item in evidence}
        reasoning_by_kn = {item.knowledge_id: item for item in reasoning}
        template_by_kn = {item.knowledge_id: item for item in templates}
        values_by_kn: dict[str, dict[str, object]] = {}
        for binding in placeholders:
            values_by_kn.setdefault(binding.knowledge_id, {})[binding.binding_path] = binding.value
        candidates: list[SentenceCandidate] = []
        for item in knowledge:
            template = template_by_kn.get(item.knowledge_id)
            if template is None:
                continue
            evidence_item = evidence_by_kn.get(item.knowledge_id)
            reasoning_item = reasoning_by_kn.get(item.knowledge_id)
            candidates.append(
                SentenceCandidate(
                    sentence_id=f"SC-{item.knowledge_id}",
                    template_id=template.template_id,
                    placeholder_values=dict(values_by_kn.get(item.knowledge_id, {})),
                    evidence_ids=() if evidence_item is None else (evidence_item.evidence_id,),
                    reasoning_ids=() if reasoning_item is None else (reasoning_item.reasoning_id,),
                    confidence="none" if evidence_item is None else evidence_item.confidence,
                    references=() if evidence_item is None else evidence_item.references,
                    knowledge_id=item.knowledge_id,
                )
            )
        return tuple(sorted(candidates, key=lambda item: item.sentence_id))

    def run(self, context: CompositionContext) -> CompositionResult:
        """Execute the full selection pipeline once in registry order."""
        order = self._registry.resolve_order()
        knowledge = self._knowledge.select(context)
        context.publish(SELECTOR_KNOWLEDGE, {"ids": [item.knowledge_id for item in knowledge]})
        evidence = self._evidence.select(context, knowledge)
        context.publish(SELECTOR_EVIDENCE, {"ids": [item.evidence_id for item in evidence]})
        reasoning = self._reasoning.select(knowledge)
        context.publish(SELECTOR_REASONING, {"ids": [item.reasoning_id for item in reasoning]})
        templates = self._templates.select(knowledge)
        context.publish(SELECTOR_TEMPLATE, {"ids": [item.template_id for item in templates]})
        placeholders = self._placeholders.bind(context, knowledge, templates)
        context.publish(
            SELECTOR_PLACEHOLDER,
            {"ids": [item.placeholder_id for item in placeholders]},
        )
        candidates = self.build_candidates(
            knowledge=knowledge,
            evidence=evidence,
            reasoning=reasoning,
            templates=templates,
            placeholders=placeholders,
        )
        context.publish(
            SELECTOR_SENTENCE_CANDIDATE,
            {"ids": [item.sentence_id for item in candidates]},
        )
        report = validate_composition(
            context=context,
            registry=self._registry,
            knowledge=knowledge,
            evidence=evidence,
            reasoning=reasoning,
            templates=templates,
            placeholders=placeholders,
            candidates=candidates,
        )
        diagnostics = list(report.codes)
        diagnostics.append(f"selector_order:{','.join(order)}")
        return build_composition_result(
            knowledge=knowledge,
            evidence=evidence,
            reasoning=reasoning,
            templates=templates,
            placeholders=placeholders,
            candidates=candidates,
            success=report.success,
            diagnostics=diagnostics,
            errors=() if report.success else (str(report.details.get("error") or "validation_failed"),),
        )
