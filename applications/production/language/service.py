"""Commercial Language Layer service — claim plans → consulting paragraphs."""

from __future__ import annotations

from applications.production.interpretation.cross_domain.models import (
    CrossDomainReasoningResult,
    ExecutiveClaimPlan,
    ThemeStatus,
)
from applications.production.language.models import (
    CommercialLanguageInput,
    FeatureKind,
    FeatureLanguageResult,
    ParagraphIntent,
)
from applications.production.language import plain_language as pl
from applications.production.language.writer import realize_paragraph

CLL_VERSION = "1.2.0"


class CommercialLanguageService:
    """Realize customer consulting language from claim plans only."""

    def realize(self, data: CommercialLanguageInput):
        """Realize one paragraph."""
        return realize_paragraph(data)

    def compose_identity(
        self,
        reasoning: CrossDomainReasoningResult,
    ) -> FeatureLanguageResult:
        """Identity Report sections via CLL."""
        plan = reasoning.executive_claim_plan
        theme, capacity, structure = self._plan_cues(reasoning, plan)
        limitations = self._limitation_keys(reasoning, plan)
        style = plan.operating_style

        who = self._para(
            FeatureKind.IDENTITY,
            "WHO",
            ParagraphIntent.OBSERVATION,
            reasoning,
            claims=["identity_core"],
            primary_theme=theme,
            operating_style=style,
            capacity_cue=capacity,
            structure_cue=structure,
        )
        operating = self._para(
            FeatureKind.IDENTITY,
            "OPERATING",
            ParagraphIntent.WORK_STYLE,
            reasoning,
            claims=["operating_style"],
            primary_theme=theme,
            operating_style=style,
            structure_cue=structure,
            capacity_cue=capacity,
        )
        strengths = self._para(
            FeatureKind.IDENTITY,
            "STRENGTHS",
            ParagraphIntent.SUPPORT,
            reasoning,
            claims=["main_support"],
            capacity_cue=capacity,
            operating_style=style,
            structure_cue=structure,
            balance_cue=plan.main_support or plan.balance_direction,
            primary_theme=theme,
        )
        blind = self._para(
            FeatureKind.IDENTITY,
            "BLIND_SPOTS",
            ParagraphIntent.LIMITATION,
            reasoning,
            claims=["main_constraint"],
            limitations=limitations,
            primary_theme=theme,
            structure_cue=structure,
            operating_style=style,
        )
        pressure = self._para(
            FeatureKind.IDENTITY,
            "PRESSURE",
            ParagraphIntent.PRESSURE_RESPONSE,
            reasoning,
            claims=["pressure"],
            primary_theme=theme,
        )
        environment = self._para(
            FeatureKind.IDENTITY,
            "ENVIRONMENT",
            ParagraphIntent.ENVIRONMENT,
            reasoning,
            claims=["environment"],
            primary_theme=theme,
            operating_style=style,
            structure_cue=structure,
            capacity_cue=capacity,
        )
        lesson = self._para(
            FeatureKind.IDENTITY,
            "LESSON",
            ParagraphIntent.INSIGHT,
            reasoning,
            claims=["primary_insight"],
            primary_theme=theme,
            operating_style=style,
            structure_cue=structure,
        )
        actions = self._action_block(
            FeatureKind.IDENTITY,
            plan.priorities[:3],
            section="ACTIONS",
            reasoning=reasoning,
        )
        memory = self._memory_line(theme, style, capacity, structure)
        summary = self._para(
            FeatureKind.IDENTITY,
            "SUMMARY",
            ParagraphIntent.CLOSING,
            reasoning,
            claims=["summary"],
            primary_theme=theme,
            operating_style=style,
            memory_candidate=memory,
        )

        section_defs = [
            ("WHO", "Tôi là ai?", [who.prose]),
            ("OPERATING", "Mẫu vận hành tự nhiên", [operating.prose]),
            ("STRENGTHS", "Điểm làm tôi mạnh hơn", [strengths.prose]),
            ("BLIND_SPOTS", "Điểm mù / biên giới", [blind.prose]),
            ("PRESSURE", "Phản ứng khi bị áp lực", [pressure.prose]),
            ("ENVIRONMENT", "Môi trường hợp tôi", [environment.prose]),
            ("LESSON", "Bài học nhận diện", [lesson.prose]),
            ("ACTIONS", "Việc nên điều chỉnh", actions),
            ("SUMMARY", "Tóm tắt danh tính", [summary.prose]),
        ]
        if limitations:
            cond = self._para(
                FeatureKind.IDENTITY,
                "CONDITION",
                ParagraphIntent.CONDITION,
                reasoning,
                claims=["nuance"],
                limitations=limitations,
            )
            section_defs.insert(
                7,
                ("CONDITION", "Đọc có điều kiện", [cond.prose]),
            )

        body = self._join_sections(section_defs)
        recs = [pl.plain_priority(p) for p in plan.priorities[:3]]
        recs = [r for r in recs if r]
        return FeatureLanguageResult(
            sections=section_defs,
            body=body,
            recommendations=recs,
            memory_line=memory,
            diagnostics=self._diagnostics(body, theme, "identity"),
        )

    def compose_career(
        self,
        reasoning: CrossDomainReasoningResult,
    ) -> FeatureLanguageResult:
        """Career Report sections via CLL."""
        plan = reasoning.executive_claim_plan
        theme, capacity, structure = self._plan_cues(reasoning, plan)
        limitations = self._limitation_keys(reasoning, plan)
        style = plan.operating_style

        work = self._para(
            FeatureKind.CAREER,
            "WORK_STYLE",
            ParagraphIntent.WORK_STYLE,
            reasoning,
            claims=["operating_style"],
            primary_theme=theme,
            operating_style=style,
            structure_cue=structure,
            capacity_cue=capacity,
        )
        # Authority / role posture — prefer primary output/self-carry over secondary standards.
        posture = self._role_posture(theme, style)
        environment = self._para(
            FeatureKind.CAREER,
            "ENVIRONMENT",
            ParagraphIntent.ENVIRONMENT,
            reasoning,
            claims=["environment"],
            primary_theme=theme,
            operating_style=style,
            structure_cue=structure,
            capacity_cue=capacity,
        )
        risk = self._para(
            FeatureKind.CAREER,
            "RISK",
            ParagraphIntent.LIMITATION,
            reasoning,
            claims=["main_constraint"],
            primary_theme=theme,
            operating_style=style,
            capacity_cue=capacity,
            structure_cue=structure,
            limitations=limitations or (["OVERLOAD_RISK"] if theme == "OPERATING_SELF_CARRY" else []),
        )
        focus = self._action_block(
            FeatureKind.CAREER,
            plan.priorities[:3],
            section="FOCUS",
            reasoning=reasoning,
        )
        avoids = self._avoid_block(
            FeatureKind.CAREER,
            plan.avoidances[:3],
            section="AVOIDS",
            reasoning=reasoning,
        )
        balance = self._para(
            FeatureKind.CAREER,
            "BALANCE",
            ParagraphIntent.SUPPORT,
            reasoning,
            claims=["balance_direction"],
            balance_cue=plan.balance_direction or plan.main_support,
            capacity_cue=capacity,
            operating_style=style,
            primary_theme=theme,
        )
        pressure = self._para(
            FeatureKind.CAREER,
            "PRESSURE",
            ParagraphIntent.PRESSURE_RESPONSE,
            reasoning,
            claims=["pressure"],
            primary_theme=theme,
        )
        memory = self._memory_line(theme, style, capacity, structure, career=True)
        closing = self._para(
            FeatureKind.CAREER,
            "SUMMARY",
            ParagraphIntent.CLOSING,
            reasoning,
            claims=["summary"],
            primary_theme=theme,
            operating_style=style,
            memory_candidate=memory,
        )

        section_defs = [
            ("WORK_STYLE", "Bạn làm việc tốt nhất như thế nào", [work.prose]),
            ("ENVIRONMENT", "Môi trường nghề nghiệp hợp bạn", [environment.prose]),
            ("POSTURE", "Tư thế vai trò phù hợp", [posture]),
            ("PRESSURE", "Phản ứng với áp lực công việc", [pressure.prose]),
            ("BALANCE", "Hướng cân bằng trong công việc", [balance.prose]),
            ("RISK", "Rủi ro nghề nghiệp chính", [risk.prose]),
            ("FOCUS", "Trọng tâm nên giữ", focus),
            ("AVOIDS", "Điều nên tránh", avoids),
            ("SUMMARY", "Tóm tắt hướng sự nghiệp", [closing.prose]),
        ]
        if limitations:
            cond = self._para(
                FeatureKind.CAREER,
                "CONDITION",
                ParagraphIntent.CONDITION,
                reasoning,
                claims=["nuance"],
                limitations=limitations,
            )
            section_defs.insert(
                5,
                ("CONDITION", "Đọc có điều kiện", [cond.prose]),
            )

        body = self._join_sections(section_defs)
        recs = [pl.plain_priority(p) for p in plan.priorities[:3]]
        recs = [r for r in recs if r]
        return FeatureLanguageResult(
            sections=section_defs,
            body=body,
            recommendations=recs,
            memory_line=memory,
            diagnostics=self._diagnostics(body, theme, "career"),
        )

    def compose_executive(
        self,
        reasoning: CrossDomainReasoningResult,
    ) -> FeatureLanguageResult:
        """Executive Consulting via CLL — one consultant voice."""
        plan = reasoning.executive_claim_plan
        theme, capacity, structure = self._plan_cues(reasoning, plan)
        limitations = self._limitation_keys(reasoning, plan)
        style = plan.operating_style

        who = self._para(
            FeatureKind.EXECUTIVE,
            "WHO",
            ParagraphIntent.RECOGNITION,
            reasoning,
            claims=["identity_core"],
            primary_theme=theme,
            operating_style=style,
            capacity_cue=capacity,
            structure_cue=structure,
        )
        system = self._para(
            FeatureKind.EXECUTIVE,
            "SYSTEM",
            ParagraphIntent.WORK_STYLE,
            reasoning,
            claims=["operating_style"],
            primary_theme=theme,
            operating_style=style,
            structure_cue=structure,
            capacity_cue=capacity,
        )
        supports = self._para(
            FeatureKind.EXECUTIVE,
            "SUPPORTS",
            ParagraphIntent.SUPPORT,
            reasoning,
            claims=["main_support"],
            balance_cue=plan.main_support or plan.balance_direction,
            capacity_cue=capacity,
            operating_style=style,
            primary_theme=theme,
            structure_cue=structure,
        )
        limits = self._para(
            FeatureKind.EXECUTIVE,
            "LIMITS",
            ParagraphIntent.LIMITATION,
            reasoning,
            claims=["main_constraint"],
            limitations=limitations,
            primary_theme=theme,
            structure_cue=structure,
            operating_style=style,
        )
        direction = self._para(
            FeatureKind.EXECUTIVE,
            "DIRECTION",
            ParagraphIntent.SUPPORT,
            reasoning,
            claims=["balance_direction"],
            balance_cue=plan.balance_direction,
            structure_cue=structure,
            primary_theme=theme,
            operating_style=style,
        )
        insight = self._para(
            FeatureKind.EXECUTIVE,
            "INSIGHT",
            ParagraphIntent.INSIGHT,
            reasoning,
            claims=["primary_insight"],
            primary_theme=theme,
            operating_style=style,
            structure_cue=structure,
        )
        priorities = self._action_block(
            FeatureKind.EXECUTIVE,
            plan.priorities[:3],
            section="PRIORITIES",
            reasoning=reasoning,
            numbered=True,
        )
        avoids = self._avoid_block(
            FeatureKind.EXECUTIVE,
            plan.avoidances[:3],
            section="AVOIDS",
            reasoning=reasoning,
            numbered=True,
        )
        memory = self._memory_line(theme, style, capacity, structure)
        final = self._para(
            FeatureKind.EXECUTIVE,
            "CONCLUSION",
            ParagraphIntent.CLOSING,
            reasoning,
            claims=["conclusion"],
            primary_theme=theme,
            operating_style=style,
            memory_candidate=(
                f"{memory} Báo cáo này tổng hợp các miền đã có dữ liệu; "
                "không tạo timeline cuộc đời khi luận vận trình đầy đủ chưa sẵn sàng."
            ),
        )

        section_defs = [
            ("WHO", "Bạn là ai", [who.prose]),
            ("SYSTEM", "Hệ thống nội tại vận hành ra sao", [system.prose]),
            ("SUPPORTS", "Điều gì hỗ trợ bạn", [supports.prose]),
            ("LIMITS", "Điều gì giới hạn bạn", [limits.prose]),
            ("DIRECTION", "Trọng tâm chiến lược hiện tại", [direction.prose]),
            ("INSIGHT", "Một insight quan trọng nhất", [insight.prose]),
            ("PRIORITIES", "Ba ưu tiên", priorities),
            ("AVOIDS", "Ba điều cần tránh", avoids),
            ("CONCLUSION", "Kết luận tư vấn", [final.prose]),
        ]
        body = self._join_sections(section_defs)
        recs = [pl.plain_priority(p) for p in plan.priorities[:3]]
        recs = [r for r in recs if r]
        return FeatureLanguageResult(
            sections=section_defs,
            body=body,
            recommendations=recs,
            memory_line=memory,
            diagnostics=self._diagnostics(body, theme, "executive"),
        )

    def _para(
        self,
        feature: FeatureKind,
        section: str,
        intent: ParagraphIntent,
        reasoning: CrossDomainReasoningResult,
        *,
        claims: list[str],
        limitations: list[str] | None = None,
        primary_theme: str = "",
        operating_style: str = "",
        capacity_cue: str = "",
        structure_cue: str = "",
        balance_cue: str = "",
        memory_candidate: str = "",
        actionability: str = "",
    ):
        return realize_paragraph(
            CommercialLanguageInput(
                feature=feature,
                section=section,
                intent=intent,
                claims=claims,
                limitations=list(limitations or []),
                question_context=reasoning.question_context.value,
                primary_theme=primary_theme,
                operating_style=operating_style,
                capacity_cue=capacity_cue,
                structure_cue=structure_cue,
                balance_cue=balance_cue,
                memory_candidate=memory_candidate,
                actionability=actionability,
                versions={"cll": CLL_VERSION},
            )
        )

    def _action_block(
        self,
        feature: FeatureKind,
        items: list[str],
        *,
        section: str,
        reasoning: CrossDomainReasoningResult,
        numbered: bool = False,
    ) -> list[str]:
        lines: list[str] = []
        for index, item in enumerate(items, start=1):
            paragraph = self._para(
                feature,
                section,
                ParagraphIntent.ACTION,
                reasoning,
                claims=[item],
                actionability=item,
            )
            text = paragraph.action or paragraph.prose
            if numbered:
                lines.append(f"{index}. {text}")
            else:
                lines.append(text)
        if not lines:
            lines.append("Giữ quyết định bám dữ liệu đã công bố — không mở rộng ngoài phạm vi.")
        return lines

    def _avoid_block(
        self,
        feature: FeatureKind,
        items: list[str],
        *,
        section: str,
        reasoning: CrossDomainReasoningResult,
        numbered: bool = False,
    ) -> list[str]:
        lines: list[str] = []
        for index, item in enumerate(items, start=1):
            text = pl.plain_avoid(item)
            if not text:
                continue
            if numbered:
                lines.append(f"{index}. {text}")
            else:
                lines.append(text)
        while len(lines) < 1:
            lines.append("Đừng kết luận ngoài phạm vi dữ liệu đã có.")
        return lines[:3]

    @staticmethod
    def _role_posture(theme: str, style: str) -> str:
        """Career authority/posture in lived work language — not generic chuẩn mực."""
        style_plain = pl.plain_style(style)
        if theme == "OPERATING_OUTPUT" or "Thương Quan" in (style or "") or "Thực Thần" in (style or ""):
            return (
                "Tư thế vai trò hợp bạn hơn khi được giao phạm vi tạo ra kết quả / biểu đạt rõ, "
                f"với quyền quyết định trên chất lượng đầu ra"
                + (f" — gắn với {style_plain}." if style_plain else ".")
                + " Đây là tư thế sản xuất và thể hiện, không phải tư thế chỉ giữ quy trình hình thức."
            )
        if theme == "OPERATING_SELF_CARRY":
            return (
                "Tư thế vai trò hợp bạn hơn khi được tự chủ triển khai trong biên tải rõ — "
                "có quyền từ chối việc tràn về theo phản xạ."
            )
        if theme == "OPERATING_STANDARDS":
            return (
                "Tư thế vai trò hợp bạn hơn khi phạm vi trách nhiệm và kỳ vọng được viết rõ — "
                "bạn làm tốt khi biết ‘đúng chuẩn’ nghĩa là gì trong tuần."
            )
        if theme == "FOLLOW_STRUCTURE":
            return (
                "Tư thế vai trò hợp bạn hơn khi tổ chức tôn trọng khung dài hạn riêng của bạn, "
                "không ép checklist khuôn thường trái nhịp."
            )
        return (
            "Tư thế vai trò được nêu theo kênh vận hành đã công bố — "
            "không suy diễn chức danh hay cấp bậc."
        )

    @staticmethod
    def _plan_cues(
        reasoning: CrossDomainReasoningResult,
        plan: ExecutiveClaimPlan,
    ) -> tuple[str, str, str]:
        theme = reasoning.primary_theme
        theme_hint, capacity, structure = pl.parse_identity_core(plan.identity_core)
        if not theme and theme_hint:
            # Best-effort from label text — do not invent doctrine.
            for key, label in (
                ("OPERATING_OUTPUT", "đầu ra"),
                ("OPERATING_SELF_CARRY", "tự gánh"),
                ("FOLLOW_STRUCTURE", "Tòng"),
            ):
                if label.lower() in theme_hint.lower():
                    theme = key
                    break
        if not capacity:
            for claim in reasoning.claims:
                if claim.claim_id == "str_body_level":
                    capacity = claim.value
                    break
        if not structure:
            for claim in reasoning.claims:
                if claim.claim_id == "pat_structure":
                    structure = claim.value
                    break
        # Prefer PRIMARY theme id over hint.
        primary = next(
            (t for t in reasoning.themes if t.status == ThemeStatus.PRIMARY),
            None,
        )
        if primary:
            theme = primary.theme_id
        return theme, capacity, structure

    @staticmethod
    def _limitation_keys(
        reasoning: CrossDomainReasoningResult,
        plan: ExecutiveClaimPlan,
    ) -> list[str]:
        keys: list[str] = []
        if plan.main_constraint:
            keys.append(plan.main_constraint)
        for relation in reasoning.relations:
            if relation.relation_id in {
                "follow_qualifies_strength",
                "str_pattern_scope",
                "follow_strength_nuance",
                "tg_vs_pattern_scope",
            }:
                if relation.relation_id not in keys:
                    keys.append(relation.relation_id)
        return keys[:4]

    @staticmethod
    def _memory_line(
        theme: str,
        style: str,
        capacity: str,
        structure: str,
        *,
        career: bool = False,
    ) -> str:
        style_plain = pl.plain_style(style)
        theme_plain = pl.plain_theme(theme)
        follow = "tòng" in (structure or "").lower() or "tong" in (structure or "").lower()
        if career:
            if theme == "OPERATING_OUTPUT" and follow:
                return (
                    "Công việc hợp bạn khi được trả bằng kết quả nhìn thấy được, "
                    "trong nhịp tải–nghỉ rõ — không khi cố giống khuôn làm việc chung."
                )
            if theme == "OPERATING_OUTPUT" and style_plain:
                return f"Công việc hợp bạn khi {style_plain} được đặt đúng chỗ."
            if theme == "OPERATING_SELF_CARRY":
                return "Công việc hợp bạn khi tự chủ có biên tải — không phải ôm hết theo phản xạ."
            if theme_plain:
                return f"Công việc hợp bạn khi bạn được {theme_plain}."
        if theme == "OPERATING_OUTPUT" and follow:
            return (
                "Bạn rõ và bền hơn khi tạo ra đầu ra trong đúng khung riêng — "
                "không khi ép mình vào khuôn chung hay ôm thêm cho đủ."
            )
        if theme == "OPERATING_SELF_CARRY":
            return "Bạn mạnh ở chỗ tự gánh — và bền hơn khi biết dừng nhận thêm."
        if style_plain and theme_plain:
            return f"Bạn mạnh hơn khi đi đúng {style_plain}."
        if theme_plain:
            return f"Nhớ điều này: bạn {theme_plain}."
        if style_plain:
            return f"Bạn rõ hơn khi đi đúng {style_plain}."
        return "Giữ quyết định bám những gì đã được công bố về bạn."

    @staticmethod
    def _join_sections(section_defs: list[tuple[str, str, list[str]]]) -> str:
        parts: list[str] = []
        for _, title, paragraphs in section_defs:
            body = "\n\n".join(paragraphs)
            parts.append(f"# {title}\n\n{body}")
        return "\n\n".join(parts)

    @staticmethod
    def _diagnostics(body: str, theme: str, feature: str) -> dict:
        leaks = pl.contains_forbidden_leak(body)
        return {
            "cll_version": CLL_VERSION,
            "feature": feature,
            "primary_theme": theme,
            "forbidden_leaks": leaks,
            "leak_free": len(leaks) == 0,
        }
