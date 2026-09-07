"""Project Marriage Assessment cards from a completed Decision.

Does not create Decision, Recommendation, or Canonical facts.
"""

from __future__ import annotations

from consulting.marriage.models.assessment import (
    ASSESSMENT_MODEL_VERSION,
    CUSTOMER_QUESTIONS,
    Q1_OVERALL_COMPATIBILITY,
    Q2_MUTUAL_SUPPORT,
    Q3_PERSONALITY_BALANCE,
    Q4_MARRIAGE_STABILITY,
    Q5_CHILDREN,
    Q6_OVERALL_MARRIAGE,
    QUESTION_SET_ID,
    MarriageAssessmentCard,
    MarriageAssessmentResult,
)
from consulting.marriage.models.comparison import MarriageComparisonFact, MarriageComparisonResult
from consulting.marriage.models.enums import (
    CanonicalGender,
    ComparisonFactKind,
    CompatibilityLevel,
    ConfidenceLevel,
    FiveElement,
    MarriageDomain,
    PresenceBand,
    RelationshipSubject,
    YinYang,
)
from consulting.marriage.models.result import MarriageDecisionResult
from consulting.marriage.models.snapshot import DayMasterSnapshot
from consulting.marriage.narrative.facts import render_fact

_ELEMENT_VI = {
    FiveElement.WOOD: "Mộc",
    FiveElement.FIRE: "Hỏa",
    FiveElement.EARTH: "Thổ",
    FiveElement.METAL: "Kim",
    FiveElement.WATER: "Thủy",
}
_GENERATES = {
    FiveElement.WOOD: FiveElement.FIRE,
    FiveElement.FIRE: FiveElement.EARTH,
    FiveElement.EARTH: FiveElement.METAL,
    FiveElement.METAL: FiveElement.WATER,
    FiveElement.WATER: FiveElement.WOOD,
}
_CONTROLS = {
    FiveElement.WOOD: FiveElement.EARTH,
    FiveElement.EARTH: FiveElement.WATER,
    FiveElement.WATER: FiveElement.FIRE,
    FiveElement.FIRE: FiveElement.METAL,
    FiveElement.METAL: FiveElement.WOOD,
}
_CONFIDENCE = {
    ConfidenceLevel.HIGH: "High",
    ConfidenceLevel.MEDIUM: "Medium",
    ConfidenceLevel.REFERENCE_ONLY: "Reference",
}
_MAX_FACTS = 4


def project_marriage_assessment(result: MarriageDecisionResult) -> MarriageAssessmentResult:
    """Project six customer questions from Decision comparison facts only."""
    comparison = result.comparison
    person_a = result.person_a.display_name or "Người A"
    person_b = result.person_b.display_name or "Người B"
    confidence = _CONFIDENCE.get(result.confidence.level, "Reference")
    cards = [
        _q1(result, comparison, person_a, person_b, confidence),
        _q2(result, comparison, person_a, person_b, confidence),
        _q3(result, comparison, person_a, person_b, confidence),
        _q4(result, comparison, person_a, person_b, confidence),
        _q5(result, comparison, person_a, person_b, confidence),
        _q6(result, comparison, person_a, person_b, confidence),
    ]
    return MarriageAssessmentResult(
        assessment_id=f"AS-{result.consultation_id}",
        consultation_id=result.consultation_id,
        question_set_id=QUESTION_SET_ID,
        version=ASSESSMENT_MODEL_VERSION,
        cards=cards,
        source_decision_id=result.consultation_id,
    )


def _q1(
    result: MarriageDecisionResult,
    comparison: MarriageComparisonResult | None,
    person_a: str,
    person_b: str,
    confidence: str,
) -> MarriageAssessmentCard:
    """Overall compatibility. Semantic conclusion only. No fake score."""
    level = comparison.overall.compatibility_level if comparison else CompatibilityLevel.INSUFFICIENT
    conflict = comparison.overall.conflict_strength if comparison else PresenceBand.NONE
    rescue = comparison.overall.rescue_strength if comparison else PresenceBand.NONE
    answer, key = _compatibility_answer(level, conflict, rescue)
    facts = _facts(
        comparison,
        person_a,
        person_b,
        kinds={ComparisonFactKind.SUPPORT, ComparisonFactKind.CONFLICT, ComparisonFactKind.RESCUE},
        prefer_domains=(MarriageDomain.FIVE_ELEMENTS, MarriageDomain.STEM_BRANCH),
    )
    return _card(Q1_OVERALL_COMPATIBILITY, answer, facts, confidence, result, key)


