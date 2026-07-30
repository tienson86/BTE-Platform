"""Sentence Selection — choose library sentences from AnalysisResult."""

from __future__ import annotations

from typing import Any, Mapping

from engines.analysis_engine.interpretation_engine.exceptions import (
    InterpretationKnowledgeError,
)
from engines.analysis_engine.interpretation_engine.knowledge_access import (
    ASSET_SECTIONS,
    ASSET_SENTENCES,
    KnowledgeSession,
)
from engines.analysis_engine.interpretation_engine.models import (
    InterpretationContext,
    SelectedSentence,
)
from engines.analysis_engine.interpretation_engine.validators import stage_payload
from engines.analysis_engine.runtime.models import AnalysisResult


class SentenceSelector:
    """Select deterministic sentence candidates from knowledge."""

    def select(
        self,
        context: InterpretationContext,
        *,
        session: KnowledgeSession,
    ) -> tuple[SelectedSentence, ...]:
        """Select matching sentences ordered by priority then sentence_id."""
        analysis = context.analysis_result
        rows = list(session.get_asset(ASSET_SENTENCES).data.get("rows") or [])
        if not rows:
            raise InterpretationKnowledgeError(
                "interpretation.sentences has no rows",
            )

        section_cfg = session.get_asset(ASSET_SECTIONS).data
        max_per_section = int(section_cfg.get("max_sentences_per_section") or 3)

        matched: list[SelectedSentence] = []
        for row in rows:
            selected = self._try_match(row, analysis)
            if selected is not None:
                matched.append(selected)

        matched.sort(key=lambda item: (-item.priority, item.sentence_id))

        limited: list[SelectedSentence] = []
        counts: dict[str, int] = {}
        for item in matched:
            count = counts.get(item.section_id, 0)
            if count >= max_per_section:
                continue
            limited.append(item)
            counts[item.section_id] = count + 1
        return tuple(limited)

    def _try_match(
        self,
        row: Mapping[str, Any],
        analysis: AnalysisResult,
    ) -> SelectedSentence | None:
        sentence_id = str(row.get("sentence_id") or "").strip()
        section_id = str(row.get("section_id") or "").strip()
        source_stage = str(row.get("source_stage") or "").strip()
        template_id = str(row.get("template_id") or "").strip()
        if not sentence_id or not section_id or not source_stage or not template_id:
            return None
        if analysis.get_stage_result(source_stage) is None:
            return None

        payload = stage_payload(analysis, source_stage)
        match = dict(row.get("match") or {})
        for key, expected in match.items():
            if payload.get(key) != expected:
                return None

        return SelectedSentence(
            sentence_id=sentence_id,
            section_id=section_id,
            source_stage=source_stage,
            template_id=template_id,
            priority=int(row.get("priority") or 0),
            match=match,
            placeholders=tuple(row.get("placeholders") or ()),
            required_placeholders=tuple(row.get("required_placeholders") or ()),
            metadata=dict(row.get("metadata") or {}),
        )
