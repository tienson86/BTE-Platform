"""Generic Executive Consulting composer — never loads CASE-0001 Part 08."""

from __future__ import annotations

from applications.production.interpretation.contracts import (
    DomainSection,
    DomainStatus,
    ExecutiveConsultingResult,
    IntegratedInterpretationContext,
    KnowledgeStatus,
)
from applications.production.interpretation.theme_keys import (
    THEME_BALANCE_STRATEGY,
    THEME_ENDURANCE,
    THEME_LONG_STRUCTURE,
    THEME_NO_EXTRA_LOAD,
    THEME_OPERATING_SYSTEM,
    THEME_OUTPUT_RELEASE,
    THEME_PRESSURE,
    THEME_RESOURCE_SUPPORT,
)


class ExecutiveConsultingComposer:
    """Compose executive consulting from integrated domain context."""

    def compose(
        self,
        context: IntegratedInterpretationContext,
    ) -> ExecutiveConsultingResult:
        """Build 9-section executive consulting without Luck timeline claims."""
        domains = context.domain_results
        by_theme = {claim.theme_id: claim.text for claim in context.claims}

        who = self._claim_or(
            by_theme,
            THEME_ENDURANCE,
            domains.get("strength").conclusion if domains.get("strength") else "",
            "Bạn mang một hệ vận hành có thể mô tả từ các tín hiệu đã công bố.",
        )
        system = self._claim_or(
            by_theme,
            THEME_OPERATING_SYSTEM,
            domains.get("ten_gods").conclusion if domains.get("ten_gods") else "",
            "Hệ nội tại được đọc qua cấu trúc vai trò đã công bố.",
        )
        supports = self._supports(by_theme, domains)
        limits = self._limits(by_theme, domains)
        direction = self._claim_or(
            by_theme,
            THEME_LONG_STRUCTURE,
            domains.get("pattern").conclusion if domains.get("pattern") else "",
            "Hướng chiến lược bám khung cấu trúc đã xác định.",
        )
        insight = self._insight(by_theme, domains)
        priorities = context.recommendations[:3]
        while len(priorities) < 3:
            priorities.append("Giữ quyết định bám dữ liệu đã công bố — không mở rộng ngoài phạm vi.")
        avoids = self._avoids(by_theme, domains)
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

        body_parts = [f"# {section.title}\n\n{chr(10).join(section.paragraphs)}" for section in sections]
        body = "\n\n".join(body_parts)

        status = DomainStatus.AVAILABLE
        if context.missing_domains:
            status = DomainStatus.PARTIAL
        if len(domains) == 0:
            status = DomainStatus.NOT_AVAILABLE
            body = "EXECUTIVE_CONSULTING_NOT_AVAILABLE"

        return ExecutiveConsultingResult(
            status=status,
            body=body,
            sections=sections if status != DomainStatus.NOT_AVAILABLE else [],
            recommendations=priorities,
            version="1.0.0",
            knowledge_status=KnowledgeStatus.PILOT,
            diagnostics={
                "missing_domains": list(context.missing_domains),
                "themes": list(context.themes),
                "conflicts": [item.to_dict() for item in context.conflicts],
                "suppressed_duplicates": list(context.suppressed_duplicates),
                "luck_timeline": "OMITTED_NO_GENERIC_LUCK_INTERPRETATION",
            },
        )

    @staticmethod
    def _claim_or(by_theme: dict[str, str], theme: str, fallback: str, default: str) -> str:
        return by_theme.get(theme) or fallback or default

    @staticmethod
    def _supports(by_theme: dict[str, str], domains: dict) -> str:
        parts: list[str] = []
        if THEME_RESOURCE_SUPPORT in by_theme:
            parts.append(by_theme[THEME_RESOURCE_SUPPORT])
        if THEME_ENDURANCE in by_theme:
            parts.append("Nền nội lực đã xác định là một lớp hỗ trợ.")
        if THEME_BALANCE_STRATEGY in by_theme:
            parts.append(by_theme[THEME_BALANCE_STRATEGY])
        if not parts and domains.get("useful_god"):
            parts.append(domains["useful_god"].conclusion)
        return " ".join(parts) if parts else "Các yếu tố hỗ trợ được nêu khi có dữ liệu miền tương ứng."

    @staticmethod
    def _limits(by_theme: dict[str, str], domains: dict) -> str:
        parts: list[str] = []
        if THEME_PRESSURE in by_theme:
            parts.append(by_theme[THEME_PRESSURE])
        if THEME_NO_EXTRA_LOAD in by_theme:
            parts.append(by_theme[THEME_NO_EXTRA_LOAD])
        if THEME_OUTPUT_RELEASE in by_theme:
            parts.append(by_theme[THEME_OUTPUT_RELEASE])
        if not parts and domains.get("strength"):
            parts.append("Giới hạn chính gắn với cách dùng lực — không phải thiếu năng lực tuyệt đối.")
        return " ".join(parts) if parts else "Giới hạn được nêu khi có tín hiệu bất lợi đã công bố."

    @staticmethod
    def _insight(by_theme: dict[str, str], domains: dict) -> str:
        if THEME_OUTPUT_RELEASE in by_theme and THEME_ENDURANCE in by_theme:
            return (
                "Điểm then chốt: sức bền thật sự nằm ở khả năng chuyển tải thành đầu ra có chu kỳ — "
                "không phải gánh thêm vô hạn."
            )
        if THEME_BALANCE_STRATEGY in by_theme:
            return by_theme[THEME_BALANCE_STRATEGY]
        if domains.get("strength"):
            return domains["strength"].conclusion
        return "Insight then chốt chỉ được nêu khi đủ dữ liệu miền."

    @staticmethod
    def _avoids(by_theme: dict[str, str], domains: dict) -> list[str]:
        avoids: list[str] = []
        if THEME_NO_EXTRA_LOAD in by_theme:
            avoids.append("Nhận thêm tải theo phản xạ khi hệ đã căng.")
        if THEME_PRESSURE in by_theme:
            avoids.append("Im lặng tự gánh khi áp lực chuẩn tăng cao.")
        if THEME_LONG_STRUCTURE in by_theme:
            avoids.append("Đổi khung dài hạn liên tục vì áp lực ngắn hạn.")
        while len(avoids) < 3:
            avoids.append("Đưa ra kết luận ngoài phạm vi dữ liệu đã công bố.")
        return avoids[:3]