def _q2(
    result: MarriageDecisionResult,
    comparison: MarriageComparisonResult | None,
    person_a: str,
    person_b: str,
    confidence: str,
) -> MarriageAssessmentCard:
    """Directional mutual support. Vượng Phu / Vượng Thê only if evidence supports."""
    a_facts = _directional_support(comparison, RelationshipSubject.A_TO_B, person_a, person_b)
    b_facts = _directional_support(comparison, RelationshipSubject.B_TO_A, person_a, person_b)
    lines = []
    if a_facts:
        lines.append(f"{person_a} → {person_b}: {a_facts[0]}")
    if b_facts:
        lines.append(f"{person_b} → {person_a}: {b_facts[0]}")
    labels = _vuong_labels(result, comparison, person_a, person_b)
    if labels:
        lines.append("; ".join(labels) + ".")
    if not lines:
        lines.append("Chưa đủ tín hiệu bổ trợ cụ thể theo từng chiều.")
    facts = (a_facts + b_facts)[:_MAX_FACTS]
    if not facts:
        facts = _facts(comparison, person_a, person_b, kinds={ComparisonFactKind.NEED})
    return _card(Q2_MUTUAL_SUPPORT, ". ".join(lines), facts, confidence, result, "mutual_support")


def _q3(
    result: MarriageDecisionResult,
    comparison: MarriageComparisonResult | None,
    person_a: str,
    person_b: str,
    confidence: str,
) -> MarriageAssessmentCard:
    """Day Master and role-structure balance in customer language."""
    dm_a = result.canonical_a.day_master
    dm_b = result.canonical_b.day_master
    answer, key = _personality_answer(dm_a, dm_b, person_a, person_b)
    facts = [
        f"{person_a} Nhật Chủ {_stem_label(dm_a)} {_ELEMENT_VI[dm_a.element]}.",
        f"{person_b} Nhật Chủ {_stem_label(dm_b)} {_ELEMENT_VI[dm_b.element]}.",
        _polarity_fact(dm_a, dm_b, person_a, person_b),
    ]
    role = _facts(
        comparison,
        person_a,
        person_b,
        kinds={ComparisonFactKind.SUPPORT, ComparisonFactKind.CONFLICT},
        prefer_domains=(MarriageDomain.TEN_GODS,),
        limit=1,
    )
    facts.extend(role)
    return _card(Q3_PERSONALITY_BALANCE, answer, facts[:_MAX_FACTS], confidence, result, key)


def _q4(
    result: MarriageDecisionResult,
    comparison: MarriageComparisonResult | None,
    person_a: str,
    person_b: str,
    confidence: str,
) -> MarriageAssessmentCard:
    """Stability: one conclusion plus main conflict, rescue, and condition."""
    overall = comparison.overall if comparison else None
    if overall is None:
        answer = "Chưa đủ dữ liệu để nói về độ ổn định."
        key = "insufficient"
        facts: list[str] = []
    else:
        answer, key = _stability_answer(overall.q6_long_term, overall.conflict_strength, overall.rescue_strength)
        facts = _named_conflict_rescue(comparison, person_a, person_b)
    return _card(Q4_MARRIAGE_STABILITY, answer, facts, confidence, result, key)


