"""Rank an editorial whitelist using existing Canonical signals, read-only."""

from __future__ import annotations

import json
from collections import Counter
from functools import lru_cache
from pathlib import Path
from typing import Any

from consulting.marriage.adapters.canonical_runtime import CanonicalOrchestratorAdapter
from consulting.marriage.dto.request import BirthPlaceInput, MarriagePersonInput
from consulting.marriage.evidence.snapshot_access import (
    favorable_elements,
    unfavorable_elements,
    useful_elements,
)
from consulting.marriage.models.enums import CanonicalGender, FiveElement, PersonSide
from consulting.marriage.models.snapshot import MarriageCanonicalSnapshot
from consulting.marriage.runtime.canonical_labels import try_map_five_element
from consulting.marriage.runtime.snapshot_builder import build_marriage_snapshot
from consulting.naming.models import NamingBirthInput, NamingRequest, normalize_name

MODULE_VERSION = "naming.consulting.v0.1"
ELEMENT_LABELS = {
    FiveElement.WOOD: "Mộc", FiveElement.FIRE: "Hỏa", FiveElement.EARTH: "Thổ",
    FiveElement.METAL: "Kim", FiveElement.WATER: "Thủy",
}
GENERATES = {
    FiveElement.WOOD: FiveElement.FIRE,
    FiveElement.FIRE: FiveElement.EARTH,
    FiveElement.EARTH: FiveElement.METAL,
    FiveElement.METAL: FiveElement.WATER,
    FiveElement.WATER: FiveElement.WOOD,
}
CONTROLS = {
    FiveElement.WOOD: FiveElement.EARTH,
    FiveElement.EARTH: FiveElement.WATER,
    FiveElement.WATER: FiveElement.FIRE,
    FiveElement.FIRE: FiveElement.METAL,
    FiveElement.METAL: FiveElement.WOOD,
}


@lru_cache(maxsize=1)
def load_catalog() -> dict[str, Any]:
    catalog = json.loads(Path(__file__).with_name("catalog.json").read_text(encoding="utf-8"))
    identifiers: set[str] = set()
    names: set[str] = set()
    for entry in catalog["names"]:
        FiveElement(entry["element"].lower())
        name = normalize_name(entry["name"]).casefold()
        if entry["id"] in identifiers or name in names:
            raise ValueError("naming_catalog_duplicate")
        if not entry["meaning"] or not entry["basis"] or not entry["genders"]:
            raise ValueError("naming_catalog_incomplete")
        if not set(entry["genders"]) <= {"male", "female"}:
            raise ValueError("naming_catalog_gender_invalid")
        identifiers.add(entry["id"])
        names.add(name)
    for gender in ("male", "female"):
        if sum(gender in entry["genders"] for entry in catalog["names"]) < 11:
            raise ValueError("naming_catalog_too_small")
    return catalog


def analyze_naming(
    request: NamingRequest,
    *,
    adapter: CanonicalOrchestratorAdapter | None = None,
) -> dict[str, Any]:
    snapshot, cung_element = build_naming_birth_snapshot(
        request, full_name=request.current_name, adapter=adapter,
    )
    return recommend_names(request, snapshot, cung_element=cung_element)


def build_naming_birth_snapshot(
    request: NamingBirthInput,
    *,
    full_name: str = "",
    adapter: CanonicalOrchestratorAdapter | None = None,
) -> tuple[MarriageCanonicalSnapshot, FiveElement | None]:
    person = MarriagePersonInput(
        gender=CanonicalGender(request.gender),
        birth_date=request.birth_date,
        birth_time=request.birth_time,
        full_name=full_name or None,
        birth_place=BirthPlaceInput(display_name=request.birth_place) if request.birth_place else None,
        timezone=request.timezone,
    )
    analysis = (adapter or CanonicalOrchestratorAdapter()).analyze(person)
    snapshot = build_marriage_snapshot(
        analysis=analysis, person=person, analysis_id="NAMING-V01", side=PersonSide.A,
    )
    calendar = analysis["canonical"].get("calendar") or {}
    cung_element = try_map_five_element(calendar.get("hanh_cung"))
    if cung_element is None and snapshot.feng_shui:
        cung_element = snapshot.feng_shui.element
    return snapshot, cung_element


