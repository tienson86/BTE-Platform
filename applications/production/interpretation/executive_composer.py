"""Generic Executive Consulting composer from ExecutiveClaimPlan — no CASE-0001 stitch."""

from __future__ import annotations

from applications.production.interpretation.contracts import (
    DomainSection,
    DomainStatus,
    ExecutiveConsultingResult,
    IntegratedInterpretationContext,
    KnowledgeStatus,
)
from applications.production.interpretation.cross_domain.models import (
    CrossDomainReasoningResult,
    RelationType,
    ThemeStatus,
)


_AVOIDANCE_VI = {
    "avoid_reflex_extra_load": "Nhận thêm tải theo phản xạ khi hệ đã căng.",
    "avoid_forcing_ordinary_daymaster_frame": (
        "Ép khung Nhật chủ thường lên cấu trúc Tòng / đặc biệt."
    ),
    "avoid_suppressing_expression_channel": "Dập tắt kênh biểu đạt / đầu ra đã công bố.",
    "avoid_overexertion_cycles": "Ép chu kỳ làm việc quá sức khi nội lực trung hòa.",
    "avoid_claims_beyond_published_data": (
        "Đưa ra kết luận ngoài phạm vi dữ liệu đã công bố."
    ),
}

_PRIORITY_PREFIX_VI = {
    "align_operating_role": "Điều phối theo vai trò vận hành",
    "apply_balance": "Áp dụng hướng điều tiết",
    "keep_load_recovery_rhythm": "Giữ nhịp tải / phục hồi cân bằng",
    "convert_load_to_defined_output": "Chuyển tải thành đầu ra có định nghĩa rõ",
    "keep_structure_consistency": "Giữ nhất quán khung cấu trúc",
}


