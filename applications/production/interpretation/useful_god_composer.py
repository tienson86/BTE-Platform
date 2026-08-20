"""Useful God / balance strategy published facts + Vietnamese composer."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from applications.production.interpretation.contracts import (
    DomainClaim,
    DomainInterpretationResult,
    DomainSection,
    DomainStatus,
    KnowledgeStatus,
)
from applications.production.interpretation.theme_keys import (
    THEME_BALANCE_STRATEGY,
    THEME_NO_EXTRA_LOAD,
    THEME_OUTPUT_RELEASE,
)


@dataclass(slots=True)
class UsefulGodPublishedFacts:
    """Published Useful God facts for balance composition."""

    useful_god: str = ""
    favorable_gods: list[str] = field(default_factory=list)
    unfavorable_gods: list[str] = field(default_factory=list)
    reasoning: str = ""
    confidence: float = 0.0
    missing_data: list[str] = field(default_factory=list)


def build_useful_god_published_facts(useful_god_view: Any) -> UsefulGodPublishedFacts:
    """Map UsefulGodView / dict to published facts."""
    if useful_god_view is None:
        return UsefulGodPublishedFacts(missing_data=["useful_god"])
    data = (
        useful_god_view.to_dict()
        if hasattr(useful_god_view, "to_dict")
        else dict(useful_god_view)
    )
    incomplete = bool(data.get("overall_incomplete"))
    useful = "" if incomplete else str(data.get("useful_display") or data.get("useful_god") or "")
    missing: list[str] = []
    if incomplete or not useful:
        missing.append("useful_god")
    return UsefulGodPublishedFacts(
        useful_god=useful,
        favorable_gods=[str(item) for item in data.get("favorable_gods") or []],
        unfavorable_gods=[str(item) for item in data.get("unfavorable_gods") or []],
        reasoning=str(data.get("reasoning") or ""),
        confidence=float(data.get("confidence") or 0.0),
        missing_data=missing,
    )


class UsefulGodDomainComposer:
    """Compose balance strategy — how should this chart maintain balance?"""

    def compose(self, facts: UsefulGodPublishedFacts) -> DomainInterpretationResult:
        """Build Useful God / balance interpretation from published facts."""
        if not facts.useful_god:
            return DomainInterpretationResult(
                domain="useful_god",
                status=DomainStatus.INSUFFICIENT,
                missing_data=facts.missing_data or ["useful_god"],
                knowledge_status=KnowledgeStatus.DRAFT_KNOWLEDGE,
            )

        conclusion = (
            f"Chiến lược cân bằng lấy {facts.useful_god} làm trọng tâm điều tiết."
        )
        if facts.reasoning:
            conclusion += f" Cơ sở từ dữ liệu đã công bố: {facts.reasoning}."

        sections = [
            DomainSection(
                section_id="STRATEGY",
                title="Chiến lược cân bằng",
                paragraphs=[conclusion],
                theme_ids=[THEME_BALANCE_STRATEGY, THEME_OUTPUT_RELEASE],
            )
        ]
        claims = [
            DomainClaim(
                claim_id="ug_strategy",
                theme_id=THEME_BALANCE_STRATEGY,
                text=conclusion,
                domain="useful_god",
            ),
            DomainClaim(
                claim_id="ug_output",
                theme_id=THEME_OUTPUT_RELEASE,
                text=f"Trọng tâm điều tiết: {facts.useful_god}",
                domain="useful_god",
            ),
        ]

        if facts.favorable_gods:
            fav = ", ".join(facts.favorable_gods)
            fav_text = f"Các yếu tố thuận: {fav}."
            sections.append(
                DomainSection(
                    section_id="FAVORABLE",
                    title="Yếu tố thuận",
                    paragraphs=[fav_text],
                    theme_ids=[],
                )
            )

        if facts.unfavorable_gods:
            unfav = ", ".join(facts.unfavorable_gods)
            unfav_text = (
                f"Các yếu tố cần hạn chế: {unfav}. "
                "Không diễn giải thành lối sống nếu thiếu cơ sở tri thức."
            )
            sections.append(
                DomainSection(
                    section_id="UNFAVORABLE",
                    title="Yếu tố bất lợi",
                    paragraphs=[unfav_text],
                    theme_ids=[THEME_NO_EXTRA_LOAD],
                )
            )
            claims.append(
                DomainClaim(
                    claim_id="ug_no_extra",
                    theme_id=THEME_NO_EXTRA_LOAD,
                    text=unfav_text,
                    domain="useful_god",
                    polarity="caution",
                )
            )

        recommendations = [
            f"Ưu tiên hành động theo hướng {facts.useful_god} khi cần điều tiết hệ.",
        ]
        if facts.unfavorable_gods:
            recommendations.append(
                f"Tránh khuếch đại {', '.join(facts.unfavorable_gods[:2])} khi hệ đã căng."
            )

        return DomainInterpretationResult(
            domain="useful_god",
            status=DomainStatus.AVAILABLE,
            conclusion=conclusion,
            sections=sections,
            recommendations=recommendations,
            executive_claims=[conclusion],
            missing_data=list(facts.missing_data),
            diagnostics={
                "useful_god": facts.useful_god,
                "confidence": facts.confidence,
                "knowledge_note": "No PACK Useful God catalog — pilot fact composer",
            },
            version="1.0.0",
            knowledge_status=KnowledgeStatus.DRAFT_KNOWLEDGE,
            claims=claims,
        )
