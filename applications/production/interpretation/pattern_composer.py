"""Pattern / destiny structure published facts + Vietnamese composer."""

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
from applications.production.interpretation.theme_keys import THEME_LONG_STRUCTURE, THEME_STRUCTURAL_FRAME


@dataclass(slots=True)
class PatternPublishedFacts:
    """Published Pattern facts for structural composition."""

    success: bool
    pattern_key: str = ""
    pattern_label: str = ""
    tong_cach: str = ""
    dieu_hau: str = ""
    than: str = ""
    than_vuong_nhuoc: str = ""
    dung_than: str = ""
    hy_than: str = ""
    ky_than: str = ""
    missing_data: list[str] = field(default_factory=list)


def build_pattern_published_facts(pattern_view: Any) -> PatternPublishedFacts:
    """Map PatternView / dict to published facts."""
    if pattern_view is None:
        return PatternPublishedFacts(success=False, missing_data=["pattern"])
    data = pattern_view.to_dict() if hasattr(pattern_view, "to_dict") else dict(pattern_view)
    if not data.get("success"):
        return PatternPublishedFacts(success=False, missing_data=["pattern_success"])
    missing: list[str] = []
    for key in ("cach_cuc", "dieu_hau"):
        if not data.get(key):
            missing.append(key)
    return PatternPublishedFacts(
        success=True,
        pattern_key=str(data.get("pattern") or ""),
        pattern_label=str(data.get("cach_cuc") or ""),
        tong_cach=str(data.get("tong_cach") or ""),
        dieu_hau=str(data.get("dieu_hau") or ""),
        than=str(data.get("than") or ""),
        than_vuong_nhuoc=str(data.get("than_vuong_nhuoc") or ""),
        dung_than=str(data.get("dung_than") or ""),
        hy_than=str(data.get("hy_than") or ""),
        ky_than=str(data.get("ky_than") or ""),
        missing_data=missing,
    )


class PatternDomainComposer:
    """Compose destiny structure interpretation — structural only."""

    def compose(self, facts: PatternPublishedFacts) -> DomainInterpretationResult:
        """Answer: how is this chart structurally organized?"""
        if not facts.success or not facts.pattern_label:
            return DomainInterpretationResult(
                domain="pattern",
                status=DomainStatus.INSUFFICIENT,
                missing_data=facts.missing_data or ["pattern_label"],
                knowledge_status=KnowledgeStatus.DRAFT_KNOWLEDGE,
            )

        conclusion = (
            f"Lá số được tổ chức quanh khung cấu trúc {facts.pattern_label}"
            + (f" ({facts.tong_cach})" if facts.tong_cach and facts.tong_cach != facts.pattern_label else "")
            + ". Đây là khung dài hạn — không phải mô tả nội lực hay hệ Thập Thần."
        )
        sections = [
            DomainSection(
                section_id="STRUCTURE",
                title="Khung cấu trúc",
                paragraphs=[conclusion],
                theme_ids=[THEME_STRUCTURAL_FRAME, THEME_LONG_STRUCTURE],
            )
        ]
        claims = [
            DomainClaim(
                claim_id="pat_frame",
                theme_id=THEME_STRUCTURAL_FRAME,
                text=conclusion,
                domain="pattern",
            ),
            DomainClaim(
                claim_id="pat_long",
                theme_id=THEME_LONG_STRUCTURE,
                text=f"Khung dài hạn: {facts.pattern_label}",
                domain="pattern",
            ),
        ]

        detail_parts: list[str] = []
        if facts.dieu_hau:
            detail_parts.append(f"điều hầu: {facts.dieu_hau}")
        if facts.than:
            detail_parts.append(f"thân: {facts.than}")
        if facts.than_vuong_nhuoc:
            detail_parts.append(f"thân khí trong khung: {facts.than_vuong_nhuoc}")
        if detail_parts:
            sections.append(
                DomainSection(
                    section_id="QUALIFIERS",
                    title="Đặc điểm khung",
                    paragraphs=[
                        "Trong khung này, "
                        + "; ".join(detail_parts)
                        + ". Các chỉ số này thuộc cấu trúc — không thay thế luận nội lực."
                    ],
                    theme_ids=[],
                )
            )

        recommendations = [
            f"Giữ nhất quán với khung {facts.pattern_label} — ưu tiên lộ trình dài hạn hơn đổi hướng liên tục."
        ]
        status = (
            DomainStatus.PARTIAL if facts.missing_data else DomainStatus.AVAILABLE
        )
        return DomainInterpretationResult(
            domain="pattern",
            status=status,
            conclusion=conclusion,
            sections=sections,
            recommendations=recommendations,
            executive_claims=[conclusion],
            missing_data=list(facts.missing_data),
            diagnostics={
                "pattern_key": facts.pattern_key,
                "knowledge_note": "No PACK Pattern catalog — pilot fact composer",
            },
            version="1.0.0",
            knowledge_status=KnowledgeStatus.DRAFT_KNOWLEDGE,
            claims=claims,
        )
