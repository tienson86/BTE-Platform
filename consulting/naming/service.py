"""Rank an editorial whitelist using existing Canonical signals, read-only."""

from __future__ import annotations

import json
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
from consulting.naming.models import NamingRequest, normalize_name

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
    person = MarriagePersonInput(
        gender=CanonicalGender(request.gender),
        birth_date=request.birth_date,
        birth_time=request.birth_time,
        full_name=request.current_name or None,
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
    return recommend_names(request, snapshot, cung_element=cung_element)


def recommend_names(
    request: NamingRequest,
    snapshot: MarriageCanonicalSnapshot,
    *,
    cung_element: FiveElement | None = None,
) -> dict[str, Any]:
    catalog = load_catalog()
    hour_known = request.birth_time is not None and snapshot.pillars.hour is not None
    useful = set(useful_elements(snapshot.useful_god)) if hour_known else set()
    favorable = set(favorable_elements(snapshot.useful_god)) if hour_known else set()
    unfavorable = set(unfavorable_elements(snapshot.useful_god)) if hour_known else set()
    nap_am = snapshot.pillars.year.na_yin or ""
    nap_element = try_map_five_element(nap_am.rsplit(" ", 1)[-1])
    cung = snapshot.feng_shui.cung_phi if snapshot.feng_shui else None
    cung_element = cung_element or (snapshot.feng_shui.element if snapshot.feng_shui else None)
    warnings = []
    if not hour_known:
        warnings.append("Chưa biết giờ sinh: chỉ gợi ý sơ bộ theo ý nghĩa, Nạp Âm và Cung Phi; không dùng Dụng/Hỷ/Kỵ thần từ giờ giả định. Gần giao tiết, giao ngày hoặc giao năm, cần xác minh thêm giờ sinh.")
    elif not useful and not favorable:
        warnings.append("Module hiện có chưa công bố hành Dụng/Hỷ thần; chỉ tham khảo Nạp Âm, Cung Phi và ý nghĩa tên.")
    if not nap_element:
        warnings.append("Chưa có hành Nạp Âm hợp lệ từ trụ năm BTE; tiêu chí này không tham gia xếp hạng.")
    if not cung or not cung_element:
        warnings.append("Chưa có đủ Cung Phi và hành cung từ BTE; tiêu chí này không tham gia xếp hạng.")
        cung_element = None
    if request.birth_place:
        warnings.append("Nơi sinh được ghi nhận; V0.1 tính theo múi giờ đã chọn, chưa hiệu chỉnh giờ Mặt Trời theo tọa độ.")
    recommendations = []
    for entry in catalog["names"]:
        if request.gender not in entry["genders"]:
            continue
        full_name = normalize_name(f"{request.family_name} {entry['name']}")
        if request.mode == "rename" and normalize_name(request.current_name).casefold() in {
            full_name.casefold(), entry["name"].casefold(),
        }:
            continue
        element = FiveElement(entry["element"].lower())
        points = 0
        reasons = []
        if element in unfavorable:
            points -= 100
            level = "Cần cân nhắc theo Kỵ thần"
            reasons.append("Hành tên trùng hành Kỵ thần do BTE công bố; không ưu tiên theo tiêu chí Bát Tự.")
        elif element in useful:
            points += 60
            level = "Ưu tiên theo Dụng thần"
            reasons.append("Hành tên trùng hành Dụng thần do BTE công bố.")
        elif element in favorable:
            points += 30
            level = "Phù hợp theo Hỷ thần"
            reasons.append("Hành tên trùng hành Hỷ thần do BTE công bố.")
        else:
            level = "Tham khảo về ý nghĩa"
            reasons.append("Chưa có đối chiếu Dụng/Hỷ thần cho tên này." if not hour_known else "Hành tên chưa trùng Dụng/Hỷ thần được công bố; điều này không có nghĩa tên xấu.")
        reference_points = 0
        for label, target in (("Nạp Âm trụ năm", nap_element), ("Cung Phi", cung_element)):
            delta, reason = describe_element_relation(element, target, label)
            reference_points += delta
            reasons.append(reason)
        points += reference_points
        if level == "Tham khảo về ý nghĩa" and reference_points > 0:
            level = "Tham khảo theo Nạp Âm/Cung Phi"
        if not hour_known:
            level = "Sơ bộ · " + level
        recommendations.append({
            "id": entry["id"], "given_name": entry["name"], "full_name": full_name,
            "element": ELEMENT_LABELS[element], "meaning": entry["meaning"],
            "element_basis": entry["basis"], "fit_level": level,
            "rank_points": points, "reasons": reasons,
        })
    recommendations.sort(key=lambda item: (-item["rank_points"], item["id"]))
    return {
        "module_version": MODULE_VERSION,
        "mode": request.mode,
        "current_name": request.current_name if request.mode == "rename" else None,
        "quality": "preliminary" if not hour_known or not (useful or favorable) else "with_birth_time",
        "signals": {
            "pillars": {
                slot: getattr(snapshot.pillars, slot).can_chi
                if getattr(snapshot.pillars, slot) and (slot != "hour" or hour_known) else None
                for slot in ("year", "month", "day", "hour")
            },
            "useful_elements": _labels(useful), "favorable_elements": _labels(favorable),
            "unfavorable_elements": _labels(unfavorable),
            "nap_am": nap_am or None, "nap_am_element": ELEMENT_LABELS.get(nap_element),
            "cung_phi": cung, "cung_phi_element": ELEMENT_LABELS.get(cung_element),
        },
        "recommendations": recommendations[:request.count],
        "warnings": warnings,
        "catalog": {key: catalog[key] for key in ("version", "review_note", "element_convention")},
        "method": "Ưu tiên hành trùng Dụng thần (+60), sau đó Hỷ thần (+30); hành Kỵ thần (-100). Mỗi tiêu chí Nạp Âm/Cung Phi: tên sinh cho hành đích (+10), đồng hành (+6), hành đích sinh tên (+2), khắc hai chiều (-6). Không cộng đồng thời điểm Dụng và Hỷ cho cùng hành. Điểm chỉ dùng sắp xếp trong danh mục, không phải xác suất hay dự báo vận mệnh.",
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
