"""Commercial presentation helpers for Result polish (P0 orchestration).

Does not change analytical meaning. Applies customer-facing framing only.
"""

from __future__ import annotations

import re
from typing import Any

from .models import CareerSelectionAssessment, PromotionReadinessAssessment

_TECHNICAL_REPLACEMENTS: tuple[tuple[str, str], ...] = (
    (r"\bThan nhược\b", "Thân nhược"),
    (r"\bThan vượng\b", "Thân vượng"),
    (r"\bDụng thần\b", "trục hỗ trợ"),
    (r"\bdụng thần\b", "trục hỗ trợ"),
    (r"\bNhật chủ\b", "nền tảng ngày"),
    (r"\bnhật chủ\b", "nền tảng ngày"),
    (r"\bCách cục\b", "cấu trúc nghề"),
    (r"\bcách cục\b", "cấu trúc nghề"),
    (r"\bmức thân\b", "mức lực"),
    (r"\bphần kỵ\b", "phần lệch hướng"),
    (r"\bnuôi phần kỵ\b", "nuôi phần lệch hướng"),
    (r"\bthân được nâng đỡ\b", "đang có nền lực"),
    (r"\bthân đang mỏng lực\b", "đang cần giữ mực"),
    (r"\bNếu thân\b", "Nếu mức lực"),
    (r"\bnếu thân\b", "nếu mức lực"),
    (r"\bkhi thân\b", "khi mức lực"),
    (
        r"Chưa có Hỷ thần bổ trợ riêng",
        "Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng",
    ),
)


def commercialize_customer_text(
    text: str,
    signals: dict[str, Any] | None = None,
) -> str:
    """
    Replace technical BaZi wording with commercial customer language.

    Analytical codes in Analysis remain untouched; this is presentation-only.
    """
    result = (text or "").strip()
    if not result:
        return ""
    for pattern, replacement in _TECHNICAL_REPLACEMENTS:
        result = re.sub(pattern, replacement, result)
    result = _align_strength_band_language(result, signals)
    # Collapse accidental double phrases from overlapping replacements.
    result = re.sub(r"\s{2,}", " ", result).strip()
    return result


def _align_strength_band_language(
    text: str,
    signals: dict[str, Any] | None,
) -> str:
    """Do not call a strong/balanced chart 'mỏng lực' from leftover KU copy."""
    if not signals or not text:
        return text
    if str(signals.get("weakness_frame") or "") == "thin":
        return text
    band = str(signals.get("strength_band_label") or "").strip()
    if not band or "mỏng lực" in band:
        return text
    result = text.replace("mức lực đang mỏng lực", f"mức lực {band}")
    result = result.replace("nếu đang mỏng lực", "khi cần giữ mực")
    result = result.replace("đang mỏng lực", band)
    return result


def build_executive_composition(
    career: CareerSelectionAssessment | None,
    promotion: PromotionReadinessAssessment | None = None,
) -> dict[str, Any]:
    """
    Compose Executive Summary: 1 central + ≤3 supporting + 1 conclusion.

    Promotion is intentionally excluded from Exec (secondary milestone only).
    """
    _ = promotion  # reserved — must not densify Exec
    central = ""
    supporting: list[str] = []
    conclusion = ""

    if career and career.career_direction:
        central = _short(
            commercialize_customer_text(career.career_direction.text),
            max_chars=220,
        )
    if career and career.working_environment:
        supporting.append(
            _short(
                commercialize_customer_text(career.working_environment.text),
                max_chars=140,
            )
        )
    if career and career.career_strengths:
        supporting.append(
            _short(
                commercialize_customer_text(career.career_strengths.text),
                max_chars=140,
            )
        )
    if career and career.career_risks:
        risk = commercialize_customer_text(career.career_risks.text)
        if career.career_mitigation:
            risk = (
                f"{_short(risk, 90)} "
                f"{_short(commercialize_customer_text(career.career_mitigation.text), 90)}"
            )
        supporting.append(_short(risk, max_chars=160))
    supporting = [item for item in supporting if item][:3]

    if career and career.development_focus:
        conclusion = _short(
            commercialize_customer_text(career.development_focus.text),
            max_chars=160,
        )
    elif career and career.timing_guidance:
        conclusion = _short(
            commercialize_customer_text(career.timing_guidance.text),
            max_chars=160,
        )
    elif career and career.action_plan_90d:
        conclusion = (
            "Kết luận: giữ hướng nghề đã chọn và thực hiện kế hoạch 90 ngày "
            "trước khi mở bước lớn."
        )

    composed = _compose_executive_text(central, supporting, conclusion)
    return {
        "central_message": central,
        "supporting_points": supporting,
        "conclusion": conclusion,
        "composed_text": composed,
        "capability_labels": _capability_labels(career, promotion),
    }