def _q5(
    result: MarriageDecisionResult,
    comparison: MarriageComparisonResult | None,
    person_a: str,
    person_b: str,
    confidence: str,
) -> MarriageAssessmentCard:
    """Parenting only when the Children domain is supported. Never fertility."""
    children_ok = bool(comparison and comparison.children.available)
    if not children_ok:
        return _card(
            Q5_CHILDREN,
            "Insufficient.",
            ["Chưa đủ bằng chứng cấu trúc để luận nuôi dạy con chung."],
            confidence,
            result,
            "insufficient",
            extra_limitations=["children_unsupported"],
        )
    facts = _facts(
        comparison,
        person_a,
        person_b,
        kinds={ComparisonFactKind.SUPPORT, ComparisonFactKind.CONFLICT},
        prefer_domains=(MarriageDomain.CHILDREN,),
        fallback=False,
    )
    if not facts:
        return _card(
            Q5_CHILDREN,
            "Insufficient.",
            ["Miền con cái chưa có sự kiện đủ để luận nuôi dạy con chung."],
            confidence,
            result,
            "insufficient",
            extra_limitations=["children_unsupported"],
        )
    answer = "Hai người có nền tảng gia đạo có thể phối hợp nuôi dạy, không phải dự đoán sinh con."
    return _card(Q5_CHILDREN, answer, facts, confidence, result, "family_support")


def _q6(
    result: MarriageDecisionResult,
    comparison: MarriageComparisonResult | None,
    person_a: str,
    person_b: str,
    confidence: str,
) -> MarriageAssessmentCard:
    """Overall marriage question. Foundation conclusion, not an action plan."""
    overall = comparison.overall if comparison else None
    q1_card_key = comparison.overall.compatibility_level.value if comparison else "insufficient"
    if overall is None:
        answer = "Nên tìm hiểu thêm vì dữ liệu nền tảng chưa đủ."
        key = "insufficient"
        facts = []
    else:
        answer, key = _overall_answer(overall.q6_long_term, overall.compatibility_level)
        facts = _overall_facts(result, comparison, person_a, person_b, q1_card_key)
    return _card(Q6_OVERALL_MARRIAGE, answer, facts, confidence, result, key)


def _card(
    question_id: str,
    answer: str,
    facts: list[str],
    confidence: str,
    result: MarriageDecisionResult,
    semantic_key: str,
    extra_limitations: list[str] | None = None,
) -> MarriageAssessmentCard:
    """Assemble one card with shared limitations and traces."""
    limitations = list(result.limitations)
    if extra_limitations:
        limitations.extend(extra_limitations)
    finding_ids, evidence_ids, fact_ids = _traces(result, facts)
    return MarriageAssessmentCard(
        question_id=question_id,
        question=CUSTOMER_QUESTIONS[question_id],
        answer=_clip_answer(answer),
        supporting_facts=facts[:_MAX_FACTS],
        confidence=confidence,
        limitations=list(dict.fromkeys(limitations)),
        semantic_key=semantic_key,
        finding_ids=finding_ids,
        evidence_ids=evidence_ids,
        fact_ids=fact_ids,
    )


def _compatibility_answer(
    level: CompatibilityLevel,
    conflict: PresenceBand,
    rescue: PresenceBand,
) -> tuple[str, str]:
    """Map frozen compatibility level onto customer semantic labels."""
    if level is CompatibilityLevel.INSUFFICIENT:
        return "Chưa đủ dữ liệu để kết luận tương hợp.", "insufficient"
    if level is CompatibilityLevel.VERY_SUPPORTIVE:
        return "Rất hợp.", "very_compatible"
    if level is CompatibilityLevel.SUPPORTIVE:
        return "Khá hợp.", "quite_compatible"
    if level is CompatibilityLevel.MODERATELY_SUPPORTIVE:
        return "Khá hợp.", "quite_compatible"
    if level in {CompatibilityLevel.PRESSURED, CompatibilityLevel.HIGHLY_PRESSURED}:
        return "Áp lực cao.", "high_pressure"
    if conflict is PresenceBand.PROMINENT and rescue is PresenceBand.NONE:
        return "Cần điều chỉnh.", "needs_adjustment"
    return "Trung bình.", "average"


