"""Apply ProductContextResult to composed features — delivery only, no claim rewrite."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from applications.production.interpretation.contracts import (
    DomainSection,
    DomainStatus,
    ExecutiveConsultingResult,
    KnowledgeStatus,
)
from applications.production.interpretation.service import MultiDomainCompositionResult
from applications.production.product_context import adaptive as adp
from applications.production.product_context.feature_filter import (
    FEATURE_CAREER,
    FEATURE_DEVELOPMENT,
    FEATURE_EXECUTIVE,
    FEATURE_IDENTITY,
    FEATURE_PARENT,
)
from applications.production.product_context.models import (
    LanguageProfile,
    LifeStage,
    ProductContextResult,
)


@dataclass(slots=True)
class ContextDeliveryBundle:
    """Customer-facing feature bodies after context filtering."""

    identity: ExecutiveConsultingResult
    career: ExecutiveConsultingResult
    executive: ExecutiveConsultingResult
    development_guidance: str = ""
    parent_guidance: str = ""
    context: ProductContextResult | None = None
    diagnostics: dict[str, Any] | None = None


class ContextDeliveryAdapter:
    """
    Transform composed consulting into audience-correct delivery.

    Does not modify CDR claims or CLL source. For adult pass-through,
    returns original feature bodies unchanged.
    """

    def apply(
        self,
        composition: MultiDomainCompositionResult,
        context: ProductContextResult,
    ) -> ContextDeliveryBundle:
        """Filter and reframe feature delivery by product context."""
        if context.pass_through and FEATURE_CAREER in context.visible_features:
            return ContextDeliveryBundle(
                identity=composition.identity,
                career=composition.career,
                executive=composition.executive,
                development_guidance="",
                parent_guidance="",
                context=context,
                diagnostics={"delivery": "pass_through"},
            )

        identity = composition.identity
        career = composition.career
        executive = composition.executive
        development = ""
        parent = ""

        if FEATURE_CAREER not in context.visible_features:
            career = ExecutiveConsultingResult(
                status=DomainStatus.NOT_AVAILABLE,
                body="CAREER_REPORT_HIDDEN_BY_PRODUCT_CONTEXT",
                sections=[],
                recommendations=[],
                version="1.0.0",
                knowledge_status=KnowledgeStatus.PILOT,
                diagnostics={
                    "blocked_by": "product_context",
                    "life_stage": context.life_stage.value,
                    "safety_blocks": list(context.safety_blocks),
                },
            )

        if context.life_stage in {LifeStage.CHILD, LifeStage.TEEN} or (
            context.language_profile == LanguageProfile.PARENT_SUPPORT
        ):
            identity = self._development_identity(composition, context)
            executive = self._parent_executive(composition, context)
            if FEATURE_DEVELOPMENT in context.visible_features:
                development = self._development_guidance(composition, context)
            if FEATURE_PARENT in context.visible_features:
                parent = self._parent_guidance(composition, context)

        if FEATURE_IDENTITY not in context.visible_features:
            identity = ExecutiveConsultingResult(
                status=DomainStatus.NOT_AVAILABLE,
                body="IDENTITY_REPORT_HIDDEN_BY_PRODUCT_CONTEXT",
                sections=[],
                version="1.0.0",
                knowledge_status=KnowledgeStatus.PILOT,
                diagnostics={"blocked_by": "product_context"},
            )

        if FEATURE_EXECUTIVE not in context.visible_features:
            executive = ExecutiveConsultingResult(
                status=DomainStatus.NOT_AVAILABLE,
                body="EXECUTIVE_CONSULTING_HIDDEN_BY_PRODUCT_CONTEXT",
                sections=[],
                version="1.0.0",
                knowledge_status=KnowledgeStatus.PILOT,
                diagnostics={"blocked_by": "product_context"},
            )

        return ContextDeliveryBundle(
            identity=identity,
            career=career,
            executive=executive,
            development_guidance=development,
            parent_guidance=parent,
            context=context,
            diagnostics={
                "delivery": "adaptive",
                "language_profile": context.language_profile.value,
                "action_profile": context.action_profile.value,
                "replacements": [src for src, _dst, _why in adp.REPLACEMENTS],
            },
        )

    def _development_identity(
        self,
        composition: MultiDomainCompositionResult,
        context: ProductContextResult,
    ) -> ExecutiveConsultingResult:
        reasoning = composition.cross_domain
        theme = reasoning.primary_theme
        weak = adp.is_weak_capacity(reasoning)
        actions = adp.parent_actions(
            theme=theme,
            weak=weak,
            action_profile=context.action_profile,
        )
        nuance = adp.conflict_nuance(reasoning)
        sections = [
            DomainSection("WHO", "Nhận diện phát triển", [adp.parent_who(context)]),
            DomainSection(
                "OPERATING",
                "Nhu cầu phát triển cần nuôi dưỡng",
                [adp.development_operating_frame(theme)],
            ),
            DomainSection(
                "CAPACITY",
                "Nền năng lượng & biên bảo toàn",
                [adp.conservation_line(weak)],
            ),
            DomainSection(
                "LEARNING",
                "Môi trường học tập",
                [adp.learning_environment(theme)],
            ),
            DomainSection(
                "CONFIDENCE",
                "Xây tự tin",
                [adp.confidence_building(theme)],
            ),
        ]
        if nuance:
            sections.append(DomainSection("CONDITION", "Đọc có điều kiện", [nuance]))
        sections.append(DomainSection("ACTIONS", "Việc phụ huynh nên làm", actions))
        sections.append(
            DomainSection(
                "SUMMARY",
                "Tóm tắt định hướng phát triển",
                [
                    "Đồng hành học tập và xây tự tin trong biên bảo toàn — "
                    "không biến lá số trẻ em thành tư vấn nghề hay kinh doanh người lớn."
                ],
            )
        )
        body = "\n\n".join(
            f"# {s.title}\n\n" + "\n\n".join(s.paragraphs) for s in sections
        )
        return ExecutiveConsultingResult(
            status=DomainStatus.AVAILABLE,
            body=body,
            sections=sections,
            recommendations=actions[:3],
            version="1.1.0",
            knowledge_status=KnowledgeStatus.PILOT,
            diagnostics={
                "product_context": "adaptive_development_identity",
                "source_theme": theme,
                "claims_unchanged": True,
            },
        )

    def _parent_executive(
        self,
        composition: MultiDomainCompositionResult,
        context: ProductContextResult,
    ) -> ExecutiveConsultingResult:
        reasoning = composition.cross_domain
        theme = reasoning.primary_theme
        weak = adp.is_weak_capacity(reasoning)
        conflicts = reasoning.conflicts
        limits = adp.conservation_line(weak)
        nuance = adp.conflict_nuance(reasoning)
        if nuance:
            limits = f"{limits} {nuance}"
        raw_actions = adp.parent_actions(
            theme=theme,
            weak=weak,
            action_profile=context.action_profile,
        )
        numbered = [f"{index}. {item}" for index, item in enumerate(raw_actions[:3], start=1)]
        sections = [
            DomainSection(
                "WHO",
                "Đối tượng đọc",
                [
                    "Đây là bản đồng hành cho phụ huynh — "
                    "không phải báo cáo tự quyết nghề nghiệp của người lớn."
                ],
            ),
            DomainSection(
                "SYSTEM",
                "Nhu cầu phát triển cần hiểu",
                [adp.development_operating_frame(theme)],
            ),
            DomainSection("LIMITS", "Biên cần giữ", [limits]),
            DomainSection(
                "LEARNING",
                "Học tập thay cho kinh doanh",
                [adp.learning_environment(theme)],
            ),
            DomainSection(
                "CONFIDENCE",
                "Tự tin thay cho lãnh đạo",
                [adp.confidence_building(theme)],
            ),
            DomainSection("PRIORITIES", "Ưu tiên của phụ huynh", numbered),
            DomainSection(
                "CONCLUSION",
                "Kết luận đồng hành",
                [
                    "Đồng hành học tập và xây tự tin trong biên bảo toàn. "
                    "Career Decision bị ẩn — thay bằng định hướng phát triển."
                ],
            ),
        ]
        body = "\n\n".join(
            f"# {s.title}\n\n" + "\n\n".join(s.paragraphs) for s in sections
        )
        return ExecutiveConsultingResult(
            status=DomainStatus.AVAILABLE,
            body=body,
            sections=sections,
            recommendations=raw_actions[:3],
            version="1.1.0",
            knowledge_status=KnowledgeStatus.PILOT,
            diagnostics={
                "product_context": "adaptive_parent_executive",
                "hidden_career": True,
                "cdr_conflicts": list(conflicts),
            },
        )

    def _development_guidance(
        self,
        composition: MultiDomainCompositionResult,
        context: ProductContextResult,
    ) -> str:
        theme = composition.cross_domain.primary_theme
        weak = adp.is_weak_capacity(composition.cross_domain)
        return "\n".join(
            [
                "# Định hướng phát triển",
                "",
                "Thay cho Career Decision: nuôi dưỡng học tập và xây tự tin theo độ tuổi.",
                "",
                adp.development_operating_frame(theme),
                "",
                adp.learning_environment(theme),
                "",
                adp.confidence_building(theme),
                "",
                adp.conservation_line(weak),
            ]
        )

    def _parent_guidance(
        self,
        composition: MultiDomainCompositionResult,
        context: ProductContextResult,
    ) -> str:
        theme = composition.cross_domain.primary_theme
        weak = adp.is_weak_capacity(composition.cross_domain)
        actions = adp.parent_actions(
            theme=theme,
            weak=weak,
            action_profile=context.action_profile,
        )
        lines = [
            "# Hướng dẫn cho phụ huynh",
            "",
            "Bạn đang đọc với vai trò phụ huynh đồng hành — không phải chủ thể tự quyết nghề.",
            "",
        ]
        for index, item in enumerate(actions, start=1):
            lines.append(f"{index}. {item}")
        lines.extend(
            [
                "",
                "Career Decision và tư vấn kinh doanh không thuộc gói này. "
                "Thay bằng học tập và xây tự tin.",
            ]
        )
        return "\n".join(lines)