class ExecutiveConsultingComposer:
    """Compose executive consulting from cross-domain claim plan."""

    def compose(
        self,
        context: IntegratedInterpretationContext,
        *,
        reasoning: CrossDomainReasoningResult | None = None,
    ) -> ExecutiveConsultingResult:
        """Build 9-section executive consulting from CDR when available."""
        if reasoning is not None:
            return self._compose_from_reasoning(reasoning, context)

        # Legacy fallback — should not be used once service always passes CDR.
        return self._compose_legacy(context)

    def _compose_from_reasoning(
        self,
        reasoning: CrossDomainReasoningResult,
        context: IntegratedInterpretationContext,
    ) -> ExecutiveConsultingResult:
        plan = reasoning.executive_claim_plan
        primary = next(
            (t for t in reasoning.themes if t.status == ThemeStatus.PRIMARY),
            None,
        )
        who = plan.identity_core or (
            primary.label if primary else "Bạn mang một hệ vận hành có thể mô tả từ tín hiệu đã công bố."
        )
        system = plan.operating_style or "Hệ nội tại được đọc qua cấu trúc vai trò đã công bố."
        supports = plan.main_support or self._fallback_support(context)
        limits = self._limit_from_plan(reasoning, plan.main_constraint)
        direction = plan.balance_direction or (
            next(
                (
                    t.label
                    for t in reasoning.themes
                    if "structure" in t.theme_id.lower() or "FOLLOW" in t.theme_id
                ),
                "Hướng chiến lược bám khung cấu trúc đã xác định.",
            )
        )
        insight = plan.primary_insight or (
            primary.label if primary else "Insight then chốt chỉ được nêu khi đủ dữ liệu miền."
        )
        priorities = self._priorities_vi(plan.priorities)
        avoids = self._avoidances_vi(plan.avoidances)

        # Surface unresolved / nuance honestly — never hide.
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
                RelationType.UNRESOLVED,
            }
        ]
        if nuance:
            limits = f"{limits} {nuance[0]}".strip()

        final = (
            f"{insight} "
            "Báo cáo này tổng hợp các miền đã có dữ liệu; "
            "không tạo timeline cuộc đời khi luận vận trình đầy đủ chưa sẵn sàng."
        )

        sections = [
            DomainSection("WHO", "Bạn là ai", [who]),
            DomainSection("SYSTEM", "Hệ thống nội tại vận hành ra sao", [system]),
            DomainSection("SUPPORTS", "Điều gì hỗ trợ bạn", [supports]),
            DomainSection("LIMITS", "Điều gì giới hạn bạn", [limits]),
            DomainSection("DIRECTION", "Trọng tâm chiến lược hiện tại", [direction]),
            DomainSection("INSIGHT", "Một insight quan trọng nhất", [insight]),
            DomainSection(
                "PRIORITIES",
                "Ba ưu tiên",
                [f"{index}. {item}" for index, item in enumerate(priorities, start=1)],
            ),
            DomainSection(
                "AVOIDS",
                "Ba điều cần tránh",
                [f"{index}. {item}" for index, item in enumerate(avoids, start=1)],
            ),
            DomainSection("CONCLUSION", "Kết luận tư vấn", [final]),
        ]

        body = "\n\n".join(
            f"# {section.title}\n\n{chr(10).join(section.paragraphs)}"
            for section in sections
        )

        status = DomainStatus.AVAILABLE
        if context.missing_domains or reasoning.diagnostics.get("missing_domains"):
            status = DomainStatus.PARTIAL
        if not reasoning.claims and not context.domain_results:
            status = DomainStatus.NOT_AVAILABLE
            body = "EXECUTIVE_CONSULTING_NOT_AVAILABLE"

        return ExecutiveConsultingResult(
            status=status,
            body=body,
            sections=sections if status != DomainStatus.NOT_AVAILABLE else [],
            recommendations=priorities,
            version="1.1.0",
            knowledge_status=KnowledgeStatus.PILOT,
            diagnostics={
                "missing_domains": list(context.missing_domains),
                "primary_theme": reasoning.primary_theme,
                "themes": [t.theme_id for t in reasoning.themes],
                "suppressed_themes": list(
                    reasoning.diagnostics.get("suppressed_themes") or []
                ),
                "conflicts": list(reasoning.conflicts),
                "tensions": list(reasoning.tensions),
                "unresolved": list(reasoning.unresolved),
                "executive_claim_plan": plan.to_dict(),
                "why_primary": dict(reasoning.diagnostics.get("why_primary") or {}),
                "luck_timeline": "OMITTED_NO_GENERIC_LUCK_INTERPRETATION",
                "source": "cross_domain_reasoning_v1_1",
            },
        )

    def _compose_legacy(
        self,
        context: IntegratedInterpretationContext,
    ) -> ExecutiveConsultingResult:
        """Minimal legacy path without CDR — domains only."""
        domains = context.domain_results
        who = domains["strength"].conclusion if domains.get("strength") else (
            "Bạn mang một hệ vận hành có thể mô tả từ các tín hiệu đã công bố."
        )
        system = domains["ten_gods"].conclusion if domains.get("ten_gods") else (
            "Hệ nội tại được đọc qua cấu trúc vai trò đã công bố."
        )
        supports = (
            domains["useful_god"].conclusion
            if domains.get("useful_god")
            else "Các yếu tố hỗ trợ được nêu khi có dữ liệu miền tương ứng."
        )
        limits = "Giới hạn được nêu khi có tín hiệu bất lợi đã công bố."
        direction = (
            domains["pattern"].conclusion
            if domains.get("pattern")
            else "Hướng chiến lược bám khung cấu trúc đã xác định."
        )
        insight = who
        priorities = context.recommendations[:3]
        while len(priorities) < 3:
            priorities.append(
                "Giữ quyết định bám dữ liệu đã công bố — không mở rộng ngoài phạm vi."
            )
        avoids = [
            "Đưa ra kết luận ngoài phạm vi dữ liệu đã công bố.",
            "Ẩn mâu thuẫn liên miền khi chưa đủ chính sách.",
            "Suy diễn timeline khi luận vận trình chưa sẵn sàng.",
        ]
        final = (
            f"{insight} Báo cáo này tổng hợp các miền đã có dữ liệu; "
            "không tạo timeline cuộc đời khi luận vận trình đầy đủ chưa sẵn sàng."
        )
        sections = [
            DomainSection("WHO", "Bạn là ai", [who]),
            DomainSection("SYSTEM", "Hệ thống nội tại vận hành ra sao", [system]),
            DomainSection("SUPPORTS", "Điều gì hỗ trợ bạn", [supports]),
            DomainSection("LIMITS", "Điều gì giới hạn bạn", [limits]),
            DomainSection("DIRECTION", "Trọng tâm chiến lược hiện tại", [direction]),
            DomainSection("INSIGHT", "Một insight quan trọng nhất", [insight]),
            DomainSection(
                "PRIORITIES",
                "Ba ưu tiên",
                [f"{i}. {p}" for i, p in enumerate(priorities, start=1)],
            ),
            DomainSection(
                "AVOIDS",
                "Ba điều cần tránh",
                [f"{i}. {a}" for i, a in enumerate(avoids, start=1)],
            ),
            DomainSection("CONCLUSION", "Kết luận tư vấn", [final]),
        ]
        body = "\n\n".join(
            f"# {s.title}\n\n{chr(10).join(s.paragraphs)}" for s in sections
        )
        status = DomainStatus.AVAILABLE
        if context.missing_domains:
            status = DomainStatus.PARTIAL
        if not domains:
            status = DomainStatus.NOT_AVAILABLE
            body = "EXECUTIVE_CONSULTING_NOT_AVAILABLE"
        return ExecutiveConsultingResult(
            status=status,
            body=body,
            sections=sections if status != DomainStatus.NOT_AVAILABLE else [],
            recommendations=priorities,
            version="1.1.0",
            knowledge_status=KnowledgeStatus.PILOT,
            diagnostics={
                "missing_domains": list(context.missing_domains),
                "source": "legacy_domain_fallback",
                "luck_timeline": "OMITTED_NO_GENERIC_LUCK_INTERPRETATION",
            },
        )

    @staticmethod
    def _limit_from_plan(
        reasoning: CrossDomainReasoningResult,
        constraint_key: str,
    ) -> str:
        for relation in reasoning.relations:
            if relation.relation_id == constraint_key and relation.customer_safe_state:
                return relation.customer_safe_state
        if constraint_key == "OVERLOAD_RISK":
            return "Rủi ro ôm quá tải khi nội lực mạnh — cần chuyển tải thành đầu ra có chu kỳ."
        return "Giới hạn chính gắn với cách dùng lực và căng liên miền đã công bố."

    @staticmethod
    def _fallback_support(context: IntegratedInterpretationContext) -> str:
        ug = context.domain_results.get("useful_god")
        if ug and ug.conclusion:
            return ug.conclusion
        return "Các yếu tố hỗ trợ được nêu khi có dữ liệu miền tương ứng."

    @staticmethod
    def _priorities_vi(raw: list[str]) -> list[str]:
        out: list[str] = []
        for item in raw:
            if ":" in item:
                key, rest = item.split(":", 1)
                prefix = _PRIORITY_PREFIX_VI.get(key, key)
                out.append(f"{prefix}: {rest}")
            else:
                out.append(_PRIORITY_PREFIX_VI.get(item, item))
        while len(out) < 3:
            out.append(
                "Giữ quyết định bám dữ liệu đã công bố — không mở rộng ngoài phạm vi."
            )
        return out[:3]

    @staticmethod
    def _avoidances_vi(raw: list[str]) -> list[str]:
        out = [_AVOIDANCE_VI.get(item, item) for item in raw]
        while len(out) < 3:
            out.append(_AVOIDANCE_VI["avoid_claims_beyond_published_data"])
        return out[:3]