def _stability_answer(q6: str, conflict: PresenceBand, rescue: PresenceBand) -> tuple[str, str]:
    """One stability conclusion. No divorce prediction."""
    if q6 == "insufficient":
        return "Chưa đủ dữ liệu để nói cuộc hôn nhân có ổn định hay không.", "insufficient"
    if q6 == "structure_supports_long_term":
        return "Có nền tảng để ổn định nếu giữ đúng nhịp hỗ trợ đã có.", "stable_if_kept"
    if q6 == "needs_active_management" or conflict is PresenceBand.PROMINENT and rescue is PresenceBand.NONE:
        return "Ổn định được nếu xử lý đúng điểm căng chính, không phải kết luận đổ vỡ.", "needs_management"
    if rescue is PresenceBand.PROMINENT:
        return "Có thể ổn định vì điểm căng đi kèm yếu tố cứu giải.", "stable_with_rescue"
    return "Có thể ổn định nếu hai người quản lý đúng điểm lệch.", "maintainable"


def _overall_answer(q6: str, level: CompatibilityLevel) -> tuple[str, str]:
    """Q6 is a foundation conclusion, not a command to marry."""
    if q6 == "insufficient" or level is CompatibilityLevel.INSUFFICIENT:
        return "Nên tìm hiểu thêm.", "learn_more"
    if q6 == "structure_supports_long_term" or level in {
        CompatibilityLevel.VERY_SUPPORTIVE,
        CompatibilityLevel.SUPPORTIVE,
    }:
        return "Có nền tảng tốt.", "good_foundation"
    if q6 == "needs_active_management" or level in {
        CompatibilityLevel.PRESSURED,
        CompatibilityLevel.HIGHLY_PRESSURED,
    }:
        return "Cần giải quyết điểm căng chính trước khi tiến tới.", "resolve_first"
    return "Có thể tiến tới.", "can_proceed"


def _personality_answer(
    dm_a: DayMasterSnapshot,
    dm_b: DayMasterSnapshot,
    person_a: str,
    person_b: str,
) -> tuple[str, str]:
    """Structural Day Master comparison. Not a psychology essay."""
    if dm_a.element is dm_b.element:
        return (
            f"Hai Nhật Chủ cùng hành {_ELEMENT_VI[dm_a.element]}, tính khí gần nhau hơn là bù trừ.",
            "similar",
        )
    if _GENERATES.get(dm_a.element) is dm_b.element or _GENERATES.get(dm_b.element) is dm_a.element:
        return "Hai người bù trừ tốt.", "complementary"
    if _CONTROLS.get(dm_a.element) is dm_b.element or _CONTROLS.get(dm_b.element) is dm_a.element:
        return "Có xung ở tính cách gốc, cần quy ước rõ.", "conflict"
    if dm_a.yin_yang is not dm_b.yin_yang:
        return "Cân bằng: một người thiên quyết đoán, một người thiên mềm dẻo.", "balanced"
    return "Có khác biệt Nhật Chủ, chưa hẳn xung đột.", "different"


def _polarity_fact(
    dm_a: DayMasterSnapshot,
    dm_b: DayMasterSnapshot,
    person_a: str,
    person_b: str,
) -> str:
    """Name the main Day Master difference in customer language."""
    style_a = "quyết đoán" if dm_a.yin_yang is YinYang.YANG else "mềm dẻo"
    style_b = "quyết đoán" if dm_b.yin_yang is YinYang.YANG else "mềm dẻo"
    if style_a == style_b:
        return f"Cả hai cùng thiên {style_a} ở Nhật Chủ."
    return f"{person_a} thiên {style_a}. {person_b} thiên {style_b}."


def _stem_label(day_master: DayMasterSnapshot) -> str:
    """Use the published stem token. Do not invent a new name."""
    return day_master.stem or "Nhật Chủ"


def _directional_support(
    comparison: MarriageComparisonResult | None,
    subject: RelationshipSubject,
    person_a: str,
    person_b: str,
) -> list[str]:
    """Concrete support facts in one direction."""
    return _facts(
        comparison,
        person_a,
        person_b,
        kinds={ComparisonFactKind.SUPPORT},
        subjects={subject},
        prefer_domains=(MarriageDomain.FIVE_ELEMENTS, MarriageDomain.TEN_GODS),
        limit=2,
    )