def naming_birth_signals(
    request: NamingBirthInput,
    snapshot: MarriageCanonicalSnapshot,
    *,
    cung_element: FiveElement | None = None,
) -> tuple[dict[str, Any], list[str]]:
    hour_known = request.birth_time is not None and snapshot.pillars.hour is not None
    useful = set(useful_elements(snapshot.useful_god)) if hour_known else set()
    favorable = set(favorable_elements(snapshot.useful_god)) if hour_known else set()
    unfavorable = set(unfavorable_elements(snapshot.useful_god)) if hour_known else set()
    nap_am = snapshot.pillars.year.na_yin or ""
    nap_element = try_map_five_element(nap_am.rsplit(" ", 1)[-1])
    cung = snapshot.feng_shui.cung_phi if snapshot.feng_shui else None
    cung_element = cung_element or (snapshot.feng_shui.element if snapshot.feng_shui else None)
    warnings = []
    conflicts = (useful | favorable) & unfavorable
    if conflicts:
        warnings.append(
            f"BTE công bố tín hiệu xung đột ở hành {', '.join(_labels(conflicts))}. "
            "Tạm loại các hành này khỏi gợi ý và cần xác minh lại lá số."
        )
    useful -= unfavorable
    favorable -= unfavorable | useful
    if not hour_known:
        warnings.append("Chưa biết giờ sinh: chỉ gợi ý sơ bộ theo ý nghĩa, Nạp Âm và Cung Phi; không dùng Dụng/Hỷ/Kỵ thần từ giờ giả định. Gần giao tiết, giao ngày hoặc giao năm, cần xác minh thêm giờ sinh.")
    elif not useful and not favorable:
        warnings.append("Module hiện có chưa công bố hành Dụng/Hỷ thần; chỉ tham khảo Nạp Âm, Cung Phi và ý nghĩa tên.")
        if unfavorable:
            warnings.append("Vẫn loại các tên trùng hành Kỵ thần đã công bố.")
    if not nap_element:
        warnings.append("Chưa có hành Nạp Âm hợp lệ từ trụ năm BTE; tiêu chí này không tham gia xếp hạng.")
    if not cung or not cung_element:
        warnings.append("Chưa có đủ Cung Phi và hành cung từ BTE; tiêu chí này không tham gia xếp hạng.")
        cung_element = None
    if request.birth_place:
        warnings.append("Nơi sinh được ghi nhận; V0.1 tính theo múi giờ đã chọn, chưa hiệu chỉnh giờ Mặt Trời theo tọa độ.")
    signals = {
        "pillars": {
            slot: getattr(snapshot.pillars, slot).can_chi
            if getattr(snapshot.pillars, slot) and (slot != "hour" or hour_known) else None
            for slot in ("year", "month", "day", "hour")
        },
        "useful_elements": _labels(useful), "favorable_elements": _labels(favorable),
        "unfavorable_elements": _labels(unfavorable),
        "nap_am": nap_am or None, "nap_am_element": ELEMENT_LABELS.get(nap_element),
        "cung_phi": cung, "cung_phi_element": ELEMENT_LABELS.get(cung_element),
    }
    return signals, warnings


