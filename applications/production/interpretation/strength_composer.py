"""Strength domain composition — wraps V2 runtime with Vietnamese customer prose."""

from __future__ import annotations

from engines.interpretation_engine_v2.strength.contracts.models import AudienceMode
from engines.interpretation_engine_v2.strength.runtime.published_facts_adapter import (
    build_published_strength_facts,
)
from engines.interpretation_engine_v2.strength.runtime.service import (
    StrengthInterpretationService,
)
from engines.strength_engine.context import StrengthContext
from engines.strength_engine.models import StrengthResult

from applications.production.interpretation.contracts import (
    DomainClaim,
    DomainInterpretationResult,
    DomainSection,
    DomainStatus,
    KnowledgeStatus,
)
from applications.production.interpretation.theme_keys import (
    STRENGTH_LEVEL_VI,
    THEME_ENDURANCE,
    THEME_OUTPUT_RELEASE,
)


class StrengthDomainComposer:
    """Compose Strength domain interpretation from live engine facts."""

    def __init__(
        self,
        strength_service: StrengthInterpretationService | None = None,
    ) -> None:
        self._service = strength_service or StrengthInterpretationService()

    def compose(
        self,
        *,
        case_id: str,
        strength_result: StrengthResult,
        strength_context: StrengthContext,
    ) -> DomainInterpretationResult:
        """Run Strength V2 and project to DomainInterpretationResult."""
        if not strength_result.success:
            return DomainInterpretationResult(
                domain="strength",
                status=DomainStatus.INSUFFICIENT,
                conclusion="",
                missing_data=["strength_result"],
                knowledge_status=KnowledgeStatus.DRAFT_KNOWLEDGE,
                diagnostics={"reason": "strength_engine_failed"},
            )

        published = build_published_strength_facts(
            case_id=case_id,
            strength_result=strength_result,
            strength_context=strength_context,
        )
        v2 = self._service.interpret(
            published=published,
            audience=AudienceMode.CUSTOMER,
        )

        level = strength_result.strength_level
        level_vi = STRENGTH_LEVEL_VI.get(level, level)
        conclusion = (
            f"Nội lực của bạn thuộc nhóm {level_vi} — "
            f"hệ vận hành nghiêng về sức bền và khả năng chịu tải."
            if level in {"strong", "very_strong"}
            else (
                f"Nội lực của bạn thuộc nhóm {level_vi} — "
                f"hệ cần giữ nhịp cân bằng, tránh ép quá sức."
                if level == "balanced"
                else (
                    f"Nội lực của bạn thuộc nhóm {level_vi} — "
                    f"ưu tiên bảo toàn lực và chọn tải phù hợp."
                )
            )
        )

        sections = [
            DomainSection(
                section_id="CONCLUSION",
                title="Kết luận nội lực",
                paragraphs=[conclusion],
                theme_ids=[THEME_ENDURANCE],
            )
        ]
        claims = [
            DomainClaim(
                claim_id="str_endurance",
                theme_id=THEME_ENDURANCE,
                text=conclusion,
                domain="strength",
                polarity="support" if level in {"strong", "very_strong"} else "neutral",
            )
        ]

        if strength_context.drain_count == 0:
            release = (
                "Khi nội lực đủ mạnh mà đầu ra tiết khí chưa rõ, "
                "hệ dễ tích áp lực — cần kênh đầu ra có chu kỳ."
            )
            sections.append(
                DomainSection(
                    section_id="BALANCE_HINT",
                    title="Gợi ý cân bằng",
                    paragraphs=[release],
                    theme_ids=[THEME_OUTPUT_RELEASE],
                )
            )
            claims.append(
                DomainClaim(
                    claim_id="str_output_hint",
                    theme_id=THEME_OUTPUT_RELEASE,
                    text=release,
                    domain="strength",
                    polarity="caution",
                )
            )

        why_parts: list[str] = []
        if strength_context.season:
            why_parts.append(f"bối cảnh mùa ({strength_context.season})")
        if strength_context.root_level:
            why_parts.append(f"căn khí ({strength_context.root_level})")
        if strength_context.support_type:
            why_parts.append(f"hỗ trợ ({strength_context.support_type})")
        if strength_context.control_type:
            why_parts.append(f"kiểm soát ({strength_context.control_type})")
        if why_parts:
            why_text = (
                "Các tín hiệu chính tạo nên kết luận này gồm: "
                + "; ".join(why_parts)
                + "."
            )
            sections.append(
                DomainSection(
                    section_id="WHY",
                    title="Vì sao",
                    paragraphs=[why_text],
                    theme_ids=[],
                )
            )

        recommendations: list[str] = []
        if level in {"strong", "very_strong"}:
            recommendations.append(
                "Ưu tiên chuyển tải thành đầu ra có hình dạng — không chỉ gánh thêm."
            )
        elif level in {"weak", "very_weak"}:
            recommendations.append(
                "Ưu tiên bảo toàn lực và chọn cam kết vừa sức trước khi mở rộng."
            )
        else:
            recommendations.append(
                "Giữ nhịp cân bằng: đủ tải để phát triển, đủ nghỉ để phục hồi."
            )

        missing: list[str] = []
        if published.facts.get("luck_interaction") and str(
            published.facts["luck_interaction"].value
        ) == "MISSING":
            missing.append("luck_interaction")
        if published.facts.get("hidden_stems") and str(
            published.facts["hidden_stems"].value
        ) == "MISSING":
            missing.append("hidden_stems")

        return DomainInterpretationResult(
            domain="strength",
            status=DomainStatus.AVAILABLE,
            conclusion=conclusion,
            sections=sections,
            recommendations=recommendations,
            executive_claims=[conclusion],
            missing_data=missing,
            diagnostics={
                "class_id": published.class_id,
                "narrative_primary": v2.narrative_plan.primary_conclusion,
                "v2_section_count": len(v2.customer_mode),
                "catalog_version": v2.meta.catalog_version,
            },
            version="1.0.0",
            knowledge_status=KnowledgeStatus.DRAFT_KNOWLEDGE,
            claims=claims,
        )
