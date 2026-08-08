"""Section Composer — Sprint D2."""

from __future__ import annotations

from engines.narrative_engine.runtime.models import ComponentType, NarrativeNode

from .constants import COMPONENT_TITLES
from .models import NarrativeSection
from .paragraph_builder import Pack05ParagraphBuilder
from .recommendation_composer import RecommendationComposer
from .source_bundle import CompositionSource
from .tone_resolver import ToneResolver


class SectionComposer:
    """Compose one NarrativeSection from a NarrativeNode."""

    def __init__(
        self,
        paragraph_builder: Pack05ParagraphBuilder | None = None,
        recommendation_composer: RecommendationComposer | None = None,
        tone_resolver: ToneResolver | None = None,
    ) -> None:
        self._paragraphs = paragraph_builder or Pack05ParagraphBuilder()
        self._recommendations = recommendation_composer or RecommendationComposer()
        self._tones = tone_resolver or ToneResolver()

    def compose(self, node: NarrativeNode, source: CompositionSource) -> NarrativeSection:
        """Build a section for the given tree node."""
        paragraphs = self._paragraphs.build(node, source)
        recommendations = self._recommendations.compose(node, source)
        insufficient = all(item.insufficient_data for item in paragraphs) and (
            not recommendations or all(item.insufficient_data for item in recommendations)
        )
        evidence_refs = tuple(
            dict.fromkeys(
                list(node.evidence_refs)
                + [ref for paragraph in paragraphs for ref in paragraph.evidence_refs]
            )
        )
        interpretation_refs = tuple(
            dict.fromkeys(
                list(node.interpretation_refs)
                + [
                    ref
                    for paragraph in paragraphs
                    for ref in paragraph.interpretation_refs
                ]
            )
        )
        return NarrativeSection(
            id=f"sec-{node.component_type.value}",
            intent=_intent_for(node.component_type),
            title=COMPONENT_TITLES.get(node.component_type.value, node.component_type.value),
            paragraphs=paragraphs,
            recommendations=recommendations,
            evidence_refs=evidence_refs,
            interpretation_refs=interpretation_refs,
            confidence=node.confidence,
            insufficient_data=insufficient,
            tone=self._tones.resolve(node.component_type),
        )


def _intent_for(component_type: ComponentType) -> str:
    """Map component type to Sprint A section intent."""
    mapping = {
        ComponentType.EXECUTIVE_SUMMARY: "overview",
        ComponentType.OBSERVATION: "observation",
        ComponentType.REASONING: "reasoning",
        ComponentType.IMPACT: "impact",
        ComponentType.RECOMMENDATION: "priority",
        ComponentType.WARNING: "warning",
        ComponentType.CONCLUSION: "closing",
    }
    return mapping.get(component_type, component_type.value)
