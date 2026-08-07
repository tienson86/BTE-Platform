"""Build Pack 04 NarrativeInterpretationResult from rendered sentences."""

from __future__ import annotations

import uuid
from typing import Any

from .models import (
    InterpretationMetadata,
    InterpretationSection,
    NarrativeInterpretationResult,
    NarrativeSentence,
    utc_now_iso,
)
from .narrative_context import NarrativeContext

_SECTION_TITLES: dict[str, str] = {
    "overview": "Tổng quan",
    "strength": "Thân vượng nhược",
    "pattern": "Cách cục",
    "useful_god": "Dụng thần",
    "ten_gods": "Thập thần",
    "five_elements": "Ngũ hành",
    "season": "Khí mùa",
    "temperature": "Khí hậu",
    "summary": "Kết luận",
}


class InterpretationBuilder:
    """Stage — Interpretation Builder."""

    def build(
        self,
        sentences: list[NarrativeSentence],
        context: NarrativeContext,
        *,
        matched_rules: list[dict[str, Any]] | None = None,
        duration_ms: float = 0.0,
    ) -> NarrativeInterpretationResult:
        """Assemble the Pack 04 interpretation aggregate."""
        by_section: dict[str, list[NarrativeSentence]] = {}
        for sentence in sentences:
            by_section.setdefault(sentence.section, []).append(sentence)

        def _section(section_id: str) -> InterpretationSection:
            items = by_section.get(section_id) or []
            return InterpretationSection(
                section_id=section_id,
                title=_SECTION_TITLES.get(section_id, section_id),
                sentences=list(items),
                summary=" ".join(item.text for item in items if item.text),
            )

        return NarrativeInterpretationResult(
            metadata=InterpretationMetadata(
                interpretation_id=str(uuid.uuid4()),
                analysis_id=context.analysis_id,
                generated_at=utc_now_iso(),
                duration_ms=float(duration_ms),
            ),
            overview=_section("overview"),
            strength=_section("strength"),
            pattern=_section("pattern"),
            useful_god=_section("useful_god"),
            ten_gods=_section("ten_gods"),
            five_elements=_section("five_elements"),
            season=_section("season"),
            temperature=_section("temperature"),
            summary=_section("summary"),
            evidence_refs=list(context.evidence_ids),
            matched_rules=[
                str(rule.get("rule_id") or "")
                for rule in (matched_rules or [])
                if rule.get("rule_id")
            ],
            success=bool(context.analysis.success),
        )
