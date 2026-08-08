"""Paragraph Builder — Sprint D2 (Pack 05, not WP7)."""

from __future__ import annotations

from engines.narrative_engine.runtime.models import NarrativeNode

from .models import NarrativeParagraph
from .sentence_composer import SentenceComposer
from .source_bundle import CompositionSource


class Pack05ParagraphBuilder:
    """
    Build NarrativeParagraph units for one NarrativeNode.

    Distinct from WP7 ``paragraph_builder.ParagraphBuilder``.
    """

    def __init__(self, sentence_composer: SentenceComposer | None = None) -> None:
        self._sentences = sentence_composer or SentenceComposer()

    def build(self, node: NarrativeNode, source: CompositionSource) -> tuple[NarrativeParagraph, ...]:
        """Build one primary paragraph for the node (compact Sprint C density)."""
        paragraph = self._sentences.compose_paragraph(
            paragraph_id=f"p-{node.component_type.value}-1",
            component_type=node.component_type,
            status=node.status,
            source=source,
            evidence_refs=node.evidence_refs,
            interpretation_refs=node.interpretation_refs,
            confidence=node.confidence,
        )
        return (paragraph,)
