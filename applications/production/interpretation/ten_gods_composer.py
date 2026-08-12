"""Ten Gods published facts + Vietnamese system composer."""

from __future__ import annotations

from dataclasses import dataclass, field

from engines.ten_gods_engine.constants import GOD_ID_TO_FAMILY, GOD_ID_TO_LABEL
from engines.ten_gods_engine.models import TenGodsResult

from applications.production.interpretation.contracts import (
    DomainClaim,
    DomainInterpretationResult,
    DomainSection,
    DomainStatus,
    KnowledgeStatus,
)
from applications.production.interpretation.theme_keys import (
    FAMILY_VI,
    RELATION_VI,
    THEME_OPERATING_SYSTEM,
    THEME_PRESSURE,
    THEME_RESOURCE_SUPPORT,
    THEME_RESPONSIBILITY,
)


@dataclass(slots=True)
class TenGodsPublishedFacts:
    """Published Ten Gods facts for composition — no recalculation."""

    day_master_stem: str
    day_master_element: str
    day_master_yin_yang: str
    dominant_status: str
    primary_labels: list[str] = field(default_factory=list)
    secondary_labels: list[str] = field(default_factory=list)
    relationship_summaries: list[str] = field(default_factory=list)
    family_presence: dict[str, list[str]] = field(default_factory=dict)
    missing_data: list[str] = field(default_factory=list)
    has_system: bool = False


def build_ten_gods_published_facts(result: TenGodsResult) -> TenGodsPublishedFacts:
    """Map TenGodsResult to published composition facts."""
    primary = [
        GOD_ID_TO_LABEL.get(god_id, god_id)
        for god_id in result.dominant.primary_god_ids
    ]
    secondary = [
        entry.label
        for entry in result.hierarchy
        if entry.tier == "SECONDARY"
    ]
    families: dict[str, list[str]] = {}
    for entry in result.hierarchy:
        if entry.tier in {"PRIMARY", "SECONDARY"}:
            family = GOD_ID_TO_FAMILY.get(entry.god_id, "unknown")
            families.setdefault(family, []).append(entry.label)

    relationships: list[str] = []
    for edge in result.relationships[:8]:
        left = GOD_ID_TO_LABEL.get(edge.from_god_id, edge.from_god_id)
        right = GOD_ID_TO_LABEL.get(edge.to_god_id, edge.to_god_id)
        rel = RELATION_VI.get(edge.relation, edge.relation)
        relationships.append(f"{left} → {right} ({rel})")

    return TenGodsPublishedFacts(
        day_master_stem=result.day_master.stem,
        day_master_element=result.day_master.element,
        day_master_yin_yang=result.day_master.yin_yang,
        dominant_status=result.dominant.status,
        primary_labels=primary,
        secondary_labels=secondary,
        relationship_summaries=relationships,
        family_presence=families,
        missing_data=list(result.missing_data),
        has_system=bool(primary or secondary),
    )


