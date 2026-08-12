"""Executive Consulting composer — ExecutiveClaimPlan → Commercial Language Layer."""

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
)
from applications.production.language.service import CommercialLanguageService


class ExecutiveConsultingComposer:
    """Compose executive consulting from claim plan via CLL."""

    def __init__(self, language_service: CommercialLanguageService | None = None) -> None:
        self._language = language_service or CommercialLanguageService()

    def compose(
        self,
        context: IntegratedInterpretationContext,
        *,
        reasoning: CrossDomainReasoningResult | None = None,
    ) -> ExecutiveConsultingResult:
        """Build executive consulting from CDR + CLL when available."""
        if reasoning is not None and reasoning.claims:
            return self._compose_from_reasoning(reasoning, context)
        return self._compose_legacy(context)

    def _compose_from_reasoning(
        self,
        reasoning: CrossDomainReasoningResult,
        context: IntegratedInterpretationContext,
    ) -> ExecutiveConsultingResult:
        realized = self._language.compose_executive(reasoning)
        sections = [
            DomainSection(section_id=sid, title=title, paragraphs=paragraphs)
            for sid, title, paragraphs in realized.sections
        ]
        status = DomainStatus.AVAILABLE
        if context.missing_domains or reasoning.diagnostics.get("missing_domains"):
            status = DomainStatus.PARTIAL

        return ExecutiveConsultingResult(
            status=status,
            body=realized.body,
            sections=sections,
            recommendations=list(realized.recommendations)[:3],
            version="1.2.0",
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
                "executive_claim_plan": reasoning.executive_claim_plan.to_dict(),
                "why_primary": dict(reasoning.diagnostics.get("why_primary") or {}),
                "luck_timeline": "OMITTED_NO_GENERIC_LUCK_INTERPRETATION",
                "source": "commercial_language_v1_2",
                "cll": dict(realized.diagnostics),
                "memory_line": realized.memory_line,
            },
        )

    def _compose_legacy(
        self,
        context: IntegratedInterpretationContext,
    ) -> ExecutiveConsultingResult:
        """Minimal legacy path without CDR — domains only, still no claim keys."""
        domains = context.domain_results
        who = (
            domains["strength"].conclusion
            if domains.get("strength")
            else "Hệ vận hành của bạn có thể mô tả từ các tín hiệu đã công bố."
        )
        system = (
            domains["ten_gods"].conclusion
            if domains.get("ten_gods")
            else "Hệ nội tại được đọc qua cấu trúc vai trò đã công bố."
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
        priorities = list(context.recommendations[:3])
        while len(priorities) < 3:
            priorities.append(
                "Giữ quyết định bám dữ liệu đã công bố — không mở rộng ngoài phạm vi."
            )
        avoids = [
            "Đừng kết luận ngoài phạm vi dữ liệu đã có.",
            "Đừng ẩn mâu thuẫn liên miền khi chưa đủ chính sách.",
            "Đừng suy diễn timeline khi luận vận trình chưa sẵn sàng.",
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
            version="1.2.0",
            knowledge_status=KnowledgeStatus.PILOT,
            diagnostics={
                "missing_domains": list(context.missing_domains),
                "source": "legacy_domain_fallback",
                "luck_timeline": "OMITTED_NO_GENERIC_LUCK_INTERPRETATION",
            },
        )
