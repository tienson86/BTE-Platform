"""Interpretation Pipeline orchestration."""

from __future__ import annotations

import logging

from engines.analysis_engine.interpretation_engine.interpretation_builder import (
    InterpretationBuilder,
)
from engines.analysis_engine.interpretation_engine.knowledge_access import (
    ASSET_SECTIONS,
    KnowledgeSession,
)
from engines.analysis_engine.interpretation_engine.models import (
    InterpretationContext,
    InterpretationResult,
)
from engines.analysis_engine.interpretation_engine.paragraph_builder import (
    ParagraphBuilder,
)
from engines.analysis_engine.interpretation_engine.placeholder_binding import (
    PlaceholderBinder,
)
from engines.analysis_engine.interpretation_engine.sentence_selection import (
    SentenceSelector,
)
from engines.analysis_engine.interpretation_engine.template_binding import (
    TemplateBinder,
)

logger = logging.getLogger(__name__)


class InterpretationPipeline:
    """Canonical Interpretation Engine pipeline.

    Flow:

    AnalysisResult
            │
            ▼
    Sentence Selection
            │
            ▼
    Template Binding
            │
            ▼
    Placeholder Binding
            │
            ▼
    Paragraph Builder
            │
            ▼
    Interpretation Builder
            │
            ▼
    InterpretationResult
    """

    def __init__(
        self,
        *,
        sentence_selector: SentenceSelector | None = None,
        template_binder: TemplateBinder | None = None,
        placeholder_binder: PlaceholderBinder | None = None,
        paragraph_builder: ParagraphBuilder | None = None,
        interpretation_builder: InterpretationBuilder | None = None,
        module_version: str = "1.0.0",
    ) -> None:
        self._sentence_selector = sentence_selector or SentenceSelector()
        self._template_binder = template_binder or TemplateBinder()
        self._placeholder_binder = placeholder_binder or PlaceholderBinder()
        self._paragraph_builder = paragraph_builder or ParagraphBuilder()
        self._interpretation_builder = (
            interpretation_builder or InterpretationBuilder()
        )
        self._module_version = module_version

    def run(
        self,
        context: InterpretationContext,
        *,
        session: KnowledgeSession,
        knowledge_version: str,
    ) -> InterpretationResult:
        """Execute the full interpretation pipeline."""
        selected = self._sentence_selector.select(context, session=session)
        logger.debug(
            "interpretation_sentences_selected",
            extra={"count": len(selected), "request_id": context.request_id},
        )

        templates = self._template_binder.bind(selected, session=session)
        sentences = self._placeholder_binder.bind(templates, context)

        section_order = tuple(
            session.get_asset(ASSET_SECTIONS).data.get("order") or ()
        )
        paragraphs = self._paragraph_builder.build(
            sentences,
            section_order=section_order,
        )
        return self._interpretation_builder.build(
            request_id=context.request_id,
            paragraphs=paragraphs,
            session=session,
            knowledge_version=knowledge_version,
            module_version=self._module_version,
            all_sentences=sentences,
        )