def format_primary_recommendation(
    *,
    career: CareerSelectionAssessment | None,
    wave_recommendation: str = "",
) -> dict[str, str]:
    """
    Format primary Career Strategy recommendation as What/Why/How/When/Outcome.

    Returns an empty dict when Career Selection is absent (Wave 1.1-only path).
    """
    if not career or not career.knowledge_unit_ids:
        return {}

    plan = ""
    direction = ""
    why_extra = ""
    if career.action_plan_90d:
        plan = commercialize_customer_text(career.action_plan_90d.text)
    elif wave_recommendation:
        plan = commercialize_customer_text(wave_recommendation)
    if career.career_direction:
        direction = commercialize_customer_text(career.career_direction.text)
    if career.career_mitigation:
        why_extra = commercialize_customer_text(career.career_mitigation.text)

    what = _short(direction or "Chọn và giữ một hướng nghề phù hợp cấu trúc của bạn.", 160)
    why = _short(
        why_extra
        or "Vì hướng này giúp bạn giữ mực và tạo kết quả lặp lại thay vì lan man.",
        160,
    )
    how = _short(
        plan
        or "Giữ mực trước, chọn một việc nhỏ đúng hướng, rồi mở rộng có kiểm soát.",
        220,
    )
    when = "Trong 90 ngày tới (Tháng 1 giữ mực · Tháng 2 sâu hơn · Tháng 3 rà soát)."
    expected = (
        "Kỳ vọng tư vấn: rõ hướng nghề, giảm việc lệch hướng, và có kế hoạch "
        "hành động có thể theo dõi — không cam kết chức danh hay thu nhập."
    )
    composed = (
        f"What: {what}\n"
        f"Why: {why}\n"
        f"How: {how}\n"
        f"When: {when}\n"
        f"Expected outcome: {expected}"
    )
    return {
        "what": what,
        "why": why,
        "how": how,
        "when": when,
        "expected_outcome": expected,
        "composed_text": composed,
        "capability_label": "Career Selection Assessment",
        "role": "primary_career_strategy",
    }


def format_secondary_promotion_milestone(
    promotion: PromotionReadinessAssessment | None,
) -> dict[str, str] | None:
    """Format Promotion Readiness as a secondary career milestone (not primary Rec)."""
    if not promotion or not promotion.knowledge_unit_ids:
        return None
    readiness = ""
    plan = ""
    if promotion.promotion_readiness:
        readiness = commercialize_customer_text(promotion.promotion_readiness.text)
    if promotion.action_plan_90d:
        plan = commercialize_customer_text(promotion.action_plan_90d.text)
    if promotion.advancement_posture and not readiness:
        readiness = commercialize_customer_text(promotion.advancement_posture.text)
    summary = _short(readiness or plan, 180)
    if not summary:
        return None
    composed = (
        "Promotion Readiness Assessment (mốc nghề phụ): "
        f"{summary}"
    )
    if plan and plan not in composed:
        composed = f"{composed} Mốc 90 ngày: {_short(plan, 160)}"
    return {
        "capability_label": "Promotion Readiness Assessment",
        "role": "secondary_career_milestone",
        "summary": summary,
        "composed_text": composed,
    }


def _capability_labels(
    career: CareerSelectionAssessment | None,
    promotion: PromotionReadinessAssessment | None,
) -> list[str]:
    labels: list[str] = []
    if career and career.knowledge_unit_ids:
        labels.append("Career Selection Assessment")
    if promotion and promotion.knowledge_unit_ids:
        labels.append("Promotion Readiness Assessment")
    return labels


def _compose_executive_text(
    central: str,
    supporting: list[str],
    conclusion: str,
) -> str:
    parts: list[str] = []
    if central:
        parts.append(central)
    for index, point in enumerate(supporting, start=1):
        parts.append(f"({index}) {point}")
    if conclusion:
        parts.append(conclusion)
    return " ".join(parts).strip()


def _short(text: str, max_chars: int) -> str:
    cleaned = re.sub(r"\s+", " ", (text or "").strip())
    if len(cleaned) <= max_chars:
        return cleaned
    cut = cleaned[: max_chars - 1].rsplit(" ", 1)[0]
    return f"{cut}…"
