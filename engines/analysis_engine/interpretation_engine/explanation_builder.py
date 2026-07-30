"""Explanation Builder — assemble explainable InterpretationResult."""

from __future__ import annotations

from typing import Any, Mapping

from engines.analysis_engine.interpretation_engine.exceptions import (
    InterpretationExecutionError,
)
from engines.analysis_engine.interpretation_engine.html_builder import HtmlBuilder
from engines.analysis_engine.interpretation_engine.json_builder import JsonBuilder
from engines.analysis_engine.interpretation_engine.knowledge_access import (
    ASSET_CONFIDENCE,
    KnowledgeSession,
)
from engines.analysis_engine.interpretation_engine.markdown_builder import (
    MarkdownBuilder,
)
from engines.analysis_engine.interpretation_engine.models import (
    BoundSentence,
    ExplanationEntry,
    InterpretationChapter,
    InterpretationResult,
    InterpretationSection,
    SelectedSentence,
)
from engines.analysis_engine.runtime.models import (
    ConfidenceEvaluation,
    DiagnosticInfo,
    RuleEvidence,
)


class ExplanationBuilder:
    """Build explainable, traceable InterpretationResult and render artifacts."""

    def __init__(
        self,
        *,
        markdown_builder: MarkdownBuilder | None = None,
        html_builder: HtmlBuilder | None = None,
        json_builder: JsonBuilder | None = None,
    ) -> None:
        self._markdown = markdown_builder or MarkdownBuilder()
        self._html = html_builder or HtmlBuilder()
        self._json = json_builder or JsonBuilder()

    def build(
        self,
        *,
        request_id: str,
        chapters: tuple[InterpretationChapter, ...],
        session: KnowledgeSession,
        knowledge_version: str,
        module_version: str,
        all_sentences: tuple[BoundSentence, ...],
        ranked: tuple[SelectedSentence, ...],
        resolved: tuple[SelectedSentence, ...],
        phrase_ids: Mapping[str, str | None] | None = None,
        terminology_ids: Mapping[str, tuple[str, ...]] | None = None,
    ) -> InterpretationResult:
        """Assemble InterpretationResult with explanations and render formats."""
        phrase_ids = dict(phrase_ids or {})
        terminology_ids = dict(terminology_ids or {})
        sections = self._flatten_sections(chapters)
        if not sections:
            raise InterpretationExecutionError(
                "No interpretive sections could be assembled",
            )

        resolved_ids = {item.sentence_id for item in resolved}
        rank_index = {
            item.sentence_id: index for index, item in enumerate(ranked, start=1)
        }
        explanations = self._build_explanations(
            all_sentences=all_sentences,
            resolved_ids=resolved_ids,
            rank_index=rank_index,
            phrase_ids=phrase_ids,
            terminology_ids=terminology_ids,
        )
        overview = self._resolve_overview(sections)
        confidence = self._build_confidence(session, section_count=len(sections))
        evidence = tuple(
            RuleEvidence(
                rule_id=sentence.sentence_id,
                version=knowledge_version,
                category=sentence.section_id,
                priority=sentence.priority,
                reference=sentence.template_id,
                details={
                    "source_stage": sentence.source_stage,
                    "bound_values": dict(sentence.bound_values),
                    "rank": rank_index.get(sentence.sentence_id),
                    "conflict_action": (
                        "kept"
                        if sentence.sentence_id in resolved_ids
                        else "suppressed"
                    ),
                    "phrase_id": phrase_ids.get(sentence.section_id),
                    "terminology_ids": list(
                        terminology_ids.get(sentence.sentence_id, ())
                    ),
                },
            )
            for sentence in all_sentences
        )
        diagnostics = (
            DiagnosticInfo(
                code="interpretation.assembled",
                message="InterpretationResult assembled",
                level="info",
                stage_id="interpretation",
                details={
                    "section_count": len(sections),
                    "sentence_count": len(all_sentences),
                    "chapter_count": len(chapters),
                    "explanation_count": len(explanations),
                },
            ),
        )
        summary: dict[str, Any] = {
            "section_count": len(sections),
            "sentence_count": len(all_sentences),
            "chapter_count": len(chapters),
            "section_ids": [section.section_id for section in sections],
            "chapter_ids": [chapter.chapter_id for chapter in chapters],
        }
        result = InterpretationResult(
            request_id=request_id,
            sections=sections,
            overview=overview,
            confidence=confidence,
            evidence=evidence,
            diagnostics=diagnostics,
            knowledge_version=knowledge_version,
            module_version=module_version,
            summary=summary,
            chapters=chapters,
            explanations=explanations,
        )
        result.markdown = self._markdown.build(result)
        result.html = self._html.build(result)
        result.json_text = self._json.build(result)
        return result

    @staticmethod
    def _flatten_sections(
        chapters: tuple[InterpretationChapter, ...],
    ) -> tuple[InterpretationSection, ...]:
        sections: list[InterpretationSection] = []
        for chapter in chapters:
            sections.extend(chapter.sections)
        return tuple(sections)

    @staticmethod
    def _resolve_overview(sections: tuple[InterpretationSection, ...]) -> str:
        for section in sections:
            if section.section_id == "overview" and section.body.strip():
                return section.body
        return sections[0].body

    @staticmethod
    def _build_confidence(
        session: KnowledgeSession,
        *,
        section_count: int,
    ) -> ConfidenceEvaluation:
        cfg = session.get_asset(ASSET_CONFIDENCE).data
        base = float(cfg.get("base_score") or 0.5)
        bonus = float(cfg.get("per_section_bonus") or 0.0)
        max_score = float(cfg.get("max_score") or 1.0)
        score = min(max_score, base + bonus * section_count)
        level = str(cfg.get("level") or "medium")
        return ConfidenceEvaluation(
            score=round(score, 4),
            level=level,
            details={
                "base_score": base,
                "section_count": section_count,
                "per_section_bonus": bonus,
            },
        )

    @staticmethod
    def _build_explanations(
        *,
        all_sentences: tuple[BoundSentence, ...],
        resolved_ids: set[str],
        rank_index: Mapping[str, int],
        phrase_ids: Mapping[str, str | None],
        terminology_ids: Mapping[str, tuple[str, ...]],
    ) -> tuple[ExplanationEntry, ...]:
        entries: list[ExplanationEntry] = []
        for sentence in all_sentences:
            action = "kept" if sentence.sentence_id in resolved_ids else "suppressed"
            entries.append(
                ExplanationEntry(
                    sentence_id=sentence.sentence_id,
                    section_id=sentence.section_id,
                    source_stage=sentence.source_stage,
                    template_id=sentence.template_id,
                    priority=sentence.priority,
                    rank=int(rank_index.get(sentence.sentence_id) or 0),
                    conflict_action=action,
                    text=sentence.text,
                    bound_values=dict(sentence.bound_values),
                    phrase_id=phrase_ids.get(sentence.section_id),
                    terminology_ids=terminology_ids.get(sentence.sentence_id, ()),
                    reason=(
                        f"Matched stage '{sentence.source_stage}', "
                        f"ranked #{rank_index.get(sentence.sentence_id, 0)}, "
                        f"conflict={action}"
                    ),
                )
            )
        return tuple(entries)
