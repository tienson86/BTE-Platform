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
from applications.production.product_context.feature_filter import (
    FEATURE_CAREER,
    FEATURE_DEVELOPMENT,
    FEATURE_EXECUTIVE,
    FEATURE_IDENTITY,
    FEATURE_PARENT,
)
from applications.production.product_context.models import (
    ActionProfile,
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
                "delivery": "context_adapted",
                "language_profile": context.language_profile.value,
                "action_profile": context.action_profile.value,
            },
        )

    def _development_identity(
        self,
        composition: MultiDomainCompositionResult,
        context: ProductContextResult,
    ) -> ExecutiveConsultingResult:
        plan = composition.cross_domain.executive_claim_plan
        theme = composition.cross_domain.primary_theme
        age_note = (
            f"Độ tuổi hiện tại khoảng {context.subject_age} — "
            if context.subject_age is not None
            else ""
        )
        who = (
            f"{age_note}Báo cáo này hướng tới nhận diện tiềm năng phát triển của trẻ, "
            "không phải tư vấn nghề nghiệp người lớn."
        )
        style = (
            "Xu hướng vận hành nổi bật nghiêng về việc được tạo ra / biểu đạt / có phản hồi rõ — "
            "nên được hiểu như nhu cầu phát triển, không phải áp lực thành tích."
            if theme == "OPERATING_OUTPUT"
            else "Xu hướng vận hành cần được nuôi dưỡng theo đúng kênh đã công bố, với biên bảo toàn."
        )
        capacity = ""
        if "weak" in (plan.identity_core or "") or "body:weak" in (plan.identity_core or ""):
            capacity = (
                "Nền năng lượng đang thiên về cần bảo toàn: ưu tiên nghỉ ngơi, nhịp nhẹ, "
                "tránh ép cường độ học / hoạt động quá tải."
            )
        elif "balanced" in (plan.identity_core or ""):
            capacity = "Nền năng lượng trung hòa: giữ nhịp đều, tránh dồn ép thành tích ngắn hạn."
        else:
            capacity = "Nền năng lượng cần được đọc cùng khung phát triển dài hạn — không ép khuôn người lớn."

        nuance = ""
        if composition.cross_domain.tensions or composition.cross_domain.conflicts:
            nuance = (
                "Có điểm cần đọc có điều kiện giữa các lớp phân tích — "
                "người lớn nên giữ cả hai tín hiệu thay vì gắn một nhãn duy nhất cho trẻ."
            )

        actions = [
            "Tạo môi trường có sản phẩm nhỏ / phản hồi rõ, không biến thành áp lực thành tích.",
            "Ưu tiên bảo toàn năng lượng trước khi mở rộng lịch hoạt động.",
            "Không dùng báo cáo này để chọn nghề, kinh doanh, hoặc timing hôn nhân.",
        ]
        if context.action_profile == ActionProfile.PARENT_ACTIONS:
            actions = [f"Phụ huynh: {a}" for a in actions]

        sections = [
            DomainSection("WHO", "Nhận diện phát triển", [who]),
            DomainSection("OPERATING", "Xu hướng vận hành cần nuôi dưỡng", [style]),
            DomainSection("CAPACITY", "Nền năng lượng & biên bảo toàn", [capacity]),
            DomainSection(
                "ENVIRONMENT",
                "Môi trường hỗ trợ",
                [
                    "Môi trường hợp hơn khi có không gian tạo ra / thể hiện nhẹ nhàng và được công nhận đúng mức — "
                    "không phải sân chơi cạnh tranh người lớn."
                ],
            ),
        ]
        if nuance:
            sections.append(DomainSection("CONDITION", "Đọc có điều kiện", [nuance]))
        sections.append(
            DomainSection(
                "ACTIONS",
                "Việc người lớn nên làm",
                actions,
            )
        )
        sections.append(
            DomainSection(
                "SUMMARY",
                "Tóm tắt định hướng phát triển",
                [
                    "Nuôi dưỡng đúng kênh vận hành với biên bảo toàn — "
                    "không biến lá số trẻ em thành tư vấn nghề nghiệp."
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
            version="1.0.0",
            knowledge_status=KnowledgeStatus.PILOT,
            diagnostics={
                "product_context": "development_identity",
                "source_theme": theme,
                "claims_unchanged": True,
            },
        )

    def _parent_executive(
        self,
        composition: MultiDomainCompositionResult,
        context: ProductContextResult,
    ) -> ExecutiveConsultingResult:
        theme = composition.cross_domain.primary_theme
        conflicts = composition.cross_domain.conflicts
        who = (
            "Đây là bản tư vấn cho người lớn đang đồng hành với trẻ — "
            "không phải báo cáo tự quyết nghề nghiệp của người lớn."
        )
        system = (
            "Trẻ có xu hướng vận hành theo kênh đầu ra / biểu đạt."
            if theme == "OPERATING_OUTPUT"
            else "Trẻ có xu hướng vận hành theo kênh đã công bố trong claim plan."
        )
        limits = (
            "Ưu tiên bảo toàn năng lượng; tránh ép lịch và thành tích."
            if "weak" in (composition.cross_domain.executive_claim_plan.identity_core or "")
            else "Giữ biên tải phù hợp độ tuổi."
        )
        if conflicts:
            limits += (
                " Có xung đột điều tiết đã được đánh dấu ở tầng lý giải — "
                "không kết luận một hướng duy nhất khi dữ liệu còn treo."
            )
        actions = [
            "1. Giữ môi trường phản hồi rõ, cường độ nhẹ.",
            "2. Bảo toàn nghỉ ngơi trước khi thêm hoạt động.",
            "3. Không dùng báo cáo trẻ em cho Career / business / marriage timing.",
        ]
        sections = [
            DomainSection("WHO", "Đối tượng đọc", [who]),
            DomainSection("SYSTEM", "Xu hướng cần hiểu", [system]),
            DomainSection("LIMITS", "Biên cần giữ", [limits]),
            DomainSection("PRIORITIES", "Ưu tiên của phụ huynh", actions),
            DomainSection(
                "CONCLUSION",
                "Kết luận đồng hành",
                [
                    "Đồng hành phát triển theo đúng kênh và biên bảo toàn — "
                    "Career Decision bị ẩn bởi Product Context."
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
            recommendations=[a[3:] if a[0].isdigit() else a for a in actions],
            version="1.0.0",
            knowledge_status=KnowledgeStatus.PILOT,
            diagnostics={
                "product_context": "parent_executive",
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
        lines = [
            "# Định hướng phát triển",
            "",
            "Báo cáo phát triển (không phải Career Decision).",
            "",
            f"- Life stage: {context.life_stage.value}",
            f"- Language profile: {context.language_profile.value}",
            f"- Theme định hướng (từ claim plan): {theme}",
            "",
            "Tập trung nuôi dưỡng kênh vận hành phù hợp và bảo toàn năng lượng theo độ tuổi.",
        ]
        return "\n".join(lines)

    def _parent_guidance(
        self,
        composition: MultiDomainCompositionResult,
        context: ProductContextResult,
    ) -> str:
        return "\n".join(
            [
                "# Hướng dẫn cho phụ huynh",
                "",
                "Bạn đang đọc với vai trò người lớn đồng hành.",
                "",
                "1. Không biến nhận diện vận hành thành áp lực thành tích.",
                "2. Ưu tiên bảo toàn năng lượng nếu tín hiệu nền yếu / cần nghỉ.",
                "3. Career Decision, business advice, và marriage timing bị chặn ở độ tuổi này.",
                "4. Khi có căng giữa các lớp phân tích, giữ đọc có điều kiện — không gắn một nhãn.",
                "",
                f"Action profile: {context.action_profile.value}",
            ]
        )
