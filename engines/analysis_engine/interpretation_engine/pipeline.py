"""Interpretation Pipeline orchestration."""

from __future__ import annotations

import logging

from engines.analysis_engine.interpretation_engine.chapter_builder import (
    ChapterBuilder,
)
from engines.analysis_engine.interpretation_engine.conflict_resolution import (
    ConflictResolver,
)
from engines.analysis_engine.interpretation_engine.explanation_builder import (
    ExplanationBuilder,
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
from engines.analysis_engine.interpretation_engine.phrase_library import PhraseLibrary
from engines.analysis_engine.interpretation_engine.placeholder_binding import (
    PlaceholderBinder,
)
from engines.analysis_engine.interpretation_engine.sentence_ranking import (
    SentenceRanker,
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
    Sentence Ranking
            │
            ▼
    Conflict Resolution
            │
            ▼
    Placeholder Binding
            │
            ▼
    Paragraph Builder
            │
            ▼
    Chapter Builder
            │
            ▼
    Explanation Builder
            │
            ▼
    Markdown / HTML / JSON Builders
            │
            ▼
    InterpretationResult
    """

    def __init__(
        self,
        *,
        sentence_selector: SentenceSelector | None = None,
        sentence_ranker: SentenceRanker | None = None,
        conflict_resolver: ConflictResolver | None = None,
        template_binder: TemplateBinder | None = None,
        placeholder_binder: PlaceholderBinder | None = None,
        paragraph_builder: ParagraphBuilder | None = None,
        chapter_builder: ChapterBuilder | None = None,
        explanation_builder: ExplanationBuilder | None = None,
        phrase_library: PhraseLibrary | None = None,
        module_version: str = "1.0.0",
    ) -> None:
        self._sentence_selector = sentence_selector or SentenceSelector()
        self._sentence_ranker = sentence_ranker or SentenceRanker()
        self._conflict_resolver = conflict_resolver or ConflictResolver()
        self._template_binder = template_binder or TemplateBinder()
        self._placeholder_binder = placeholder_binder or PlaceholderBinder()
        self._phrase_library = phrase_library or PhraseLibrary()
        self._paragraph_builder = paragraph_builder or ParagraphBuilder(
            phrase_library=self._phrase_library,
        )
        self._chapter_builder = chapter_builder or ChapterBuilder()
        self._explanation_builder = explanation_builder or ExplanationBuilder()
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
        ranked = self._sentence_ranker.rank(selected, session=session)
        resolved = self._conflict_resolver.resolve(ranked, session=session)
        logger.debug(
            "interpretation_sentences_resolved",
            extra={
                "selected": len(selected),
                "ranked": len(ranked),
                "resolved": len(resolved),
                "request_id": context.request_id,
            },
        )

        templates = self._template_binder.bind(resolved, session=session)
        sentences = self._placeholder_binder.bind(
            templates,
            context,
            session=session,
        )

        section_order = tuple(
            session.get_asset(ASSET_SECTIONS).data.get("order") or ()
        )
        paragraphs = self._paragraph_builder.build(
            sentences,
            section_order=section_order,
            session=session,
            apply_phrases=True,
        )
        chapters = self._chapter_builder.build(paragraphs, session=session)

        phrase_ids: dict[str, str | None] = {}
        for paragraph in paragraphs:
            phrase_id, _ = self._phrase_library.opening_for_section(
                paragraph.section_id,
                session=session,
            )
            phrase_ids[paragraph.section_id] = phrase_id

        terminology_ids = {
            sentence.sentence_id: tuple(
                sentence.metadata.get("terminology_ids") or ()
            )
            for sentence in sentences
        }

        return self._explanation_builder.build(
            request_id=context.request_id,
            chapters=chapters,
            session=session,
            knowledge_version=knowledge_version,
            module_version=self._module_version,
            all_sentences=sentences,
            ranked=ranked,
            resolved=resolved,
            phrase_ids=phrase_ids,
            terminology_ids=terminology_ids,
        )
