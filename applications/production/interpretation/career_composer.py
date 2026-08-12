"""Career Report feature — composed from CrossDomainReasoningResult (CAREER context)."""

from __future__ import annotations

from applications.production.interpretation.contracts import (
    DomainSection,
    DomainStatus,
    ExecutiveConsultingResult,
    KnowledgeStatus,
)
from applications.production.interpretation.cross_domain.models import (
    CrossDomainReasoningResult,
    RelationType,
    ThemeStatus,
)
from applications.production.interpretation.cross_domain import theme_engine as te


# Forbidden invented career claims — not supported by V1.1 domains.
_FORBIDDEN_CAREER_TOKENS = (
    "chức danh",
    "job title",
    "thu nhập",
    "income",
    "timing sự nghiệp",
    "thành công kinh doanh",
)


class CareerFeatureComposer:
    """Career feature from CDR with CAREER salience — no invented titles/income."""

    def compose(
        self,
        reasoning: CrossDomainReasoningResult,
    ) -> ExecutiveConsultingResult:
        """Build Career feature body from CDR result."""
        plan = reasoning.executive_claim_plan
        primary = next(
            (t for t in reasoning.themes if t.status == ThemeStatus.PRIMARY),
            None,
        )
        work_style = plan.operating_style or (
            primary.label if primary else "Phong cách làm việc chưa đủ dữ liệu."
        )
        authority = self._authority(reasoning)
        autonomy = self._autonomy(reasoning)
        structure = plan.identity_core
        pressure = self._pressure(reasoning, plan)
        balance = plan.balance_direction or "Hướng cân bằng chưa công bố."

        nuance = [
            r.customer_safe_state
            for r in reasoning.relations
            if r.customer_safe_state
            and r.relation_type
            in {
                RelationType.CONDITIONAL_NUANCE,
                RelationType.DEPENDENCY_OVERRIDE,
                RelationType.DIFFERENT_SCOPE,
                RelationType.TRUE_CONFLICT,
            }
        ]

        sections = [
            DomainSection("WORK_STYLE", "Phong cách làm việc", [work_style]),
            DomainSection("AUTHORITY", "Quan hệ quyền lực / chuẩn mực", [authority]),
            DomainSection("AUTONOMY", "Mức tự chủ vận hành", [autonomy]),
            DomainSection("STRUCTURE", "Khung cấu trúc nghề nghiệp dài hạn", [structure]),
            DomainSection("PRESSURE", "Phản ứng với áp lực", [pressure]),
            DomainSection("BALANCE", "Hướng cân bằng trong công việc", [balance]),
            DomainSection(
                "PRIORITIES",
                "Ưu tiên nghề nghiệp (từ claim plan)",
                [" · ".join(plan.priorities[:3]) or "Giữ phạm vi dữ liệu đã công bố."],
            ),
            DomainSection(
                "AVOIDS",
                "Cần tránh",
                [" · ".join(plan.avoidances[:3])],
            ),
        ]
        if nuance:
            sections.append(
                DomainSection(
                    "NUANCE",
                    "Đọc có điều kiện",
                    [nuance[0]],
                )
            )

        body = "\n\n".join(
            f"# {section.title}\n\n{chr(10).join(section.paragraphs)}"
            for section in sections
        )
        for token in _FORBIDDEN_CAREER_TOKENS:
            if token in body.lower():
                body = body.replace(token, "[không công bố]")

        status = DomainStatus.AVAILABLE
        if reasoning.diagnostics.get("missing_domains"):
            status = DomainStatus.PARTIAL
        if not reasoning.claims:
            status = DomainStatus.NOT_AVAILABLE
            body = "CAREER_REPORT_NOT_AVAILABLE"

        return ExecutiveConsultingResult(
            status=status,
            body=body,
            sections=sections if status != DomainStatus.NOT_AVAILABLE else [],
            recommendations=list(plan.priorities)[:3],
            version="1.1.0",
            knowledge_status=KnowledgeStatus.PILOT,
            diagnostics={
                "question_context": reasoning.question_context.value,
                "primary_theme": reasoning.primary_theme,
                "conflicts": list(reasoning.conflicts),
                "tensions": list(reasoning.tensions),
                "forbidden_inventions": "titles_income_timing_business_success_blocked",
            },
        )

    @staticmethod
    def _authority(reasoning: CrossDomainReasoningResult) -> str:
        theme_ids = {t.theme_id for t in reasoning.themes if t.status != ThemeStatus.SUPPRESSED}
        if te.THEME_OPERATING_STANDARDS in theme_ids:
            return "Áp lực chuẩn mực / trách nhiệm là một tín hiệu vận hành đã công bố."
        return (
            "Quan hệ quyền lực chỉ được nêu khi có tín hiệu Quan/Sát hoặc chuẩn mực "
            "trong dữ liệu Thập Thần — không suy diễn chức danh."
        )

    @staticmethod
    def _autonomy(reasoning: CrossDomainReasoningResult) -> str:
        theme_ids = {t.theme_id for t in reasoning.themes if t.status != ThemeStatus.SUPPRESSED}
        if te.THEME_OPERATING_OUTPUT in theme_ids:
            return "Xu hướng tự chủ qua kênh biểu đạt / đầu ra — không phải cam kết thu nhập."
        if te.THEME_OPERATING_SELF_CARRY in theme_ids:
            return "Xu hướng tự lực đồng hành — cần ranh giới tải rõ."
        if te.THEME_FOLLOW_STRUCTURE in theme_ids:
            return "Tự chủ cần bám khung cấu trúc Tòng đã công bố — không ép khung Nhật chủ thường."
        return "Mức tự chủ được nêu khi có tín hiệu vận hành tương ứng."

    @staticmethod
    def _pressure(reasoning: CrossDomainReasoningResult, plan) -> str:
        if plan.main_constraint:
            for relation in reasoning.relations:
                if relation.relation_id == plan.main_constraint and relation.customer_safe_state:
                    return relation.customer_safe_state
        return "Phản ứng áp lực được đọc qua căng liên miền và hướng cân bằng — không timeline."
