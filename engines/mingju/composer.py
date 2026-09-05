"""MC-01 structural composer. Not Pack 07 Narrative Composer."""

from __future__ import annotations

from engines.mingju.enums import AnalysisState, IntegrityState
from engines.mingju.models import MingJuComposedDecision, MingJuDecisionResult
from engines.mingju.versions import SCHEMA_COMPOSER

_HEADLINE = {
    IntegrityState.COMPLETE.value: ("mc01.headline.complete", "Mệnh Cục đứng vững và vận hành rõ."),
    IntegrityState.SUBSTANTIALLY_COMPLETE.value: (
        "mc01.headline.substantially_complete",
        "Mệnh Cục cơ bản vững, còn vài điểm cần giữ.",
    ),
    IntegrityState.CONDITIONALLY_COMPLETE.value: (
        "mc01.headline.conditionally_complete",
        "Mệnh Cục vận hành được khi đúng điều kiện then chốt.",
    ),
    IntegrityState.MIXED.value: ("mc01.headline.mixed", "Mệnh Cục có nhiều lực cùng hiện diện."),
    IntegrityState.DAMAGED_BUT_RESCUED.value: (
        "mc01.headline.damaged_but_rescued",
        "Mệnh Cục có tổn thương nhưng đã có lực cứu.",
    ),
    IntegrityState.DAMAGED.value: ("mc01.headline.damaged", "Mệnh Cục chịu tổn thương cấu trúc."),
    IntegrityState.FAILED.value: ("mc01.headline.failed", "Mệnh Cục không giữ được trọn vẹn."),
    IntegrityState.UNRESOLVED.value: ("mc01.headline.unresolved", "Chưa đủ cơ sở để kết luận Mệnh Cục."),
}

_PURITY_VI = {
    "very_pure": "rất thuần",
    "pure": "thuần",
    "moderately_pure": "thuần vừa",
    "mixed": "pha tạp",
    "heavily_mixed": "pha tạp mạnh",
    "structurally_impure": "không thuần cấu trúc",
    "unresolved": "chưa xác định",
}

_STRENGTH_VI = {
    "very_strong": "rất mạnh",
    "strong": "mạnh",
    "moderate": "vừa",
    "weak": "yếu",
    "very_weak": "rất yếu",
    "unresolved": "chưa xác định",
}

_INTEGRITY_VI = {
    "complete": "toàn vẹn",
    "substantially_complete": "gần toàn vẹn",
    "conditionally_complete": "toàn vẹn có điều kiện",
    "mixed": "hỗn hợp",
    "damaged_but_rescued": "tổn thương đã cứu",
    "damaged": "tổn thương",
    "failed": "không giữ được",
    "unresolved": "chưa xác định",
}


class MingJuComposerMode:
    """Composer presentation mode."""

    COMMERCIAL = "commercial"
    TECHNICAL = "technical"


def compose_mingju_decision(
    result: MingJuDecisionResult,
    *,
    locale: str = "vi",
    mode: str = MingJuComposerMode.COMMERCIAL,
    composer_version: str | None = None,
) -> MingJuComposedDecision:
    """Turn structural results into customer-facing keys and short copy."""
    _ = mode
    integrity_state = result.integrity.state
    headline_key, headline = _HEADLINE.get(
        integrity_state,
        ("mc01.headline.unresolved", "Chưa đủ cơ sở để kết luận Mệnh Cục."),
    )
    pattern_label = result.pattern.label or result.pattern.pattern_id or "chưa xác định"
    purity = _PURITY_VI.get(result.purity.classification, result.purity.classification)
    strength = _STRENGTH_VI.get(
        result.pattern_strength.classification, result.pattern_strength.classification
    )
    integrity = _INTEGRITY_VI.get(result.integrity.state, result.integrity.state)
    grade = result.grade.grade
    summary = (
        f"{pattern_label}: độ thuần {purity}, lực cách {strength}, "
        f"toàn vẹn {integrity}, hạng cấu trúc {grade}."
    )
    strengths: list[str] = []
    if result.purity.classification in {"very_pure", "pure"}:
        strengths.append("Cấu trúc chủ đạo rõ.")
    if result.pattern_strength.classification in {"strong", "very_strong"}:
        strengths.append("Lực cách đủ để vận hành.")
    if result.rescue.findings:
        strengths.append("Có lực cứu cấu trúc.")
    risks = [item.damage_type for item in result.damage.findings]
    conditions = list(result.achievement.conditions_for_expression)
    if result.integrity.state == IntegrityState.CONDITIONALLY_COMPLETE.value:
        conditions.append("Cần giữ đúng lực hỗ trợ then chốt.")
    if result.pattern.state != AnalysisState.RESOLVED.value:
        summary = "Chưa xác định được cách cục nên chưa kết luận Mệnh Cục."
    return MingJuComposedDecision(
        composer_version=composer_version or SCHEMA_COMPOSER,
        locale=locale,
        headline_key=headline_key,
        headline=headline,
        summary_key="mc01.summary.structural",
        summary=summary,
        strength_keys=tuple(f"mc01.strength.{index}" for index, _ in enumerate(strengths, start=1)),
        strengths=tuple(strengths),
        risk_keys=tuple(f"mc01.risk.{item}" for item in risks),
        risks=tuple(risks),
        condition_keys=tuple(f"mc01.condition.{index}" for index, _ in enumerate(conditions, start=1)),
        conditions=tuple(conditions),
    )