def _vuong_labels(
    result: MarriageDecisionResult,
    comparison: MarriageComparisonResult | None,
    person_a: str,
    person_b: str,
) -> list[str]:
    """Vượng Phu / Vượng Thê only from useful-god support plus opposite genders."""
    if comparison is None:
        return []
    gender_a = result.person_a.gender
    gender_b = result.person_b.gender
    if gender_a is gender_b:
        return []
    if {gender_a, gender_b} != {CanonicalGender.MALE, CanonicalGender.FEMALE}:
        return []
    husband_is_a = gender_a is CanonicalGender.MALE
    labels: list[str] = []
    useful = [
        item
        for item in comparison.facts
        if item.template_key == "useful_god_support" and item.kind is ComparisonFactKind.SUPPORT
    ]
    wife_to_husband = RelationshipSubject.B_TO_A if husband_is_a else RelationshipSubject.A_TO_B
    husband_to_wife = RelationshipSubject.A_TO_B if husband_is_a else RelationshipSubject.B_TO_A
    wife = person_b if husband_is_a else person_a
    husband = person_a if husband_is_a else person_b
    if any(item.subject is wife_to_husband for item in useful):
        labels.append(f"Vượng Phu: {wife} hỗ trợ Dụng thần của {husband}")
    if any(item.subject is husband_to_wife for item in useful):
        labels.append(f"Vượng Thê: {husband} hỗ trợ Dụng thần của {wife}")
    return labels


def _named_conflict_rescue(
    comparison: MarriageComparisonResult | None,
    person_a: str,
    person_b: str,
) -> list[str]:
    """Main conflict, rescue, and condition as concrete bullets."""
    facts: list[str] = []
    conflict = _facts(
        comparison,
        person_a,
        person_b,
        kinds={ComparisonFactKind.CONFLICT},
        prefer_domains=(MarriageDomain.STEM_BRANCH, MarriageDomain.FINANCE, MarriageDomain.INTERACTION),
        limit=1,
    )
    if conflict:
        facts.append("Xung chính: " + conflict[0])
    rescue = _facts(comparison, person_a, person_b, kinds={ComparisonFactKind.RESCUE}, limit=1)
    if rescue:
        facts.append("Cứu giải: " + rescue[0])
    elif comparison and comparison.overall.q5_rescue == "conflict_unmitigated":
        facts.append("Điều kiện: điểm căng chưa có yếu tố giảm đi kèm.")
    else:
        facts.append("Điều kiện: giữ các điểm hỗ trợ đang có để giảm ma sát.")
    extra = _facts(
        comparison,
        person_a,
        person_b,
        kinds={ComparisonFactKind.SUPPORT},
        prefer_domains=(MarriageDomain.FINANCE, MarriageDomain.INTERACTION),
        limit=1,
    )
    facts.extend(extra)
    return facts[:_MAX_FACTS]


def _overall_facts(
    result: MarriageDecisionResult,
    comparison: MarriageComparisonResult | None,
    person_a: str,
    person_b: str,
    compatibility_key: str,
) -> list[str]:
    """Relationship, finance, growth, long-term, condition."""
    facts = [
        f"Quan hệ: {CUSTOMER_QUESTIONS[Q1_OVERALL_COMPATIBILITY]} → {_compatibility_short(compatibility_key)}",
    ]
    finance = _facts(
        comparison,
        person_a,
        person_b,
        kinds={ComparisonFactKind.SUPPORT, ComparisonFactKind.CONFLICT},
        prefer_domains=(MarriageDomain.FINANCE,),
        fallback=False,
        limit=1,
    )
    if finance:
        facts.append("Tài chính: " + finance[0])
    else:
        facts.append("Tài chính: chưa đủ để luận hợp tác tiền bạc riêng.")
    luck = _facts(
        comparison,
        person_a,
        person_b,
        prefer_domains=(MarriageDomain.LUCK,),
        fallback=False,
        limit=1,
    )
    if luck:
        facts.append("Tăng trưởng: " + luck[0])
    else:
        facts.append("Hợp tác dài hạn: " + _long_term_vi(comparison.overall.q6_long_term if comparison else "insufficient"))
    condition = _facts(comparison, person_a, person_b, kinds={ComparisonFactKind.CONFLICT}, limit=1)
    if condition:
        facts.append("Điều kiện chính: " + condition[0])
    hour_missing = any("hour" in item or "birth_time" in item for item in result.limitations)
    if hour_missing:
        facts.append("Giới hạn: thiếu giờ sinh nên kết luận mang tính tham khảo.")
    return facts[:_MAX_FACTS]


