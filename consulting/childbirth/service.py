"""Childbirth consulting service.

The module evaluates future birth years for a married couple from already
published Canonical signals. It does not change Canonical truth.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

from consulting.marriage.adapters.canonical_runtime import (
    CanonicalOrchestratorAdapter,
    build_person_analysis,
)
from consulting.marriage.dto.request import MarriagePersonInput
from consulting.marriage.models.enums import CanonicalGender, FiveElement, PersonSide
from consulting.marriage.models.snapshot import MarriageCanonicalSnapshot
from consulting.marriage.runtime.snapshot_builder import build_marriage_snapshot

CHILDBIRTH_MODULE_VERSION = "childbirth.consulting.v1"
DEFAULT_YEARS_AHEAD = 12
MAX_YEARS_AHEAD = 24

_STEMS = ("Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý")
_BRANCHES = ("Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi")
_STEM_ELEMENTS = (
    FiveElement.WOOD,
    FiveElement.WOOD,
    FiveElement.FIRE,
    FiveElement.FIRE,
    FiveElement.EARTH,
    FiveElement.EARTH,
    FiveElement.METAL,
    FiveElement.METAL,
    FiveElement.WATER,
    FiveElement.WATER,
)
_BRANCH_ELEMENTS = {
    "Tý": FiveElement.WATER,
    "Sửu": FiveElement.EARTH,
    "Dần": FiveElement.WOOD,
    "Mão": FiveElement.WOOD,
    "Thìn": FiveElement.EARTH,
    "Tỵ": FiveElement.FIRE,
    "Ngọ": FiveElement.FIRE,
    "Mùi": FiveElement.EARTH,
    "Thân": FiveElement.METAL,
    "Dậu": FiveElement.METAL,
    "Tuất": FiveElement.EARTH,
    "Hợi": FiveElement.WATER,
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
_CLASHES = {
    frozenset(("Tý", "Ngọ")),
    frozenset(("Sửu", "Mùi")),
    frozenset(("Dần", "Thân")),
    frozenset(("Mão", "Dậu")),
    frozenset(("Thìn", "Tuất")),
    frozenset(("Tỵ", "Hợi")),
}
_POSITIVE_SHEN_SHA = ("Thiên Ất", "Quý Nhân", "Thiên Đức", "Nguyệt Đức", "Phúc Đức", "Văn Xương")
_CAUTION_SHEN_SHA = ("Cô Thần", "Quả Tú", "Kiếp Sát", "Tai Sát", "Kình Dương")
_ELEMENT_LABELS = {
    FiveElement.WOOD: "Mộc",
    FiveElement.FIRE: "Hỏa",
    FiveElement.EARTH: "Thổ",
    FiveElement.METAL: "Kim",
    FiveElement.WATER: "Thủy",
}
_GUA_NAMES = {
    1: "Khảm",
    2: "Khôn",
    3: "Chấn",
    4: "Tốn",
    6: "Càn",
    7: "Đoài",
    8: "Cấn",
    9: "Ly",
}
_EAST_GUA = {1, 3, 4, 9}


@dataclass(frozen=True, slots=True)
class ParentSignals:
    """Signals selected from one Canonical snapshot."""

    name: str
    gender: str
    birth_date: str
    day_master: str
    day_master_element: FiveElement
    day_branch: str
    strength: str
    pattern: str | None
    useful_elements: frozenset[FiveElement]
    favorable_elements: frozenset[FiveElement]
    unfavorable_elements: frozenset[FiveElement]
    useful_stems: frozenset[str]
    ten_gods: tuple[str, ...]
    shen_sha: tuple[str, ...]
    cung_phi: str | None
    trach_group: str | None


def analyze_childbirth_plan(
    *,
    father: MarriagePersonInput,
    mother: MarriagePersonInput,
    start_year: int | None = None,
    years_ahead: int = DEFAULT_YEARS_AHEAD,
    adapter: CanonicalOrchestratorAdapter | None = None,
    today: date | None = None,
) -> dict[str, Any]:
    """Analyze future childbirth timing for a married couple."""
    _validate_parent(father, CanonicalGender.MALE, "father")
    _validate_parent(mother, CanonicalGender.FEMALE, "mother")
    current = today or date.today()
    start = start_year or current.year
    if years_ahead < 1 or years_ahead > MAX_YEARS_AHEAD:
        raise ValueError("years_ahead_out_of_range")
    runtime = adapter or CanonicalOrchestratorAdapter()
    father_snapshot = _snapshot_for(runtime, father, PersonSide.B, "CB-FATHER")
    mother_snapshot = _snapshot_for(runtime, mother, PersonSide.A, "CB-MOTHER")
    return evaluate_childbirth_years(
        father_snapshot=father_snapshot,
        mother_snapshot=mother_snapshot,
        father_birth_date=father.birth_date,
        mother_birth_date=mother.birth_date,
        start_year=start,
        years_ahead=years_ahead,
    )


def evaluate_childbirth_years(
    *,
    father_snapshot: MarriageCanonicalSnapshot,
    mother_snapshot: MarriageCanonicalSnapshot,
    father_birth_date: str,
    mother_birth_date: str,
    start_year: int,
    years_ahead: int,
) -> dict[str, Any]:
    """Evaluate years from snapshots. Public for deterministic tests."""
    father = _signals(father_snapshot, father_birth_date)
    mother = _signals(mother_snapshot, mother_birth_date)
    father_birth = _parse_date(father_birth_date)
    mother_birth = _parse_date(mother_birth_date)
    results = []
    ineligible = []
    for year in range(start_year, start_year + years_ahead):
        father_age = _age_on(father_birth, date(year, 12, 31))
        mother_age = _age_on(mother_birth, date(year, 12, 31))
        if father_age < 20 or mother_age < 18:
            ineligible.append(
                {
                    "year": year,
                    "father_age": father_age,
                    "mother_age": mother_age,
                    "reason": "Bố cần đủ 20 tuổi và mẹ cần đủ 18 tuổi trong năm sinh dự kiến.",
                }
            )
            continue
        results.append(_evaluate_year(year, father, mother, father_age, mother_age))
    results.sort(key=lambda item: (-item["score"], item["year"]))
    top = results[:5]
    return {
        "module": "childbirth_consulting",
        "module_version": CHILDBIRTH_MODULE_VERSION,
        "status": "SUCCESS",
        "start_year": start_year,
        "years_ahead": years_ahead,
        "eligibility": {
            "father_min_age": 20,
            "mother_min_age": 18,
            "rule": "Một năm chỉ được xét khi đến 31/12 của năm đó bố đủ 20 tuổi và mẹ đủ 18 tuổi.",
            "ineligible_years": ineligible,
        },
        "parents": {
            "father": _public_parent(father),
            "mother": _public_parent(mother),
        },
        "recommendations": top,
        "all_years": results,
        "summary": _summary(top, bool(ineligible)),
    }


def _validate_parent(person: MarriagePersonInput, expected: CanonicalGender, role: str) -> None:
    if person.gender is not expected:
        raise ValueError(f"{role}_gender_mismatch")
    _parse_date(person.birth_date)


def _snapshot_for(
    adapter: CanonicalOrchestratorAdapter,
    person: MarriagePersonInput,
    side: PersonSide,
    analysis_id: str,
) -> MarriageCanonicalSnapshot:
    analysis = build_person_analysis(adapter, person, analysis_id=analysis_id, side=side)
    return build_marriage_snapshot(analysis=analysis, person=person, analysis_id=analysis_id, side=side)


def _signals(snapshot: MarriageCanonicalSnapshot, birth_date: str) -> ParentSignals:
    ten_gods = [
        item.name
        for group in (snapshot.ten_gods.visible, snapshot.ten_gods.hidden)
        for item in (group or [])
        if item.name
    ]
    useful = snapshot.useful_god.useful or []
    favorable = snapshot.useful_god.favorable or []
    unfavorable = snapshot.useful_god.unfavorable or []
    shen_sha = tuple(item.name for item in (snapshot.shen_sha.items if snapshot.shen_sha else []) if item.name)
    return ParentSignals(
        name=snapshot.person.display_name or "",
        gender=snapshot.person.gender.value,
        birth_date=birth_date,
        day_master=snapshot.day_master.stem,
        day_master_element=snapshot.day_master.element,
        day_branch=snapshot.pillars.day.branch,
        strength=snapshot.strength.classification,
        pattern=snapshot.pattern.pattern_name or snapshot.pattern.pattern_id,
        useful_elements=frozenset(ref.element for ref in useful if ref.element is not None),
        favorable_elements=frozenset(ref.element for ref in favorable if ref.element is not None),
        unfavorable_elements=frozenset(ref.element for ref in unfavorable if ref.element is not None),
        useful_stems=frozenset(ref.stem for ref in useful if ref.stem),
        ten_gods=tuple(dict.fromkeys(ten_gods)),
        shen_sha=tuple(dict.fromkeys(shen_sha)),
        cung_phi=snapshot.feng_shui.cung_phi if snapshot.feng_shui else None,
        trach_group=snapshot.feng_shui.group if snapshot.feng_shui else None,
    )


def _evaluate_year(
    year: int,
    father: ParentSignals,
    mother: ParentSignals,
    father_age: int,
    mother_age: int,
) -> dict[str, Any]:
    stem, branch = _year_ganzhi(year)
    year_element = _STEM_ELEMENTS[_STEMS.index(stem)]
    branch_element = _BRANCH_ELEMENTS[branch]
    score = 50
    reasons: list[str] = []
    cautions: list[str] = []
    score += _parent_score("bố", father, stem, branch, year_element, branch_element, reasons, cautions)
    score += _parent_score("mẹ", mother, stem, branch, year_element, branch_element, reasons, cautions)
    gender = _gender_options(year, father, mother)
    score += gender["score_adjustment"]
    if gender["recommended_child_gender"] == "boy":
        reasons.append("Cung phi giả định của bé trai hài hòa với nhóm trạch của bố mẹ hơn.")
    elif gender["recommended_child_gender"] == "girl":
        reasons.append("Cung phi giả định của bé gái hài hòa với nhóm trạch của bố mẹ hơn.")
    else:
        reasons.append("Chênh lệch cung phi giữa bé trai và bé gái không lớn, có thể ưu tiên năm hơn giới tính.")
    clipped = max(0, min(100, score))
    return {
        "year": year,
        "can_chi": f"{stem} {branch}",
        "stem": stem,
        "branch": branch,
        "primary_element": _ELEMENT_LABELS[year_element],
        "branch_element": _ELEMENT_LABELS[branch_element],
        "father_age": father_age,
        "mother_age": mother_age,
        "score": clipped,
        "level": _level(clipped),
        "recommended_child_gender": gender["recommended_child_gender"],
        "boy": gender["boy"],
        "girl": gender["girl"],
        "reasons": list(dict.fromkeys(reasons))[:6],
        "cautions": list(dict.fromkeys(cautions))[:4],
    }


def _parent_score(
    label: str,
    parent: ParentSignals,
    stem: str,
    branch: str,
    year_element: FiveElement,
    branch_element: FiveElement,
    reasons: list[str],
    cautions: list[str],
) -> int:
    score = 0
    if year_element in parent.useful_elements or stem in parent.useful_stems:
        score += 10
        reasons.append(f"Năm {stem} {branch} chạm đúng Dụng thần/yếu tố cần của {label}.")
    if year_element in parent.favorable_elements or branch_element in parent.favorable_elements:
        score += 6
        reasons.append(f"Ngũ hành năm có phần thuộc Hỷ thần của {label}.")
    if year_element in parent.unfavorable_elements:
        score -= 8
        cautions.append(f"Thiên can năm kích hoạt nhóm Kỵ thần của {label}, cần chọn tháng/ngày kỹ hơn.")
    output = _GENERATES[parent.day_master_element]
    if year_element is output or branch_element is output:
        score += 7
        reasons.append(f"Năm mở kênh biểu đạt/con cái cho Nhật chủ {parent.day_master} của {label}.")
    if _GENERATES[year_element] is parent.day_master_element:
        score += 4
        reasons.append(f"Ngũ hành năm sinh trợ cho Nhật chủ của {label}.")
    if _CONTROLS[year_element] is parent.day_master_element:
        score -= 5
        cautions.append(f"Ngũ hành năm tạo áp lực lên Nhật chủ của {label}.")
    if frozenset((branch, parent.day_branch)) in _CLASHES:
        score -= 7
        cautions.append(f"Địa chi năm xung với chi ngày của {label}; nên thận trọng tháng sinh.")
    if branch == parent.day_branch:
        score += 3
        reasons.append(f"Địa chi năm đồng khí với cung ngày của {label}.")
    score += _strength_adjustment(label, parent, year_element, reasons, cautions)
    score += _ten_god_adjustment(label, parent, reasons)
    score += _shen_sha_adjustment(label, parent, reasons, cautions)
    return score


def _strength_adjustment(
    label: str,
    parent: ParentSignals,
    year_element: FiveElement,
    reasons: list[str],
    cautions: list[str],
) -> int:
    strength = parent.strength.lower()
    if "vượng" in strength or "strong" in strength:
        if year_element is _GENERATES[parent.day_master_element]:
            reasons.append(f"{label.capitalize()} có thân vượng, năm có kênh tiết xuất giúp cân bằng hơn.")
            return 4
        if year_element is parent.day_master_element:
            cautions.append(f"{label.capitalize()} đã thiên vượng, năm cùng hành có thể làm lực quá đầy.")
            return -2
    if "nhược" in strength or "weak" in strength or "yếu" in strength:
        if _GENERATES[year_element] is parent.day_master_element:
            reasons.append(f"{label.capitalize()} có thân nhược, năm sinh trợ giúp nền ổn hơn.")
            return 4
        if _CONTROLS[year_element] is parent.day_master_element:
            return -3
    return 0


def _ten_god_adjustment(label: str, parent: ParentSignals, reasons: list[str]) -> int:
    names = set(parent.ten_gods)
    score = 0
    if {"Thực Thần", "Thương Quan"} & names:
        score += 3
        reasons.append(f"Thập thần của {label} có kênh con cái/biểu đạt để tham chiếu.")
    if {"Chính Quan", "Thất Sát"} & names:
        score += 2
        reasons.append(f"Thập thần của {label} có trục trách nhiệm/gia đạo rõ để nâng quyết định sinh con.")
    return score


def _shen_sha_adjustment(
    label: str,
    parent: ParentSignals,
    reasons: list[str],
    cautions: list[str],
) -> int:
    score = 0
    text = " ".join(parent.shen_sha)
    if any(name in text for name in _POSITIVE_SHEN_SHA):
        score += 2
        reasons.append(f"Thần sát của {label} có tín hiệu trợ lực/quý nhân.")
    if any(name in text for name in _CAUTION_SHEN_SHA):
        score -= 2
        cautions.append(f"Thần sát của {label} có tín hiệu cần giữ nhịp gia đạo ổn định.")
    return score


def _gender_options(year: int, father: ParentSignals, mother: ParentSignals) -> dict[str, Any]:
    boy = _child_cung_phi(year, "male", father, mother)
    girl = _child_cung_phi(year, "female", father, mother)
    diff = boy["score"] - girl["score"]
    if diff >= 3:
        recommendation = "boy"
    elif diff <= -3:
        recommendation = "girl"
    else:
        recommendation = "either"
    return {
        "recommended_child_gender": recommendation,
        "boy": boy,
        "girl": girl,
        "score_adjustment": max(boy["score"], girl["score"]),
    }


def _child_cung_phi(
    year: int,
    gender: str,
    father: ParentSignals,
    mother: ParentSignals,
) -> dict[str, Any]:
    number = _kua_number(year, gender)
    group = "Đông Tứ Trạch" if number in _EAST_GUA else "Tây Tứ Trạch"
    score = 0
    matched = []
    for label, parent in (("bố", father), ("mẹ", mother)):
        if parent.trach_group and parent.trach_group == group:
            score += 4
            matched.append(label)
        if parent.cung_phi == _GUA_NAMES[number]:
            score += 2
    return {
        "cung_phi": _GUA_NAMES[number],
        "trach_group": group,
        "score": score,
        "matched_parent_groups": matched,
    }


def _kua_number(year: int, gender: str) -> int:
    digits = sum(int(char) for char in str(year)[-2:])
    while digits > 9:
        digits = sum(int(char) for char in str(digits))
    if year >= 2000:
        number = 9 - digits if gender == "male" else 6 + digits
    else:
        number = 10 - digits if gender == "male" else 5 + digits
    while number > 9:
        number = sum(int(char) for char in str(number))
    if number == 5:
        return 2 if gender == "male" else 8
    if number == 0:
        return 9
    return number


def _year_ganzhi(year: int) -> tuple[str, str]:
    index = (year - 1984) % 60
    return _STEMS[index % 10], _BRANCHES[index % 12]


def _age_on(birth: date, target: date) -> int:
    return target.year - birth.year - ((target.month, target.day) < (birth.month, birth.day))


def _parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def _level(score: int) -> str:
    if score >= 80:
        return "very_suitable"
    if score >= 68:
        return "suitable"
    if score >= 55:
        return "consider"
    return "sensitive"


def _public_parent(parent: ParentSignals) -> dict[str, Any]:
    return {
        "display_name": parent.name,
        "gender": parent.gender,
        "birth_date": parent.birth_date,
        "day_master": parent.day_master,
        "day_master_element": _ELEMENT_LABELS[parent.day_master_element],
        "strength": parent.strength,
        "pattern": parent.pattern,
        "useful_elements": [_ELEMENT_LABELS[item] for item in sorted(parent.useful_elements, key=lambda x: x.value)],
        "favorable_elements": [_ELEMENT_LABELS[item] for item in sorted(parent.favorable_elements, key=lambda x: x.value)],
        "unfavorable_elements": [_ELEMENT_LABELS[item] for item in sorted(parent.unfavorable_elements, key=lambda x: x.value)],
        "ten_gods": list(parent.ten_gods),
        "shen_sha": list(parent.shen_sha),
        "cung_phi": parent.cung_phi,
        "trach_group": parent.trach_group,
    }


def _summary(top: list[dict[str, Any]], has_ineligible: bool) -> dict[str, Any]:
    if not top:
        return {
            "headline": "Chưa có năm đủ điều kiện tuổi trong khoảng đang xét.",
            "recommended_years": [],
            "note": "Hãy mở rộng khoảng năm hoặc kiểm tra lại ngày sinh bố mẹ.",
        }
    years = [str(item["year"]) for item in top[:3]]
    best = top[0]
    note = "Một số năm đầu đã bị loại vì chưa đạt điều kiện tuổi tối thiểu." if has_ineligible else None
    return {
        "headline": f"Nên ưu tiên {', '.join(years)}; năm nổi bật nhất là {best['year']} ({best['can_chi']}).",
        "recommended_years": [item["year"] for item in top],
        "best_year": best["year"],
        "best_child_gender": best["recommended_child_gender"],
        "note": note,
    }
