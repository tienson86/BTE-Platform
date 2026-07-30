"""Interpretation Builder — assemble InterpretationResult."""

from __future__ import annotations

from typing import Any, Mapping

from engines.analysis_engine.interpretation_engine.exceptions import (
    InterpretationExecutionError,
)
from engines.analysis_engine.interpretation_engine.knowledge_access import (
    ASSET_CONFIDENCE,
    ASSET_SECTIONS,
    KnowledgeSession,
)
from engines.analysis_engine.interpretation_engine.models import (
    BoundSentence,
    InterpretationParagraph,
    InterpretationResult,
    InterpretationSection,
)
from engines.analysis_engine.runtime.models import (
    ConfidenceEvaluation,
    DiagnosticInfo,
    RuleEvidence,
)


class InterpretationBuilder:
    """Assemble paragraphs into the public InterpretationResult."""

    def build(
        self,
        *,
        request_id: str,
        paragraphs: tuple[InterpretationParagraph, ...],
        session: KnowledgeSession,
        knowledge_version: str,
        module_version: str,
        all_sentences: tuple[BoundSentence, ...],
    ) -> InterpretationResult:
        """Create immutable InterpretationResult from paragraphs."""
        section_cfg = session.get_asset(ASSET_SECTIONS).data
        order = tuple(section_cfg.get("order") or ())
        titles = dict(section_cfg.get("titles") or {})

        paragraph_map = {item.section_id: item for item in paragraphs}
        sections: list[InterpretationSection] = []
        for section_id in order:
            paragraph = paragraph_map.get(section_id)
            if paragraph is None or not paragraph.text.strip():
                continue
            sections.append(
                InterpretationSection(
                    section_id=section_id,
                    title=str(titles.get(section_id) or section_id),
                    paragraphs=(paragraph,),
                    body=paragraph.text,
                    sentence_ids=tuple(
                        sentence.sentence_id for sentence in paragraph.sentences
                    ),
                    source_stages=tuple(
                        dict.fromkeys(
                            sentence.source_stage for sentence in paragraph.sentences
                        )
                    ),
                )
            )

        # Preserve unexpected section ids deterministically after canonical order.
        for section_id in sorted(set(paragraph_map) - set(order)):
            paragraph = paragraph_map[section_id]
            if not paragraph.text.strip():
                continue
            sections.append(
                InterpretationSection(
                    section_id=section_id,
                    title=str(titles.get(section_id) or section_id),
                    paragraphs=(paragraph,),
                    body=paragraph.text,
                    sentence_ids=tuple(
                        sentence.sentence_id for sentence in paragraph.sentences
                    ),
                    source_stages=tuple(
                        dict.fromkeys(
                            sentence.source_stage for sentence in paragraph.sentences
                        )
                    ),
                )
            )

        if not sections:
            raise InterpretationExecutionError(
                "No interpretive sections could be assembled",
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
                },
            ),
        )
        summary: Mapping[str, Any] = {
            "section_count": len(sections),
            "sentence_count": len(all_sentences),
            "section_ids": [section.section_id for section in sections],
        }
        return InterpretationResult(
            request_id=request_id,
            sections=tuple(sections),
            overview=overview,
            confidence=confidence,
            evidence=evidence,
            diagnostics=diagnostics,
            knowledge_version=knowledge_version,
            module_version=module_version,
            summary=dict(summary),
        )

    @staticmethod
    def _resolve_overview(sections: list[InterpretationSection]) -> str:
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