def _long_term_vi(key: str) -> str:
    """Customer wording for the frozen long-term comparison key."""
    mapping = {
        "structure_supports_long_term": "nền tảng có thể giữ lâu",
        "maintainable_if_managed": "đi được lâu nếu quản lý điểm căng",
        "needs_active_management": "cần quản lý chủ động",
        "insufficient": "chưa đủ dữ liệu",
    }
    return mapping.get(key, "cần đọc kèm giới hạn dữ liệu")


def _compatibility_short(key: str) -> str:
    """Short Q1 echo for Q6 supporting facts."""
    mapping = {
        "very_supportive": "Rất hợp",
        "supportive": "Khá hợp",
        "moderately_supportive": "Khá hợp",
        "mixed": "Trung bình",
        "pressured": "Áp lực cao",
        "highly_pressured": "Áp lực cao",
        "insufficient": "Insufficient",
    }
    return mapping.get(key, key)


def _facts(
    comparison: MarriageComparisonResult | None,
    person_a: str,
    person_b: str,
    *,
    kinds: set[ComparisonFactKind] | None = None,
    subjects: set[RelationshipSubject] | None = None,
    prefer_domains: tuple[MarriageDomain, ...] | None = None,
    fallback: bool = True,
    limit: int = _MAX_FACTS,
) -> list[str]:
    """Render concrete comparison facts. Skip generic leftovers."""
    if comparison is None:
        return []
    selected = list(comparison.facts)
    if kinds:
        selected = [item for item in selected if item.kind in kinds]
    if subjects:
        selected = [item for item in selected if item.subject in subjects]
    if prefer_domains:
        preferred = [item for item in selected if item.domain in prefer_domains]
        if preferred:
            selected = preferred
        elif not fallback:
            return []
    selected = _rank(selected)
    texts: list[str] = []
    seen: set[str] = set()
    for item in selected:
        text = render_fact(item, person_a, person_b).strip()
        if not text or text in seen or _generic(text):
            continue
        seen.add(text)
        texts.append(text)
        if len(texts) >= limit:
            break
    return texts


def _rank(items: list[MarriageComparisonFact]) -> list[MarriageComparisonFact]:
    """Prominent facts first, then stable id order."""
    return sorted(
        items,
        key=lambda item: (
            0 if item.significance.value in {"major", "critical"} else 1,
            item.domain.value,
            item.fact_id,
        ),
    )


def _generic(text: str) -> bool:
    """Reject standalone generic labels if they leak into a fact sentence."""
    banned = (
        "Điểm hỗ trợ nền tảng",
        "Điểm bổ trợ vai trò",
        "Điểm cần lưu ý ở nền tảng",
        "Điểm ma sát Can Chi",
        "Có điểm hỗ trợ.",
    )
    return text.strip() in banned or text.startswith("Có tín hiệu so sánh cụ thể")


def _clip_answer(text: str) -> str:
    """Keep the answer to a few short lines."""
    parts = [item.strip() for item in text.replace("\n", " ").split(".") if item.strip()]
    clipped = ". ".join(parts[:4])
    if clipped and not clipped.endswith("."):
        clipped += "."
    return clipped or text


def _traces(
    result: MarriageDecisionResult,
    _facts_text: list[str],
) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    """Bind cards to existing finding/evidence ids from comparison."""
    comparison = result.comparison
    if comparison is None:
        return (), (), ()
    facts = comparison.facts[:8]
    finding_ids = tuple(dict.fromkeys(fid for item in facts for fid in item.finding_ids))
    evidence_ids = tuple(dict.fromkeys(eid for item in facts for eid in item.evidence_ids))
    fact_ids = tuple(item.fact_id for item in facts)
    return finding_ids[:12], evidence_ids[:12], fact_ids[:12]