class TenGodsDomainComposer:
    """Compose Ten Gods system interpretation — not ten textbook definitions."""

    def compose(self, facts: TenGodsPublishedFacts) -> DomainInterpretationResult:
        """Build Ten Gods domain interpretation from published facts."""
        if not facts.has_system:
            return DomainInterpretationResult(
                domain="ten_gods",
                status=DomainStatus.INSUFFICIENT,
                missing_data=["ten_gods_system"],
                knowledge_status=KnowledgeStatus.DRAFT_KNOWLEDGE,
            )

        primary = ", ".join(facts.primary_labels) or "chưa xác định"
        secondary = ", ".join(facts.secondary_labels[:3])
        conclusion = (
            f"Hệ Thập Thần vận hành quanh vai trò chủ đạo {primary}"
            + (f", với lớp phụ {secondary}" if secondary else "")
            + ". Đây là cấu trúc vận hành tổng thể — không phải mười định nghĩa rời."
        )

        sections = [
            DomainSection(
                section_id="SYSTEM",
                title="Cấu trúc vận hành",
                paragraphs=[conclusion],
                theme_ids=[THEME_OPERATING_SYSTEM, THEME_RESPONSIBILITY],
            )
        ]
        claims = [
            DomainClaim(
                claim_id="tg_system",
                theme_id=THEME_OPERATING_SYSTEM,
                text=conclusion,
                domain="ten_gods",
            ),
            DomainClaim(
                claim_id="tg_responsibility",
                theme_id=THEME_RESPONSIBILITY,
                text=f"Vai trò chủ đạo: {primary}",
                domain="ten_gods",
            ),
        ]

        family_lines: list[str] = []
        for family, labels in sorted(facts.family_presence.items()):
            family_lines.append(
                f"{FAMILY_VI.get(family, family)}: {', '.join(labels)}"
            )
        if family_lines:
            sections.append(
                DomainSection(
                    section_id="ROLES",
                    title="Vai trò nổi bật",
                    paragraphs=[
                        "Các nhóm vai trò đang hiện diện: "
                        + "; ".join(family_lines)
                        + "."
                    ],
                    theme_ids=[],
                )
            )

        if "officer" in facts.family_presence:
            pressure = (
                "Lớp quan sát/áp lực chuẩn đang hiện diện — "
                "hệ dễ vận hành theo trách nhiệm và chuẩn mực."
            )
            sections.append(
                DomainSection(
                    section_id="PRESSURE",
                    title="Áp lực và chuẩn",
                    paragraphs=[pressure],
                    theme_ids=[THEME_PRESSURE],
                )
            )
            claims.append(
                DomainClaim(
                    claim_id="tg_pressure",
                    theme_id=THEME_PRESSURE,
                    text=pressure,
                    domain="ten_gods",
                    polarity="caution",
                )
            )

        if "resource" in facts.family_presence:
            support = (
                "Lớp ấn/hỗ trợ hiện diện — "
                "hệ có nền học hỏi và phục hồi bên cạnh tải trách nhiệm."
            )
            sections.append(
                DomainSection(
                    section_id="SUPPORT",
                    title="Hỗ trợ nội tại",
                    paragraphs=[support],
                    theme_ids=[THEME_RESOURCE_SUPPORT],
                )
            )
            claims.append(
                DomainClaim(
                    claim_id="tg_resource",
                    theme_id=THEME_RESOURCE_SUPPORT,
                    text=support,
                    domain="ten_gods",
                    polarity="support",
                )
            )

        if facts.relationship_summaries:
            sections.append(
                DomainSection(
                    section_id="RELATIONSHIPS",
                    title="Quan hệ cấu trúc",
                    paragraphs=[
                        "Một số quan hệ cấu trúc chính: "
                        + "; ".join(facts.relationship_summaries[:5])
                        + "."
                    ],
                    theme_ids=[],
                )
            )

        recommendations = [
            f"Điều phối theo vai trò chủ đạo ({primary}) — không phân tán sang mọi hướng cùng lúc."
        ]
        if "officer" in facts.family_presence:
            recommendations.append(
                "Đặt ranh giới cam kết rõ trước khi nhận thêm trách nhiệm."
            )

        status = (
            DomainStatus.PARTIAL
            if facts.missing_data
            else DomainStatus.AVAILABLE
        )
        return DomainInterpretationResult(
            domain="ten_gods",
            status=status,
            conclusion=conclusion,
            sections=sections,
            recommendations=recommendations,
            executive_claims=[conclusion],
            missing_data=list(facts.missing_data),
            diagnostics={
                "dominant_status": facts.dominant_status,
                "primary": facts.primary_labels,
                "secondary": facts.secondary_labels,
                "knowledge_note": "No PACK Ten Gods catalog — pilot fact composer",
            },
            version="1.0.0",
            knowledge_status=KnowledgeStatus.DRAFT_KNOWLEDGE,
            claims=claims,
        )
