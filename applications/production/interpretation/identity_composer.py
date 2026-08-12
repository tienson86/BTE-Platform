"""Identity Report feature — composed from CrossDomainReasoningResult."""

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


class IdentityFeatureComposer:
    """Answer identity questions from cross-domain reasoning — not raw domains."""

    def compose(
        self,
        reasoning: CrossDomainReasoningResult,
    ) -> ExecutiveConsultingResult:
        """Build Identity feature body from CDR result."""
        plan = reasoning.executive_claim_plan
        primary = next(
            (t for t in reasoning.themes if t.status == ThemeStatus.PRIMARY),
            None,
        )
        who = plan.identity_core or (primary.label if primary else "Chưa đủ dữ liệu để mô tả lõi danh tính.")
        operating = plan.operating_style or "Phong cách vận hành chưa được công bố đủ."
        support = plan.main_support or "Yếu tố hỗ trợ được nêu khi có tín hiệu miền tương ứng."
        limit = self._limit_text(reasoning, plan.main_constraint)
        change = self._change_text(plan)

        nuance_notes = [
            r.customer_safe_state
            for r in reasoning.relations
            if r.customer_safe_state
            and r.relation_type
            in {
                RelationType.CONDITIONAL_NUANCE,
                RelationType.DEPENDENCY_OVERRIDE,
                RelationType.DIFFERENT_SCOPE,
                RelationType.TRUE_CONFLICT,
                RelationType.UNRESOLVED,
            }
        ]
        unresolved_block = ""
        if nuance_notes:
            unresolved_block = nuance_notes[0]
        elif reasoning.unresolved:
            unresolved_block = (
                "Dữ liệu hiện tại chưa đủ để khẳng định một kết luận danh tính duy nhất "
                "cho mọi lớp phân tích."
            )

        sections = [
            DomainSection("WHO", "Tôi là ai?", [who]),
            DomainSection("OPERATING", "Mẫu vận hành chủ đạo", [operating]),
            DomainSection("SUPPORT", "Điều gì làm tôi mạnh hơn", [support]),
            DomainSection("LIMIT", "Điều gì giới hạn tôi", [limit]),
            DomainSection("CHANGE", "Tôi nên điều chỉnh gì", [change]),
        ]
        if unresolved_block:
            sections.append(
                DomainSection(
                    "UNRESOLVED",
                    "Điểm cần đọc có điều kiện",
                    [unresolved_block],
                )
            )

        body_parts = [
            f"# {section.title}\n\n{chr(10).join(section.paragraphs)}"
            for section in sections
        ]
        body = "\n\n".join(body_parts)

        status = DomainStatus.AVAILABLE
        if reasoning.diagnostics.get("missing_domains"):
            status = DomainStatus.PARTIAL
        if not reasoning.claims:
            status = DomainStatus.NOT_AVAILABLE
            body = "IDENTITY_REPORT_NOT_AVAILABLE"

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
                "unresolved": list(reasoning.unresolved),
                "why_primary": dict(reasoning.diagnostics.get("why_primary") or {}),
            },
        )

    @staticmethod
    def _limit_text(reasoning: CrossDomainReasoningResult, constraint_key: str) -> str:
        for relation in reasoning.relations:
            if relation.relation_id == constraint_key and relation.customer_safe_state:
                return relation.customer_safe_state
        if constraint_key:
            return (
                "Giới hạn chính gắn với cách đọc liên miền đã công bố — "
                "không ẩn mâu thuẫn khi có căng giữa các lớp."
            )
        return "Giới hạn được nêu khi có tín hiệu bất lợi hoặc căng liên miền."

    @staticmethod
    def _change_text(plan) -> str:
        if plan.priorities:
            return " · ".join(plan.priorities[:3])
        return "Giữ quyết định bám dữ liệu đã công bố — không mở rộng ngoài phạm vi."