def recommend_names(
    request: NamingRequest,
    snapshot: MarriageCanonicalSnapshot,
    *,
    cung_element: FiveElement | None = None,
) -> dict[str, Any]:
    catalog = load_catalog()
    signals, warnings = naming_birth_signals(request, snapshot, cung_element=cung_element)
    hour_known = signals["pillars"]["hour"] is not None
    useful = signals["useful_elements"]
    favorable = signals["favorable_elements"]
    unfavorable = signals["unfavorable_elements"]
    nap_element = try_map_five_element(signals["nap_am_element"])
    cung_element = try_map_five_element(signals["cung_phi_element"])
    recommendations = []
    group_counts: Counter[str] = Counter()
    for entry in catalog["names"]:
        if request.gender not in entry["genders"]:
            continue
        full_name = normalize_name(f"{request.family_name} {entry['name']}")
        if request.mode == "rename" and normalize_name(request.current_name).casefold() in {
            full_name.casefold(), entry["name"].casefold(),
        }:
            continue
        element = FiveElement(entry["element"].lower())
        element_label = ELEMENT_LABELS[element]
        if element_label in unfavorable:
            continue

        if element_label in useful:
            group, points = "useful", 60
            level = "Ưu tiên theo Dụng thần"
            reason = "Hành tên trùng hành Dụng thần do BTE công bố."
        elif element_label in favorable:
            group, points = "favorable", 30
            level = "Phù hợp theo Hỷ thần"
            reason = "Hành tên trùng hành Hỷ thần do BTE công bố."
        else:
            group, points = "reference", 0
            level = "Tham khảo về ý nghĩa"
            reason = "Tên được xét theo ý nghĩa và các nguồn tham khảo hiện có."
        group_counts[group] += 1

        reasons = [reason]
        nap_points, nap_reason = describe_element_relation(element, nap_element, "Nạp Âm trụ năm")
        cung_points, cung_reason = describe_element_relation(element, cung_element, "Cung Phi")
        reference_points = nap_points + cung_points
        if nap_element is not None and nap_element == cung_element:
            reference_points = nap_points
            cung_reason += " Cùng hành với Nạp Âm trụ năm, nên hai nguồn chỉ tính điểm một lần."
        reasons.extend((nap_reason, cung_reason))
        if min(nap_points, cung_points) < 0 < max(nap_points, cung_points):
            reasons.append("Hai nguồn tham khảo có cả quan hệ thuận và khắc.")
        points += reference_points
        if level == "Tham khảo về ý nghĩa" and reference_points > 0:
            level = "Tham khảo theo Nạp Âm/Cung Phi"
        if not hour_known:
            level = "Sơ bộ · " + level
        recommendations.append({
            "id": entry["id"], "given_name": entry["name"], "full_name": full_name,
            "element": ELEMENT_LABELS[element], "meaning": entry["meaning"],
            "element_basis": entry["basis"], "fit_level": level,
            "rank_points": points, "reasons": reasons, "priority_group": group,
        })
    priority_order = {"useful": 0, "favorable": 1, "reference": 2}
    recommendations.sort(key=lambda item: (
        priority_order[item["priority_group"]], -item["rank_points"], item["id"],
    ))
    if len(recommendations) < request.count:
        warnings.append(
            f"Có {len(recommendations)} tên đủ điều kiện trong danh mục cho yêu cầu {request.count} tên."
        )
    return {
        "module_version": MODULE_VERSION,
        "mode": request.mode,
        "current_name": request.current_name if request.mode == "rename" else None,
        "quality": "preliminary" if not hour_known or not (useful or favorable) else "with_birth_time",
        "signals": signals,
        "recommendations": recommendations[:request.count],
        "eligible_counts": {group: group_counts[group] for group in priority_order},
        "warnings": warnings,
        "catalog": {key: catalog[key] for key in ("version", "review_note", "element_convention")},
        "method": (
            "Xếp theo thứ tự Dụng thần, Hỷ thần, rồi tên tham khảo. Loại hành Kỵ khỏi gợi ý. "
            "Trong từng nhóm, dùng điểm Nạp Âm trụ năm và Cung Phi: tên sinh hành đích +10, "
            "đồng hành +6, hành đích sinh tên +2, khắc mỗi chiều -6. "
            "Hai nguồn cùng hành chỉ tính một lần. Điểm chỉ dùng để sắp xếp trong danh mục."
        ),
        "notice": "Tên là lựa chọn văn hóa và cá nhân. Gợi ý phong thủy chỉ để tham khảo, không cam kết làm tăng thành công, tài lộc hay danh tiếng. V0.1 chưa đánh giá toàn bộ họ tên, âm điệu, tên trùng trong gia đình hoặc thủ tục đổi tên.",
    }


def _labels(elements: set[FiveElement]) -> list[str]:
    return [ELEMENT_LABELS[element] for element in FiveElement if element in elements]


def describe_element_relation(
    element: FiveElement, target: FiveElement | None, label: str,
    *, include_priority_note: bool = True,
) -> tuple[int, str]:
    if target is None:
        return 0, f"{label}: thiếu dữ liệu, không chấm tiêu chí này."
    source_label, target_label = ELEMENT_LABELS[element], ELEMENT_LABELS[target]
    if element == target:
        return 6, f"{label}: hành tên {source_label} đồng hành {target_label}."
    if GENERATES[element] == target:
        return 10, f"{label}: hành tên {source_label} sinh {target_label}."
    if GENERATES[target] == element:
        if not include_priority_note:
            return 2, f"{label}: {target_label} sinh hành tên {source_label}."
        return 2, f"{label}: {target_label} sinh hành tên {source_label}; đây là chiều sinh ngược, chỉ tham khảo phụ."
    return -6, f"{label}: {source_label} khắc {target_label}." if CONTROLS[element] == target else f"{label}: {target_label} khắc {source_label}."
